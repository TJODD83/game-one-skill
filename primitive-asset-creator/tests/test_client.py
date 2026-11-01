import contextlib
import base64
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import threading
import tempfile
import struct
import zlib
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('primitive_agent', Path(__file__).parents[1] / 'primitive_agent.py')
client = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(client)

PROJECT_ID = '11111111-1111-4111-8111-111111111111'
REVISION = '2026-11-01T10:00:00.000Z'


def png(width, height, extra=b''):
    def chunk(kind, data):
        return struct.pack('>I',len(data)) + kind + data + struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
    header = struct.pack('>IIBBBBB',width,height,8,2,0,0,0)
    raw = b''.join(b'\0'+b'\x45\x67\x89'*width for _ in range(height))
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',header)+(chunk(b'tEXt',extra) if extra else b'')+chunk(b'IDAT',zlib.compress(raw))+chunk(b'IEND',b'')


# Actual one-pixel JPEG fixture, including tables, frame, entropy scan and EOI.
JPEG_ONE = base64.b64decode('/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAX/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIQAxAAAAF//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABBQJ//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPwF//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPwF//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQAGPwJ//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPyF//9oADAMBAAIAAwAAABAf/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAwEBPxB//8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAgBAgEBPxB//8QAFBABAAAAAAAAAAAAAAAAAAAAAP/aAAgBAQABPxB//9k=')


def write_views(folder, dimensions=None):
    for view in client.VIEW_ORDER:
        width,height = dimensions or (4,3)
        (folder/(view+'.png')).write_bytes(png(width,height))


class Handler(BaseHTTPRequestHandler):
    seen = []
    key = 'test-key-never-printed'

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        self.seen.append((self.path, self.headers.get('Authorization'), body))
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'ok': True, 'action': body['action'], 'echo': self.key}).encode())

    def log_message(self, *args):
        pass


class ClientTest(unittest.TestCase):
    def test_https_and_credential_url_rules(self):
        self.assertEqual(client.endpoint('https://agent.example/'), 'https://agent.example/api')
        self.assertEqual(client.endpoint('http://127.0.0.1:1234'), 'http://127.0.0.1:1234/api')
        for url in ('http://agent.example', 'https://user:secret@agent.example', 'https://agent.example/api', 'https://agent.example/?key=x'):
            with self.assertRaises(ValueError):
                client.endpoint(url)

    def test_payload_uses_json_objects(self):
        args = client.parser().parse_args(['call', 'inspect_thing', '{"id":"one"}'])
        self.assertEqual(client.payload(args), {'action': 'tool', 'name': 'inspect_thing', 'arguments': {'id': 'one'}})
        with self.assertRaises(ValueError):
            client.payload(client.parser().parse_args(['call', 'inspect_thing', '[]']))

    def test_cli_authentication_payload_and_secret_redaction(self):
        Handler.seen = []
        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            env = {'PRIMITIVE_AGENT_KEY': Handler.key, 'PRIMITIVE_AGENT_URL': 'http://127.0.0.1:%s' % server.server_port}
            output = io.StringIO()
            with patch.dict(os.environ, env), contextlib.redirect_stdout(output):
                status = client.main(['login', '--provider', 'Test provider', '--model', 'test-model', '--reason', 'Protocol fixture'])
            self.assertEqual(status, 0)
            path, authorization, body = Handler.seen[0]
            self.assertEqual(path, '/api')
            self.assertEqual(authorization, 'Bearer ' + Handler.key)
            self.assertEqual(body, {'action': 'begin', 'provider': 'Test provider', 'model': 'test-model', 'reason': 'Protocol fixture'})
            self.assertNotIn(Handler.key, output.getvalue())
            self.assertIn('[redacted]', output.getvalue())
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

    def test_noninteractive_missing_key_fails_without_request(self):
        err = io.StringIO()
        with patch.dict(os.environ, {'PRIMITIVE_AGENT_KEY': ''}), patch.object(client.sys.stdin, 'isatty', return_value=False), contextlib.redirect_stderr(err):
            self.assertEqual(client.main(['context']), 2)
        self.assertIn('PRIMITIVE_AGENT_KEY', err.getvalue())

    def test_redirects_do_not_receive_a_key(self):
        self.assertIsNone(client.NoRedirect().redirect_request(None, None, 302, 'Found', {}, 'https://other.example/'))

    def test_real_png_and_jpeg_dimensions(self):
        self.assertEqual(client.image_dimensions(png(9,7)),('image/png',(9,7)))
        self.assertEqual(client.image_dimensions(JPEG_ONE),('image/jpeg',(1,1)))
        for data in (b'not an image',b'\x89PNG\r\n\x1a\n',png(9,7)[:-5],b'\xff\xd8fake\xff\xd9'):
            with self.assertRaises(ValueError):
                client.image_dimensions(data)
        broken = bytearray(png(9,7));broken[-8] ^= 1
        with self.assertRaises(ValueError):
            client.image_dimensions(bytes(broken))

    def test_independent_six_import_uses_actual_bytes_and_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory);write_views(folder)
            (folder/'front.png').unlink();(folder/'front.jpg').write_bytes(JPEG_ONE)
            args = client.parser().parse_args(['upload-views',str(folder),'--source-project-id',PROJECT_ID,'--source-revision',REVISION])
            result = client.payload(args)
            self.assertEqual(result['action'],'tool')
            self.assertEqual(result['name'],'create_multiview_reference_set')
            value = result['arguments']
            self.assertEqual([image['view'] for image in value['images']],list(client.VIEW_ORDER))
            self.assertEqual((value['images'][0]['pixelWidth'],value['images'][0]['pixelHeight']),(1,1))
            self.assertTrue(value['images'][0]['dataUrl'].startswith('data:image/jpeg;base64,'))
            canonical = '\n'.join(image['view']+'\n'+image['dataUrl'] for image in value['images'])
            self.assertEqual(value['images_hash'],hashlib.sha256(canonical.encode()).hexdigest())
            self.assertNotIn('sheet_hash',value)
            self.assertNotIn('sheet',[image['view'] for image in value['images']])

    def test_actual_sheet_import_checks_grid_and_sheet_hash(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);write_views(folder,(4,4));(folder/'sheet.png').write_bytes(png(12,8))
            value=client.views_payload(folder,PROJECT_ID,REVISION)['arguments']
            self.assertEqual(len(value['images']),7)
            self.assertEqual(value['sheet_hash'],hashlib.sha256(value['images'][0]['dataUrl'].encode()).hexdigest())
            self.assertNotIn('images_hash',value)
            (folder/'top.png').write_bytes(png(3,4))
            with self.assertRaisesRegex(ValueError,'exact sheet grid'):
                client.views_payload(folder,PROJECT_ID,REVISION)

    def test_upload_cli_posts_tool_once_and_redacts_auth(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);write_views(folder)
            env={'PRIMITIVE_AGENT_KEY':'test-secret','PRIMITIVE_AGENT_URL':'https://gateway.example'}
            output=io.StringIO()
            with patch.dict(os.environ,env),patch.object(client,'request',return_value={'result':{'isError':False,'echo':'test-secret'}}) as send,contextlib.redirect_stdout(output):
                status=client.main(['upload-views',str(folder),'--source-project-id',PROJECT_ID,'--source-revision',REVISION])
            self.assertEqual(status,0)
            send.assert_called_once()
            url,key,body,timeout=send.call_args.args
            self.assertEqual(url,'https://gateway.example')
            self.assertEqual(key,'test-secret')
            self.assertEqual(body['name'],'create_multiview_reference_set')
            self.assertEqual(len(body['arguments']['images']),6)
            self.assertNotIn(key,output.getvalue())

    def test_folder_validation_and_image_limits(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory);write_views(folder)
            (folder/'bottom.png').unlink()
            with self.assertRaisesRegex(ValueError,'Missing view files: bottom'):
                client.views_payload(folder,PROJECT_ID,REVISION)
            (folder/'bottom.png').write_bytes(png(4,3));(folder/'front.jpg').write_bytes(JPEG_ONE)
            with self.assertRaisesRegex(ValueError,'More than one'):
                client.views_payload(folder,PROJECT_ID,REVISION)
            (folder/'front.jpg').unlink();(folder/'other.png').write_bytes(png(4,3))
            with self.assertRaisesRegex(ValueError,'Unexpected image'):
                client.views_payload(folder,PROJECT_ID,REVISION)
            (folder/'other.png').unlink();(folder/'front.png').write_bytes(png(1601,1))
            with self.assertRaisesRegex(ValueError,'1600'):
                client.views_payload(folder,PROJECT_ID,REVISION)
            (folder/'front.png').write_bytes(b'x'*340000)
            with self.assertRaisesRegex(ValueError,'per-image'):
                client.views_payload(folder,PROJECT_ID,REVISION)
        with self.assertRaisesRegex(ValueError,'not a directory'):
            client.views_payload(Path('/does/not/exist'),PROJECT_ID,REVISION)

    def test_total_upload_limit_before_any_http_request(self):
        with tempfile.TemporaryDirectory() as directory:
            folder=Path(directory)
            for view in client.VIEW_ORDER:
                (folder/(view+'.png')).write_bytes(png(4,4,b'x'*330000))
            (folder/'sheet.png').write_bytes(png(12,8,b'x'*330000))
            result=client.views_payload(folder,PROJECT_ID,REVISION)
            self.assertLess(len(client.encoded_body(result)),3400000)
        with patch.object(client.urllib.request,'build_opener') as opener:
            with self.assertRaisesRegex(ValueError,'3.4 MB'):
                client.request('https://gateway.example','secret',{'huge':'x'*3400000})
            opener.assert_not_called()

    def test_resume_payload_and_nested_tool_errors(self):
        value=client.payload(client.parser().parse_args(['resume','--provider','xAI','--model','Grok']))
        self.assertEqual(value,{'action':'resume','provider':'xAI','model':'Grok'})
        env={'PRIMITIVE_AGENT_KEY':'test-secret','PRIMITIVE_AGENT_URL':'https://gateway.example'}
        output=io.StringIO()
        with patch.dict(os.environ,env),patch.object(client,'request',return_value={'result':{'isError':True,'content':[]}}),contextlib.redirect_stdout(output):
            self.assertEqual(client.main(['tools']),1)

    def test_keepalive_liveness_only_and_bounded_duration(self):
        current=[0.0];seen=[]
        def send(url,key,body,timeout):
            seen.append(body);return {'ok':True}
        def sleep(seconds):
            current[0]+=seconds
        result=client.keepalive('https://gateway.example','secret',duration=61,interval=30,send=send,clock=lambda:current[0],sleep=sleep)
        self.assertEqual(seen,[{'action':'heartbeat'}]*3)
        self.assertEqual(result['heartbeats_sent'],3)
        self.assertEqual(result['duration_seconds'],61)
        for duration,interval in ((0,30),(3601,30),(900,0),(900,9),(900,61),(float('nan'),30)):
            with self.assertRaises(ValueError):
                client.keepalive('https://gateway.example','secret',duration,interval,send=send)

    def test_keepalive_stops_on_auth_errors_or_rejected_response(self):
        for response in ({'error':'expired'},{'result':{'isError':True}},None):
            seen=[]
            def send(*args):
                seen.append(args);return response
            with self.assertRaisesRegex(ValueError,'rejected heartbeat'):
                client.keepalive('https://gateway.example','secret',send=send,sleep=lambda _:self.fail('Should not sleep after failure'))
            self.assertEqual(len(seen),1)
        with self.assertRaisesRegex(ValueError,'HTTP 401'):
            client.keepalive('https://gateway.example','secret',send=lambda *args:(_ for _ in ()).throw(ValueError('HTTP 401')))
        env={'PRIMITIVE_AGENT_KEY':'test-secret','PRIMITIVE_AGENT_URL':'https://gateway.example'}
        error=io.StringIO()
        with patch.dict(os.environ,env),patch.object(client,'keepalive',side_effect=KeyboardInterrupt),contextlib.redirect_stderr(error):
            self.assertEqual(client.main(['keepalive']),130)
        self.assertIn('no further heartbeats',error.getvalue())

if __name__ == '__main__':
    unittest.main()

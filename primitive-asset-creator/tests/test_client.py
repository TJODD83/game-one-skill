import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('primitive_agent', Path(__file__).parents[1] / 'primitive_agent.py')
client = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(client)


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


if __name__ == '__main__':
    unittest.main()

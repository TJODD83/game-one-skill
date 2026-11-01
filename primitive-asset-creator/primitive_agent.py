#!/usr/bin/env python3
"""Primitive Asset Creator external agent client. Python standard library only."""
import argparse
import base64
import hashlib
import getpass
import json
import math
import os
from pathlib import Path
import sys
import struct
import time
import zlib
from datetime import datetime
import uuid
import urllib.error
import urllib.parse
import urllib.request


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--url', default=os.environ.get('PRIMITIVE_AGENT_URL'), help='Agent gateway root (or PRIMITIVE_AGENT_URL)')
    p.add_argument('--output', type=Path, help='Write the JSON response to this file instead of stdout')
    p.add_argument('--timeout', type=float, default=90, help='Request timeout in seconds (default: 90)')
    sub = p.add_subparsers(dest='command', required=True)
    login = sub.add_parser('login', help='Begin this key-scoped workspace and report runner identity')
    login.add_argument('--provider', required=True, help='Reported provider, e.g. Anthropic, OpenAI or xAI')
    login.add_argument('--model', required=True, help='Exact model identifier supplied by your runner')
    login.add_argument('--reason', required=True, help='Brief work summary or runner reasoning setting; never private reasoning')
    resume = sub.add_parser('resume', help='Resume an interrupted workspace with its existing provider and model')
    resume.add_argument('--provider', required=True)
    resume.add_argument('--model', required=True)
    for command in ('context', 'tools', 'snapshot'):
        sub.add_parser(command)
    call = sub.add_parser('call', help='Call an available workshop tool')
    call.add_argument('name')
    call.add_argument('arguments', nargs='?', default='{}', help='JSON object, or @path/to/arguments.json')
    heartbeat = sub.add_parser('heartbeat')
    heartbeat.add_argument('--stage', required=True)
    heartbeat.add_argument('--message', required=True)
    keep = sub.add_parser('keepalive', help='Send liveness-only heartbeats while waiting for external output')
    keep.add_argument('--duration', type=float, default=900, help='Seconds to keep alive (1–3600; default: 900)')
    keep.add_argument('--interval', type=float, default=30, help='Heartbeat interval in seconds (10–60; default: 30)')
    upload = sub.add_parser('upload-views', help='Upload six named PNG/JPEG crops from a local folder; actual sheet optional')
    upload.add_argument('folder', type=Path)
    upload.add_argument('--source-project-id', required=True)
    upload.add_argument('--source-revision', required=True, help='Exact saved source revision returned by prepare_multiview_reference')
    finish = sub.add_parser('finish')
    finish.add_argument('--outcome', required=True, choices=('completed', 'blocked', 'failed'))
    finish.add_argument('--note', required=True)
    submit = sub.add_parser('submit', help='Submit a saved workshop model JSON using the gateway model contract')
    submit.add_argument('model_file', type=Path)
    return p


def payload(args):
    if args.command == 'login':
        return {'action': 'begin', 'provider': args.provider, 'model': args.model, 'reason': args.reason}
    if args.command == 'resume':
        return {'action': 'resume', 'provider': args.provider, 'model': args.model}
    if args.command == 'upload-views':
        return views_payload(args.folder, args.source_project_id, args.source_revision)
    if args.command == 'call':
        raw = Path(args.arguments[1:]).read_text(encoding='utf-8') if args.arguments.startswith('@') else args.arguments
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise ValueError('Tool arguments must be a JSON object')
        return {'action': 'tool', 'name': args.name, 'arguments': value}
    if args.command == 'heartbeat':
        return {'action': 'heartbeat', 'stage': args.stage, 'message': args.message}
    if args.command == 'finish':
        return {'action': 'finish', 'outcome': args.outcome, 'note': args.note}
    if args.command == 'submit':
        value = json.loads(args.model_file.read_text(encoding='utf-8'))
        if not isinstance(value, dict):
            raise ValueError('A submitted model must be a JSON object')
        return {'action': 'submit', 'model': value}
    return {'action': args.command}


VIEW_ORDER = ('front', 'back', 'left', 'right', 'top', 'bottom')
MAX_REQUEST_BYTES = 3400000
MAX_DATA_URL = 450000
MAX_IMAGE_DIMENSION = 1600


def encoded_body(body):
    data = json.dumps(body).encode('utf-8')
    if len(data) > MAX_REQUEST_BYTES:
        raise ValueError('Request exceeds the 3.4 MB gateway limit; resize or recompress the actual images before upload')
    return data


def image_dimensions(data):
    """Read actual PNG/JPEG dimensions; not a visual-content or full JPEG decoder."""
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        offset, dimensions, image_data, ended = 8, None, [], False
        while offset + 12 <= len(data):
            length = struct.unpack('>I', data[offset:offset+4])[0]
            kind = data[offset+4:offset+8]
            end = offset + 12 + length
            if end > len(data):
                raise ValueError('Truncated PNG chunk')
            chunk = data[offset+8:offset+8+length]
            crc = struct.unpack('>I', data[offset+8+length:end])[0]
            if zlib.crc32(kind + chunk) & 0xffffffff != crc:
                raise ValueError('PNG chunk checksum failed')
            if dimensions is None:
                if kind != b'IHDR' or length != 13:
                    raise ValueError('PNG must begin with a valid IHDR')
                width, height, depth, colour, compression, filtering, interlace = struct.unpack('>IIBBBBB', chunk)
                legal_depths = {0:(1,2,4,8,16), 2:(8,16), 3:(1,2,4,8), 4:(8,16), 6:(8,16)}
                if not width or not height or depth not in legal_depths.get(colour, ()) or compression or filtering or interlace not in (0,1):
                    raise ValueError('Unsupported or invalid PNG header')
                if width > MAX_IMAGE_DIMENSION or height > MAX_IMAGE_DIMENSION:
                    raise ValueError('PNG must be at most 1600 pixels on each axis')
                dimensions = (width, height)
            elif kind == b'IHDR':
                raise ValueError('Duplicate PNG header')
            if kind == b'IDAT' and length:
                image_data.append(chunk)
            if kind == b'IEND':
                if length or end != len(data):
                    raise ValueError('Invalid PNG ending')
                ended = True
                break
            offset = end
        if not dimensions or not image_data or not ended:
            raise ValueError('Incomplete PNG image')
        bits = {0:1,2:3,3:1,4:2,6:4}[colour] * depth
        passes = ((0,0,1,1),) if not interlace else ((0,0,8,8),(4,0,8,8),(0,4,4,8),(2,0,4,4),(0,2,2,4),(1,0,2,2),(0,1,1,2))
        row_lengths = []
        for x,y,dx,dy in passes:
            columns, rows = max(0,(width-x+dx-1)//dx), max(0,(height-y+dy-1)//dy)
            if columns and rows:
                row_lengths.extend([1+(columns*bits+7)//8] * rows)
        expected = sum(row_lengths)
        try:
            decoder = zlib.decompressobj()
            raw = decoder.decompress(b''.join(image_data), expected+1)
        except zlib.error:
            raise ValueError('PNG pixel data is not a valid compressed image') from None
        if len(raw) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
            raise ValueError('PNG pixel data does not match its actual dimensions')
        offset = 0
        for length in row_lengths:
            if raw[offset] > 4:
                raise ValueError('Invalid PNG scanline filter')
            offset += length
        return 'image/png', dimensions
    if data.startswith(b'\xff\xd8'):
        offset, dimensions = 2, None
        sof = {0xc0,0xc1,0xc2,0xc3,0xc5,0xc6,0xc7,0xc9,0xca,0xcb,0xcd,0xce,0xcf}
        while offset < len(data):
            if data[offset] != 0xff:
                raise ValueError('Invalid JPEG marker')
            while offset < len(data) and data[offset] == 0xff:
                offset += 1
            if offset >= len(data):
                break
            marker = data[offset]
            offset += 1
            if marker in (0x00,0xd8,0xd9):
                raise ValueError('Invalid JPEG marker order')
            if marker in range(0xd0,0xd8) or marker == 0x01:
                continue
            if offset + 2 > len(data):
                raise ValueError('Truncated JPEG segment')
            length = struct.unpack('>H', data[offset:offset+2])[0]
            if length < 2 or offset + length > len(data):
                raise ValueError('Truncated JPEG segment')
            segment = data[offset+2:offset+length]
            if marker in sof:
                if len(segment) < 6:
                    raise ValueError('Invalid JPEG frame header')
                height, width = struct.unpack('>HH', segment[1:5])
                components = segment[5]
                if not width or not height or not components or len(segment) != 6 + 3 * components:
                    raise ValueError('Invalid JPEG frame dimensions')
                if dimensions and dimensions != (width, height):
                    raise ValueError('Conflicting JPEG frame dimensions')
                dimensions = (width, height)
            if marker == 0xda:
                if not dimensions or len(segment) < 4 or not data.endswith(b'\xff\xd9') or offset + length >= len(data)-2:
                    raise ValueError('Incomplete JPEG scan')
                return 'image/jpeg', dimensions
            offset += length
        raise ValueError('JPEG has no complete frame and scan')
    raise ValueError('Use actual PNG or JPEG image bytes')


def views_payload(folder, source_project_id, source_revision):
    if not folder.is_dir():
        raise ValueError('View folder does not exist or is not a directory')
    try:
        uuid.UUID(source_project_id)
        datetime.fromisoformat(source_revision.replace('Z', '+00:00'))
    except (ValueError, TypeError, AttributeError):
        raise ValueError('Provide the actual saved source project UUID and revision timestamp') from None
    files = {}
    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() in ('.png', '.jpg', '.jpeg'):
            stem = path.stem.lower()
            if stem not in (*VIEW_ORDER, 'sheet'):
                raise ValueError('Unexpected image filename: ' + path.name)
            if stem in files:
                raise ValueError('More than one file supplied for ' + stem)
            files[stem] = path
    missing = [view for view in VIEW_ORDER if view not in files]
    if missing:
        raise ValueError('Missing view files: ' + ', '.join(missing))
    order = ('sheet', *VIEW_ORDER) if 'sheet' in files else VIEW_ORDER
    images = []
    for view in order:
        path = files[view]
        if path.stat().st_size > MAX_DATA_URL * 3 // 4:
            raise ValueError(path.name + ' exceeds the per-image encoded limit; resize/recompress it')
        data = path.read_bytes()
        mime, (width, height) = image_dimensions(data)
        if not (1 <= width <= MAX_IMAGE_DIMENSION and 1 <= height <= MAX_IMAGE_DIMENSION):
            raise ValueError(path.name + ' must be at most 1600 pixels on each axis')
        data_url = 'data:' + mime + ';base64,' + base64.b64encode(data).decode('ascii')
        if len(data_url) > MAX_DATA_URL:
            raise ValueError(path.name + ' exceeds the 450000-character data URL limit; resize/recompress it')
        images.append({'view':view, 'dataUrl':data_url, 'pixelWidth':width, 'pixelHeight':height})
    arguments = {'source_project_id':source_project_id, 'source_revision':source_revision, 'images':images}
    if 'sheet' in files:
        sheet = images[0]
        width, height = sheet['pixelWidth'], sheet['pixelHeight']
        if width < 3 or height < 2 or min(abs(width/height-16/9), abs(width/height-3/2)) > .04:
            raise ValueError('Sheet must be landscape 16:9 or 3:2 with three columns and two rows')
        # Match JavaScript Math.round for positive boundaries, including odd sizes.
        rounded = lambda numerator, denominator: (2*numerator + denominator) // (2*denominator)
        for i, image in enumerate(images[1:]):
            column, row = i % 3, i // 3
            expected_width = rounded((column+1)*width,3) - rounded(column*width,3)
            expected_height = rounded((row+1)*height,2) - rounded(row*height,2)
            if (image['pixelWidth'],image['pixelHeight']) != (expected_width,expected_height):
                raise ValueError(image['view'] + ' dimensions do not match the exact sheet grid crop')
        arguments['sheet_hash'] = hashlib.sha256(sheet['dataUrl'].encode('utf-8')).hexdigest()
    else:
        canonical = '\n'.join(image['view'] + '\n' + image['dataUrl'] for image in images)
        arguments['images_hash'] = hashlib.sha256(canonical.encode('utf-8')).hexdigest()
    body = {'action':'tool', 'name':'create_multiview_reference_set', 'arguments':arguments}
    encoded_body(body)
    return body


def failed_result(value):
    if not isinstance(value, dict):
        return False
    if value.get('isError') is True or value.get('ok') is False or value.get('error'):
        return True
    return isinstance(value.get('result'), dict) and failed_result(value['result'])


def keepalive(url, key, duration=900, interval=30, timeout=90, *, send=None, clock=None, sleep=None):
    if not (1 <= duration <= 3600) or not (10 <= interval <= 60):
        raise ValueError('Keepalive duration must be 1–3600 seconds and interval 10–60 seconds')
    send, clock, sleep = send or request, clock or time.monotonic, sleep or time.sleep
    start = clock()
    sent = 0
    while clock() - start < duration:
        result = send(url, key, {'action':'heartbeat'}, timeout)
        if not isinstance(result, dict) or failed_result(result):
            raise ValueError('Keepalive stopped after a rejected heartbeat: ' + json.dumps(result))
        sent += 1
        remaining = duration - (clock() - start)
        if remaining <= 0:
            break
        sleep(min(interval, remaining))
    return {'heartbeats_sent':sent, 'duration_seconds':round(clock()-start,3), 'notice':'Liveness heartbeats only; no tool progress or stage completion was reported.'}


def endpoint(url):
    if not url:
        raise ValueError('Set PRIMITIVE_AGENT_URL to the gateway root from your handoff packet')
    parsed = urllib.parse.urlsplit(url)
    if not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('Gateway URL must have a hostname and no credentials, query or fragment')
    local = parsed.hostname in ('localhost', '127.0.0.1', '::1')
    if parsed.scheme != 'https' and not (local and parsed.scheme == 'http'):
        raise ValueError('Use HTTPS for the agent gateway')
    if parsed.path.rstrip('/'):
        raise ValueError('Use the gateway root URL, without /api or another path')
    return url.rstrip('/') + '/api'


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Do not forward a credential to a redirect target.
        return None


def request(url, key, body, timeout=90):
    req = urllib.request.Request(endpoint(url), data=encoded_body(body), headers={
        'Authorization': 'Bearer ' + key,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }, method='POST')
    try:
        with urllib.request.build_opener(NoRedirect).open(req, timeout=timeout) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as error:
        try:
            detail = json.loads(error.read().decode('utf-8'))
        except (ValueError, UnicodeError):
            detail = {'error': error.reason}
        raise ValueError('HTTP %s: %s' % (error.code, json.dumps(detail))) from None


def main(argv=None):
    args = parser().parse_args(argv)
    key = os.environ.get('PRIMITIVE_AGENT_KEY', '').strip()
    if not key and sys.stdin.isatty():
        key = getpass.getpass('Agent key (hidden): ').strip()
    if not key:
        print('Set PRIMITIVE_AGENT_KEY in your secret environment or run interactively for hidden entry.', file=sys.stderr)
        return 2
    try:
        if '\n' in key or '\r' in key:
            raise ValueError('Invalid agent key')
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise ValueError('Timeout must be positive')
        result = keepalive(args.url, key, args.duration, args.interval, args.timeout) if args.command == 'keepalive' else request(args.url, key, payload(args), args.timeout)
        output = json.dumps(result, indent=2, ensure_ascii=False).replace(key, '[redacted]') + '\n'
        if args.output:
            args.output.write_text(output, encoding='utf-8')
        else:
            sys.stdout.write(output)
        return 1 if failed_result(result) else 0
    except KeyboardInterrupt:
        print('Stopped by user; no further heartbeats sent.', file=sys.stderr)
        return 130
    except (ValueError, OSError, urllib.error.URLError) as error:
        print(str(error).replace(key, '[redacted]'), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

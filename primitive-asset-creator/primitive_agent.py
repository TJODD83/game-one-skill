#!/usr/bin/env python3
"""Primitive Asset Creator external agent client. Python standard library only."""
import argparse
import getpass
import json
import os
from pathlib import Path
import sys
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
    for command in ('context', 'tools', 'snapshot'):
        sub.add_parser(command)
    call = sub.add_parser('call', help='Call an available workshop tool')
    call.add_argument('name')
    call.add_argument('arguments', nargs='?', default='{}', help='JSON object, or @path/to/arguments.json')
    heartbeat = sub.add_parser('heartbeat')
    heartbeat.add_argument('--stage', required=True)
    heartbeat.add_argument('--message', required=True)
    finish = sub.add_parser('finish')
    finish.add_argument('--outcome', required=True, choices=('completed', 'blocked', 'failed'))
    finish.add_argument('--note', required=True)
    submit = sub.add_parser('submit', help='Submit a saved workshop model JSON using the gateway model contract')
    submit.add_argument('model_file', type=Path)
    return p


def payload(args):
    if args.command == 'login':
        return {'action': 'begin', 'provider': args.provider, 'model': args.model, 'reason': args.reason}
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
    req = urllib.request.Request(endpoint(url), data=json.dumps(body).encode('utf-8'), headers={
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
        if args.timeout <= 0:
            raise ValueError('Timeout must be positive')
        result = request(args.url, key, payload(args), args.timeout)
        output = json.dumps(result, indent=2, ensure_ascii=False).replace(key, '[redacted]') + '\n'
        if args.output:
            args.output.write_text(output, encoding='utf-8')
        else:
            sys.stdout.write(output)
        return 1 if isinstance(result, dict) and (result.get('isError') is True or result.get('ok') is False or result.get('error')) else 0
    except (ValueError, OSError, urllib.error.URLError) as error:
        print(str(error).replace(key, '[redacted]'), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

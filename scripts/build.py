#!/usr/bin/env python3
"""Render all client rule sets from the policy-free canonical sources."""
import argparse
import ipaddress
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    'AI': 'ai', 'CLOUD': 'cloud', 'PAYMENTS & COMMERCE': 'payments-commerce',
    'SOCIAL': 'social', 'STREAMING': 'streaming', 'IM & MEETINGS': 'im-meetings',
    'TRAVEL & MAPS': 'travel-maps', 'SHOPPING & DAILY LIFE': 'shopping-daily-life',
    'PRODUCTIVITY & DEV': 'productivity-dev', 'FINANCE & BANKING': 'finance-banking',
}


def read_domains():
    text = (ROOT / 'source/domains/common.list').read_text()
    groups = OrderedDict()
    category = None
    rules = []
    for line in text.splitlines():
        if '[ ' in line and line.startswith('#'):
            if len(line) != 68:
                raise ValueError('Section banner must be 68 characters')
            category = line.split('[ ', 1)[1].split(' ]', 1)[0]
            groups[category] = []
        elif line and not line.startswith('#'):
            if category not in CATEGORIES or not re.fullmatch(r'DOMAIN(?:-SUFFIX)?,[a-z0-9.-]+', line):
                raise ValueError(f'Invalid domain rule: {line}')
            kind, domain = line.split(',')
            if any(not x or x.startswith('-') or x.endswith('-') for x in domain.split('.')):
                raise ValueError(f'Invalid hostname: {domain}')
            groups[category].append(line)
            rules.append(line)
    if len(rules) != len(set(rules)):
        raise ValueError('Duplicate domain rules')
    suffixes = {r.split(',')[1] for r in rules if r.startswith('DOMAIN-SUFFIX,')}
    for rule in rules:
        kind, domain = rule.split(',')
        if any('.'.join(domain.split('.')[i:]) in suffixes for i in range(1, len(domain.split('.')))):
            raise ValueError(f'Redundant child rule: {rule}')
        if kind == 'DOMAIN' and domain in suffixes:
            raise ValueError(f'Redundant exact rule: {rule}')
    return text, groups, rules


def read_ips():
    text = (ROOT / 'source/ip/optional.list').read_text()
    networks = []
    for line in text.splitlines():
        if line and not line.startswith('#'):
            kind, cidr, flag = line.split(',')
            if kind != 'IP-CIDR' or flag != 'no-resolve':
                raise ValueError(f'Invalid canonical IP rule: {line}')
            networks.append(ipaddress.ip_network(cidr))
    if len(networks) != len(set(networks)):
        raise ValueError('Duplicate IP prefixes')
    return text, networks


def domain_yaml(rules, title):
    # Stash domain suffix syntax matches both the root and all subdomains.
    values = [('+.' if r.startswith('DOMAIN-SUFFIX,') else '') + r.split(',')[1] for r in rules]
    return f'# Generated: {title}; behavior: domain\npayload:\n' + ''.join(f'  - "{v}"\n' for v in values)


def rendered():
    domain_text, groups, domains = read_domains()
    ip_text, networks = read_ips()
    outputs = {}
    for client in ('shadowrocket', 'surge'):
        outputs[f'rules/{client}/common.list'] = domain_text
        if client == 'shadowrocket':
            outputs[f'rules/{client}/optional-ip.list'] = ip_text
        else:
            lines = []
            for line in ip_text.splitlines():
                if line.startswith('IP-CIDR,') and ipaddress.ip_network(line.split(',')[1]).version == 6:
                    line = line.replace('IP-CIDR,', 'IP-CIDR6,', 1)
                lines.append(line.replace('Shadowrocket optional IP supplement', 'Surge optional IP supplement'))
            outputs[f'rules/{client}/optional-ip.list'] = '\n'.join(lines) + '\n'
        for category, rules in groups.items():
            outputs[f'rules/{client}/categories/{CATEGORIES[category]}.list'] = '# Generated category: ' + category + '\n' + '\n'.join(rules) + '\n'
    outputs['rules/stash/common.yaml'] = domain_yaml(domains, 'common domains')
    outputs['rules/stash/optional-ip.yaml'] = '# Generated; behavior: ipcidr\npayload:\n' + ''.join(f'  - "{n}"\n' for n in networks)
    for category, rules in groups.items():
        outputs[f'rules/stash/categories/{CATEGORIES[category]}.yaml'] = domain_yaml(rules, category)
    return outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true', help='Validate sources and reject stale or unexpected generated files')
    args = parser.parse_args()
    outputs = rendered()
    if args.check:
        stale = [p for p, text in outputs.items() if not (ROOT / p).exists() or (ROOT / p).read_text() != text]
        unexpected = [str(p.relative_to(ROOT)) for p in (ROOT / 'rules').rglob('*') if p.is_file() and str(p.relative_to(ROOT)) not in outputs]
        if stale or unexpected:
            raise SystemExit(f'Run python3 scripts/build.py; stale={stale}, unexpected={unexpected}')
    else:
        for path, text in outputs.items():
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
    print(f'OK: {len(read_domains()[2])} domain rules, {len(read_ips()[1])} IP prefixes, {len(outputs)} generated files')


if __name__ == '__main__':
    main()

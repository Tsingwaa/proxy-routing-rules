import ipaddress
import json
import unittest
import build


class RuleFormats(unittest.TestCase):
    def test_client_semantics(self):
        outputs = build.rendered()
        _, groups, domains = build.read_domains()
        # Converting between clients must preserve exact versus suffix matching.
        yaml_values = [json.loads(x.strip()[2:]) for x in outputs['rules/stash/common.yaml'].splitlines() if x.startswith('  - ')]
        converted = [('DOMAIN-SUFFIX,' + v[2:]) if v.startswith('+.') else ('DOMAIN,' + v) for v in yaml_values]
        self.assertEqual(converted, domains)
        for client in ('shadowrocket', 'surge'):
            text_rules = [x for x in outputs[f'rules/{client}/common.list'].splitlines() if x.startswith('DOMAIN')]
            self.assertEqual(text_rules, domains)
            self.assertEqual(sum(len(rs) for rs in groups.values()), len(text_rules))
        stash_ips = [ipaddress.ip_network(json.loads(x.strip()[2:])) for x in outputs['rules/stash/optional-ip.yaml'].splitlines() if x.startswith('  - ')]
        self.assertEqual(stash_ips, build.read_ips()[1])
        # Surge requires IP-CIDR6 for IPv6; Shadowrocket uses IP-CIDR for both.
        for client in ('shadowrocket', 'surge'):
            networks = []
            for x in outputs[f'rules/{client}/optional-ip.list'].splitlines():
                if x.startswith('IP-CIDR'):
                    kind, cidr, flag = x.split(',')
                    network = ipaddress.ip_network(cidr)
                    expected = 'IP-CIDR6' if client == 'surge' and network.version == 6 else 'IP-CIDR'
                    self.assertEqual(kind, expected)
                    self.assertEqual(flag, 'no-resolve')
                    networks.append(network)
            self.assertEqual(networks, build.read_ips()[1])

    def test_required_services(self):
        rules = build.read_domains()[2]
        def matches(host):
            return any(host == d or k == 'DOMAIN-SUFFIX' and host.endswith('.' + d) for k, d in (r.split(',') for r in rules))
        hosts = 'v2ex.com i.v2ex.co reddit.com redd.it x.com twimg.com telegram.org t.me instagram.com cdninstagram.com facebook.com fbcdn.net threads.com whatsapp.net messenger.com tiktok.com tiktokcdn.com discord.com discordapp.net slack.com slack-files.com line.me line-scdn.net snapchat.com pinterest.com linkedin.com github.com githubusercontent.com google.com maps.googleapis.com youtube.com googlevideo.com lazada.sg lazcdn.com ibkr.com ibllc.com bochk.com hsbc.com.hk wise.com notion.so notionusercontent.com gemini.google.com chatgpt.com oaistatic.com claude.ai claudemcpcontent.com grok.com grokusercontent.com muse.ai metaaivm.com cursor.sh cursorvm.com guzzoni.apple.com apple-relay.apple.com'.split()
        for host in hosts:
            self.assertTrue(matches(host), host)
        for host in ['notgithub.com', 'google.com.evil.example', 'evilwise.com', 'unknown.example']:
            self.assertFalse(matches(host), host)


if __name__ == '__main__':
    unittest.main()

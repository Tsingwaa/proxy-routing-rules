# Proxy Routing Rules

常用国外应用的专用出口分流名单。**559 条域名规则、10 个分类**；另提供 Telegram / ChatGPT 语音的 **37 条可选 IP 规则**。所有规则均不包含节点、密码或策略组，出口由客户端配置决定。

## 可直接引用的链接

| 客户端 | 全部常用域名 | 可选 IP 补充 |
| --- | --- | --- |
| Shadowrocket | [common.list](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/shadowrocket/common.list) | [optional-ip.list](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/shadowrocket/optional-ip.list) |
| Surge | [common.list](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/surge/common.list) | [optional-ip.list](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/surge/optional-ip.list) |
| Stash | [common.yaml](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/stash/common.yaml) · `behavior: domain` | [optional-ip.yaml](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/stash/optional-ip.yaml) · `behavior: ipcidr` |

使用 **Raw 链接**，不要使用 GitHub 的 `blob` 页面地址。这是路由规则订阅，不是节点订阅或完整代理配置。

## Shadowrocket / Surge 接入

将下面规则加入现有配置的 `[Rule]` 段，把 `STATIC_IP` 替换为你的专用出口节点或策略组名称。放在会覆盖它的直连规则和最终兜底规则之前。

Shadowrocket：

```ini
RULE-SET,https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/shadowrocket/common.list,STATIC_IP
# 可选：Telegram 直接 IP 连接和 ChatGPT 语音
RULE-SET,https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/shadowrocket/optional-ip.list,STATIC_IP
```

Surge：

```ini
RULE-SET,https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/surge/common.list,STATIC_IP
# 可选：Telegram 直接 IP 连接和 ChatGPT 语音
RULE-SET,https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/surge/optional-ip.list,STATIC_IP,no-resolve
```

Shadowrocket 也可在规则界面添加类型 `RULE-SET`，填入 Raw URL，并选择专用出口。文件自身不绑定策略组；只添加 URL 不会自动选择出口。

## Stash 接入

合并到已有配置中，不要重复创建同名 `rules` / `rule-providers` 顶层字段。保留现有其他规则及兜底项；`STATIC_IP` 替换为现有节点或策略组名称。

```yaml
rule-providers:
  dedicated-domains:
    behavior: domain
    format: yaml
    url: https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/stash/common.yaml
    interval: 86400
  dedicated-ips:
    behavior: ipcidr
    format: yaml
    url: https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/stash/optional-ip.yaml
    interval: 86400
rules:
  - RULE-SET,dedicated-domains,STATIC_IP
  # 不需要 IP 补充时可删除 provider 与下面这一行
  - RULE-SET,dedicated-ips,STATIC_IP,no-resolve
```

## 按类别订阅

全部域名已在 `common` 内；不必同时订阅全部文件和分类文件。需要不同类别走不同出口时，使用 `rules/<client>/categories/<category>.list`（Stash 为 `.yaml`）。

| 类别 | 文件名 | 规则数 |
| --- | --- | ---: |
| AI | `ai` | 72 |
| 云平台 | `cloud` | 103 |
| 支付与电商 | `payments-commerce` | 41 |
| 社交媒体 | `social` | 66 |
| 流媒体 | `streaming` | 105 |
| IM 与会议 | `im-meetings` | 53 |
| 旅游与地图 | `travel-maps` | 46 |
| 购物与日常消费 | `shopping-daily-life` | 33 |
| 生产力与开发 | `productivity-dev` | 21 |
| 金融与银行 | `finance-banking` | 19 |

例如 [Surge 社媒分类](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/surge/categories/social.list)、[Shadowrocket AI 分类](https://raw.githubusercontent.com/Tsingwaa/proxy-routing-rules/main/rules/shadowrocket/categories/ai.list)。部分业务共用 Google / Meta / Microsoft 根域；拆分使用时，需要同时引入相应云平台或社媒依赖，不能把单个分类当作应用的完全独立依赖包。

## 目录与后续扩展

```text
source/
  domains/common.list      # 唯一域名源，按业务分类，不带策略
  ip/optional.list         # 可选 IP 源；IPv4/IPv6 均用规范化 IP-CIDR
rules/
  shadowrocket/            # RULE-SET 格式
  surge/                   # RULE-SET 格式，IPv6 转为 IP-CIDR6
  stash/                   # domain / ipcidr YAML 格式
  <client>/categories/     # 从同一来源生成的分类文件
scripts/
  build.py                 # 标准库生成器，无第三方依赖
  test_build.py            # 转换语义与关键应用匹配验证
LICENSES/                  # 上游许可
NOTICE.md                  # 来源与署名
```

VLESS 是代理协议，不是一种域名名单格式。使用 VLESS 节点时，仍应按客户端选择名单格式。后续为 sing-box / Xray / Mihomo 等增加格式时，扩展 `scripts/build.py`，输出到 `rules/<client>/`，复用 `source/`，不再维护独立域名副本。当前未生成或声称支持这些客户端的专属格式。

维护时仅修改 `source/`，然后：

```sh
python3 scripts/build.py
python3 scripts/build.py --check
python3 -m unittest discover -s scripts -p 'test_*.py'
```

提交源文件与生成结果后，`main` Raw URL 自动对应新版本；客户端按刷新策略拉取。校验脚本仅检查文件与转换，不自动添加或扩充域名。当前 GitHub 凭据没有 workflow 写入权限，因此未启用 GitHub Actions；维护时运行上述本地校验命令。域名和可选 IP 当前为手工审核快照，不会定时抓取上游。

## 覆盖与边界

[覆盖与来源说明](docs/coverage.md)。含 V2EX、Reddit、X、Telegram、Instagram、Facebook、Threads、WhatsApp、TikTok、Discord、Slack、LINE、GitHub、Google、YouTube、Lazada、Temu、TikTok Shop、IBKR、中银香港、汇丰香港、Wise、Notion、Gemini、ChatGPT、Claude、Grok、Meta Muse、Cursor、Siri 等常用服务。

部分共享云/CDN 后缀会匹配其他租户。动态第三方域名、地区/账号限制和新的服务端主机可能超出清单。IP 列表不等于解决全部语音连接问题，出口仍需支持相应流量。规则生成和静态匹配验证不等于在客户端或中国大陆网络实际连通验证。

若 Raw URL 在当前网络无法访问，应使用可访问的网络或现有代理完成首次下载；本仓库不承诺 GitHub 在所有网络直接可达。

## 许可

基于 GPL-2.0 上游规则派生，按 [GNU GPL v2](LICENSE) 分发；V2Fly MIT 来源的版权与许可保留在 [LICENSES/v2fly-MIT.txt](LICENSES/v2fly-MIT.txt)。来源、修改说明见 [NOTICE.md](NOTICE.md)。

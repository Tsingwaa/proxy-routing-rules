# 覆盖与来源（2026-10-09）

当前为 559 条常用域名，不是所有国外应用的完整数据库。上轮比较了 210 份社区规则文件，扩充到 4,902 条；本版按常用范围精简，主动不再覆盖所有来源条目。没有使用私人浏览历史判断使用频率。

## 重点应用

- 社媒：V2EX（含 i.v2ex.co 图片）、Reddit、X、Instagram、Facebook、Threads、TikTok、Snapchat、Pinterest、LinkedIn。
- IM：Telegram、WhatsApp、Messenger、Discord、Slack、LINE；保留主要附件/CDN 后缀。
- AI：Gemini、ChatGPT、Claude、Grok、Meta AI / Muse、Cursor、Siri。Muse 按 Meta 应用收录。保留已核对的身份验证、互动组件、内容预览、云虚拟机等依赖。
- 开发：GitHub / Copilot、Notion；含附件和资源域。GitHub 用户自定义域、Notion 自定义站点等仍需按实际访问补充。
- 金融：Wise、IBKR、中银香港、汇丰香港；香港银行及共享服务，IBKR 主要入口与 TWS 服务域。未登录验证交易。
- 电商：Amazon、eBay、Lazada、Temu、TikTok Shop、Shopee 等。Lazada 保留 lazcdn.com、slatic.net 和特定 alicdn 主机；未扩大到整个 alicdn.com。
- 旅行：Google Maps、Grab、Booking、Agoda、Skyscanner、Trip.com 等。保留国际 Trip.com 页面实际引用的 tripcdn.cn，移除大陆版携程入口。
- 云平台/媒体：Google、AWS、Azure、Oracle 及常用部署平台；YouTube、Netflix、Disney+、Spotify 等。

单条 DOMAIN-SUFFIX 规则已匹配根域及所有子域，不必逐个列出。只保留部分地区入口，未保留所有国家站点。共享云后缀仍会覆盖其他租户；分类文件跨类别依赖见 README。

## 主要来源

社区规则：

- https://github.com/blackmatrix7/ios_rule_script/tree/master/rule/Shadowrocket
- https://github.com/v2fly/domain-list-community/tree/master/data

官方网络与服务资料：

- OpenAI：https://help.openai.com/en/articles/9247338-network-recommendations-for-chatgpt-errors-on-web-and-apps
- Claude：https://code.claude.com/docs/en/desktop#network-access-requirements ，https://code.claude.com/docs/en/network-config
- Cursor：https://cursor.com/docs/enterprise/network-configuration ，https://cursor.com/help/troubleshooting/sign-in-domains
- Notion：https://www.notion.com/help/allowlist-ip
- GitHub：https://api.github.com/meta
- Apple：https://support.apple.com/en-us/101555
- Meta Muse：https://about.fb.com/news/2026/09/introducing-muse-personal-ai-agent/
- V2EX：https://www.v2ex.com/i/about
- 中银香港：https://its.bochk.com/login/ibs_lgn_index_e.jsp
- 汇丰香港：https://www.hsbc.com.hk/
- Wise：https://wise.com/
- Lazada：https://www.lazada.sg/
- Temu：https://www.temu.com/
- TikTok Shop：https://seller.tiktok.com/
- Grab：https://www.grab.com/sg/
- Agoda：https://www.agoda.com/
- Trip.com：https://www.trip.com/

部分公开页面（Booking、Klook、Expedia、Meta AI/Muse 下载页）在核对时无法取得完整正文，对这些服务采用其他可得资料及社区源。未把页面读取失败视作网络依赖核对通过。

## 可选 IP 来源

- Telegram：https://core.telegram.org/resources/cidr.txt （14 个 IPv4/IPv6 前缀）。
- ChatGPT 语音：https://openai.com/chatgpt-voice.json （23 个前缀；下载时文件 creationTime 为 2026-03-26T20:12:45.451356+00:00）。

这些前缀会变化，本版无定时更新。Surge 输出将 IPv6 转为 IP-CIDR6；Shadowrocket 沿用上游 IP-CIDR 写法；Stash 输出纯 CIDR 集。

## 验证边界

本地转换检查覆盖精确匹配/后缀匹配语义及 IPv4/IPv6 转换，检查生成文件与规范源一致。关键应用匹配检查通过。未在 Shadowrocket / Surge / Stash 实际加载，也未在中国大陆网络测试登录、视频、语音或交易。Apple AI 仍受设备与账号地区要求影响。

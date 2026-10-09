# 来源、署名与修改说明

本仓库为筛选及格式转换后的派生规则清单，非上游官方发行。

- **blackmatrix7 / ios_rule_script**：https://github.com/blackmatrix7/ios_rule_script ，原许可 GNU GPL v2。本仓库 LICENSE 保留上游许可文本。主要参考 Shadowrocket 应用列表。
- **V2Fly / domain-list-community**：https://github.com/v2fly/domain-list-community ，MIT。原版权及许可见 LICENSES/v2fly-MIT.txt。
- 官方网络要求和公开服务入口：见 docs/coverage.md。官方页面是域名事实依据，不表示上游作者或服务运营方认可本仓库。

2026-10-09 修改：将来源按常用服务范围筛选为 559 条域名；移除大量长尾服务、地区与保留域；按父域覆盖语义去重；增加官方登录/API/CDN 依赖；分离 37 条可选 IP 前缀；生成 Shadowrocket、Surge、Stash 及分类格式。原上游完整文件并未整包发布。

本地规则源读取时记录的仓库 HEAD（master 文件下载并非原子快照）：

- blackmatrix7：036c097eb26c6a52c4f04ebcb6633043cb942669
- V2Fly：c6adacf29cc4fb05e04651fcf03e00989ef9f797

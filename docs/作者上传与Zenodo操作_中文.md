# 作者操作指南：从私有 GitHub 仓库到可引用 DOI

> 本仓库尚未上传 GitHub，尚未创建 DOI，尚未得到发表许可审查的全部结果。请不要误认为下载 ZIP 即完成代码存档。

## 第一阶段：只在私人账户里准备，不对外发布

1. 登录 https://github.com/ ，点击右上角 **+ → New repository**。
2. Repository name 建议 `comparative-sentiment-validity`，Visibility 选择 **Private**；初始化设置可以不勾选 README，因为 ZIP 已含 README。
3. 将下载 ZIP 中的 `comparative-sentiment-validity` 文件夹内容上传到新建仓库。可通过 **Add file → Upload files** 上传；需要把这些文件放在仓库根目录，而非再嵌套一层。
4. 仓库中应有 `README.md`、`analysis/`、`audit/aggregates/`、`docs/`、`tests/`、`.gitignore` 等文件。**不要上传** `Tweets.csv`、`GOP_REL_ONLY.csv`、`airline_predictions.csv`、`gop_external_validation_results.zip`、恢复 ZIP、Colab 缓存或原始社交账号信息。
5. 用仓库的文件搜索确认没有手机、私人通讯邮箱、账号凭证、推文正文、文本 SHA256 行级映射。个人姓名作为拟定作者署名不是需要秘密保存的凭证。

## 第二阶段：许可和研究声明校验

1. 核实两份历史原始语料的取得与使用条款。原文件可从第三方网址下载，并**不必然允许你重新发布推文全文或用户身份信息**。
2. 由作者选择代码许可，如 MIT；在此之前仓库保留 `LICENSE_PENDING.md`，**不能直接对外宣称开源授权已经完成**。
3. 核对研究论文描述与 `docs/INFERENCE_PROTOCOL.md` 的模型版本限制一致：准确的旧 RoBERTa Git commit 仍未确认。
4. 需要作者完成伦理审查适用性处理与 AI 辅助声明；“公开社交媒体历史数据”不是自动的伦理豁免凭证。

## 第三阶段：正式可引用存档

1. 只在完成以上核查后，将 GitHub 仓库公开：**Settings → General → Danger Zone → Change repository visibility**（GitHub 界面可能更新）。
2. 打开 https://zenodo.org/ ，登录，并授权连接 GitHub。
3. 依照 https://help.zenodo.org/docs/github/ 启用对应公开仓库；创建带版本标签的 GitHub Release。
4. 待 Zenodo 把该 Release 归档后，记录页面实际生成的 **版本 DOI**，再写入论文 Data/Code Availability 声明及 `CITATION.cff`。不要凭空填写 DOI。
5. 投稿前再检查全部作者真实声明、文件许可、图表版权、伦理适用性与官方期刊要求。

## 若暂时只想完成论文而不公开代码

维持私人仓库即可；它能保护代码和审计历史，但**不能算作“公开的 DOI 存档”**。可以先保留文中临时占位，并在真正公开时再换成可访问的永久链接。

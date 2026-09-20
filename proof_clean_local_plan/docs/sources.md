# 参考资料与证据边界

初始检索日期：2026-09-19；Phase 1 公开来源复核日期：2026-09-20。以下是阅读入口，不替代参与者阅读原文。没有获得原始实验数据；本包也没有复制论文图片或作者数据。扩展来源 S6–S11 的完整元数据与核对级别见仓库根目录 `research/source_ledger.csv`，综合结论见 `docs/PRIOR_ART_AUDIT.md`。

## S1 · Novel Technologies for Rapid Proof of Clean in Professional Environments

https://www.innocentive.com/challenges/novel-technologies-for-rapid-proof-of-clean-in-professional-environments/

核查本次比赛的范围、排除项、提交规则、截止时间、AI 条款和协议；最终以实时页面及登录后协议为准。 可支持：赛事规则。不能据此断言：本方案已经被主办方接受，或已经达到 TRL 3。

## S2 · NASA: Technology Readiness Levels

https://www.nasa.gov/directorates/somd/space-communications-navigation-program/technology-readiness-levels/

理解原理验证与成熟系统的区别。 可支持：TRL 分级的一般解释。不能据此断言：纯仿真自动构成整套硬件技术的 TRL 3。

## S3 · Huang et al. (2019), Structured-light modulation analysis technique for contamination and defect detection of specular surfaces and transparent objects

https://doi.org/10.1364/OE.27.037721

最接近的结构光调制检测工作，应作为基线与已有技术。 可支持：相关光学机制及已有实验先例。不能据此断言：本项目的创新性、真实食品残留检出限、细菌检测、整室性能。

## S4 · Tian et al. (2025), A Polarimetry-based Field-deployable Non-interruptive Mirror Soiling Detection Method

https://arxiv.org/abs/2501.01643

核对大面积镜面污染光学检测的相邻技术。 可支持：太阳能镜面场景已有不同路线的研究先例。不能据此断言：室内卫生表面上可以直接得到相同性能。

## S5 · WO2008029946A1: Contamination evaluation method and related systems

https://patents.google.com/patent/WO2008029946A1/en

提醒参与者污染评估、指纹及清洁前后恢复评估有长期已有技术。 可支持：存在相关已公开技术内容。不能据此断言：该专利的当前法律状态、自由实施结论或本方案的专利性。

## Phase 1 扩展来源

- **S6**：Huang et al. (2020), improved SMAT models；已有双正交条纹融合和污染/缺陷形貌建模。
- **S7**：Huang (2020), direct structured-light inspection；已有二值结构光污染/缺陷直接成像。
- **S8**：Burke et al. (2023), deflectometry review；反射表面条纹检测是成熟领域，且污染/缺陷可混淆。
- **S9**：Mäkilä et al. (2019), hospital optical contamination imaging；专业环境光学清洁成像已有实证先例，但其高光谱路线受本赛事 TRL 条件限制。
- **S10**：Mari et al. (2025), automotive cleaning QC；不同角度及可见/红外照明的清洁前后视觉质检已有先例。
- **S11**：Li et al. (2003), two-frequency phase measurement；多频相移与噪声权衡并非新概念。

未在本轮检索到完整组合不等于该组合不存在；novelty 和 freedom-to-operate 均保持 `UNVERIFIED`。

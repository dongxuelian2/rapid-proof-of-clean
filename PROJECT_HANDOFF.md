# Rapid Proof of Clean — project handoff

这是下一轮工作的唯一入口。本文档整理的是 `proof_clean_local_plan/` 中已有的实现、结果和研究记录；本轮没有新增技术方案、没有修改核心算法、没有解决 failure mode，也没有开始最终 proposal。

整理日期：2026-09-20

## 当前状态摘要

现有主线是一个“参考校准的多频主动反射/结构光调制筛查”计算原型：对清洁参照和样品分别采集两个方向、多个空间频率、每频四个相位的合成反射序列；由四相位解调得到调制幅值；在有界误差和清洁状态几何变化约束下，求额外高斯反射传递模糊方差的可行区间；当信息不足时拒判为 `UNKNOWN`，当区间支持低于阈值或高于阈值的结论时分别输出 `PASS` 或 `FLAG`。

核心代理量 `q` 的单位是照明坐标下的等效高斯模糊附加方差 `pixel²`。它没有被标定为油量、膜厚、蛋白质量、CFU、病原体浓度或任何卫生学标准。当前证据等级是 `SYNTHETIC_ONLY`：没有真实残留、相机、屏幕、专业环境或整室流程的实验验证。

archive 自带的 SHA-256 manifest 在解压后逐项匹配；本轮实际运行了原始测试和完整现有 pipeline，结果与 `reference_run/` 的 metrics/stress 内容一致。核心实现保持原样，作为独立子项目保留在 `proof_clean_local_plan/`；临时生成的运行输出没有导入正式仓库。

## 核心技术思路（现有内容的准确表述）

模型对每个方向、位置和频率使用：

```text
z_j = log(M_ref,j / M_sam,j) = a + x_j t
x_j = 2π² f_j²
t = b + q
```

其中 `b` 是清洁状态的几何/焦点变化，`q >= 0` 是待测残留在模型中的额外模糊代理。四相位幅值由
`0.5 * hypot(I0 - I2, I3 - I1)` 恢复。若每帧误差界为 `ε`，程序使用 `Δ = sqrt(2) * ε` 推出幅值和对数比值的区间，再通过所有频率对的斜率约束得到 `t` 的可行区间，结合 `|b| <= b_max` 得到 `q` 的上下界。

判定规则是：

- `PASS`：两个方向的所有可行 `q` 都低于 `q_crit`；
- `FLAG`：至少一个方向的 `q` 下界达到或超过 `q_crit`；
- `UNKNOWN`：信号不足、饱和、相位闭合失败、可见性无效、区间为空或结论不够确定。

这是模型条件下的区间包含和拒判逻辑，不是现实世界的无菌证明或零错误率保证。

## 已实现内容

- `src/core.py`：四相位解调、斜率可行区间、双方向 `PASS/FLAG/UNKNOWN` 推断。
- `src/simulation.py`：32×32 合成场景、六种基准条件和十二种 stress 条件。
- `run_pipeline.py`：`doctor`、`tests`、`smoke`、`benchmark`、`stress`、`report` 和 `all` 入口。
- `check_outputs.py`：输出文件、状态计数、证据标签及不支持声明的完整性检查。
- `time_budget.py`：明确标记为假设的采集/移动/报告时间预算。
- `tests/test_core.py`：8 个单元测试，涵盖解调、误差界、斜率区间、真值包含、盲区拒判、增加频率的可行集关系、高斯核和数值稳定性。
- `extensions/adaptive_spec.md`：自适应频率测量规格，明确标记为尚未实现。

## 已验证结果

本轮在当前 Windows 项目虚拟环境中实际执行：

```text
run_pipeline.py tests     -> 8 tests, 0 failures, 0 errors, exit 0
run_pipeline.py all       -> doctor/tests/smoke/benchmark/stress/report completed
check_outputs.py          -> pipeline_integrity_passed=true, exit 0
reference vs current      -> metrics_equal=True, stress_equal=True
```

archive 的 reference run 记录为 72 个 benchmark 场景（6 条件 × 12）、48 个 stress 场景（12 条件 × 4），均为合成场景。reference run 的原始环境是 Linux、Python 3.13.5、NumPy 2.3.5；本轮复现环境是仓库 `.venv` 的 Windows、Python 3.12.11，指标仍完全一致，但耗时和环境元数据不应逐字节比较。

## 当前 baseline 指标

配置：`image_size=32`；频率为 `[2, 4, 8, 16, 32, 48]` cycles/screen；两个方向；四相位；`q_crit=0.5 pixel²`；`scenes_per_condition=12`。下表是合成像素比例，不是独立样本统计量。

| 方法 | 代理量超标却 PASS | `q=0` 像素 PASS | UNKNOWN | 代理量超标 FLAG |
| --- | ---: | ---: | ---: | ---: |
| `uniform_DC` | 99.1111% | 99.07% | 0.00% | 0.89% |
| `single_frequency_modulation` | 8.2833% | 100.00% | 0.00% | 91.72% |
| `multi_frequency_point_estimate` | 6.4879% | 100.00% | 0.00% | 93.51% |
| `bounded_interval`（六频） | 0.0000% | 100.00% | 18.43% | 69.23% |
| `interval_two_frequencies` | 0.0000% | 100.00% | 19.15% | 69.23% |
| `interval_three_frequencies` | 0.0000% | 100.00% | 19.14% | 69.23% |

`uniform_DC` 在此合成器中本来就不占优势，因为主要响应改变的是调制幅值而非平均亮度；这不能证明对所有普通机器视觉方法全面领先。更多频率在当前结果中没有显著降低 UNKNOWN，且不能修复错误物理假设。

## 四个主要 failure modes

1. **污染或错误对应的参照（false PASS）**：`dirty_reference` 在 stress run 中为 100% `PASS`。如果参照本身带有同类变化，前后比较缺少可信基准，区间推断不能发现它。
2. **光学不可见或只改变直流吸收的残留（不可辨识）**：`uniform_absorber` 和 `optically_invisible_residue` 均为 100% `PASS`。当前模型观测的是调制传递变化；完全相同的可观测数据无法由算法区分不同物理状态。
3. **几何/焦点/相位/频率增益失配**：超出焦点变化界时为 100% `FLAG`；`negative_blur_cancellation` 为 100% `PASS`；`frequency_dependent_gain` 约 99.78% `FLAG`；`phase_motion` 为 100% `UNKNOWN`。这说明有界误差结论依赖误差界和固定增益假设。
4. **可观测性、饱和与表面缺陷混淆**：低信号、裁切、超出噪声界和相位运动会大量转为 `UNKNOWN`，遮挡场景只有可见半面被处理；`scratch_like_response` 为 100% `FLAG`，即干净但有划痕的表面可能被当作需要复查的异常。视场外表面没有证书。

## 状态分类

### CONFIRMED

- 现有代码可在 CPU、无网络环境下运行；本轮 8 项测试通过，完整 pipeline 和完整性检查通过。
- `infer` 的输入是 `reference`、`sample`、`cfg`、`visible` 和可选频率索引，不接收 `q_truth` 或物理污染标签；真值只在评估阶段使用。
- 模型实现了四相位解调、误差界区间、斜率可行集、三态输出和合成 stress cases。
- 在当前固定合成配置下，`bounded_interval` 没有代理量超标的 PASS；这只是模型/合成器条件下的结果。
- 参考结果、当前复现结果和输出完整性标记均为 `SYNTHETIC_ONLY`；物理验证、novelty 和完整系统 TRL 标记为 false。

### ASSUMPTION

- 高斯反射传递核近似；`q`、`b_max`、`q_crit` 和 `ε` 的数值均为模型设定。
- 同一方向同一位置的参照/样品增益比在频率间固定；四相位序列满足相移关系；未饱和且灰度误差被给定界覆盖。
- 参照对应清洁基准、可见性 mask 正确、样品位置/焦点变化可由 `b_max` 覆盖。
- 32×32 图像、六频、12 场景/条件、20 m² 目标面积、有效视场和时间预算参数都是假设；时间预算不是现场测量。
- 合成器中的材料/残留标签是抽象构造，不是实物真值。

### OPEN

- `q` 与真实残留种类、质量、膜厚、微生物负荷或卫生判定的关系；真实灵敏度、检出限和校准方法。
- 真实相机/屏幕采集、同步、线性化、曝光、白平衡、压缩、材质变化和独立重复实验。
- 参照获取和污染监测、整室/目标表面覆盖、盲区审计、实际时间和成本。
- 主办方当前规则、协议、AI 条款、截止时间以及参与者的人工贡献记录；archive 的来源快照日期为 2026-09-19，需人工重新核对。
- 与既有结构光调制、镜面污染检测和清洁前后评估相比的可核对差异；当前 novelty 状态仍是 `unverified`。
- 自适应频率扩展是否值得实现；物理小样实验是否具备安全、合适且已有的设备条件。

### KNOWN LIMITATION

- 不能检测完全光学不可见或只造成均匀吸收的状态。
- 污染参照、几何变化抵消和超出误差界的频率增益会造成错误 PASS、错误 FLAG 或 UNKNOWN。
- 低信号、遮挡、饱和、相位移动和覆盖盲区会使结果不可判定；算法不会把相邻位置外推成已检查。
- 划痕、纹理和其他非残留异常可能触发 FLAG；`FLAG` 不是“发现残留”。
- 合成像素共享场景参数，不能当作独立实验样本；零错误 PASS 不能转成真实世界零错误率。
- 当前没有硬件、专业空间、真实残留、微生物检测、商业成本、整室流程或实验 TRL 3 证据。

## 当前 claims 与证据边界

| Claim | 状态 | 依据/边界 |
| --- | --- | --- |
| 结构光调制在部分镜面/透明表面的污染或缺陷检测已有公开先例 | `OPEN / SOURCE-RECORDED` | S3 及 `docs/sources.md`；本轮未扩大检索，需人工读原文 |
| 本实现包含合成渲染、误差区间、拒判、benchmark 和 failure cases | `CONFIRMED` | 代码、8 项测试、完整 pipeline |
| 在给定模型和误差界内，区间推断可避免当前合成代理量超标的 PASS | `CONFIRMED / MODEL-CONDITIONAL` | `reference_run/summary.json` 与当前复现；不是物理准确率 |
| 可以检测真实残留、细菌、菌株或证明无菌 | `KNOWN LIMITATION / NOT CLAIMED` | `docs/claims.json` 明确列为未验证 |
| 已经达到实验系统 TRL 3、具备整室能力或可投稿 | `OPEN / NOT ESTABLISHED` | `reference_run/integrity_check.json` 明确否定这些状态 |
| 本组合具有新颖性或专利性 | `OPEN / UNVERIFIED` | `docs/prior_art.csv` 只有初步比较，不能支持结论 |

## Prior art / 引用情况

当前 archive 的引用表包含 5 个来源，检索核对日期写为 2026-09-19；本轮只整理原有记录，没有进行新的文献搜索：

- **S1**：InnoCentive 的 Rapid Proof of Clean challenge 页面，用于规则、范围、提交和协议核对；实时页面与登录后协议优先。
- **S2**：NASA Technology Readiness Levels，用于 TRL 一般概念；不能把纯仿真自动升级为硬件 TRL 3。
- **S3**：Huang et al. (2019), *Structured-light modulation analysis technique for contamination and defect detection of specular surfaces and transparent objects*；最接近的结构光调制先例。
- **S4**：Tian et al. (2025), *A Polarimetry-based Field-deployable Non-interruptive Mirror Soiling Detection Method*；相邻镜面污染路线。
- **S5**：WO2008029946A1, *Contamination evaluation method and related systems*；长期公开的污染/清洁评估相关技术。

`docs/prior_art.csv` 已将屏幕/相机结构光、四相位调制、光学污染映射和清洁前后评估标为已有或未主张新颖；“可行区间 + 拒判 + 覆盖预算”的差异仍未完成逐文献核对。不能把“未看到”解释为“不存在”。

## 关键文件导航

- 项目内说明：[proof_clean_local_plan/README.md](proof_clean_local_plan/README.md)
- 执行代理边界：[proof_clean_local_plan/AGENTS.md](proof_clean_local_plan/AGENTS.md)
- 总任务顺序：[proof_clean_local_plan/执行计划.md](proof_clean_local_plan/执行计划.md)
- 核心推断：[proof_clean_local_plan/src/core.py](proof_clean_local_plan/src/core.py)
- 合成器：[proof_clean_local_plan/src/simulation.py](proof_clean_local_plan/src/simulation.py)
- 运行入口：[proof_clean_local_plan/run_pipeline.py](proof_clean_local_plan/run_pipeline.py)
- 完整性检查：[proof_clean_local_plan/check_outputs.py](proof_clean_local_plan/check_outputs.py)
- 数学边界：[proof_clean_local_plan/docs/mathematical_basis.md](proof_clean_local_plan/docs/mathematical_basis.md)
- Claims：[proof_clean_local_plan/docs/claims.json](proof_clean_local_plan/docs/claims.json)
- Prior art：[proof_clean_local_plan/docs/prior_art.csv](proof_clean_local_plan/docs/prior_art.csv)
- 来源边界：[proof_clean_local_plan/docs/sources.md](proof_clean_local_plan/docs/sources.md)
- 结果报告：[proof_clean_local_plan/reference_run/report.md](proof_clean_local_plan/reference_run/report.md)
- 机器可读结果：[proof_clean_local_plan/reference_run/summary.json](proof_clean_local_plan/reference_run/summary.json)
- 失败/应力结果：[proof_clean_local_plan/reference_run/stress.csv](proof_clean_local_plan/reference_run/stress.csv)
- 测试：[proof_clean_local_plan/tests/test_core.py](proof_clean_local_plan/tests/test_core.py)
- 任务卡：`proof_clean_local_plan/tasks/T00.md` … `T23.md`
- 人工审阅状态：[proof_clean_local_plan/human/review.json](proof_clean_local_plan/human/review.json)

## 如何复现实验

先从仓库根目录运行一次现有项目的 bootstrap，之后进入独立子项目：

```powershell
Set-Location E:\rapid-proof-of-clean
.\scripts\bootstrap.ps1
Set-Location .\proof_clean_local_plan
& ..\.venv\Scripts\python.exe run_pipeline.py tests
& ..\.venv\Scripts\python.exe run_pipeline.py all
& ..\.venv\Scripts\python.exe check_outputs.py
& ..\.venv\Scripts\python.exe time_budget.py
```

这些命令使用 CPU、Python 和 NumPy，不需要 GPU、网络、账号、付费 API 或云服务。`run_pipeline.py all` 会在 `proof_clean_local_plan/outputs/` 生成本机结果；该目录除 `.gitkeep` 外被忽略。`reference_run/` 是 archive 制作时保存的参考运行，不能冒充参与者自己的实验。当前合并版运行输出已删除，没有被当作证据提交。

## 尚未解决的问题

1. 先由参与者完成 T00–T02：确认边界、阅读实时 challenge/协议和 AI 条款、复核最接近 prior art，并写出真实人工贡献；这些不能由模型代签。
2. 完成 T03–T13 的冻结配置、机器记录、时间/面积审计、信息泄漏检查、结果复现和状态图审查；只保留可追溯的运行记录。
3. 对真实残留相关光学响应、参考可靠性、几何/相机误差和目标表面范围建立证据；在此之前不要把 `q_crit` 当成物理检出限。
4. 在有人作出明确决定后，才判断是否实现 adaptive extension 或进行符合协议的安全小样验证；当前二者均未实现/未进行。
5. 最后才处理 TRL、部署、成本、claim audit 和是否提交；不要把计算报告直接当作最终 proposal。

## 推荐的下一阶段工作顺序

按现有任务卡顺序继续，而不是另起一条方案线：

1. **人工边界与规则门槛（T00–T02）**：先完成参与边界、实时规则/IP/AI 条款和 prior-art/novelty 记录。
2. **可复现性和计算审计（T03–T13）**：冻结配置，复核时间预算、数据流、反例、状态图和双次运行一致性。
3. **扩展/小样决策门（T14–T17）**：只在参与者明确选择并具备条件时处理自适应规格或安全物理小样；不把计划写成实现。
4. **证据、TRL 和交付审阅（T18–T23）**：分开公开先例、计算结果、本人实测和未验证预测，完成 claim audit 后再决定是否继续提交准备。

本 handoff 到此停止；下一轮应先读完本文档，再打开对应任务卡，不要从 README 或结果表直接推导新的物理结论。

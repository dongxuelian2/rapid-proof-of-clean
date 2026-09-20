# 执行记录

本文件初始为空记录。每完成一张任务卡，追加真实执行的日期、命令、退出码、输出路径及验收结果。不得将 reference_run 的结果记为自己的实验。

## 2026-09-20 · T00–T02 machine-assist boundary

完成的动作：核对官方公开挑战页，整理截止、范围、表单、AI 与公开 IP 条款；对 S3–S11 做公开来源审计；更新 source/claims/prior-art ledgers。输出路径：仓库根目录 `CHALLENGE_RULES.md`、`research/`、`docs/PRIOR_ART_AUDIT.md`。验收结果：公开事实均带 URL 和访问日期；登录协议、地域、付款、税务、保密及人的贡献判断保留 `TO VERIFY`，未代签人工事项。仍未证明的内容：完整协议合规、参与者资格、novelty、FTO 和投稿资格。

## 2026-09-20 · v0 freeze and Phase 1 benchmark

完成的动作：在修改核心模拟器前运行 `run_pipeline.py all`、`check_outputs.py`、root pytest 与 ruff，核对 reference/current；创建 `v0-baseline`；随后实现并执行 `scripts/run_phase1.py`。输出路径：`experiments/v0_baseline/`、`experiments/failure_mode_registry.csv`、`experiments/results/`。验收结果：v0 metrics/stress/8 tests 一致；Phase 1 pipeline exit 0；v1 标准回归没有 proxy false-clean 或 q=0 PASS 退化。仍未证明的内容：所有结果均为 SYNTHETIC_ONLY，未进行物理实验。

## 2026-09-20 · Phase 1 final verification

完成的动作：运行 root `pytest`、原始 `run_pipeline.py tests`、`check_outputs.py`、root `ruff check .`、`scripts/verify_repo.py` 和完整 `scripts/run_phase1.py`。输出路径：终端记录及 `experiments/results/`。验收结果：root 8/8、原始 8/8，ruff/完整性/repo verification 全部 exit 0；registry 192 行（4 failure modes × 8 scenes × 6 methods），JSON 全部可解析。仍未证明的内容：没有真实硬件、残留、专业环境、30 分钟覆盖或 submission readiness 证据。

## 2026-09-20 · final adaptive/domain-shift computation

完成的动作：执行 `scripts/run_final_research.py` 与 `scripts/run_final_validation.py`，实现顺序采集、dated-anchor 参考完整性、不同响应算子的域偏移测试、400 例对抗搜索和自适应覆盖预算；随后运行 root ruff 与 pytest。输出路径：`experiments/results/final_research_results.json`、`final_policy_benchmark.csv`、`adaptive_coverage_time_model.csv`、`experiments/adversarial_regressions.json`。验收结果：v2.2 在原模型保持 5.568% 非匹配污染像素 false-clean，clean PASS 由 44 帧降至 36 帧；域偏移 FOV false-clean 由 11.667% 降至 1.111%，但 UNKNOWN 上升；ruff 通过。仍未证明的内容：所有新数字均为合成结果，没有真实残留、真实噪声、硬件时序、现场覆盖或物理非劣效性证据。

## 2026-09-20 · final canonical verification

完成的动作：运行 `scripts/run_submission_pipeline.py`，依次重建 Phase 1、最终研究、最终验证、v2、帧预算、proposal audit、图件和 submission package，并执行 repository verification、ruff 与 pytest；随后将 Phase 1 墙钟微基准标记为空值并规范化 unittest 耗时，避免固定种子结果因机器负载产生无意义 diff。输出路径：全部受管结果、图件及 `submission_package/`。验收结果：repository verification 检查 91 个必需文件并通过，ruff 通过，pytest 34 项通过；连续两次 Phase 1 生成物哈希一致。仍未证明的内容：这些是软件与合成证据，不能替代 coupon、硬件、现场、法律或正式提交验证。

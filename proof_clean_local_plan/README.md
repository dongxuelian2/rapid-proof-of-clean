# Proof-clean：零预算、本地 CPU 的研究执行包

本包供参与者探索“参考校准的主动光学残留筛查与保守判定”方向。它包含可运行的计算原型、24 张任务卡、中文详细执行计划、已有工作核对表、英文投稿写作框架和失败案例。**它没有完成真实残留检测、专业空间整室验证、创新性确认或 TRL 认证，不能原样冒充已验证参赛作品。** 主方向是已校准光滑表面上具有可测反射调制变化的残留筛查，不承担微生物物种鉴定。

## 最短启动路径

要求 Python 3.10 及以上。进入解压后的项目目录。Linux/macOS：

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_pipeline.py all
.venv/bin/python check_outputs.py
.venv/bin/python time_budget.py
```

Windows PowerShell：

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_pipeline.py all
.\.venv\Scripts\python.exe check_outputs.py
.\.venv\Scripts\python.exe time_budget.py
```

安装 NumPy 可以联网，核心运行不访问网络。不升级系统 Python，不用 sudo pip。已有 NumPy 时可使用已有环境。没有网络且没有 NumPy，先在能联网的同系统机器准备对应 wheel；不要改为付费云服务。Python 本身尚未安装时，从官方发行渠道安装，这是环境准备，不涉及训练模型。

## 阅读顺序

先读 `执行计划.md` 和 `AGENTS.md`，再交给小模型一张任务卡。`src/` 和 `run_pipeline.py` 是已实现的最小原型；`extensions/` 的内容是尚未实现的可选扩展规格。`reference_run/` 保存本包生成时实际运行的示例结果，不能写成参与者自己的实验。参与者重新运行的结果生成到 `outputs/`；人的研究决定与阅读记录写到 `human/`。数据及方法均处于研究用途，最终提交前必须验证信息及权利条件。

`outputs/report.md` 是英文计算报告；`outputs/summary.json` 是机器可读摘要；`outputs/benchmark.csv` 和 `outputs/stress.csv` 包含逐场景结果；`outputs/example_map.npz` 是状态图及真值。`time_budget.py` 生成的是假设性现场时间预算，不是设备实测。

## 已知核心限制

均匀吸收薄膜、光学不可见残留、已污染参照以及未建模的几何变化可能导致危险的误通过；永久划痕可能触发异常。包中保留这些反例。现有六频方案相对两频方案的收益不大，因此不能声称“频率越多就越先进”。这套起点的价值是检验假设、确定否定性边界和组织后续人类研究，取得比赛认可仍取决于差异化、科学证据和现场可行性。

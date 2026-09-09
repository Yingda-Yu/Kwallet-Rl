# K-Wallet / ICASSP 2027 执行看板

初始化 2026-09-09；本板由 agent 用真实证据维护。执行规格见
`TRAE_KWALLET_ICASSP2027_EXECUTION.md`。

状态：TODO / RUNNING / PASS / FAIL / BLOCKED / NOT_RUN。每格证据指向命令、文件、
run ID 或 commit。未运行绝不标 PASS。

分支：`work/icassp2027-reproduce-improve`（commits 161ec75 Phase-1、
22e18e3 Phase-2 set/streaming/rules、f5960e3 ablations+assets+docs）。
`paper/` 不入库（受保护）。

## A. 环境与资料（P0）

| ID | 任务 | 状态 | 证据 |
|---|---|---|---|
| A01 | 保护旧稿/模板、记录 SHA、确认分支 | PASS | `paper/old paper.pdf` SHA256 `3c82e8d8…`；`ICASSP2027_Paper_Templates.zip` `fd1cc410…`；`paper/` 未 staged（每次 commit 前校验） |
| A02 | 通读旧稿+全仓库，PAPER_CODE_MAP | PASS | docs/PAPER_CODE_MAP.md |
| A03 | 有界搜索原 SC-FAC/PPO artifact | PASS | 仓库为 DQN 时代；PPO 策略不存在 → 判定 REIMPLEMENTED（docs/DECISIONS.md 2026-09-09） |
| A04 | 服务器资源与授权核查 | PASS（GPU BLOCKED） | 96 线程/503GB；10×RTX3090 **未授权**，仅 CPU；见 docs/BLOCKERS.md B1 |
| A05 | conda env kwallet 隔离与版本 | PASS | Python 3.10 / torch 2.14 CPU / numpy 2.2.6；`kwallet doctor` |
| A06 | TeX Live 核验、官方模板编译 | PASS | TeX Live 2022；`paper/icassp2027/Template.pdf` 3pp 编译通过 |
| A07 | progress/decisions/blockers + 退出码 | PASS | docs/；CLI 非零退出；manifest CSV |

## B. 旧论文实现（P0）

| ID | 任务 | 状态 | 证据 |
|---|---|---|---|
| B01 | 已知/未知原参数清单 | PASS | docs/DECISIONS.md「chosen_for_reimplementation」 |
| B02 | one-settle/one-flush 环境 + 3k+2 状态 | PASS | src/kwallet/envs/kwallet.py；obs_dim=3k+2 |
| B03 | 刷新/冻结/补满/oversize/冲突/terminal 时序 | PASS | tests/test_env.py（13 tests PASS） |
| B04 | attempted/executed/charged flush + Money 一致性 | PASS | env 指标；tests test_env/test_smoke |
| B05 | JA/IFAC/SC 共用 PPO/GAE/trainer | PASS | src/kwallet/training/ppo.py；policies/actors.py |
| B06 | 小 k 枚举 log-prob/ratio/mask/梯度 | PASS | tests/test_policies.py（9 tests） |
| B07 | checkpoint/resume（权重 vs 续训） | PASS | PPOTrainer.checkpoint/load；val best ckpt |
| B08 | 版本化十二分布池 + 无泄漏 | PASS | data/pools.py data/regimes.py base_seed 532；tests/test_data.py（6） |
| B09 | 恢复 constrained FA/FWF，不冒称复现 | PASS | baselines/rules.py；标记 MISSING_RULE_DEFINITION（重构参考） |
| B10 | general-collateral one/two-pool 原实现追溯 | NOT_RUN | 旧稿为 K-Wallet 特例；通用 collateral 扩展无规格 → 范围外，缺失报告 |
| B11 | reconstructed_extension_v1（若需要） | NOT_RUN | B10 范围外；未编造 |
| B12 | 端到端 smoke（生成→训练→评估→出表→编译） | PASS | `run_experiments --tier smoke`；make_paper_assets；main.pdf 编译 |

## C. 旧论文实跑与核验

| ID | 任务 | 优先级 | 状态 | 证据 |
|---|---|---|---|---|
| C01 | 计时/预算/dry-run | P0 | PASS | PPO cycle JA5.2s/IFAC6.0/SC7.1s；eval 2400 ep ~3-4min |
| C02 | 主表 3 methods×4 C×seeds | P0 | RUNNING | matrix_main 5/76 eval 完成；3×4×5 seeds + 规则；聚合 results/tables |
| C03 | k-scaling C1200 k∈{6,12,24} | P1 | RUNNING | run_kscale（k=3 改为 6，因 k=3 钱包容量>max_tx 无意义）；aggregate_kscale |
| C04 | 十二 regime 指标（旧稿图5） | P0 | RUNNING | 每 run summary 含 per-regime；regime_money.csv 聚合随 matrix 出 |
| C05 | zero-settle / 条件置零消融 | P1 | RUNNING | sc_nocond（置零）/sc_shuffled（错位）；matrix_ablation 12 runs |
| C06 | tau=1/5/10/20 post-hoc 计价 | P1 | PASS（自动） | 每 eval 写 `_tau_posthoc.csv`；仅重计价不重训 |
| C07 | model-only 效率（不混淆加速） | P1 | PASS | runs/bench/bench_C1200.0_k24.csv；JA625 vs 因式50 logits |
| C08 | one/two-pool extension / 表 III | P1 | NOT_RUN | 同 B10，无规格 |
| C09 | 配对 seed CI + drop/accept/flush 分解 | P0 | RUNNING | evaluation/stats.py paired_difference；matrix 完成后出 |
| C10 | REPRODUCTION_REPORT | P0 | DRAFT | 见下；随 C02 完成定稿 |

## D. 改进与机制实验

| ID | 任务 | 状态 | 证据 |
|---|---|---|---|
| D01 | 锁定假设/对照/预算/选模规则 | PASS | docs/NOVELTY_AND_OVERLAP.md；val 选模、test 仅一次 |
| D02 | 修复 eval/dropout/context 问题 | N/A | 本实现自带；val 未记录 bug 已修（_maybe_eval_val crossing） |
| D03 | full-wallet rotation 基线 | PASS | baselines/rules_strong.rotate_settle_action；ROT val 7894 |
| D04 | best-fit+阈值强规则（仅 val 调参） | PASS | BFP0.5 val 15290→test 15327，可恢复 drops=0 |
| D05 | IndependentScores+ConditionalMask 合法率 | PASS | mask 强制 flush≠settle；tests 覆盖 |
| D06 | 参数/深度匹配 IFAC；恒定条件对照 | PASS | sc_nocond 与 sc_fac 同参 172,883 |
| D07 | 测试期置零/打乱诊断 | RUNNING | sc_nocond/sc_shuffled × C{800,1200} × seeds 训练中（同预算） |
| D08 | set-IFAC/set-SC + 等变性/null | PASS | policies/set_actors.py；tests/test_set_equivariance.py（4 tests） |
| D09 | flat/set×IFAC/SC 四格 + 强规则/JA | RUNNING | kscale（set vs flat 跨 k）+ matrix（flat 三方法）+ BFP |
| D10 | money-aligned reward 全方法重训 | NOT_RUN | env 有 reward_mode 路径；预算内未训（标 NOT_RUN） |
| D11 | 切换/held-out 需求强度 | PASS（规则）/RUNNING（学习） | runs/switching/switch_summary.csv：BFP post-drops=0（负结果）；学习型 finalize 自动跑 |
| D12 | 固定 C 的 k 扩展 + 未见 k 测试 | RUNNING | run_kscale 跨 k train/deploy；flat 不可迁移 |
| D13 | tau/p 重训敏感性 | NOT_RUN | 与 C06 post-hoc 区分；预算内未重训 |
| D14 | 可验证等变性命题/边界例 | PASS | 置换等变性测试；cross-k 权重加载测试（missing/unexpected 为空） |
| D15 | IMPROVEMENT_REPORT | DRAFT | docs/NOVELTY_AND_OVERLAP.md；随 D07/D09/D12 完成定稿 |

## E. 新稿、编译与交付

| ID | 任务 | 优先级 | 状态 | 证据 |
|---|---|---|---|---|
| E01 | 模板/分类/篇幅/AI 披露/截止 | P0 | PASS | 4pp+≤1 refs；≥9pt；无页码；非盲；ML-REI；AI 披露在 main.tex thanks |
| E02 | 作者/ORCID/投稿状态 | P0 | BLOCKED | 需用户确认作者/单位/基金；未投稿（占位 name） |
| E03 | primary-source 文献 + NOVELTY | P0 | PASS | refs.bib 仅可确证文献；NOVELTY_AND_OVERLAP.md |
| E04 | 证据支持的大纲/正文（占位显式 DRAFT） | P1 | PASS | paper/icassp2027/main.tex（编译通过，缺失表显式 pending） |
| E05 | raw runs→统计表/矢量图 + paper_claims | P0 | PASS | scripts/make_paper_assets.py；assets/paper_claims.json 记录缺失 |
| E06 | 英文正文 4pp+refs，结果据实 | P0 | DRAFT | 正文完，待 matrix/ablation/transfer 真实表注入定稿 |
| E07 | clean build + citation/页数/字体/无页码 | P0 | RUNNING | main.pdf rc=0、3pp、无未定义引用；最终数据后复核 |
| E08 | 逐页视觉核验 | P0 | TODO | 定稿表格后 pdftoppm 逐页 |
| E09 | artifact 源码/配置/哈希/README 重建 | P0 | TODO | 待最终；脚本已可一键重建表图 |
| E10 | 敏感信息/许可 + commit；不 push/PR | P0 | PARTIAL | 本地 3 commits；**未 push/PR/投稿**（待用户） |

## 进行中作业（后台）
- `run_experiments --tier main`（matrix_main，pid 163725）：60 learned + 16 rules。
- `run_kscale --exp kscale`（pid 1958730）：18 train + 跨 k eval。
- `run_experiments --tier ablation`（matrix_ablation，pid 1958731）：12 runs。
- `scripts/finalize_wait.sh`（pid 1970903）：三者结束后自动聚合→学习型切换→重生资产→重编译。
日志：runs/matrix_main_driver.log、runs/kscale_driver.log、
runs/ablation_driver.log、runs/finalize.log。

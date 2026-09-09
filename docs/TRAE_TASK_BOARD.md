# K-Wallet / ICASSP 2027 执行看板

初始化日期：2026-09-09。执行规格见 `TRAE_KWALLET_ICASSP2027_EXECUTION.md`。

**初始状态全部为 TODO：任务书已经提交，不表示研究任务已经完成。**每完成一项，agent 必须把对应状态改为实际状态，并在“证据”列填具体命令、文件、run ID 或 commit。不得只勾选而无证据。

状态：TODO / RUNNING / PASS / FAIL / BLOCKED / NOT_RUN。实现通过与 full 实验完成是不同验收项。优先级 P0/P1/P2 表示排程顺序，不代表低优先级可被悄悄删掉。

## A. 环境与资料（P0）

| ID | 任务与验收 | 依赖 | 状态 | 证据 |
|---|---|---|---|---|
| A01 | 确认仓库、分支、用户未提交文件，保护旧稿/模板并记录 SHA-256 | 无 | TODO | |
| A02 | 通读旧稿全文、表图与全仓库，建立 PAPER_CODE_MAP | A01 | TODO | |
| A03 | 在本仓库及 Git 历史查找原 SC-FAC/PPO/扩展/artifact，给出有界搜索记录 | A02 | TODO | |
| A04 | 检查共享服务器资源与项目授权，保存非公开 runtime limits | A01 | TODO | |
| A05 | 隔离 Python 依赖安装、导入、CPU/GPU 小测试，记录真实版本 | A04 | TODO | |
| A06 | 核验远程 TeX Live/PDF 工具；官方模板示例实际编译 | A01 | TODO | |
| A07 | 建立 progress/decisions/blockers、运行清单和错误退出规范 | A01 | TODO | |

## B. 旧论文实现（P0）

| ID | 任务与验收 | 依赖 | 状态 | 证据 |
|---|---|---|---|---|
| B01 | 列已知与未知原参数；恢复原配置，或明确标重实现选择 | A02,A03 | TODO | |
| B02 | 统一 one-settlement/one-flush 环境与 3k+2 状态 | B01,A05 | TODO | |
| B03 | 验证刷新顺序、冻结/补满时序、oversize、none、冲突和 terminal | B02 | TODO | |
| B04 | 明确 attempted/executed/charged flush，奖励与 Money 指标一致性测试 | B02 | TODO | |
| B05 | JA-PPO、IFAC、SC-FAC 共用 PPO/GAE/trainer | B01,B02 | TODO | |
| B06 | 枚举小 k 检查 log-prob、ratio、conditional input、mask、entropy、梯度 | B05 | TODO | |
| B07 | 真实 checkpoint/resume 测试；清楚区分权重恢复与完整续训 | B05 | TODO | |
| B08 | 版本化十二分布/训练验证测试池、哈希、无泄漏与统计检查 | B01,A03 | TODO | |
| B09 | 恢复 constrained FA/FWF；定义缺失时不冒称复现 | B01,B02 | TODO | |
| B10 | general-collateral one/two-pool 原实现追溯与测试；缺规格明确报告 | A03,B01 | TODO | |
| B11 | 原扩展缺失时另建 documented reconstructed_extension_v1，实际实现测试 | B10 | TODO | |
| B12 | 端到端 smoke：生成/加载→训练→评估→统计→出表→编译，不用假结果 | B03-B09,A06 | TODO | |

## C. 旧论文实跑与核验（P0/P1）

| ID | 任务与验收 | 优先级 | 依赖 | 状态 | 证据 |
|---|---|---|---|---|---|
| C01 | 短运行计时、内存/显存测量、dry-run 预算与获准调度清单 | P0 | B12,A04 | TODO | |
| C02 | 主表 3 methods×4 C×10 seeds；记录原配置或重实现等级 | P0 | C01 | TODO | |
| C03 | k-scaling，C=1200、k=3/6/12/24，H128/E32 与匹配 seeds | P1 | C01 | TODO | |
| C04 | 十二 regime 指标与旧稿图 5 对应分析 | P0 | C02 | TODO | |
| C05 | 原 zero-settle 消融的实际定义、运行及完整结果 | P1 | B01,C01 | TODO | |
| C06 | tau=1/5/10/20 post-hoc 计价，不冒称重新训练 | P1 | C02 | TODO | |
| C07 | model-only 及 end-to-end 性能；不要把 logits 比当加速倍数 | P1 | C01 | TODO | |
| C08 | one/two-pool extension 实验及表 III 差异报告，资料不足明确区分重建 | P1 | B10,B11,C01 | TODO | |
| C09 | 配对 seed CI、各类 drop 与接受金额/刷新分解，完整保留失败 seed | P0 | C02 | TODO | |
| C10 | REPRODUCTION_REPORT 覆盖旧稿每项主张并给出证据等级 | P0 | C02-C09 | TODO | |

注意：C10 可以持续更新，但只有所有覆盖项均有真实状态时才能验收报告；并不要求把所有项目伪装成成功复现。原实现无法找回是 BLOCKED/REIMPLEMENTED 的原因，不是使用旧表代替运行的理由。

## D. 改进与机制实验（P1）

| ID | 任务与验收 | 依赖 | 状态 | 证据 |
|---|---|---|---|---|
| D01 | 锁定假设、主要对照、预算、选模和最终测试规则 | B12,C01 | TODO | |
| D02 | 修复已确认的 eval/dropout/context/epsilon/config 问题，受影响基线同协议重跑 | D01 | TODO | |
| D03 | full-wallet rotation 基线、条件及单元测试，报告其成本而非假设最优 | B02,D01 | TODO | |
| D04 | best-fit+阈值刷新强规则；只在验证集调参 | B02,D01 | TODO | |
| D05 | IndependentScores+ConditionalMask 对照与合法动作率 | B06,D01 | TODO | |
| D06 | 参数/深度匹配 IFAC；训练期 constant condition；反向条件化 | B05,D01 | TODO | |
| D07 | 测试期置零/打乱的独立诊断，标明分布变化局限 | D06 | TODO | |
| D08 | 共享钱包编码的 set-IFAC/set-SC，信息公平、null action 与等变性测试 | B05,D01 | TODO | |
| D09 | flat/set×IFAC/SC 四格对照，强规则与 JA 参照，按锁定 seed 实跑 | D03-D08 | TODO | |
| D10 | original 与 money-aligned reward 全方法公平重训 | D01,B04 | TODO | |
| D11 | 随机时刻/顺序切换与 held-out 需求强度评估，控制信息和难度混杂 | B08,D01 | TODO | |
| D12 | 固定 C 的 k 实验与模型扩展性测量分开；测试未见 k | D08,D01 | TODO | |
| D13 | tau/p 重新训练敏感性，明确与 C06 的区别 | D10 | TODO | |
| D14 | 可验证的表示/等变性/轮换命题与边界例；不编造理论保证 | D03,D08 | TODO | |
| D15 | IMPROVEMENT_REPORT：真实增益、负结果、统计、资源成本、相对旧稿差异 | D02-D14 | TODO | |

D07、D13、D14 与更大 k 可按预算作为次要研究项，但必须保留 NOT_RUN 或明确完成证据。切勿在结果差时删除对照，或在看了测试结果后改写主要假设。

## E. 新稿、编译与交付（P0/P1）

| ID | 任务与验收 | 优先级 | 依赖 | 状态 | 证据 |
|---|---|---|---|---|---|
| E01 | 核验官方模板、分类、篇幅、AI 披露与截止说明，保存日期 | P0 | A06 | TODO | |
| E02 | 记录旧稿投稿/发表状态、作者/ORCID 等；缺项只阻塞 release | P0 | A02 | TODO | |
| E03 | 文献 primary-source 核验与 NOVELTY_AND_OVERLAP | P0 | D01 | TODO | |
| E04 | 先写证据支持的大纲/方法，结果占位显式为 DRAFT | P1 | B12,E01 | TODO | |
| E05 | raw runs→统一统计→LaTeX 表/矢量图；建立 paper_claims 追踪 | P0 | C09,D09 | TODO | |
| E06 | 完成英文正文，4 页技术内容及至多 1 页许可内容；结果据实 | P0 | D15,E03,E05 | TODO | |
| E07 | TeX Live clean build，citation/页数/字体/大小/无页码检查 | P0 | E06 | TODO | |
| E08 | 所有页面视觉核验，修复表图过小、溢出、空白与第 5 页违规内容 | P0 | E07 | TODO | |
| E09 | artifact 源码/配置/哈希/README；干净环境 smoke+图表/论文重建 | P0 | E08 | TODO | |
| E10 | 敏感信息/许可检查，真实 commit/push/PR，最终验收报告 | P0 | E09 | TODO | |

## 每次里程碑报告格式

```text
当前阶段和任务 ID：
新增/修改文件：
实际执行命令与退出码：
测试结果：
已完成 run / 总 run：
正在运行的实际作业及日志：
主要结果及其证据等级：
资源使用、预算和预计剩余时间：
失败/阻塞及已做排查：
接下来自动执行的任务：
需要用户决定的最少事项：
```

只在确实启动了作业时填“正在运行”。只有配置文件而没有结果时，写“已配置，NOT_RUN”。已编译的空壳/DRAFT PDF 不算 E06-E08 全部通过。

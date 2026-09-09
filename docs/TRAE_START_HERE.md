# 从这里启动 TRAE Code

## 这次仓库更新做了什么

这次提交提供任务书、agent 入口和任务看板。**尚未在用户服务器安装依赖、启动训练或生成新论文。**这些实际操作由 SSH 工作区中的 TRAE Code 按任务书执行。

- 完整规格：`docs/TRAE_KWALLET_ICASSP2027_EXECUTION.md`
- 进度看板：`docs/TRAE_TASK_BOARD.md`
- 仓库 agent 入口：`AGENTS.md`
- 任务文档分支：`docs/kwallet-icassp2027-execution-20260909`

## 给 TRAE 的启动提示词

把下面整段复制到当前 SSH 项目的 Agent 对话中。无须手动把长任务书粘进聊天。

```text
你现在负责实际完成 K-Wallet 项目的研发和论文升级，而不是只给我建议。

先确认当前工作区是我的 Yingda-Yu/Kwallet-Rl 仓库。截图中的路径为 /data/yingda/Kwallet-Rl，但以 pwd、git rev-parse 和 remote 实际检查为准。

先检查 git status、当前分支和未提交改动，保护我已经放入 paper/ 的旧论文和模板，不执行 reset --hard、git clean 或覆盖我的文件。

完整任务书在远程分支 docs/kwallet-icassp2027-execution-20260909。执行 git fetch origin 获取该分支。若任务文件尚不在工作区，先使用 git show origin/docs/kwallet-icassp2027-execution-20260909:docs/TRAE_KWALLET_ICASSP2027_EXECUTION.md 阅读，不必为了阅读而切换或清空当前工作区。确认分支和改动后，以可逆方式建立/继续自己的 work 分支并引入任务文档。存在同名文件或提交冲突时先比较合并，不覆盖。

接着完整阅读 AGENTS.md、docs/TRAE_START_HERE.md、docs/TRAE_KWALLET_ICASSP2027_EXECUTION.md 和 docs/TRAE_TASK_BOARD.md；这些文件不在当前分支时，同样可从上述远程分支 git show 读取。

按任务书真正完成三个阶段：
一、通读 paper/old paper.pdf 和全项目，寻找原实现/配置/artifact，补齐 JA-PPO、IFAC、SC-FAC、环境、数据、规则、统计、扩展和测试，实际运行并区分旧结果复现与重新实现。
二、在可信基线上实现强规则、机制消融、钱包排列等变条件策略、奖励与流式变化实验。按统一协议跑完，保留负结果，不为了赢而改测试集或捏造数据。
三、用 paper/ICASSP2027_Paper_Templates.zip 和已安装的 TeX Live 完成基于真实证据的英文 ICASSP 2027 新稿，自动生成图表，编译 PDF，逐页检查，并交付可复现代码、结果说明与 Git 提交。

普通依赖、配置、路径、代码错误、测试和排版问题请自行排查处理，不要每一步都问我。复用或创建隔离 Python 环境，先验证 SSH 服务器上的 TeX Live，不重装整套系统工具。

共享服务器只使用调度器已分配或我对本项目明确授权的资源。没有明确 GPU/CPU 大任务额度时继续轻量 CPU 检查和 smoke test，把资源授权列为集中阻塞项；不要擅自抢占 GPU、杀其他人的进程、修改驱动、购买云服务或泄露凭据。

不要停在“已经写好计划/安装好环境/生成了脚手架”。维护任务看板、进度、决策、阻塞和实际 run manifest，完成测试后真实启动获准实验，定期给出有日志依据的状态；中断后从 checkpoint 和记录继续，不重复启动。

旧稿缺少的参数、作者/ORCID 和旧投稿状态不能猜。缺这些时继续能执行的研发和内部草稿，明确哪些证据尚不完整；最终论文提交、版权和付款由我处理。

现在开始第一个可执行阶段：保护工作区、读取输入与任务书、检查环境和资源、建立论文到代码的映射，然后直接推进实现和测试。只报告实际完成与真实运行状态。
```

## 纯手动查看任务书的最少命令

在正确的项目目录执行以下只读/获取命令，不会删除 `paper/` 文件：

```bash
pwd
git status --short
git remote -v
git fetch origin docs/kwallet-icassp2027-execution-20260909
git show FETCH_HEAD:docs/TRAE_KWALLET_ICASSP2027_EXECUTION.md
```

这些命令只确认/获取并显示任务书，不代表已经把文档写进当前工作分支，也不代表开始实验。让 agent 在检查工作区后决定安全的分支集成方式；不要盲目复制含 hard reset 的“修复命令”。

## 需要用户最终确认、但不应阻止其他开发的事项

- 项目实际允许使用的服务器 GPU/CPU/内存和并发额度，或可验证的调度器分配。
- 旧稿之前投的准确会议，以及目前在审、拒稿、撤稿、录用或已发表状态。
- 最终作者、顺序、单位、邮箱、ORCID 和真实资助/伦理信息。

agent 应优先从本项目已提供的材料解析这些信息；材料不支持时集中报告，不猜、不把别的项目授权拿来使用。

## 期望最后拿到的交付物

旧论文逐项复现报告、经过测试的统一代码、全部实际实验配置/日志/结果索引、改进与负结果报告、ICASS P 2027 英文稿和编译 PDF、可复现包、明确的 Git 提交/PR 状态，以及仍需作者处理的有限事项。

如果原 artifact 缺失，最后报告必须说清楚哪些是重实现而非已复现；如果某些 full runs 没跑完，必须保留 NOT_RUN/BLOCKED，不能用旧稿数字充数。

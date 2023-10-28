# Mastermind 猜数字游戏

## 游戏介绍
Mastermind 猜数字游戏是一款经典的逻辑推理游戏。在这个游戏中，玩家的目标是猜出一个隐秘的数字组合，这个组合由固定位数的数字构成。每当玩家做出一次猜测后，游戏会根据猜测的准确度提供反馈，反馈的形式是“xAyB”，其中 x 表示数字正确且位置正确的数量（A），而 y 表示数字正确但位置不对的数量（B）。玩家需要利用这些线索，尽可能在最少的尝试次数内猜出正确的数字组合。

## AutoSolver
AutoSolver 是一个自动求解 Mastermind 游戏的程序，它基于概率论和信息论的原理，通过分析和计算各种可能的猜测结果，来优化猜测策略，达到快速破解游戏的目的。AutoSolver 的主要特点包括：

- **概率论与信息论的应用**：AutoSolver 分析所有可能的答案及其发生的概率，从而制定出最优的猜测策略。
- **信息增益期望最大化**：在每一步猜测中，AutoSolver 都会选择那个能够带来最大信息增益（即最大概率地排除错误答案）的数字组合。
- **本质是贪心算法**：虽然 AutoSolver 每次只对当前的猜测进行优化，没有对整体猜测次数进行直接优化，但通过每一步的局部最优选择，通常可以以较少的总步数找到正确答案。

## requirements 依赖库
1. **numpy [Optional]**：
    - `numpy` 用于关键计算算法的演示，你可以在 `cbindings.py` 取消它的注释以启用。
2. **tqdm [Optional]**：
    - 用于实现漂亮的进度条，使得计算过程不再枯燥。这在处理大量数据或进行长时间运算时尤其有用。
    - 如果安装了 `tqdm`，可以在 `Solver.auto` 方法中设置 `pbar=True` 来添加进度条，以便实时监控处理进度。

## components compilation 组件编译
- 运行以下命令：
```
g++ -shared -fpic -o libsolver.so source/solver.cpp -std=c++17
```

---

Mastermind 游戏不仅仅是一个普通的益智游戏，它的解决过程也充分体现了计算机科学和信息理论的魅力。使用 AutoSolver，你可以更深入地理解这些理论，并体验将理论应用到实际问题中的乐趣。

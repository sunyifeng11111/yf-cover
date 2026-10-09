# yf-cover

为 AI 工具技巧视频制作小红书封面的 Codex skill。提供产品截图、人物 IP 和口播文稿或标题后，skill 会帮助确定封面标题与布局，并生成一张默认 3:4 竖版封面。

## 布局示例

三种布局图用于参考构图和视觉层级。生成时应替换为用户自己的产品界面、人物 IP 和标题。

| A：上方标题，下方大屏幕 | B：左侧标题，右侧大屏幕 | C：屏幕特写，突出具体问题 |
| --- | --- | --- |
| <img src="assets/layout-a.png" alt="A 布局：上方标题，下方大屏幕" width="240"> | <img src="assets/layout-b.png" alt="B 布局：左侧标题，右侧大屏幕" width="240"> | <img src="assets/layout-c.png" alt="C 布局：屏幕特写，突出具体问题" width="240"> |

> [!NOTE]
> 示例图展示的是布局和视觉方向，不是可复用的产品内容模板。

## 安装与调用

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/sunyifeng11111/yf-cover.git ~/.codex/skills/yf-cover
```

在 Codex 中输入 `$yf-cover`，并提供产品截图、人物 IP，以及口播文稿或标题。若缺少必要素材，skill 会先询问缺失项。

## 布局选择

- **A**：适合需要展示较完整横向界面的内容，标题位于上方，屏幕占据下半部分。
- **B**：适合关键界面能在屏幕右侧窄幅中清楚呈现，且人物指向动作有帮助的内容。
- **C**：适合讲解一两个具体 UI 区域或功能细节的内容。

用户指定布局时优先遵从；未指定时，根据需要展示的界面范围选择。屏幕内容以用户截图为事实来源，标题应准确对应口播或用户提供的标题。

## 仓库内容

- `SKILL.md`：skill 的工作流程与视觉要求。
- `references/layouts.md`：三种布局的详细说明。
- `assets/`：布局参考图。
- `scripts/place_screen.py`：将原始截图透视合成到场景屏幕中的辅助脚本，依赖 Pillow 和 NumPy；仅在需要保留截图原始像素时使用。

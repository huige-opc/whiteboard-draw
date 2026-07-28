# Whiteboard Draw

[English](README.en.md) | [GitHub](https://github.com/huige-opc/whiteboard-draw)

**白板手绘动画生成工具** — 把图片、SVG、线稿、照片或文字脚本，转换成手绘白板动画视频（MP4）。引擎已内置，clone 即用。

## 引擎下载

渲染引擎已内置在仓库中，无需单独安装：

- **GitHub 源码**：[whiteboard_skill/](https://github.com/huige-opc/whiteboard-draw/tree/master/whiteboard_skill)
- **下载 ZIP**：clone 整个仓库即可，引擎就在 `whiteboard_skill/` 目录下

```bash
git clone https://github.com/huige-opc/whiteboard-draw.git
```

## 快速开始

```bash
# 1. 装依赖
pip install numpy Pillow pydantic

# 2. 需要 ffmpeg（检查：ffmpeg -version）
# Windows: winget install ffmpeg
# macOS:   brew install ffmpeg
# Linux:   apt install ffmpeg

# 3. 验证
python3 scripts/whiteboard_cli.py doctor

# 5. 试试效果（SVG 转手绘）
python3 scripts/whiteboard_cli.py render-image examples/apple.svg -o apple.mp4 --duration 3 --hand asian

# 6. 照片转手绘
python3 scripts/whiteboard_cli.py render-photo photo.jpg -o photo-whiteboard.mp4 --duration 15 --hand asian
```

## 使用场景

### 1. SVG / 线稿转手绘

已有干净的 SVG 或黑白线稿 PNG：

```bash
python3 scripts/whiteboard_cli.py render-image input.svg -o output.mp4 --duration 10 --fps 30 --hand asian
```

参数说明：
- `--duration`：视频长度（秒）
- `--fps`：帧率，预览用 12-24，最终输出用 30-60
- `--hand`：手型光标，可选 `asian` / `black` / `children` / `white` / `procedural` / `none`
- `--width` `--height`：输出分辨率，默认 1920x1080

### 2. 照片转手绘

上传的照片或彩色插画，自动提取线稿再渲染：

```bash
# 一步到位
python3 scripts/whiteboard_cli.py render-photo photo.jpg -o out.mp4 --duration 15 --fps 30 --hand asian --stroke-detail rich

# 或分步操作（先提取线稿看看效果）
python3 scripts/whiteboard_cli.py extract-lineart photo.jpg -o lineart.png --provider auto
python3 scripts/whiteboard_cli.py render-image lineart.png --source-image photo.jpg --color-fill contour-wipe -o out.mp4 --duration 15 --fps 30 --hand asian
```

线稿提取支持两种本地模型：
- `auto` → 自动选，优先 Informative Drawings，其次 Anime2Sketch
- `informative` → Informative Drawings（照片效果好）
- `anime2sketch` → Anime2Sketch（插画/动漫效果好）

### 3. 脚本驱动（多场景视频）

写一个 Markdown 脚本，自动拆分为多个场景并合成完整视频：

```bash
# 写脚本 examples/script.md
# 然后运行
python3 scripts/whiteboard_cli.py run examples/script.md -o final.mp4 --scenes 3 --fps 24
```

脚本格式示例（参考 `examples/ten-second-demo.md`）：

```md
太阳升起时，城市开始苏醒，路灯渐渐熄灭。

一个人打开笔记本，把今天最重要的目标写下来。
```

### 4. 彩色原图叠加

线稿画完后，轮廓感上色：

```bash
python3 scripts/whiteboard_cli.py render-image lineart.png \
  --source-image photo.png \
  --color-fill contour-wipe \
  -o out.mp4 --duration 15 --fps 30 --tail-color 4.5 --hand asian
```

- `--tail-color`：颜色延后笔尖的秒数，数值越大颜色填充越慢
- `--color-fill`：上色模式，`contour-wipe` 为沿轮廓展开

### 5. 手绘文字

```bash
python3 scripts/whiteboard_cli.py render-image input.svg --draw-text "你好世界" -o out.mp4 --duration 10
```

### 6. 其他命令

```bash
# 查看可用手型
python3 scripts/whiteboard_cli.py list-hands

# 分析图片线稿复杂度
python3 scripts/whiteboard_cli.py analyze-image input.png -o analysis.json

# 拼接多个片段
python3 scripts/whiteboard_cli.py compose -i clip1.mp4 clip2.mp4 -o final.mp4
```

## 本地线稿模型（进阶）

线稿提取依赖神经网络模型，需要额外下载。**模型文件不包含在本仓库中**。

推荐目录结构（放在你的项目目录下，不是本仓库内）：

```text
my-whiteboard-project/
  tools/
    lineart/
      run_informative_drawings.py
      run_anime2sketch.py
    informative-drawings/      # 完整克隆上游仓库
      checkpoints/model/anime_style/netG_A_latest.pth
    Anime2Sketch/               # 完整克隆上游仓库
      weights/netG.pth
```

也支持环境变量指定命令：

```bash
export WHITEBOARD_INFORMATIVE_DRAWINGS_CMD="python /path/to/run_informative_drawings.py {input} {output}"
export WHITEBOARD_ANIME2SKETCH_CMD="python /path/to/run_anime2sketch.py {input} {output}"
```

## 本地开发

```bash
# 可编辑模式安装引擎（修改源码即时生效）
pip install -e /path/to/whiteboard-draw
```

## 仓库内容

| 目录/文件 | 说明 |
|-----------|------|
| `whiteboard_skill/` | 渲染引擎（已内置） |
| `scripts/whiteboard_cli.py` | 命令行入口 |
| `SKILL.md` | AI 编程助手 skill 指令 |
| `references/` | 工作流参考文档 |
| `examples/` | 示例素材 |
| `agents/openai.yaml` | AI skill 注册元数据（可选） |
| `docs/` | 文档资源 |

## 不包含

- 线稿模型仓库（需自行下载）
- 模型权重文件（.pth / .pt 等）
- 生成的 MP4 视频
- 用户上传的素材

## 许可证

MIT

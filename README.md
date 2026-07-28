# Whiteboard Draw

[English](README.en.md)

**白板手绘动画生成工具** — 把图片、SVG、线稿或脚本转换成手绘白板视频。引擎已内置，clone 即用。

## 架构

```
whiteboard-draw/
  scripts/whiteboard_cli.py  ← CLI 入口
  whiteboard_skill/          ← 渲染引擎（内置）
  SKILL.md                   ← AI 编程助手 skill 指令
```

## 安装

### 前置依赖

```bash
pip install numpy Pillow pydantic
```

需要 ffmpeg（在 PATH 上）：

```bash
winget install ffmpeg          # Windows
brew install ffmpeg             # macOS
apt install ffmpeg              # Linux
```

### 下载本仓库

```bash
git clone https://github.com/huige-opc/whiteboard-draw.git
cd whiteboard-draw
```

### 验证

```bash
python3 scripts/whiteboard_cli.py doctor
```

## 使用

```bash
# SVG 手绘渲染
python3 scripts/whiteboard_cli.py render-image input.svg -o output.mp4 --duration 10 --fps 30 --hand asian

# 照片转手绘
python3 scripts/whiteboard_cli.py render-photo photo.jpg -o output.mp4 --duration 15 --fps 30 --lineart-provider auto --stroke-detail rich --hand asian

# 线稿 + 彩色原图叠加
python3 scripts/whiteboard_cli.py render-image lineart.png --source-image photo.png --color-fill contour-wipe -o output.mp4 --duration 15 --fps 30 --tail-color 4.5 --hand asian

# 配置文件方式
python3 scripts/whiteboard_cli.py run scenes.md -o output.mp4 --scenes 3 --fps 24
```

## 本地模型

线稿提取依赖本地神经网络模型，放在**项目工作目录**下：

```text
my-whiteboard-project/
  tools/
    lineart/
      run_informative_drawings.py
      run_anime2sketch.py
    informative-drawings/      # 完整下载上游仓库
    Anime2Sketch/               # 完整下载上游仓库
```

或环境变量：

```bash
export WHITEBOARD_INFORMATIVE_DRAWINGS_CMD="python /path/to/run_informative_drawings.py {input} {output}"
export WHITEBOARD_ANIME2SKETCH_CMD="python /path/to/run_anime2sketch.py {input} {output}"
```

## 仓库内容

| 文件/目录 | 说明 |
|-----------|------|
| `SKILL.md` | AI 编程助手 skill 指令 |
| `scripts/whiteboard_cli.py` | CLI 入口 |
| `whiteboard_skill/` | 渲染引擎（已内置） |
| `references/` | 工作流说明 |
| `examples/` | 示例素材 |
| `agents/openai.yaml` | Skill 注册元数据（可选） |

## 不包含

- 线稿模型仓库（需自行下载）
- 模型权重
- 生成视频
- 用户上传素材

## 许可证

MIT。上游模型代码和权重遵循各自许可证。

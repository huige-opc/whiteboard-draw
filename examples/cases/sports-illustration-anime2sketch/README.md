# Sports Illustration Case

中文 | [English](#english)

通过 skill 调用：

```text
把这张白底运动插画转成 15s 手绘白板视频，使用 Anime2Sketch，stroke-detail rich，长短线结合，最后轮廓感上色。
```

底层命令等价于：

```bash
python3 scripts/whiteboard_cli.py render-photo input.jpg \
  -o out/sports-illustration-anime2sketch-longmix-15s.mp4 \
  --duration 15 \
  --fps 30 \
  --lineart-provider anime2sketch \
  --stroke-detail rich \
  --hand asian \
  --tail-color 4.5 \
  --color-fill contour-wipe
```

完整演示素材参见引擎的 examples 目录。

---

## English

Example request:

```text
Convert this clean sports illustration into a 15-second whiteboard animation using Anime2Sketch, rich stroke detail, mixed long/short strokes, and contour-aware color fill.
```

Equivalent command:

```bash
python3 scripts/whiteboard_cli.py render-photo input.jpg \
  -o out/sports-illustration-anime2sketch-longmix-15s.mp4 \
  --duration 15 \
  --fps 30 \
  --lineart-provider anime2sketch \
  --stroke-detail rich \
  --hand asian \
  --tail-color 4.5 \
  --color-fill contour-wipe
```

Full demo assets are in the engine's examples directory.

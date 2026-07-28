#!/usr/bin/env python3
"""Wrapper for Anime2Sketch line-art extraction.

Usage: python run_anime2sketch.py input.png output.png
"""

import os
import sys
from pathlib import Path

import torch
from PIL import Image
from torchvision import transforms


def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} input.png output.png", file=sys.stderr)
        return 1

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 1

    # Locate model
    script_dir = Path(__file__).resolve().parent
    model_dir = script_dir.parent / "Anime2Sketch"
    weights_path = model_dir / "weights" / "netG.pth"

    if not weights_path.exists():
        print(f"Model weights not found: {weights_path}", file=sys.stderr)
        return 1

    # Import model module from Anime2Sketch directory
    sys.path.insert(0, str(model_dir))

    # Temporarily chdir to model dir so model.py can find weights/netG.pth
    old_cwd = Path.cwd()
    os.chdir(str(model_dir))
    try:
        from model import create_model

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        net = create_model("default")
        net.to(device)
        net.eval()
    finally:
        os.chdir(str(old_cwd))

    # Load and prepare image
    img = Image.open(input_path).convert("RGB")
    w, h = img.size

    # U-Net with 8 downsamplings needs size divisible by 256
    target_w = ((w + 255) // 256) * 256
    target_h = ((h + 255) // 256) * 256

    if target_w != w or target_h != h:
        # Pad to multiple of 256, then crop back after inference
        padded = Image.new("RGB", (target_w, target_h), (255, 255, 255))
        padded.paste(img, (0, 0))
        print(f"Padding {w}x{h} -> {target_w}x{target_h} for model", file=sys.stderr)
        input_tensor = padded
    else:
        input_tensor = img

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
    ])
    tensor = transform(input_tensor).unsqueeze(0).to(device)

    with torch.no_grad():
        output = net(tensor)

    # Convert and crop back to original size
    out_img = output.squeeze(0).cpu()
    out_img = (out_img + 1) / 2 * 255
    out_img = out_img.byte()
    out_img = out_img.permute(1, 2, 0).numpy()
    result = Image.fromarray(out_img.squeeze().astype("uint8"), mode="L")
    result = result.crop((0, 0, w, h))
    result.save(output_path)
    print(f"Saved: {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

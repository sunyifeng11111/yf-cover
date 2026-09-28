#!/usr/bin/env python3
"""Place unmodified screenshot pixels into a photographed monitor quadrilateral.

Requires Pillow and NumPy. Coordinates are in final-scene pixels.
"""

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def points(value: str):
    result = []
    for pair in value.split():
        x, y = pair.split(",")
        result.append((float(x), float(y)))
    if len(result) != 4:
        raise argparse.ArgumentTypeError("quad needs TL TR BR BL coordinate pairs")
    return result


def crop_box(value: str):
    vals = [int(v) for v in value.split(",")]
    if len(vals) != 4:
        raise argparse.ArgumentTypeError("crop needs left,top,right,bottom")
    return tuple(vals)


def coefficients(destination, width, height):
    source = [(0, 0), (width, 0), (width, height), (0, height)]
    rows, outputs = [], []
    for (x, y), (u, v) in zip(destination, source):
        rows.extend(((x, y, 1, 0, 0, 0, -u * x, -u * y),
                     (0, 0, 0, x, y, 1, -v * x, -v * y)))
        outputs.extend((u, v))
    return np.linalg.solve(np.asarray(rows), np.asarray(outputs)).tolist()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scene", required=True, type=Path)
    parser.add_argument("--screenshot", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--screen-quad", required=True, type=points,
                        help='final-scene screen interior corners: "TLx,TLy TRx,TRy BRx,BRy BLx,BLy"')
    parser.add_argument("--source-crop", type=crop_box,
                        help="source screenshot left,top,right,bottom; omit for full image")
    parser.add_argument("--foreground-polygon", action="append", type=lambda v: [tuple(map(float, pair.split(","))) for pair in v.split()], default=[],
                        help="scene region to restore above screen, as x,y pairs; may repeat")
    args = parser.parse_args()

    scene = Image.open(args.scene).convert("RGBA")
    source = Image.open(args.screenshot).convert("RGBA")
    if args.source_crop:
        source = source.crop(args.source_crop)
    if source.width < 2 or source.height < 2:
        parser.error("source crop is empty")

    warp = source.transform(scene.size, Image.Transform.PERSPECTIVE,
                            coefficients(args.screen_quad, source.width, source.height),
                            resample=Image.Resampling.BICUBIC)
    screen_mask = Image.new("L", scene.size)
    ImageDraw.Draw(screen_mask).polygon(args.screen_quad, fill=255)
    screen_mask = screen_mask.filter(ImageFilter.GaussianBlur(0.6))
    result = Image.composite(warp, scene, screen_mask)

    if args.foreground_polygon:
        foreground = Image.new("L", scene.size)
        draw = ImageDraw.Draw(foreground)
        for polygon in args.foreground_polygon:
            if len(polygon) < 3:
                parser.error("foreground polygon needs at least three points")
            draw.polygon(polygon, fill=255)
        foreground = foreground.filter(ImageFilter.GaussianBlur(1.0))
        result = Image.composite(scene, result, foreground)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.convert("RGB").save(args.output)


if __name__ == "__main__":
    main()

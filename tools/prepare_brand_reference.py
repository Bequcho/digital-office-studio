"""Offline, lossless brand preparation from owner-supplied references.

Decode all MP4 frames with full FFmpeg first (30 fps, no frame dropping).
This preparation is separate from the website build; no video ships to the site.
"""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageFilter
from collections import deque
from statistics import median

ROOT = Path(__file__).resolve().parents[1]
PHOTO_SHA = 'a0fb2d5932aecb13c7828852cca1000c6a133850760e3997b1cee53aeb9f54d6'
VIDEO_SHA = '1a087bccded1a55a19c24d58e465aa5656580ff66c9f31084b51e5da2af6e932'


def transparent_wordmark(wordmark):
    """Remove the photographed dark background; preserve opaque letter cores.

    Solve C = alpha*F + (1-alpha)*B only in the antialiased boundary.
    B is sampled from dark neighbouring tiles, F from the nearest opaque core.
    No font substitution, blur of the letters or resampling is performed.
    """
    rgb = wordmark.convert('RGB')
    width, height = rgb.size
    pixels = list(rgb.getdata())
    seed = Image.new('L', rgb.size)
    seed.putdata([255 if max(p) > 70 else 0 for p in pixels])
    inner = list(seed.filter(ImageFilter.MinFilter(3)).getdata())
    outer = list(seed.filter(ImageFilter.MaxFilter(5)).getdata())
    # Background texture is not part of the lettering. A low-resolution model
    # avoids carrying its grain into the transparent matte.
    tile = 16
    gw, gh = (width+tile-1)//tile, (height+tile-1)//tile
    samples = {}
    for ty in range(gh):
        for tx in range(gw):
            dark = [pixels[y*width+x] for y in range(ty*tile,min(height,(ty+1)*tile))
                    for x in range(tx*tile,min(width,(tx+1)*tile)) if max(pixels[y*width+x]) < 55]
            if dark:
                samples[(tx,ty)] = tuple(round(median(p[c] for p in dark)) for c in range(3))
    grid = Image.new('RGB',(gw,gh))
    for ty in range(gh):
        for tx in range(gw):
            nearest = min(samples, key=lambda q:(q[0]-tx)**2+(q[1]-ty)**2)
            grid.putpixel((tx,ty),samples.get((tx,ty),samples[nearest]))
    background = list(grid.resize(rgb.size,Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(6)).getdata())
    nearest = [-1]*len(pixels)
    queue = deque()
    for i,value in enumerate(inner):
        if value:
            nearest[i]=i
            queue.append(i)
    while queue:
        i=queue.popleft();x,y=i%width,i//width
        for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0<=nx<width and 0<=ny<height:
                j=ny*width+nx
                if outer[j] and nearest[j]<0:
                    nearest[j]=nearest[i];queue.append(j)
    result=[]
    for i,c in enumerate(pixels):
        if inner[i]:
            result.append((*c,255));continue
        if not outer[i] or nearest[i]<0:
            result.append((0,0,0,0));continue
        b=background[i];f=pixels[nearest[i]]
        direction=[f[k]-b[k] for k in range(3)]
        a=max(0,min(1,sum((c[k]-b[k])*direction[k] for k in range(3))/max(1,sum(v*v for v in direction))))
        if a<=3/255:
            result.append((0,0,0,0));continue
        foreground=tuple(round(max(0,min(255,(c[k]-(1-a)*b[k])/a))) for k in range(3))
        result.append((*foreground,round(a*255)))
    image=Image.new('RGBA',rgb.size);image.putdata(result)
    return image


def prepare(photo, video, directory):
    assert hashlib.sha256(photo.read_bytes()).hexdigest() == PHOTO_SHA
    assert hashlib.sha256(video.read_bytes()).hexdigest() == VIDEO_SHA
    files = sorted(directory.glob('frame-*.png'))
    assert len(files) == 146
    target = ROOT / 'assets/brand'
    target.mkdir(exist_ok=True)
    wordmark = Image.open(photo).crop((205, 36, 1054, 241))
    wordmark = transparent_wordmark(wordmark)
    wordmark.save(target / 'beqson-wordmark.webp', lossless=True, method=6, exact=True)
    assert wordmark.tobytes() == Image.open(target / 'beqson-wordmark.webp').convert('RGBA').tobytes()
    alpha = Image.open(ROOT / 'assets/beqson-mark-v3.png').getchannel('A').resize((128, 128))

    def field(image):
        # Register the reference's symbol to the unchanged PNG alpha bounds.
        result = Image.new('RGB', (128, 128))
        result.paste(image.crop((185, 75, 359, 289)).resize((89, 113), Image.Resampling.LANCZOS), (19, 7))
        return result.resize((128, 128), Image.Resampling.LANCZOS)

    baseline = field(Image.open(files[0]).convert('RGB'))
    frames = []
    for file in files:
        red, green, _ = ImageChops.subtract(field(Image.open(file).convert('RGB')), baseline).split()
        values = [min(r, g * 2) if a > 150 else 0
                  for r, g, a in zip(red.getdata(), green.getdata(), alpha.getdata())]
        paths = []
        for threshold in (15, 45, 90):
            runs = []
            for y in range(128):
                x = 0
                while x < 128:
                    if values[y * 128 + x] < threshold:
                        x += 1
                        continue
                    start = x
                    while x < 128 and values[y * 128 + x] >= threshold:
                        x += 1
                    if x - start >= 1:
                        runs.append(f'M{start} {y}h{x-start}v1h-{x-start}z')
            paths.append(''.join(runs))
        frames.append(paths)
    (target / 'beqson-contours.json').write_text(json.dumps(
        {'fps': 30, 'duration': 146 / 30, 'viewBox': '0 0 128 128', 'frames': frames},
        separators=(',', ':')), encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--photo', type=Path, required=True)
    parser.add_argument('--video', type=Path, required=True)
    parser.add_argument('--frames', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.photo, args.video, args.frames)

#!/usr/bin/env python3
"""Drawwii 랜딩 파생 자산 생성기 (순수 Pillow + fontTools).

랜딩에 쓰는 스크린샷/아이콘/og:image/폰트는 전부 이 스크립트가 만든다.
소스는 Drawwii 앱 저장소(비공개, 로컬 클론)와 이 저장소의 배지 PNG다.

소스 경로 (앱 저장소):
  스크린샷 : <APP>/tools/store_screenshots/raw/android/en/*.png   (1080x2400)
  앱 아이콘 : <APP>/assets/common/app-icon.png                     (1024x1024)
  마스코트  : <APP>/assets/common/app-icon-transparent.png         (1024x1024, 알파 bbox 407x768)
  폰트      : <APP>/assets/fonts/Pretendard-*.otf                  (OFL)
  OFL       : <APP>/assets/licenses/Pretendard-OFL.txt

앱 UI가 바뀌면 스크린샷을 재캡처(store_screenshots 파이프라인)한 뒤 이 스크립트를
다시 실행하면 된다. 산출물은 저장소에 커밋한다(GitHub Pages는 빌드 플러그인이
제한적이라 런타임 이미지 처리를 못 하기 때문).

사용법:
  python3 tools/prepare_assets.py            # 전체 생성
  APP_REPO=/path/to/drawwii python3 tools/prepare_assets.py
"""

from __future__ import annotations

import io
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageOps

# ── 경로 ──────────────────────────────────────────────
HERE = Path(__file__).resolve().parent
SITE = HERE.parent
APP = Path(os.environ.get("APP_REPO", "/Users/jyr/StudioProjects/bullets/drawwii"))

RAW = APP / "tools/store_screenshots/raw/android/en"
APP_ICON = APP / "assets/common/app-icon.png"
MASCOT = APP / "assets/common/app-icon-transparent.png"
FONT_DIR = APP / "assets/fonts"
OFL = APP / "assets/licenses/Pretendard-OFL.txt"

OUT_SHOTS = SITE / "assets/screenshots"
OUT_ICONS = SITE / "assets/icons"
OUT_OG = SITE / "assets/og"
OUT_BRAND = SITE / "assets/brand"
OUT_FONTS = SITE / "assets/fonts"

# ── 브랜드 색 (앱 store_screenshots/compose/layout.py 와 동일) ──
BRAND_PINK = "#DF64A3"
BRAND_DARK = "#5A1F3D"

# 스토어 스크린샷 순서 = scenes.py order. 랜딩 갤러리도 이 순서.
SCENES = [
    ("draw", "01-draw"),
    ("eraser_before_after", "02-eraser"),
    ("bg_remove", "03-bg-remove"),
    ("templates", "04-templates"),
    ("stickers", "05-stickers"),
    ("habit", "06-habit"),
    ("gallery", "07-gallery"),
]

# 갤러리/기능 카드용 폭. 폰 종횡비(1080x2400)를 유지한다.
SHOT_W = 600
SHOT_W_2X = 1200


def log(msg: str) -> None:
    print(f"  {msg}")


def ensure_dirs() -> None:
    for d in (OUT_SHOTS, OUT_ICONS, OUT_OG, OUT_BRAND, OUT_FONTS):
        d.mkdir(parents=True, exist_ok=True)


def check_sources() -> None:
    missing = [
        str(p)
        for p in (RAW, APP_ICON, MASCOT, FONT_DIR, OFL)
        if not p.exists()
    ]
    if missing:
        print("소스를 찾지 못했습니다. APP_REPO 를 확인하세요:", file=sys.stderr)
        for m in missing:
            print("  -", m, file=sys.stderr)
        sys.exit(1)


def save_webp(im: Image.Image, path: Path, quality: int = 82) -> None:
    im.save(path, "WEBP", quality=quality, method=6)


def brand_gradient(size, color_a=BRAND_PINK, color_b=BRAND_DARK, angle_deg=115.0):
    """앱 background.py 이식. color_a(밝음)->color_b(어두움) 대각 그라데이션."""
    w, h = size
    diag = int((w**2 + h**2) ** 0.5) + 2
    grad = Image.linear_gradient("L").resize((diag, diag))
    grad = grad.rotate(angle_deg, resample=Image.BICUBIC)
    gw, gh = grad.size
    left, top = (gw - w) // 2, (gh - h) // 2
    grad = grad.crop((left, top, left + w, top + h))
    return ImageOps.colorize(grad, black=color_b, white=color_a).convert("RGB")


def rounded(im: Image.Image, radius: int) -> Image.Image:
    """카드용 라운드 코너 마스크 적용."""
    from PIL import ImageDraw

    mask = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, im.size[0], im.size[1]], radius=radius, fill=255)
    out = im.convert("RGBA")
    out.putalpha(mask)
    return out


# ── 1. 스크린샷 ───────────────────────────────────────
def build_screenshots() -> None:
    log("스크린샷 7종 → webp(600/1200w) + png 폴백")
    for src_id, out_id in SCENES:
        src = RAW / f"{src_id}.png"
        im = Image.open(src).convert("RGB")
        w, h = im.size  # 1080x2400
        ratio = h / w

        def resize(target_w: int) -> Image.Image:
            return im.resize((target_w, round(target_w * ratio)), Image.LANCZOS)

        one = resize(SHOT_W)
        two = resize(SHOT_W_2X)
        save_webp(one, OUT_SHOTS / f"{out_id}.webp", quality=80)
        save_webp(two, OUT_SHOTS / f"{out_id}@2x.webp", quality=78)
        one.save(OUT_SHOTS / f"{out_id}.png", optimize=True)
    # 히어로 poster (첫 화면)
    hero = Image.open(RAW / "draw.png").convert("RGB").resize(
        (SHOT_W, round(SHOT_W * 2400 / 1080)), Image.LANCZOS
    )
    hero.save(OUT_SHOTS / "hero-poster.jpg", "JPEG", quality=85, optimize=True)
    log(f"  → {OUT_SHOTS.relative_to(SITE)} (dims 600x{round(600*2400/1080)})")


# ── 2. 아이콘 / 파비콘 ────────────────────────────────
def build_icons() -> None:
    log("앱 아이콘 → apple-touch / pwa / favicon")
    icon = Image.open(APP_ICON).convert("RGBA")  # 1024

    def sq(size: int) -> Image.Image:
        return icon.resize((size, size), Image.LANCZOS)

    sq(180).save(OUT_ICONS / "apple-touch-icon.png")
    sq(192).save(OUT_ICONS / "icon-192.png")
    sq(512).save(OUT_ICONS / "icon-512.png")
    sq(32).save(OUT_ICONS / "favicon-32.png")
    # 멀티사이즈 favicon.ico → 사이트 루트
    icon.save(
        SITE / "favicon.ico",
        sizes=[(16, 16), (32, 32), (48, 48)],
    )


# ── 3. 마스코트 ───────────────────────────────────────
def build_mascot() -> None:
    """투명 배경 앱 아이콘(1024²)에서 마스코트만 알파 bbox 로 잘라낸다.

    drawwii_logo.png(265x500) 보다 1.54배 큰 무손실 원본(407x768)이라 히어로에서
    쓸 수 있다. 히어로 CSS 폭은 최대 184px → 2x DPR 에서 368px 이면 충분하므로
    @2x 는 만들지 않는다 (407px 를 넘기면 업스케일이라 무의미).
    """
    im = Image.open(MASCOT).convert("RGBA")  # 1024x1024
    m = im.crop(im.getchannel("A").getbbox())  # → 407x768
    log(f"마스코트 → {m.width}x{m.height} webp + png 폴백 (확대 금지)")
    save_webp(m, OUT_BRAND / "mascot.webp", quality=82)
    m.save(OUT_BRAND / "mascot.png", optimize=True)


# ── 4. og:image (1200x630) ────────────────────────────
def build_og() -> None:
    log("og:image 1200x630 생성 (브랜드 그라데이션 + 워드마크 + 폰 2장)")
    W, H = 1200, 630
    bg = brand_gradient((W, H)).convert("RGBA")

    from PIL import ImageDraw, ImageFont

    draw = ImageDraw.Draw(bg)

    # 폰트 (앱 Pretendard OTF 직접 사용)
    try:
        f_title = ImageFont.truetype(str(FONT_DIR / "Pretendard-Bold.otf"), 96)
        f_sub = ImageFont.truetype(str(FONT_DIR / "Pretendard-SemiBold.otf"), 38)
        f_small = ImageFont.truetype(str(FONT_DIR / "Pretendard-Medium.otf"), 30)
    except OSError:
        f_title = f_sub = f_small = ImageFont.load_default()

    # 우측 폰 2장을 먼저 깔고(텍스트가 위로 오도록), 텍스트는 좌측 컬럼에 가둔다.
    shots = ["templates", "draw"]
    xs = [W - 180, W - 400]
    for i, (name, x) in enumerate(zip(shots, xs)):
        s = Image.open(RAW / f"{name}.png").convert("RGB")
        ph = 600
        pw = round(ph * s.size[0] / s.size[1])
        s = s.resize((pw, ph), Image.LANCZOS)
        s = rounded(s, 30)
        s = s.rotate(-7 if i == 0 else 5, expand=True, resample=Image.BICUBIC)
        bg.alpha_composite(s, (x - pw // 2, H - s.size[1] + 70))

    pad = 80
    draw.text((pad, 196), "Drawwii", font=f_title, fill="#FFFFFF")
    draw.text((pad, 320), "Draw · Edit photos · Collage",
              font=f_sub, fill=(255, 255, 255, 240))
    draw.text((pad, 384), "A drawing studio + on-device",
              font=f_small, fill=(255, 255, 255, 200))
    draw.text((pad, 424), "AI photo editor in one app.",
              font=f_small, fill=(255, 255, 255, 200))

    bg.convert("RGB").save(OUT_OG / "drawwii-og-1200x630.png", optimize=True)


# ── 5. 폰트 서브셋 (Pretendard Latin → woff2) ─────────
# 영어 랜딩이므로 Latin + 구두점 + 자주 쓰는 기호만 남긴다.
SUBSET_UNICODES = "U+0000-00FF,U+2018-2019,U+201C-201D,U+2013-2014,U+2026,U+2022,U+00D7,U+2713,U+2212,U+2192"
FONT_WEIGHTS = [
    ("Pretendard-Regular.otf", "pretendard-latin-400", 400),
    ("Pretendard-SemiBold.otf", "pretendard-latin-600", 600),
    ("Pretendard-Bold.otf", "pretendard-latin-700", 700),
]


def build_fonts() -> None:
    log("Pretendard Latin 서브셋 → woff2")
    for src_name, out_name, _weight in FONT_WEIGHTS:
        src = FONT_DIR / src_name
        out = OUT_FONTS / f"{out_name}.woff2"
        cmd = [
            sys.executable,
            "-m",
            "fontTools.subset",
            str(src),
            f"--unicodes={SUBSET_UNICODES}",
            "--layout-features=kern,liga,calt",
            "--flavor=woff2",
            "--desubroutinize",
            f"--output-file={out}",
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        log(f"  → {out.name}  ({out.stat().st_size // 1024} KB)")
    # OFL 라이선스 동봉
    (OUT_FONTS / "Pretendard-OFL.txt").write_bytes(OFL.read_bytes())


def main() -> None:
    print("Drawwii 랜딩 자산 생성")
    check_sources()
    ensure_dirs()
    build_screenshots()
    build_icons()
    build_mascot()
    build_og()
    build_fonts()
    print("완료.")


if __name__ == "__main__":
    main()

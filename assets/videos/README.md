# 히어로 데모 영상

이 디렉터리에 영상 파일을 넣으면 **코드 수정 없이** 히어로 영역이 스크린샷 → 영상으로 자동 전환됩니다.
(`_includes/sections/hero.html`이 빌드 시점에 `site.static_files`를 검사합니다.)

```
drawwii-demo.mp4      # 필수
drawwii-demo.webm     # 선택 — 있으면 우선 사용됩니다
```

파일이 없으면 `assets/screenshots/01-draw` 스크린샷이 대신 표시되므로, 비어 있어도 페이지는 깨지지 않습니다.

## 권장 스펙

- H.264 mp4 (가능하면 VP9 webm 동봉)
- 8MB 이하
- 1080×2340 내외 (세로, 폰 화면 비율)
- 15~20초 루프
- **무음** — 브라우저 자동재생(autoplay)의 필수 조건입니다

포스터 이미지(`assets/screenshots/hero-poster.jpg`)가 영상 로딩 전에 표시되므로 레이아웃이 흔들리지 않습니다.

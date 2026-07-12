# Drawwii — Landing Page

[Drawwii](https://drawwii.com) 드로잉·사진편집 앱(iOS·Android)의 공식 랜딩 페이지입니다. Jekyll로 빌드하고 GitHub Pages에서 호스팅하며, 커스텀 도메인 `drawwii.com`으로 서비스됩니다.

앱 저장소: <https://github.com/develop-bullets/bullets-drawwii-service-app> — 이 페이지의 콘텐츠는 해당 저장소 `main` 브랜치를 기준(source of truth)으로 삼습니다.

**외부 의존이 없습니다.** 서드파티 스크립트·CSS·폰트 CDN 요청이 0건이며, 폰트(Pretendard Latin 서브셋)와 아이콘(인라인 SVG)은 저장소에 포함돼 있습니다.

## 로컬 개발

```bash
bundle install                 # 의존성 설치 (github-pages gem)
bundle exec jekyll serve       # http://localhost:4000 에서 미리보기
bundle exec jekyll build       # _site/ 에 정적 사이트 생성
```

## 콘텐츠 수정 가이드

| 변경 사항 | 수정할 곳 |
|---|---|
| 기능 목록 · 카피 | `_data/features.yml` |
| 도구 목록 | `_data/tools.yml` |
| FAQ | `_data/faq.yml` — 화면과 JSON-LD가 **함께** 쓰는 단일 소스입니다 |
| 스크린샷 갤러리 캡션 | `_data/gallery.yml` |
| 상단 내비 · 푸터 링크 | `_data/nav.yml`, `_data/footer_links.yml` |
| 앱 버전 · 스토어 링크 · 지원 OS · SEO | `_config.yml` |
| 버전 변경 내역 | `_pages/changelog.md` |
| 개인정보처리방침 / 이용약관 | `_pages/privacy.md`, `_pages/terms.md` |
| 색상 · 타이포 · 간격 | `_sass/_tokens.scss` |

`_config.yml`은 수정 시 Jekyll 서버를 재시작해야 하지만, `_data/*.yml`은 즉시 반영됩니다.

## 자산 재생성

랜딩의 스크린샷·아이콘·og:image·폰트는 앱 저장소에서 자동 생성합니다.

```bash
python3 tools/prepare_assets.py     # 필요: Pillow, fontTools, brotli
```

앱 UI가 바뀌면 앱 저장소의 `tools/store_screenshots/` 파이프라인으로 스크린샷을 재캡처한 뒤 위 스크립트를 다시 실행하세요.

## 데모 영상 추가하기

히어로 영역은 데모 영상이 있으면 영상을, 없으면 스크린샷을 보여줍니다. **파일만 넣으면 코드 수정 없이 자동 전환**됩니다.

```
assets/videos/drawwii-demo.mp4      # (선택) drawwii-demo.webm 도 함께 두면 더 좋습니다
```

권장 스펙: H.264 mp4, 8MB 이하, 1080×2340 내외, 15~20초 루프, **무음**(브라우저 자동재생 조건).

## 배포

`master` 브랜치에 push하면 GitHub Pages가 자동으로 빌드·배포합니다. **push 즉시 라이브**이므로 큰 변경은 별도 브랜치에서 검증한 뒤 올리세요.

## License

[MIT License](LICENSE) · 폰트 [Pretendard](https://github.com/orioncactus/pretendard) (SIL OFL 1.1, `assets/fonts/Pretendard-OFL.txt`) · 아이콘 [Lucide](https://lucide.dev) (ISC)

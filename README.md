# Drawwii — Landing Page

[Drawwii](https://drawwii.com) 모바일 드로잉 앱(iOS·Android)의 공식 랜딩 페이지입니다.
[Automatic App Landing Page](https://github.com/emilbaehr/automatic-app-landing-page) Jekyll 템플릿을 기반으로 하며, GitHub Pages에서 빌드·호스팅되고 커스텀 도메인 `drawwii.com`으로 서비스됩니다.

앱 저장소: <https://github.com/develop-bullets/bullets-drawwii-service-app> (이 페이지는 해당 저장소 `main` 브랜치의 변경사항을 반영합니다.)

## 로컬 개발

```bash
bundle install                 # 의존성 설치 (github-pages gem)
bundle exec jekyll serve       # http://localhost:4000 에서 미리보기
bundle exec jekyll build       # _site/ 에 정적 사이트 생성
```

## 콘텐츠 수정 가이드

대부분의 변경은 HTML/CSS 없이 아래 파일만 수정하면 됩니다.

| 변경 사항 | 수정할 곳 |
|---|---|
| 앱 이름·설명·슬로건, 기능 목록, 테마 색상, 소셜 계정 | `_config.yml` |
| 앱 아이콘·가격·App Store 링크 | `_config.yml` (비워 두면 iOS App ID로 iTunes API에서 자동 채움) |
| 버전 변경 내역 | `_pages/changelog.md` |
| 개인정보처리방침 / 이용약관 | `_pages/privacy.md`, `_pages/terms.md` |
| 스크린샷 / 데모 영상 | `assets/screenshot/` (`.png`/`.jpg`), `assets/videos/` (`.mp4`/`.mov`/`.ogg`/`.webm`) |
| 기기 프레임 색상 | `_config.yml`의 `device_color` (blue/black/yellow/coral/white) |

스크린샷·영상 권장 해상도: 828x1792, 1125x2436, 1242x2688.

## 배포

`master` 브랜치에 push하면 GitHub Pages가 자동으로 빌드·배포합니다.

## Credits

- 템플릿: [Automatic App Landing Page](https://github.com/emilbaehr/automatic-app-landing-page) by Emil Baehr (MIT License)
- [Jekyll](https://github.com/jekyll/jekyll), [FontAwesome](https://fontawesome.com/)

## License

[MIT License](LICENSE)

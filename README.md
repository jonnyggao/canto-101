# canto-101 — Survival Cantonese (modernized)

Static remaster of the **EdUHK CLE Cantonese Survival Package** (legacy HTML) with responsive layout, accessible navigation, UTF-8 encoding, and dark-mode–friendly styling.

- **Live content** is generated into [`docs/`](./docs/) (ready for GitHub Pages).
- **Source HTML** (UTF-8 exports of the original pages) lives in [`source/raw/`](./source/raw/).
- **Build** script: [`scripts/build.py`](./scripts/build.py) — extracts the lesson body, rewrites image URLs, and downloads figures from the original host (requires OpenSSL legacy renegotiation, as on Python 3.12+).

## GitHub Pages

1. Push this repository to GitHub.
2. Repo **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Branch: **main**, folder: **`/docs`**, Save.

The site will be available at `https://<user>.github.io/canto-101/` (replace `<user>` and repo name as needed).

### Rebuild after editing source

```bash
python3 scripts/build.py
```

This refreshes `docs/*.html` and fills `docs/assets/original/` with any missing images.

## Copyright

Course text, tables, and images **© The Hong Kong Institute of Education (2013)**. Do not republish commercially without permission from the copyright holder. This repository is a **layout modernization** for study and archival purposes; attribution is preserved on every page.

## Original URLs

<https://www.eduhk.hk/cle/resources/cep/cantonese-survival-package/index.html>

Appendix in this mirror: [`docs/appendix-i.html`](./docs/appendix-i.html) (filename without spaces for stable hosting).

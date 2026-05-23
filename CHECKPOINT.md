# Session Checkpoint - 2026-05-23

## What We Did Today

- Confirmed all development and testing will **stay on dev1 (this server, 192.168.22.235)**. No prod deployment.
- **Copied all needed files** into a clean directory: `/home/dev/rekanan-carousel/`
- **Updated `scripts/generate_carousel.py`** to use relative paths (no hardcoded `/home/dev/shopify` paths), portable across directories.

## Project Structure

```
/home/dev/rekanan-carousel/
├── scripts/
│   ├── generate_carousel.py         # Main generator (Linux)
│   └── deploy.sh                    # Git push → Cloudflare deploy
├── outputs/
│   └── carousel_dev.html            # Generated HTML for dev/testing
├── docs/
│   ├── pagefly_searchbox_plan.md
│   ├── google_sheets_setup.md
│   ├── QUICKSTART.md
│   └── LOGGING.md
├── .gitignore
├── requirements.txt                 # Python dependencies
└── CHECKPOINT.md                    # This file
```

## Open Tasks

- [ ] Initialize git and push to dev GitHub repo
- [ ] Connect Cloudflare Pages to dev GitHub repo (auto-deploy `carousel_dev.html`)
- [ ] Test iframe embed in PageFly using dev Cloudflare URL
- [ ] When approved, copy files to dev2, edit `OUTPUT_FILE` to `carousel_prod.html`, and push to prod GitHub repo
- [ ] Connect second Cloudflare Pages project for prod repo

## Deployment

```bash
# On dev1 (development & testing)
python3 scripts/generate_carousel.py   # outputs carousel_dev.html
./scripts/deploy.sh                    # commits and pushes to GitHub
```

## Notes

- `carousel_*.html` is fully self-contained (CSS + JS inline).
- No server-side dependencies needed for hosting.
- **Dev vs Prod switch:** Edit line 18 in `scripts/generate_carousel.py`
  - dev1: `OUTPUT_FILE = Path("outputs") / "carousel_dev.html"`
  - dev2: `OUTPUT_FILE = Path("outputs") / "carousel_prod.html"`


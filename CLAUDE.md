# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run development server (Docker, recommended)
docker-compose up

# Run Flask directly (requires Redis and Tesseract installed locally)
pip install -r requirements.txt
flask run

# Build Windows CLI executable (run on Windows)
build_windows.bat
# Produces: dist/ocr-cli.exe

# Run CLI directly (without building)
python cli.py convert image1.jpg image2.png -o output.pdf --lang spa
python cli.py langs
python cli.py info
```

There are no configured test or lint commands.

## Architecture

The app converts images (PNG, JPG, JPEG) to searchable PDFs using Tesseract OCR. It exposes two interfaces — a Flask web UI and a Click CLI — both backed by the same core service.

**Request flow (web):**
```
POST /upload (controller/UploadApi.py)
  → validates file types
  → ocr_service.images_to_searchable_pdf(image_sources, lang)
      → PIL opens each image
      → pytesseract.image_to_pdf_or_hocr() per image
      → pypdf merges all pages
  → returns PDF as download
```

**CLI flow:**
```
cli.py convert → ocr_service.images_to_searchable_pdf() → writes bytes to output file
```

**Key modules:**
- [ocr_service.py](ocr_service.py) — the only OCR logic; both the web controller and CLI call `images_to_searchable_pdf(image_sources, lang='eng')`
- [controller/UploadApi.py](controller/UploadApi.py) — Flask blueprint for `/upload`; handles file validation and response
- [app.py](app.py) — Flask app init, blueprint registration, Redis hit counter on `/`
- [cli.py](cli.py) — Click command group: `convert`, `langs`, `info`

**Deployment:** Docker Compose runs Flask on port 8000 (maps to container 5000) alongside a Redis container. The Dockerfile uses Alpine 3.7 with system packages `tesseract-ocr`, `jpeg-dev`, and `zlib-dev`.

**Windows executable:** PyInstaller packages `cli.py` using [ocr_cli.spec](ocr_cli.spec). The spec bundles the `tesseract` binary and its data files into a single-file executable.

## Dependencies

- `pytesseract` — thin wrapper around the Tesseract binary (must be installed separately outside Docker)
- `pypdf<4.0` — PDF merging; pinned because the API changed in v4
- `Pillow` — image loading before passing to pytesseract
- `redis` — only used for the hit counter in `app.py`; not involved in OCR

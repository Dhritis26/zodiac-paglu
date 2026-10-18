# ✦ Cosmic Birthday

Full-stack birthday, zodiac, birthstone, lucky number, compatibility, and anime character explorer. One Python server serves both the UI and API; no Node.js or database required.

## Run locally (Windows / macOS / Linux)

```bash
python -m venv .venv
```

Activate it:
- **Windows PowerShell:** `.venv\Scripts\Activate.ps1`
- **macOS/Linux:** `source .venv/bin/activate`

Then:

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open **http://127.0.0.1:8000** in your browser.

- Website: `/`
- Interactive backend API docs: `/docs`
- Anime and zodiac options: `/api/options`
- Generated birthday result: `POST /api/profile`

## Put on GitHub

Create an empty repository, then from this folder run:

```bash
git init
git add .
git commit -m "Initial Cosmic Birthday full-stack app"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cosmic-birthday.git
git push -u origin main
```

**Important:** GitHub stores code; it does **not** continuously host a Python backend via GitHub Pages. To publish this full-stack app publicly, connect your GitHub repository to a Python hosting service (e.g. Render or Railway). Use:
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

On Windows locally use `python -m uvicorn main:app --reload` as shown above.

## Design choices and limits

- The birth year is a direct type-in field so you don't have to scroll a calendar.
- Anime choice is a dropdown; every included show has four curated character archetypes.
- Compatibility and character scores are *illustrative*, not predictive. No official anime affiliation.
- Chinese zodiac new-year dates are included for 2000–2026 (earlier years produce an explicit unavailability notice to avoid incorrect animal assignments).
- Other traditional associations may vary by source.
- This demo does not persist users' birthdays or collect accounts.

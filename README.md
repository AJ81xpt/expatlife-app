# ExpatLife (Portugal & Malta MVP) — Defaults (Flutter + FastAPI + Strapi + Postgres)

This is a working MVP scaffold:
- **Flutter mobile app** (iOS/Android) with EN/PT localization, checklist/explore/cost screens
- **FastAPI backend** with Postgres/PostGIS
- **Strapi CMS** (runs in docker; project created on first run)

## Quick start

### 1) Run backend stack
```bash
cd infra
docker compose up -d --build
```

- API: http://localhost:8000/docs
- Strapi: http://localhost:1337/admin
- Postgres: localhost:5432 (db/user/pass: expatlife)

### 2) Seed starter content (Portugal + Malta)
```bash
cd expatlife-api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# make sure DATABASE_URL points to localhost db (default is fine if running docker locally)
python scripts/seed.py
```

### 3) Run the mobile app
```bash
cd expatlife-mobile
flutter pub get
flutter run
```

Notes:
- Android emulator accesses host API via `http://10.0.2.2:8000` (already configured).
- iOS simulator typically can use `http://localhost:8000` (adjust in code if needed).


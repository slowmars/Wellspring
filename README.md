# GoodsFlow — Women's Center Donation Ledger

A minimal, mobile-first web app for tracking donation intake and outbound distribution at a Women's Center.

## 30-Second Quickstart

```bash
# 1. Clone / unzip this folder, then:
cd goodsflow

# 2. Install dependencies (use a venv if you want)
pip install -r requirements.txt

# 3. Run
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

Open **http://localhost:8000** in your browser (or phone on same WiFi).

### Demo Passwords
| Role       | Password       |
|------------|----------------|
| Volunteer  | `volunteer123` |
| Staff      | `staff123`     |

The app seeds itself with demo data on first run. Staff can export CSV reports.

## Project Structure

```
goodsflow/
├── backend/
│   ├── main.py          # FastAPI app entry point
│   ├── database.py      # SQLAlchemy engine + session
│   ├── models.py        # ORM models (DonationItem, OutboundRecord, Category)
│   ├── schemas.py       # Pydantic request/response models
│   ├── deps.py          # Auth helpers
│   ├── seed.py          # Category + demo data seeder
│   └── routes/
│       ├── auth.py      # POST /api/auth/login
│       ├── intake.py    # POST/GET /api/intake
│       ├── outbound.py  # POST/GET /api/outbound
│       └── reports.py   # GET /api/reports/*
├── frontend/
│   └── index.html       # Single-page app (no build step)
├── uploads/             # Photo storage
├── data/                # SQLite DB (auto-created)
├── .env                 # Demo passwords
└── requirements.txt
```

## API Endpoints

| Method | Path                          | Auth       | Description              |
|--------|-------------------------------|------------|--------------------------|
| POST   | /api/auth/login               | None       | Returns token + role     |
| GET    | /api/categories               | None       | List categories          |
| POST   | /api/intake                   | Any        | Create intake (multipart)|
| GET    | /api/intake                   | Any        | List recent intake       |
| POST   | /api/outbound                 | Any        | Create outbound          |
| GET    | /api/outbound                 | Any        | List recent outbound     |
| GET    | /api/reports/summary?days=7   | Any        | 7-day totals by category |
| GET    | /api/reports/cumulative       | Any        | All-time intake vs out   |
| GET    | /api/reports/low-inventory    | Any        | Low stock warnings       |
| GET    | /api/reports/export.csv?type= | Staff only | CSV download             |

## Phone Testing

Find your laptop IP (`ifconfig` or `ipconfig`), then open `http://<your-ip>:8000` on your phone.

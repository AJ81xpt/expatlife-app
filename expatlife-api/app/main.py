from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from .config import settings
from .db import get_db, Base, engine
from . import models

app = FastAPI(title="ExpatLife API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/admin/init-db")
def init_db():
    Base.metadata.create_all(bind=engine)
    return {"created": True}

def _lang(lang: str | None) -> str:
    return "pt" if (lang or "en").lower().startswith("pt") else "en"

@app.get("/countries")
def countries(lang: str | None = Query(default="en"), db: Session = Depends(get_db)):
    l = _lang(lang)
    rows = db.execute(select(models.Country).order_by(models.Country.name_en)).scalars().all()
    out=[]
    for c in rows:
        out.append({"id": c.id, "iso2": c.iso2, "name": c.name_pt if (l=="pt" and c.name_pt) else c.name_en})
    return out

@app.get("/cities")
def cities(country_id: int, db: Session = Depends(get_db)):
    rows = db.execute(select(models.City).where(models.City.country_id==country_id).order_by(models.City.name)).scalars().all()
    return [{"id": r.id, "country_id": r.country_id, "name": r.name, "lat": float(r.lat), "lng": float(r.lng)} for r in rows]

@app.get("/tasks")
def tasks(country_id: int, lang: str | None = Query(default="en"), db: Session = Depends(get_db)):
    l = _lang(lang)
    q = (select(models.Task)
         .where(models.Task.country_id==country_id)
         .options(selectinload(models.Task.steps),
                  selectinload(models.Task.documents),
                  selectinload(models.Task.links))
         .order_by(models.Task.category, models.Task.title_en))
    rows = db.execute(q).scalars().all()
    return [task_to_json(t,l) for t in rows]

@app.get("/places")
def places(city_id: int, place_type: str | None = None, q: str | None = None, db: Session = Depends(get_db)):
    stmt = select(models.Place).where(models.Place.city_id==city_id)
    if place_type:
        stmt = stmt.where(models.Place.place_type==place_type)
    if q:
        stmt = stmt.where(models.Place.name.ilike(f"%{q}%"))
    rows = db.execute(stmt.order_by(models.Place.name)).scalars().all()
    return [{"id": p.id, "city_id": p.city_id, "place_type": p.place_type, "name": p.name,
             "address": p.address, "lat": float(p.lat), "lng": float(p.lng),
             "website": p.website, "tags": p.tags} for p in rows]

@app.get("/cost")
def cost(city_id: int, db: Session = Depends(get_db)):
    c = db.execute(select(models.CostOfLiving).where(models.CostOfLiving.city_id==city_id)).scalars().first()
    if not c:
        return {"city_id": city_id, "rent_1br_min":0,"rent_1br_max":0,"rent_3br_min":0,"rent_3br_max":0,
                "utilities_min":0,"utilities_max":0,"transport_monthly_min":0,"transport_monthly_max":0,
                "groceries_monthly_min":0,"groceries_monthly_max":0,"last_updated_at": None}
    return {"city_id": c.city_id,
            "rent_1br_min": c.rent_1br_min, "rent_1br_max": c.rent_1br_max,
            "rent_3br_min": c.rent_3br_min, "rent_3br_max": c.rent_3br_max,
            "utilities_min": c.utilities_min, "utilities_max": c.utilities_max,
            "transport_monthly_min": c.transport_monthly_min, "transport_monthly_max": c.transport_monthly_max,
            "groceries_monthly_min": c.groceries_monthly_min, "groceries_monthly_max": c.groceries_monthly_max,
            "last_updated_at": c.last_updated_at.isoformat()}

def task_to_json(t: models.Task, l: str):
    title = t.title_pt if (l=="pt" and t.title_pt) else t.title_en
    summary = t.summary_pt if (l=="pt" and t.summary_pt) else t.summary_en
    steps = sorted(t.steps, key=lambda s: s.step_order)
    return {
      "id": t.id,
      "country_id": t.country_id,
      "category": t.category,
      "title": title,
      "summary": summary,
      "last_reviewed_at": t.last_reviewed_at.isoformat(),
      "steps": [{"step_order": s.step_order,
                 "title": s.title_pt if (l=="pt" and s.title_pt) else s.title_en,
                 "body": s.body_pt if (l=="pt" and s.body_pt) else s.body_en} for s in steps],
      "documents": [{"name": d.name_pt if (l=="pt" and d.name_pt) else d.name_en,
                     "required": d.required,
                     "notes": d.notes_pt if (l=="pt" and d.notes_pt) else d.notes_en} for d in t.documents],
      "links": [{"label": ln.label_pt if (l=="pt" and ln.label_pt) else ln.label_en,
                 "url": ln.url,
                 "link_type": ln.link_type} for ln in t.links],
    }

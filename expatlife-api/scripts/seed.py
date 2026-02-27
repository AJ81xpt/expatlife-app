"""
Seeds Portugal + Malta starter data directly into Postgres.

Usage:
  python scripts/seed.py

If running docker compose locally, default DATABASE_URL works:
  postgresql+psycopg://expatlife:expatlife@localhost:5432/expatlife
"""
from sqlalchemy import create_engine, text
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://expatlife:expatlife@localhost:5432/expatlife")

COUNTRIES = [
  {"iso2":"PT","name_en":"Portugal","name_pt":"Portugal"},
  {"iso2":"MT","name_en":"Malta","name_pt":"Malta"},
]

CITIES = [
  {"iso2":"PT","name":"Lisbon","lat":38.7223,"lng":-9.1393},
  {"iso2":"PT","name":"Porto","lat":41.1579,"lng":-8.6291},
  {"iso2":"PT","name":"Faro","lat":37.0194,"lng":-7.9304},
  {"iso2":"PT","name":"Braga","lat":41.5454,"lng":-8.4265},
  {"iso2":"MT","name":"Valletta","lat":35.8989,"lng":14.5146},
  {"iso2":"MT","name":"Sliema","lat":35.9122,"lng":14.5040},
  {"iso2":"MT","name":"St Julian's","lat":35.9180,"lng":14.4890},
  {"iso2":"MT","name":"Gzira","lat":35.9055,"lng":14.4933},
]

TASKS = [
  {"country":"PT","category":"Admin",
   "title_en":"Get a NIF (Tax Identification Number)",
   "title_pt":"Obter NIF (Número de Identificação Fiscal)",
   "summary_en":"A NIF is needed for renting, banking, utilities, and most contracts in Portugal.",
   "summary_pt":"O NIF é necessário para arrendar, abrir conta, serviços e a maioria dos contratos.",
   "steps":[
      (1,"Check eligibility and route","Verificar elegibilidade e via",
       "EU/EEA/Swiss citizens can often request in person at a Finanças office. Non‑EU residents may need a fiscal representative depending on current rules.",
       "Cidadãos UE/EEE/Suíços podem pedir presencialmente nas Finanças. Não‑UE pode precisar de representante fiscal conforme regras atuais."),
      (2,"Prepare documents","Preparar documentos",
       "Bring passport/ID and proof of address. Some offices request additional documentation—check the local office page.",
       "Leve identificação e comprovativo de morada. Alguns postos pedem documentação adicional."),
      (3,"Submit request","Submeter pedido",
       "Go to Finanças (Autoridade Tributária) or use a trusted service provider. Save the confirmation with your NIF.",
       "Dirija-se às Finanças (AT) ou use um prestador de confiança. Guarde o comprovativo com o NIF."),
   ],
   "docs":[("Passport or EU ID card","Passaporte ou Cartão de Cidadão",1),
           ("Proof of address (Portugal or abroad)","Comprovativo de morada (Portugal ou estrangeiro)",1)],
   "links":[("Portuguese Tax Authority (AT)","Autoridade Tributária (AT)","https://www.portaldasfinancas.gov.pt/","official")]
  },
  {"country":"PT","category":"Banking",
   "title_en":"Open a Portuguese bank account",
   "title_pt":"Abrir conta bancária em Portugal",
   "summary_en":"Most services require a local IBAN; requirements vary by bank.",
   "summary_pt":"Muitos serviços exigem IBAN local; requisitos variam por banco.",
   "steps":[
      (1,"Choose account type","Escolher tipo de conta",
       "Compare monthly fees, cards, and app support. Some banks offer non-resident options.",
       "Compare comissões, cartões e app. Alguns bancos têm opções para não-residentes."),
      (2,"Bring required documents","Levar documentos",
       "Typically NIF, passport/ID, and proof of address. Some banks request proof of income or residency.",
       "Normalmente NIF, identificação e comprovativo de morada. Alguns pedem prova de rendimentos ou residência."),
      (3,"Verify and activate","Verificar e ativar",
       "Complete identity checks, set PINs, and enable online banking.",
       "Conclua verificações, defina PINs e ative homebanking."),
   ],
   "docs":[("NIF","NIF",1),("Passport or EU ID card","Passaporte ou Cartão de Cidadão",1),("Proof of address","Comprovativo de morada",1)],
   "links":[("Banco de Portugal consumer site","Site do Cliente Bancário","https://clientebancario.bportugal.pt/","official")]
  },
  {"country":"PT","category":"Driving",
   "title_en":"Exchange a foreign driver's license",
   "title_pt":"Trocar carta de condução estrangeira",
   "summary_en":"Rules differ for EU vs non‑EU licenses; the process is managed by IMT.",
   "summary_pt":"Regras diferem para cartas UE vs não‑UE; o processo é do IMT.",
   "steps":[
      (1,"Confirm if exchange is required","Confirmar se é necessária",
       "EU licenses are generally recognized; non‑EU may need exchange within a deadline after residency. Verify latest rules before applying.",
       "Cartas UE são geralmente reconhecidas; não‑UE pode ter prazo para troca após residência. Verifique regras atuais."),
      (2,"Gather documents","Reunir documentos",
       "Some cases require medical certificate and/or psychological assessment.",
       "Alguns casos exigem atestado médico e/ou avaliação psicológica."),
      (3,"Apply via IMT","Submeter no IMT",
       "Submit online or in person depending on availability. Keep proof of submission.",
       "Submeta online ou presencialmente. Guarde comprovativo."),
   ],
   "docs":[("Driver's license (original)","Carta de condução (original)",1),("Passport/ID","Passaporte/ID",1),("Residency proof (if applicable)","Comprovativo de residência (se aplicável)",0)],
   "links":[("IMT","IMT","https://www.imt-ip.pt/","official")]
  },
  {"country":"MT","category":"Admin",
   "title_en":"Register residence / obtain eResidence card",
   "title_pt":"Registar residência / obter eResidence",
   "summary_en":"Residence registration is handled via Identity Malta; requirements differ for EU vs non‑EU.",
   "summary_pt":"O registo de residência é via Identity Malta; requisitos diferem para UE vs não‑UE.",
   "steps":[
      (1,"Determine your route","Determinar via",
       "EU citizens register under EU rules; non‑EU typically follow permit routes tied to work/study/other permits.",
       "Cidadãos UE registam-se pelas regras UE; não‑UE seguem vias de autorização ligadas a trabalho/estudo/etc."),
      (2,"Book appointment and prepare documents","Marcar e preparar documentos",
       "Prepare passport/ID, proof of address, and supporting documents (employment, insurance, etc.).",
       "Prepare ID, comprovativo de morada e documentos (trabalho, seguro, etc.)."),
      (3,"Submit application","Submeter candidatura",
       "Submit to Identity Malta and keep receipts/confirmation.",
       "Submeta na Identity Malta e guarde recibos/confirmação."),
   ],
   "docs":[("Passport/ID","Passaporte/ID",1),("Proof of address in Malta","Comprovativo de morada em Malta",1)],
   "links":[("Identity Malta","Identity Malta","https://identitymalta.com/","official")]
  },
  {"country":"MT","category":"Driving",
   "title_en":"Convert a driver's license",
   "title_pt":"Converter carta de condução",
   "summary_en":"Transport Malta manages license conversion; conditions depend on origin country and residency status.",
   "summary_pt":"A Transport Malta gere a conversão; condições dependem do país de origem e do estatuto.",
   "steps":[
      (1,"Check eligibility","Verificar elegibilidade",
       "Verify whether your license is exchangeable and what documents are required for your case.",
       "Verifique se a sua carta é convertível e que documentos são necessários."),
      (2,"Prepare documents","Preparar documentos",
       "Bring original license, ID, proof of residence, and photos if requested.",
       "Leve carta original, ID, prova de residência e fotos se solicitado."),
      (3,"Apply with Transport Malta","Submeter na Transport Malta",
       "Submit and keep confirmation. Processing times vary.",
       "Submeta e guarde confirmação. Prazos variam."),
   ],
   "docs":[("Driver's license (original)","Carta de condução (original)",1),("Passport/ID","Passaporte/ID",1),("Proof of Malta address","Comprovativo de morada em Malta",1)],
   "links":[("Transport Malta","Transport Malta","https://www.transport.gov.mt/","official")]
  },
]

PLACES = [
  ("PT","Lisbon","supermarket","Continente (Example)","Lisbon",38.7223,-9.1393,"https://www.continente.pt/","grocery,delivery"),
  ("PT","Lisbon","supermarket","Pingo Doce (Example)","Lisbon",38.7369,-9.1427,"https://www.pingodoce.pt/","grocery"),
  ("MT","Sliema","supermarket","Lidl (Example)","Sliema",35.9122,14.5040,"https://www.lidl.com.mt/","grocery"),
  ("PT","Porto","course","Portuguese Course (Example)","Porto",41.1579,-8.6291,"","language,pt-A1"),
  ("MT","St Julian's","course","English School (Example)","St Julian's",35.9180,14.4890,"","language,en-A1"),
  ("PT","Lisbon","service","Handyman Service (Example)","Lisbon",38.7280,-9.1400,"","handyman,repairs"),
]

COSTS = [
  ("PT","Lisbon",1100,1700,2000,3200,120,220,40,60,250,450),
  ("PT","Porto",800,1300,1400,2200,110,210,35,55,230,420),
  ("MT","Sliema",1200,1900,2000,3200,120,240,30,60,260,480),
  ("MT","Valletta",1100,1800,1900,3100,120,240,30,60,260,480),
]

def main():
    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        # Create tables (same as POST /admin/init-db but without API call)
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS countries (
          id SERIAL PRIMARY KEY,
          iso2 VARCHAR(2) UNIQUE NOT NULL,
          name_en VARCHAR(120) NOT NULL,
          name_pt VARCHAR(120)
        );
        CREATE TABLE IF NOT EXISTS cities (
          id SERIAL PRIMARY KEY,
          country_id INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
          name VARCHAR(120) NOT NULL,
          lat NUMERIC(9,6) NOT NULL,
          lng NUMERIC(9,6) NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_cities_country ON cities(country_id);

        CREATE TABLE IF NOT EXISTS tasks (
          id SERIAL PRIMARY KEY,
          country_id INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
          category VARCHAR(60) NOT NULL,
          title_en VARCHAR(160) NOT NULL,
          title_pt VARCHAR(160),
          summary_en VARCHAR(280) NOT NULL,
          summary_pt VARCHAR(280),
          last_reviewed_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_tasks_country ON tasks(country_id);

        CREATE TABLE IF NOT EXISTS task_steps (
          id SERIAL PRIMARY KEY,
          task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
          step_order INTEGER NOT NULL,
          title_en VARCHAR(160) NOT NULL,
          title_pt VARCHAR(160),
          body_en TEXT NOT NULL,
          body_pt TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_steps_task ON task_steps(task_id);

        CREATE TABLE IF NOT EXISTS task_documents (
          id SERIAL PRIMARY KEY,
          task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
          name_en VARCHAR(160) NOT NULL,
          name_pt VARCHAR(160),
          required BOOLEAN NOT NULL DEFAULT TRUE,
          notes_en VARCHAR(280),
          notes_pt VARCHAR(280)
        );
        CREATE INDEX IF NOT EXISTS idx_docs_task ON task_documents(task_id);

        CREATE TABLE IF NOT EXISTS task_links (
          id SERIAL PRIMARY KEY,
          task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
          label_en VARCHAR(160) NOT NULL,
          label_pt VARCHAR(160),
          url VARCHAR(500) NOT NULL,
          link_type VARCHAR(30) NOT NULL DEFAULT 'official'
        );
        CREATE INDEX IF NOT EXISTS idx_links_task ON task_links(task_id);

        CREATE TABLE IF NOT EXISTS places (
          id SERIAL PRIMARY KEY,
          city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
          place_type VARCHAR(30) NOT NULL,
          name VARCHAR(180) NOT NULL,
          address VARCHAR(280) NOT NULL,
          lat NUMERIC(9,6) NOT NULL,
          lng NUMERIC(9,6) NOT NULL,
          website VARCHAR(500),
          tags VARCHAR(280)
        );
        CREATE INDEX IF NOT EXISTS idx_places_city ON places(city_id);

        CREATE TABLE IF NOT EXISTS cost_of_living (
          id SERIAL PRIMARY KEY,
          city_id INTEGER NOT NULL REFERENCES cities(id) ON DELETE CASCADE,
          rent_1br_min INTEGER NOT NULL,
          rent_1br_max INTEGER NOT NULL,
          rent_3br_min INTEGER NOT NULL,
          rent_3br_max INTEGER NOT NULL,
          utilities_min INTEGER NOT NULL,
          utilities_max INTEGER NOT NULL,
          transport_monthly_min INTEGER NOT NULL,
          transport_monthly_max INTEGER NOT NULL,
          groceries_monthly_min INTEGER NOT NULL,
          groceries_monthly_max INTEGER NOT NULL,
          last_updated_at TIMESTAMP NOT NULL DEFAULT NOW()
        );
        CREATE INDEX IF NOT EXISTS idx_cost_city ON cost_of_living(city_id);
        """))

        iso_to_country={}
        for c in COUNTRIES:
            res = conn.execute(text("""
              INSERT INTO countries (iso2,name_en,name_pt)
              VALUES (:iso2,:ne,:np)
              ON CONFLICT (iso2) DO UPDATE SET name_en=EXCLUDED.name_en, name_pt=EXCLUDED.name_pt
              RETURNING id
            """), {"iso2":c["iso2"],"ne":c["name_en"],"np":c["name_pt"]})
            iso_to_country[c["iso2"]] = res.scalar()

        city_id={}
        for c in CITIES:
            res = conn.execute(text("""
              INSERT INTO cities (country_id,name,lat,lng)
              VALUES (:country_id,:name,:lat,:lng)
              RETURNING id
            """), {"country_id": iso_to_country[c["iso2"]], "name": c["name"], "lat": c["lat"], "lng": c["lng"]})
            city_id[(c["iso2"], c["name"])] = res.scalar()

        for t in TASKS:
            res = conn.execute(text("""
              INSERT INTO tasks (country_id,category,title_en,title_pt,summary_en,summary_pt,last_reviewed_at)
              VALUES (:country_id,:cat,:te,:tp,:se,:sp,:lr)
              RETURNING id
            """), {"country_id": iso_to_country[t["country"]], "cat": t["category"],
                   "te": t["title_en"], "tp": t["title_pt"], "se": t["summary_en"], "sp": t["summary_pt"],
                   "lr": datetime.utcnow()})
            tid = res.scalar()
            for (o, te, tp, be, bp) in t["steps"]:
                conn.execute(text("""
                  INSERT INTO task_steps (task_id,step_order,title_en,title_pt,body_en,body_pt)
                  VALUES (:task_id,:o,:te,:tp,:be,:bp)
                """), {"task_id": tid, "o": o, "te": te, "tp": tp, "be": be, "bp": bp})
            for (ne, np, req) in t["docs"]:
                conn.execute(text("""
                  INSERT INTO task_documents (task_id,name_en,name_pt,required)
                  VALUES (:task_id,:ne,:np,:req)
                """), {"task_id": tid, "ne": ne, "np": np, "req": bool(req)})
            for (le, lp, url, lt) in t["links"]:
                conn.execute(text("""
                  INSERT INTO task_links (task_id,label_en,label_pt,url,link_type)
                  VALUES (:task_id,:le,:lp,:url,:lt)
                """), {"task_id": tid, "le": le, "lp": lp, "url": url, "lt": lt})

        for (iso, city, pt, name, addr, lat, lng, web, tags) in PLACES:
            conn.execute(text("""
              INSERT INTO places (city_id,place_type,name,address,lat,lng,website,tags)
              VALUES (:city_id,:pt,:name,:addr,:lat,:lng,:web,:tags)
            """), {"city_id": city_id[(iso, city)], "pt": pt, "name": name, "addr": addr, "lat": lat, "lng": lng,
                   "web": web or None, "tags": tags})

        for (iso, city, r1a, r1b, r3a, r3b, ua, ub, ta, tb, ga, gb) in COSTS:
            conn.execute(text("""
              INSERT INTO cost_of_living (city_id,rent_1br_min,rent_1br_max,rent_3br_min,rent_3br_max,
                utilities_min,utilities_max,transport_monthly_min,transport_monthly_max,groceries_monthly_min,groceries_monthly_max,last_updated_at)
              VALUES (:city_id,:r1a,:r1b,:r3a,:r3b,:ua,:ub,:ta,:tb,:ga,:gb,:lu)
            """), {"city_id": city_id[(iso, city)], "r1a": r1a, "r1b": r1b, "r3a": r3a, "r3b": r3b,
                   "ua": ua, "ub": ub, "ta": ta, "tb": tb, "ga": ga, "gb": gb, "lu": datetime.utcnow()})

    print("Seed complete.")

if __name__ == "__main__":
    main()

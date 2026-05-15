# 🔮 FPL‑Oracle: Distributed FPL Prediction Engine

A high‑performance, asynchronous prediction system designed to forecast Fantasy Premier League (FPL) player performance using distributed scrapers, real‑time Redis storage, and modular analytical workers (“Cooks”).  
Built for speed, resilience, and extensibility.

---

## 🧠 System Overview

FPL‑Oracle follows a **Producer → Pantry → Cook → Aggregator → Manager → API** pipeline.  
Each layer is isolated, fault‑tolerant, and independently deployable.

---

## 🏗️ Architecture Breakdown

### **1. Producers — Data Ingestors**
Located in: `producer/`

These workers fetch raw data from multiple sources and push structured fields into Redis using static player/team IDs.

- **FPL API Scraper (`fpl_scraper.py`)**  
  Official FPL data: prices, minutes, ICT, points, status.

- **FotMob Scraper (`fotmob_scrapper.py`)**  
  Advanced stats: xG, xA, xGI, shots, key passes.

- **Reddit/X Scout (`reddit_scraper.py`)**  
  Injury rumors, leaked lineups, tactical news.

- **Producer Orchestrator (`producer.py`)**  
  Coordinates async scraping cycles.

Producers never talk to each other — they only write to Redis.

---

### **2. Pantry — Redis State Store**
Located in: `db/`

Redis acts as the **single source of truth** for all player/team data.

- **`db_redis.py`** — Redis client + helper methods  
- **`players.py`** — Player schema, getters/setters  
- **`teams.py`** — Team schema, getters/setters  

Redis keys follow a clean pattern:

player:{id}
team:{id}
fixture:{gw}:{team_id}

Each producer updates only its own fields, ensuring **atomic, non‑destructive writes**.

---

### **3. Cooks — Analytical Workers**
Located in: `cook/`

Cooks read from Redis, compute a single coefficient, and write the result back.

- **`minute_cook.py`** — Minutes probability  
- **`form_cook.py`** — Weighted form score  
- **`fixture_cook.py`** — Fixture difficulty  
- **`cook.py`** — Base class for all workers  

Each Cook is intentionally narrow in scope — this makes the system modular and debuggable.

---

### **4. Aggregator — Expected Points Engine**
(Coming soon)

This worker combines all Cook coefficients into a final **xP (Expected Points)** value.

Formula (simplified):

xP = P_minutes × P_form × P_fixture × role_weight × team_strength


---

### **5. Manager — Best XI Selector**
(Coming soon)

Applies:

- Formation rules  
- Budget constraints  
- Position limits  
- Fixture weighting  
- xP ranking  

Outputs:

- Best XI  
- Captain pick  
- Bench order  

---

### **6. Waiter — API Layer**
(Coming soon)

A lightweight API that exposes:

- `/player/{id}/xp`  
- `/bestxi`  
- `/captain`  
- `/fixtures`  

---

## 📂 Project Structure

```text
fpl_oracle/
│
├── config/                 # Global settings & data schemas
│   ├── data_maps.py
│   ├── data_struct.py
│   └── settings.py
│
├── cook/                   # Analytical workers (Cooks)
│   ├── cook.py
│   ├── fixture_cook.py
│   ├── form_cook.py
│   └── minute_cook.py
│
├── db/                     # Redis abstraction layer
│   ├── db_redis.py
│   ├── players.py
│   └── teams.py
│
├── producer/               # Distributed scrapers
│   ├── producer.py
│   ├── fotmob_scrapper.py
│   ├── fpl_scraper.py
│   └── reddit_scraper.py
│
├── utils/                  # Shared utilities
│   ├── data_to_txt.py
│   ├── log.py
│   ├── pw_browser_async.py
│   └── scraper.py
│
└── main.py                 # Entry point for orchestrating the pipeline

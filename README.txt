# 🔮 FPL Oracle: Distributed Prediction Engine

A high-performance, asynchronous data pipeline designed to predict Fantasy Premier League (FPL) player performance using distributed scrapers, real-time data storage, and modular analytical workers.

## 🏗️ System Architecture

The project follows a **Producer-Consumer** pattern mediated by **Redis**, ensuring total independence between data ingestion and statistical analysis.

![System Architecture](./fpl_orcale_system.png)

### 1. The Producers (Data Ingestors)
Three independent scripts fetch raw data and push it into the Redis "Pantry" using static Player IDs as keys:
* **FPL API Worker (`fpl_api.py`)**: Fetches official prices, ownership, and current point tallies.
* **FotMob Scraper (`fotmob_scrapper.py`)**: Uses BeautifulSoup to extract advanced metrics like xG (Expected Goals) and xA (Expected Assists) from FotMob HTML.
* **News Scout (`news_scrapper.py`)**: Scrapes Reddit and X (Twitter) for injury news, "leaked" lineups, and tactical rumors.

### 2. The Shared Hub (Redis Store)
Acts as the **State Store**. Data is organized by static keys (e.g., `player:305`), allowing producers to update "ingredients" independently.
* **Atomic Updates**: If the FPL Worker updates a price, it doesn't overwrite the xG data previously sent by FotMob.
* **Persistence**: Data remains available for the Cooks even if a Producer goes offline.

### 3. The Analysts (The Cooks)
Modular workers (`cook_a.py` to `cook_d.py`) subscribe to Redis updates to calculate specific probability coefficients:
* **Worker 1 (The Physio)**: Calculates injury and fitness probability ($P_{injury}$).
* **Worker 2 (The Manager)**: Calculates rotation risk based on recent high-intensity minutes.
* **Worker 3 (The Tactician)**: Evaluates match strength and fixture difficulty.
* **Worker 4 (The Statistician)**: Computes weighted form using STAT 151 principles.

### 4. The Orchestration (Manager & Waiter)
* **The Manager**: Aggregates all coefficients from the Cooks to calculate the final **Expected Points (xP)**.
* **The Waiter (Internal API)**: An API layer that serves the final "dishes" to the dashboard.
* **Dashboard**: A NextJS/Streamlit UI providing real-time visualizations for the end-user.

---

## 📂 Project Structure

```text
fpl_oracle/
├── common/                # Shared logic, Redis client, and Schemas
├── producers/             # Raw data extractors (Workers A, B, C)
├── analysts/              # Probability and Math Workers (Cooks)
├── brain/                 # Manager/Aggregator logic
├── dashboard/             # NextJS/Streamlit frontend
└── docker-compose.yml     # Orchestration for Redis and Workers

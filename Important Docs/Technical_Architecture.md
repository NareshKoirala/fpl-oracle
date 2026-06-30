# Technical Architecture Document

## 1. System Architecture
FPL-Oracle follows a pipelined, distributed architecture designed for asynchronous processing.
**Pipeline Flow:** `Producer -> Pantry -> Cook -> Aggregator -> Manager -> API (Waiter) -> Frontend Dashboard`

## 2. Component Breakdown

### 2.1 Backend (Python & asyncio)
- **Producers (Data Ingestors):** Located in `service/oracle/producer/`. 
  - Uses asynchronous scraping (`fpl_scraper.py`, `fotmob_scrapper.py`, `reddit_scraper.py`).
  - Writes directly to Redis using atomic, non-destructive updates.
- **Pantry (Data Layer):** Located in `service/oracle/db/`.
  - **Technology:** Redis.
  - Acts as the single source of truth with keys scoped to `player:{id}`, `team:{id}`, and `fixture:{gw}:{team_id}`.
- **Cooks (Analytical Workers):** Located in `service/oracle/cook/`.
  - Focused analytical models computing single coefficients (e.g., `minute_cook`, `form_cook`, `fixture_cook`).
  - Reads data from Redis, performs calculations, and writes coefficients back.
- **Aggregator & Manager (Future Implementations):** 
  - **Aggregator:** Calculates Expected Points (`xP`) using the equation: `xP = P_minutes × P_form × P_fixture × role_weight × team_strength`.
  - **Manager:** Applies optimization rules (budget, constraints) to select the optimal starting XI and captain.
- **Waiter (API Layer):** Located in `service/oracle/waiter/`.
  - **Technology:** FastAPI.
  - Exposes fast, RESTful endpoints (`/fixtures`, `/team`, history, etc.) directly connected to the Redis Pantry.

### 2.2 Frontend (React & Vite)
- **Technology Stack:** React 19, TypeScript, Vite, Tailwind CSS 4.
- **Location:** `service/dashboard/`.
- **UI & Visualization:** 
  - Components stylized via Tailwind CSS and animated via `motion` (Framer).
  - Icons provided by `lucide-react`.
  - Data charts and analytics visualization via `recharts`.
- **Integration:** Fetches data natively from the Waiter API layer for real-time analytics viewing.

## 3. Data Flow
1. **Scraping:** External sources are scraped periodically via the async event loop managed in `main.py`.
2. **Storage:** Standardized schemas (defined in `config/data_struct.py`) are pushed to Redis.
3. **Processing:** Cooks periodically digest newly ingested data, generating statistical scores.
4. **Consumption:** The React frontend queries the Waiter FastAPI for processed data insights, rendering them visually for the end user.

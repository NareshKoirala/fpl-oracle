# Feature Ticket List

## Backend / Data Engineering
- **[BE-01] Implement Aggregator Worker:** Create the `xP` engine that reads data from Cooks and calculates the final Expected Points formula.
- **[BE-02] Implement Manager Worker:** Build the algorithm that uses xP, budget constraints, and formation rules to output the "Best XI".
- **[BE-03] Expand Waiter API:** Add the remaining REST endpoints mentioned in the docs: `/player/{id}/xp`, `/bestxi`, and `/captain`.
- **[BE-04] Secure Redis Connection:** Add authentication and configure `db_redis.py` to use secure `.env` variables for deployment.
- **[BE-05] Add Error Handling to Producers:** Ensure scrapers have robust retry logic, logging, and proxy support to prevent blockages from FotMob/FPL APIs.

## Frontend / UI
- **[FE-01] Connect Frontend to Live API:** Replace `dummy-data` inside the React Dashboard with real calls to the Waiter FastAPI service.
- **[FE-02] Player Stats Spider Chart:** Implement a `recharts` radar chart showing a player's underlying stats (xG, xA, Form, ICT).
- **[FE-03] Best XI Pitch Visualization:** Create a dynamic football pitch component in React to visually place the Manager Worker's recommended players.
- **[FE-04] Dark Mode & Theming:** Leverage Tailwind CSS to implement a sleek dark mode toggle for the dashboard.
- **[FE-05] Loading Skeletons:** Implement Framer `motion` skeleton loaders for components while waiting for API responses.

## DevOps / Infrastructure
- **[OPS-01] Dockerize Backend:** Create a `Dockerfile` and `docker-compose.yml` to spin up the FastAPI server, Producers, Cooks, and a local Redis container easily.
- **[OPS-02] Dockerize Frontend:** Create a multi-stage `Dockerfile` to build the Vite React app and serve it via Nginx.
- **[OPS-03] CI/CD Pipeline:** Setup GitHub Actions to run `flake8`/`black` for Python and `tsc --noEmit` / linting for the frontend on Pull Requests.

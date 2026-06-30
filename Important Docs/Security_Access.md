# Security & Access Document

## 1. Overview
This document outlines the security considerations, data access patterns, and environmental configurations for the FPL-Oracle platform.

## 2. Access Management
- **API Access (Waiter):**
  - Standard CORS configuration must be maintained to only allow requests from the designated frontend dashboard domains.
  - Future iterations should implement API key authentication or JWTs to secure user-specific requests and prevent abuse of the recommendation engine.
- **Database Access (Redis):**
  - Redis instance acts as the central pantry. It MUST NOT be exposed to the public internet.
  - Access is strictly limited to internal backend components (Producers, Cooks, Waiter) operating within the same network/VPC or Docker network.
  - Default Redis authentication (password protection via `REDIS_PASSWORD`) should be implemented in production.

## 3. Data Security & Scraping Constraints
- **Rate Limiting Resilience:** 
  - Producers must implement back-off strategies and jitter when scraping external endpoints (FPL API, FotMob) to avoid IP bans.
  - Playwright/Browser automation (`utils/pw_browser_async.py`) should use randomized user agents and headless browsing patterns.
- **Data Integrity:** 
  - Redis writes are atomic. Producers only overwrite specific fields they own to avoid corrupting shared entity data (e.g., player or team state).

## 4. Environment Variables
Sensitive data and configurations are managed via `.env` files (e.g., `service/dashboard/.env.example`).
Variables typically include:
- `REDIS_URL` / `REDIS_HOST` / `REDIS_PORT`
- `API_BASE_URL` (For the frontend to connect to the Waiter API)
- `SCRAPER_PROXIES` (If applicable for web scraping modules)

## 5. Deployment Security
- The system components (Frontend, API, Workers, Redis) should be containerized using Docker and orchestrated securely, ensuring only necessary ports (e.g., 80/443 for Frontend, 8000 for API) are exposed to the host machine.

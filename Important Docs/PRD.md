# Product Requirements Document (PRD)

## 1. Product Overview
**Product Name:** FPL-Oracle  
**Description:** A high-performance, asynchronous prediction system designed to forecast Fantasy Premier League (FPL) player performance using distributed scrapers, real-time storage, and modular analytical workers.  
**Target Audience:** Fantasy Premier League managers seeking data-driven insights and AI-powered recommendations to optimize their weekly team selections and transfers.

## 2. Goals & Objectives
- **Data Aggregation:** Ingest raw data from multiple sources (official FPL API, FotMob, Reddit/X) accurately and quickly.
- **Analytics:** Calculate robust Expected Points (xP) by analyzing form, fixtures, minutes probability, and tactical news.
- **Optimization:** Provide actionable insights such as the "Best XI", optimal captain picks, and bench orders.
- **Performance:** Ensure a low-latency, scalable backend capable of asynchronous data processing and real-time frontend updates.

## 3. Key Features
- **Data Ingestion (Producers):** Automated, async scrapers fetching price, minutes, ICT index, xG, xA, injury rumors, and leaked lineups.
- **Real-Time Storage (Pantry):** Redis-backed single source of truth for all player, team, and fixture data.
- **Modular Analytics (Cooks):** Specific workers computing individual coefficients (minutes, form, fixture difficulty).
- **Expected Points Engine (Aggregator):** Combine all coefficients into a final xP value.
- **Team Optimizer (Manager):** Apply formation rules, budget constraints, and position limits to select the Best XI.
- **Web Dashboard:** An interactive, rich UI for users to view player analytics, upcoming fixtures, and optimal team selections.

## 4. Non-Functional Requirements
- **Modularity:** Each component (Producer, Cook, API) must be decoupled and independently deployable.
- **Fault-Tolerance:** Scrapers must handle rate-limiting and source unavailability gracefully without crashing the system.
- **Scalability:** The architecture must support adding new data sources and analytical models easily.

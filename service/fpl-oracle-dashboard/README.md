# 🏆 FPL Oracle Dashboard

An advanced, feature-rich predictive analytics and decision-support portal for Fantasy Premier League (FPL). Built with highly customized visual layout grids, realistic probability distributions, clean-sheet odds, and expected metrics models to help users dominate their leagues with data-driven strategic insight.

---

## 🎨 Design Concept: Premium Cyber-Pitch Theme
The dashboard utilizes an eyesafe, ultra-modern dark UI styling called the **Cosmic Slate Theme** with vibrant official FPL high-contrast green accents (`#00ff85`). It matches dense mathematical data feeds with fluid, hardware-accelerated transitions via **Motion React** and vector **Lucide Icons** to produce a cinematic tactical console.

---

## 📂 Project Architecture & Component Structure

Every source file is modular, documented with headers and logical sections, and corresponds to a single responsibility.

### 🏢 Core Application Infrastructure
*   **`index.html`** – The fundamental physical landing page loading the root TypeScript module.
*   **`src/main.tsx`** – Mounts the main React 19 application within a `<StrictMode>` container.
*   **`src/App.tsx`** – The layout orchestrator of the entire platform, routing tab states (`dashboard`, `fixtures`, `processed`, `players`, `standings`, `search`) and distributing data parameters.
*   **`src/index.css`** – Central stylesheet implementing Tailwind CSS v4 directive overrides, Google modern fonts, custom glassmorphism clay-cards, responsive layouts, and scrollbar rules.

### 🍱 Component Library (`/src/components`)
All UI views are isolated into dedicated, modular components to prevent massive, complex, single-file bundles:
*   **`DashboardView.tsx`** – The central FPL Hub showing high-interest metrics, tactical expected vs. actual Teams of the Week (with detailed pitch maps and captaincy designations), and KPI cards.
*   **`FixturesView.tsx`** – The Match Center containing matchup catalogs, win/draw/loss expectations, team clean-sheet indices, and a full interactive Scoreline Heatmap Matrix showing goal-probability calculations. Fully optimized with seamless overlay dialogues on mobile.
*   **`ProcessedView.tsx`** – The mathematical core presenting team attack/defense coefficients, Clean Sheet expectation odds, premium/differential player comparison feeds, and the captaincy safety-index matrix.
*   **`PlayersView.tsx`** – Interactive player search panel, cost-to-points meters, and the dedicated **Player Dossier** drawer rendering beautiful polar radar charts or underlying stats comparisons.
*   **`StandingsView.tsx`** – Comprehensive league standings divided into home, away, form profiles, and expected (xG calculated) simulated league standings.
*   **`SearchView.tsx`** – Fuzzy global locator matching queries against players, matches, lineups, and team parameters instantly.
*   **`NavigationSidebar.tsx`** – Persistent responsive menu rail housing view buttons, Oracle synchronization toggles, and author details.
*   **`OracleStatusCard.tsx`** – Displays system status (database connection, sync timers) and supports manual triggers to simulate live data updates from background pipelines.
*   **`ChelseaHubCard.tsx`** – Chelsea-specific spotlight tracker highlighting the squad's upcoming fixtures and player profiles.
*   **`PredictionCenterCard.tsx`** – Season and gameweek selector dropdown toggles powering the application data scope.
*   **`DeveloperProfileCard.tsx`** – Holds verified development credentials and active communication networks for Naresh Koirala (`koiralanaresh10@gmail.com`).
*   **`ViewSkeleton.tsx`** – Animated skeletal loading maps customized for each view layout to keep transitions fluid.

### 📊 Statistical Repositories (`/src/data`)
Serves as the local dataset layer modeling Premier League inputs directly from a simulated high-performance FastAPI endpoint:
*   **`types.ts`** – Defines both the UI schema interfaces and the **exact FastAPI Response schemas** (which match the backend Redis Two-DB key-value schemas including `player:<id>`, `player:<id>:meta`, `player:<id>:season:<year>`, `proc_player:<id>:xp`, `proc_team:<id>:strength`, etc.).
*   **`fixtures.ts`** & **`players.ts`** – Dataset controllers mapping current gameweek selections to underlying profile parameters.
*   **`teams_strength.ts`** & **`teams_raw.ts`** – Aggregators of team difficulties, scores, and records.
*   **`goal_probabilities.ts`** & **`scorelines.ts`** – Poisson probability mappers used to draw match probability models.
*   **`status_detail.ts`** – Sync histories and deadline counters.
*   **`team_week.ts`** – FPL team of the week arrays.
*   **`proc_player.ts`** & **`proc_team.ts`** & **`t_expected.ts`** – Deep analytics outputs.

---

## 💾 FastAPI & Redis Two-DB Keyspace Specifications

The platform is designed to query from a Python FastAPI backend which streams data straight from two separated, high-velocity Redis databases. The UI typings in `/src/data/types.ts` are strictly modeled after this architecture:

### 🟢 DB 0: RAW DATA KEYSPACE (Ingested from Producers)
*   **`player:<id>`** – Hash of GKP/DEF/MID/FWD profile, cost, team ID, status.
*   **`player:<id>:meta`** – Market details (Selected %, Transfers In/Out, injury news).
*   **`player:<id>:season:<year>`** – Historical totals (Minutes, goals, assists, xG, xA).
*   **`player:<id>:gw:<gw>`** – Historical gameweek raw performance.
*   **`player:<id>:fixture:<fixture_id>`** – Fixture detailed performance.
*   **`team:<id>`** – Name, short code, raw home/away strength attributes.
*   **`team:<id>:expected`** – Team expected underlying statistics (xG, xGA, xPts).
*   **`team:<id>:form`** – Form arrays (L5, goals scored/conceded).
*   **`fixture:<id>`** – Basic fixture metadata (Home/Away IDs, kickoff, final score).
*   **`fixture:<id>:stats`** – Match statistics (Shots, xG, possession ratios).
*   **`gw:<gw>`** – Deadline timers, highest scoring metrics.
*   **`system:state`** – Current operational gameweek, active season, and sync logs.

### 🔵 DB 1: PROCESSED DATA KEYSPACE (Generated by Consumer/Cooker)
*   **`proc_player:<id>:xp`** – Simulated Expected Points (xPts) for this and future gameweeks, minute probabilities, captaincy weights, and clean sheet probabilities.
*   **`proc_team:<id>:strength`** – Compiled attacking/defending expected coefficients.
*   **`proc_fixture:<id>:poisson`** – Goal distribution Poisson weights (0, 1, 2, 3).
*   **`proc_fixture:<id>:scoreline`** – Simulated scoreline matrix probabilities.
*   **`proc_gw:<gw>:team_of_week`** – High-xPts Dream Team player coordinates.
*   **`proc:index:players`** – Sorted set indexing players based on performance score.

---

## 🛠️ Technological Stack & Dependencies

The FPL Oracle is modeled using cutting-edge, high-efficiency system layers:

1.  **Vite 6** – Fast, module-replacement bundler.
2.  **React 19** – Incorporates functional hooks, declarative DOM configurations, and strict-mode isolation.
3.  **Tailwind CSS v4** – Modern styling using compiled native CSS variables.
4.  **Motion React** – Fluid animations and layout state animations.
5.  **Recharts** – Renders interactive, highly customized radar and bar charts.
6.  **Lucide React** – Comprehensive catalog of sleek visual vector icons.

---

## 💻 Requirements to Run Locally

Before beginning deployment, ensure your local development system satisfies these requirements:
*   **Node.js**: `v18.0.0` or newer (Long Term Support/LTS recommended).
*   **npm**: `v9.0.0` or newer.
*   **Browser**: Modern evergreen browser (Chrome, Edge, Firefox, Safari) with hardware acceleration enabled for smooth canvas/animations.

---

## 🚀 Step-by-Step Process to Run Locally

If you have exported this FPL Oracle code build as a `.zip` archive or downloaded it into a Git repository, execute these steps to launch it locally:

### 1️⃣ Extract and Open Project Directory
Unzip the downloaded archive and open a terminal/command prompt window in the unzipped folder:
```bash
cd fpl-oracle-dashboard
```

### 2️⃣ Install Required Node Dependencies
Download all referenced external library dependencies by running:
```bash
npm install
```
*This installs Vite, React, Tailwind, Recharts, Motion, and Lucide into your workspace's `node_modules` directory.*

### 3️⃣ Start the Development Server
Initiate the interactive dev server:
```bash
npm run dev
```

By default, the `package.json` configurations bind server deployment to:
*   **Port**: `3000`
*   **Host**: `0.0.0.0` (accessible from any client device on your network)

Once running, you can access the application through your browser at:
```text
http://localhost:3000
```

### 4️⃣ Build the Project for Production (Optional)
If you want to package compile optimized static files of this project for deployment to web hosts (like Vercel, Netlify, Cloudflare Pages, or GitHub Pages), build your production build using:
```bash
npm run build
```
*This transpiles, tree-shakes, and compresses target scripts into a standalone, statically deliverable folder named `dist/`.*

### 5️⃣ Preview the Production Build Locally (Optional)
Test the compiled production bundle locally to guarantee absolute layout compliance and page load speeds:
```bash
npm run preview
```
This serves the output in the `dist/` folder on a static local server.

---

*Compiled and verified for FPL managers by **Naresh Koirala**.*

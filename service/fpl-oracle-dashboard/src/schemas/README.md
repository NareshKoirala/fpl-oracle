# FPL-Oracle Prediction Center Schema Reference

This directory serves as the technical reference for your Python/FastAPI backend and any database models you construct. To ensure perfect compatibility with the React prediction engine, your live API endpoints should return data conforming to these structural contracts.

---

## Model Index & Descriptions

### 1. Fixture Model
Represents a predictive simulation for a matchup between two teams during a specific gameweek.
- **Key Features**: Model prediction probabilities (win/draw/loss), home/away xG forecasts, and exact-score probabilities.
- **TypeScript Reference**: `Fixture`

### 2. Player Model
Tracks all relevant on-field statistics, cost parameters, and advanced underlying metrics (e.g. xG, xA, ict_index) for individual players.
- **Key Features**: Interactive filtering by team, position (element_type), search strings, and sorting parameters.
- **TypeScript Reference**: `Player`

### 3. TeamRaw Model
Represents the comprehensive regular-season league stats for a team. Used in rendering the Standing Tables and analyzing current form.
- **Key Features**: xG, xGA, xPoints, big chances created vs conceded, possession trackers, and historical game results list.
- **TypeScript Reference**: `TeamRaw`

### 4. TeamStrength Model
Represents advanced machine-learning strength indexes for attacking and defensive attributes (further split into home vs away capabilities).
- **Key Features**: Real vs Expected attack/defense indices, expected points per game, and last 5 games form.
- **TypeScript Reference**: `TeamStrength`

### 5. TeamWeek (Team of the Week) Model
Represents the optimized dream lineup for a given gameweek calculated using predicting algorithms.
- **Key Features**: Captaincy status, player prices, coordinates, actual points, and projected points.
- **TypeScript Reference**: `TeamWeek`

### 6. PlayerProcMetrics Model
Represents the fixture-specific predictive projections and processed metrics for individual players based on live form and model calculation.
- **Key Features**: Fixture-specific xPts projections, parsed xG, xA, clean sheet projections, and selected bias.
- **TypeScript Reference**: `PlayerProcMetrics`

### 7. TeamProcMetrics Model
Holds processed, underlying baseline squad values comparing on-paper superior expected values alongside actual metrics and variances.
- **Key Features**: Multi-dimensional splits (home/away, last 5, expected ratings, actual ratings, delta variances).
- **TypeScript Reference**: `TeamProcMetrics`

---

## Complete JSON Sample Snippets

Review the individual JSON files in this directory for detailed, copy-pasteable database models:
- [Fixture Sample](./Fixture.json)
- [Player Sample](./Player.json)
- [PlayerProcMetrics Sample](./PlayerProcMetrics.json)
- [TeamRaw Sample](./TeamRaw.json)
- [TeamStrength Sample](./TeamStrength.json)
- [TeamProcMetrics Sample](./TeamProcMetrics.json)
- [TeamWeek Sample](./TeamWeek.json)

# Frontend Spec Document

## 1. Tech Stack Overview
The FPL-Oracle frontend (Dashboard) is a modern, responsive web application designed for high performance and aesthetic data visualization.
- **Framework:** React 19
- **Build Tool:** Vite
- **Language:** TypeScript
- **Styling:** Tailwind CSS (v4)
- **Icons:** `lucide-react`
- **Charting/Data Vis:** `recharts`
- **Animations:** `motion` (Framer Motion)

## 2. Directory Structure
Located in `service/dashboard/src/`:
- `components/` - Reusable UI widgets (cards, buttons, tables).
- `data/` & `dummy-data/` - Static data stores or mock data for UI testing.
- `lib/` - Utility functions, API wrappers, and constants.
- `schemas/` - TypeScript interfaces and Zod/validation schemas aligning with the backend Python structures.
- `App.tsx` & `main.tsx` - Application entry points and routing structure.

## 3. UI/UX Principles
- **Modern Aesthetics:** Implement a dynamic interface utilizing glassmorphism, dark modes, and harmonious color palettes to create a premium feel.
- **Interactive Elements:** Use micro-animations (via `motion`) for hover states, loading transitions, and layout changes.
- **Data Heavy, Clean Layout:** Because FPL data is dense, use data grids, spider charts (via `recharts`), and collapsible menus to maintain a clean aesthetic without overwhelming the user.

## 4. Key Pages / Views
1. **Overview Dashboard:** High-level summary of upcoming Gameweeks, system status, and top trending players.
2. **Player Analytics:** Detailed breakdown of a specific player's Expected Points (xP) formula (minutes, form, fixture difficulty).
3. **Best XI / Squad Optimizer:** Visual representation of the recommended starting 11 on a football pitch graphic. Includes captain/vice-captain suggestions.
4. **Fixture Difficulty Ranker:** Interactive list of teams ranked by upcoming fixture difficulty.

## 5. API Integration
The frontend interfaces with the `Waiter` FastAPI service. Standard fetch or React Query patterns should be utilized for fetching real-time Redis data from endpoints like `/fixtures`, `/team`, and `/history`.

# EquiNexa AI

EquiNexa AI is an AI-driven stock market intelligence and prediction platform. It combines deterministic technical indicators, candlestick pattern recognition, and LLM-powered RAG (Retrieval-Augmented Generation) sentiment analysis into a cohesive quantitative pipeline.

**Important Disclaimer:** This project is for **informational and research purposes only**. It does not constitute personalized financial advice or a recommendation to buy, sell, or hold any financial instrument. The outputs are experimental and should not be used as the sole basis for automated trading or capital allocation.

## Status: Ongoing Prospective Evaluation
*   **Model Version:** `1.0.0` (FROZEN)
*   **Performance Claims:** Unverified. 
*   **Evaluation Status:** The prospective evaluation gate is currently **LOCKED**. The system is accumulating live real-world observations against a strict threshold (Required N = 100). No performance claims (such as historical backtest benchmarks) are established or endorsed until validated out-of-sample by the live prospective ledger.

## Features and Architecture
*   **Technical Baseline:** A scikit-learn based machine learning pipeline leveraging normalized technical indicators.
*   **Retrieval-Augmented Generation (RAG):** Extracts and maps financial news sentiment to ticker-specific confidence scores using LLMs.
*   **Pattern Engines:** Deterministic pattern recognition logic for Candlesticks and Chart Geometry.
*   **Immutable Prospective Ledger:** Ensures forward-tested predictions cannot be retroactively modified or subjected to lookahead bias.
*   **FastAPI Backend:** Secure, read-only REST endpoints that expose the current research and model statuses.
*   **React/Vite Frontend:** A responsive dashboard for data visualization.

## Technology Stack
*   **Backend:** Python 3.12+, FastAPI, Pytest, Pandas, Scikit-learn, OpenAI SDK, ChromaDB, Sentence-Transformers.
*   **Frontend:** Node.js 20+, React, Vite, TailwindCSS (v4), Recharts.

## Repository Structure
*   `backend/` - Core Python application, containing models, technical engines, RAG pipelines, API routes, and testing.
*   `frontend/` - React and Vite-based dashboard.
*   `docs/` - System architecture, provider verifications, audit logs, and model cards.
*   `tests/` - The comprehensive test suite verifying leakage barriers and ML targets.
*   `.github/workflows/` - CI/CD pipeline configuration.

## Local Setup and Run Instructions

### 1. Environment Variable Setup
Copy the example environment file and configure any necessary API credentials (do NOT commit your `.env` file):
```bash
cp .env.example .env
```

### 2. Backend (FastAPI)
It is recommended to use a virtual environment.
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Start the server (Requires uvicorn, can be run from the backend directory)
python -m uvicorn app.api.main:app --reload
```

### 3. Frontend (React/Vite)
```bash
cd frontend
npm ci
npm run dev
```

## Testing

**Backend Tests:**
EquiNexa AI enforces a stringent test suite covering data leakage, model target calculation, and prospective integrity.
```bash
# From the project root
pytest
```

**Frontend Tests:**
```bash
cd frontend
npx vitest run
```

## CI Workflow Description
The repository utilizes GitHub Actions (`.github/workflows/ci.yml`) to enforce build integrity on every push to `main` and Pull Requests. The CI is completely **offline** (no live API or market data fetching) and handles:
*   Python dependency installation and `pytest` execution.
*   Generation of a `pip-licenses` inventory artifact.
*   Node.js dependency installation, `oxlint` linting, Vite build generation, and `vitest` execution.

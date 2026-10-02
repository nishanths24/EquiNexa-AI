# Continuous Integration (CI) Runbook

## Overview
EquiNexa AI uses GitHub Actions for continuous integration. The CI pipeline ensures that the core functionalities remain intact, leakage barriers are unbreached, and no regressions are introduced during development.

The CI workflow (`.github/workflows/ci.yml`) triggers on pushes and pull requests to the `main` branch.

## Workflow Behavior

The workflow is strictly **offline**. It explicitly avoids live API calls (e.g., OpenAI, live market data endpoints) and does not interact with the frozen prospective ledger or any external databases. 

### Jobs:
1.  **Backend Pytest and Licensing**:
    *   Sets up Python 3.12.
    *   Installs dependencies from `backend/requirements.txt`.
    *   Uses `pip-licenses` to generate a markdown inventory of all installed dependencies.
    *   Uploads the generated `licenses.md` file as a GitHub Actions artifact. 
    *   Executes the `pytest` suite covering backend models, retrieval isolation, metrics, evaluation loops, and documentation tests.
2.  **Frontend Vitest and Build**:
    *   Sets up Node.js 20.
    *   Uses `npm ci` referencing `frontend/package-lock.json` for deterministic installation.
    *   Runs the `oxlint` linter (`npm run lint`).
    *   Verifies the production build (`npm run build`).
    *   Runs frontend tests (`npx vitest run`).

## Local Reproduction Commands

To replicate the CI checks on your local machine, ensure you are in the repository root and execute the following:

**Backend Tests & Licenses:**
```bash
# Ensure your virtual environment is active and dependencies are installed
pip install -r backend/requirements.txt
pip install pip-licenses

# Run tests
pytest

# Generate License Report
pip-licenses --format=markdown > docs/licenses.md
```

**Frontend Tests & Build:**
```bash
cd frontend
npm ci
npm run lint
npm run build
npx vitest run
```

## License Report Limitations

The generated `docs/licenses.md` (and the corresponding CI artifact) acts as an inventory snapshot at the time of the build. 
*   **Not Legal Advice:** Generating an inventory automatically does not inherently establish license compliance or resolve complex dual-licensing scenarios. 
*   **Third-party Data:** This inventory only tracks Python packages. Licenses and usage constraints relating to APIs (OpenAI, yfinance) and market data consumption must still be reviewed manually (see `docs/provider_verification.md`).

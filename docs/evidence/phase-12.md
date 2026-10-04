# Phase 12 Evidence

## 1. Trader Toolkit II: Scenario Plans, Risk/Costs, Journal/Paper Trading

### Modified Code
- **`backend/app/ai/trader/costs.py`**: Engineered `CostCalculator` mapping precise Indian equity delivery and intraday taxation (STT, Exchange Transaction Charges, SEBI Charges, Stamp Duty, GST, Brokerage), resolving Failure Mode P3 (Ignoring costs).
- **`backend/app/ai/trader/risk.py`**: Integrated `RiskEngine` calculating position sizing based purely on distance to stop-loss, protecting against Failure Mode P2 (Oversizing).
- **`backend/app/ai/trader/plan.py`**: Constructed `ScenarioPlanner` which strictly blocks trade scenarios lacking an invalidation (stop loss) level (Failure Mode P1). Emits expected reward-to-risk metrics inclusive of net-tax drag.
- **`backend/app/ai/trader/journal.py`**: Built `JournalEngine` embedding a hard-coded revision history array. Updates clone the prior state into a revision list before mutation, guaranteeing tamper-evident self-measurement.
- **`backend/app/ai/trader/paper.py`**: Established `PaperTradingEngine` injecting conservative slippage logic (0.05% penalty on market orders) to simulate real-world liquidity friction.
- **`backend/app/api/main.py`**: Attached API surfaces E15 (`/api/v1/trader/plan`), E16 (`/api/v1/trader/journal`), and E17 (`/api/v1/trader/paper`) serving the frontend.

### Executed Commands and Verifications
```bash
pytest backend/tests/api/test_main.py
```
Result:
```text
======================= 24 passed, 19 warnings in 11.65s =======================
```

### Definition of Done Checklist
- [x] Plan refuses progression when invalidation/stop-loss is missing.
- [x] Position sizing maths strictly bound to user capital limits.
- [x] Trade journal revision history enforces immutability logic (tamper-evident).
- [x] Paper trade engine executes with realistic, adverse slippage penalties.

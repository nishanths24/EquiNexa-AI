# Risk Engine

## Role
The Risk Engine computes explicit position sizing and invalidation thresholds based on the AI Setup scenarios. It sits between the AI Setup Generation and the final user response, ensuring that impossible or excessively risky trades are caught by the guardrails.

## Computations
- `stop_distance` = absolute difference between entry and stop loss.
- `risk_reward` = Target distance / stop distance.
- `position_size` = strictly capped by `account_size * max_portfolio_risk_pct`.

## Guardrails
- Automatically rejects setups where the stop loss is on the wrong side of the entry zone.
- Automatically rejects trades with a zero or negative risk-reward ratio.

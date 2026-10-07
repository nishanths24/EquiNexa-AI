# Prediction Engine

## Walk-Forward Validation
The engine exclusively uses walk-forward validation. Random shuffling of time-series data is strictly prohibited to prevent data leakage.

## Leakage Tests
Automated tests (`test_v2_leakage.py`) run in CI to ensure that the prediction output at time `T` does not change when future data (time > `T`) is mutated.

## Ledger V2
A completely isolated `ai_predictions_v2` and `ai_prediction_outcomes` schema ensures the V1 ledger remains an immutable, frozen historical record. No joins or mutations against V1 tables are permitted.

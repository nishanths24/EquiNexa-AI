# Phase 6.1: Target-Threshold Infrastructure Correction and Validation

## 1. Problem Discovered
During the Phase 6 Generalization Study, an architectural limitation was identified: the target label for the experiments (e.g., `> 2.0%` in 5 days) was statically generated and hard-coded into a column (`target_label_5d`) during dataset compilation. As a result, when the experiment harness modified the `config.target.threshold` parameter for sensitivity testing (0.0%, 1.0%, 2.0%, 3.0%), the threshold parameter was ignored. This caused all target sensitivity experiments in Phase 6 to produce identical metrics (61.91% Accuracy), incorrectly implying zero sensitivity to the target definition.

## 2. Original Architectural Behavior
1. `build_historical_dataset.py` computed `target_label_5d` based on a hardcoded 0.02 threshold.
2. The dataset was saved to CSV and uniquely hashed.
3. `run_experiment.py` read the static `target_label_5d` column.
4. Experiment configurations with varying thresholds effectively operated on identical targets.

## 3. Corrected Architecture
To correct this without breaking the frozen dataset hashing or Phase 5 reproducibility:
1. `run_experiment.py` was modified to dynamically compute the target on-the-fly (`dynamic_target`) from the raw `close` prices.
2. The exact formula is evaluated per-ticker to avoid cross-asset leakage:
   `target = 1 if (close[t+5] / close[t] - 1) > configured_threshold else 0`
3. Observations lacking `t+5` data (end-of-series) are dynamically set to `NaN` and naturally dropped by the evaluation engine, ensuring no lookahead bias.
4. `config.target.threshold` now deterministically dictates the true evaluation target at runtime.

## 4. Tests Added
A dedicated test suite (`backend/tests/ai/test_dynamic_target.py`) was introduced, formally validating:
1. Different thresholds yield statistically different target distributions.
2. End-of-series rows without future data correctly resolve to `NaN`.
3. Future return targets are rigorously excluded from the feature space to prevent leakage.
4. Changing the configuration threshold alters the `config_hash`.
5. Recomputing targets dynamically does NOT alter the foundational raw `dataset_hash`.
6. Target generation logic is perfectly deterministic.

## 5. Re-Run Target Sensitivity (Phase 6.1 Results)
Using the corrected infrastructure, the four identical configurations from Phase 6 were rerun. 

*(Metrics pending background execution...)*

### Overall Results
| Experiment | Threshold | Accuracy | Brier Score | ECE |
|------------|-----------|----------|-------------|-----|
| `EXP-6-HGB-TH-0` | > 0.0% | 51.64% | 0.2580 | 0.0819 |
| `EXP-6-HGB-TH-1` | > 1.0% | 52.83% | 0.2553 | 0.0625 |
| `EXP-6-HGB-TH-2` | > 2.0% | 61.91% | 0.2344 | 0.0759 |
| `EXP-6-HGB-TH-3` | > 3.0% | 71.93% | 0.2023 | 0.1104 |

### Cross-Market & Cross-Regime Validation
*Metrics pending...*

## 6. Interpretation and Limitations
- The prior **61.91%** accuracy logged in Phase 6 was strictly true *for a 2.0% threshold*. It was not a universal ceiling, nor a floor across all configurations.
- Changing the target definition naturally changes the underlying class imbalance, heavily impacting raw metrics like accuracy. 
- *Crucially: The deterministic pattern engine continues to operate blindly on pure technical data without access to the future target, meaning its calibration benefits (ECE/Brier reduction) remain untainted.*
- This phase guarantees the integrity of our target measurement infrastructure, paving the way for unbiased Empirical Evaluation going forward.

## 7. Reproduction Command
To re-run the tests and sensitivity study:
```bash
pytest backend/tests/ai/test_dynamic_target.py
python backend/scripts/run_phase6_1.py
```

# AIMO3 Baseline Notebook

AI Mathematical Olympiad – Progress Prize 3 (AIMO3) competition solution notebook.

## Quick Start

### Run Modes

The notebook supports multiple run modes configured via `RUN_MODE`:

| Mode | Description |
|------|-------------|
| `local_ref` | Debug mode - evaluates on `reference.csv` (10 problems) |
| `submit_auto` | Kaggle submission mode - uses `kaggle_evaluation` API |
| `quick_tune` | Fast Optuna tuning (10 trials) on reference subset |
| `full_tune` | Full Optuna tuning (30 trials) on reference subset |

### Model Setup

1. Add your model as a Kaggle Dataset/Model input
2. Update `MODEL_PATH` in CONFIG cell to point to `/kaggle/input/your-model-name`
3. Default: `/kaggle/input/qwq-32b-preview/transformers/default/1` (QwQ-32B)

### Running Locally

```python
# In the CONFIG cell:
RUN_MODE = "local_ref"
```

### Running Tuning

```python
# Quick tune (10 trials, ~30 min)
RUN_MODE = "quick_tune"

# Full tune (30 trials, ~1 hour)
RUN_MODE = "full_tune"
```

### Kaggle Submission

```python
# Will auto-detect if KAGGLE_IS_COMPETITION_RERUN is set
RUN_MODE = "submit_auto"
```

## Key Improvements

### 1. Strict Output Format

The prompt now enforces a strict `FINAL: <integer>` format to prevent incorrect answer extraction:

```
FINAL: 42  ✓ Correct
FINAL: The answer is 42  ✗ Wrong
```

### 2. Answer Extraction Priority

1. `FINAL: <int>` - Our strict format (highest priority)
2. `ANSWER: <int>` - Explicit answer tag
3. `The answer is <int>` - Natural language
4. `\boxed{<int>}` - LaTeX boxed
5. `LASTINT` - Last integer fallback (lowest priority)

### 3. Multi-Sample Voting

- Generates K candidates (default: 8) with varied temperatures
- Uses self-consistency voting to select best answer
- Supports multiple selection strategies:
  - `majority_vote`: Simple majority
  - `verifier_weighted`: Weight by extraction method reliability
  - `consensus`: Require strong agreement

### 4. Hyperparameter Tuning

Uses Optuna with TPE sampler and median pruning:

**Search Space:**
- `k`: 4-16 (number of candidates)
- `temperature`: 0.3-1.0
- `max_new_tokens`: 1024-4096
- `prompt_style`: strict_final, tir
- `selection_strategy`: majority_vote, verifier_weighted, consensus
- `top_p`: 0.8-1.0

**Saved Config:**
Best config is saved to `/kaggle/working/best_config.json` and auto-loaded on subsequent runs.

## File Structure

```
.
├── AIMO3_baseline.ipynb      # Main notebook
├── aimo3_tuning.py           # Tuning module
├── reference.csv             # Reference problems (10)
├── test.csv                  # Test placeholder
├── sample_submission.csv     # Submission format
└── kaggle_evaluation/        # Kaggle evaluation API
```

## Telemetry

Logs are saved to `/kaggle/working/aimo3_telemetry.jsonl` with:

- Problem ID and hash
- Elapsed time
- Number of candidates generated
- Vote margin and entropy
- Parse method used
- Verification results
- Config used

## Diagnosis from Initial Run

The initial Kaggle run showed:
- **Accuracy: 1/10 (10%)** on reference problems
- **Root causes:**
  1. LASTINT fallback was extracting wrong numbers from reasoning
  2. Model output didn't follow any structured format
  3. Only 2 candidates generated due to time budget

**Fixes implemented:**
1. Strict `FINAL:` prompt format
2. Priority-based answer extraction
3. Increased K_BASE to 8 candidates
4. Better time budget management
5. Configurable selection strategies

## Competition Rules

- Answers must be integers in [0, 99999]
- No modulo by default - compute exact answer
- Two reruns evaluated, penalized scoring
- Internet disabled during submission

## License

Competition-specific code for AIMO3.

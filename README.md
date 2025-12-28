# AMOP - AI Mathematical Olympiad Progress Prize 3

This repository contains resources and code for the [AI Mathematical Olympiad - Progress Prize 3 (AIMO3)](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3) Kaggle competition.

## 🏆 Competition Overview

### Objective
Build an AI algorithm/model (open-source/open-weight at runtime) that can solve Mathematical Olympiad problems written in LaTeX and return integer answers.

### Key Features
- **Problem Format**: Mathematical Olympiad problems written in LaTeX
- **Answer Format**: Integer answers in the range [0, 99999]
- **No Default Modulo**: If modulo operation is needed, the problem statement will explicitly specify it (e.g., "remainder when ... divided by ...")
- **Submission Type**: Code Competition (Notebook submission using Python evaluation API)

## 📁 Repository Structure

```
AMOP/
├── reference.csv                    # 10 reference problems with answers for benchmarking
├── AIMO3_Reference_Problems.pdf     # Full solutions for the 10 reference problems
├── test.csv                         # Placeholder file for code schema (NOT actual test data)
├── sample_submission.csv            # Example submission format (id, answer)
└── kaggle_evaluation/               # Python evaluation API (proto/grpc) for serving problems
    ├── __init__.py
    ├── aimo_3_gateway.py           # Gateway for serving problems one-by-one
    ├── aimo_3_inference_server.py  # Base class for inference server
    └── core/                        # Core evaluation framework
```

### File Descriptions

| File | Purpose | Description |
|------|---------|-------------|
| `reference.csv` | Benchmarking | Contains 10 reference problems with answers to test your solution locally |
| `AIMO3_Reference_Problems.pdf` | Solutions | Full detailed solutions for all 10 reference problems |
| `test.csv` | Placeholder | Example schema only - NOT the actual test data used in competition |
| `sample_submission.csv` | Format Reference | Shows the required submission format: `id,answer` |
| `kaggle_evaluation/` | Evaluation API | Python API using proto/grpc to serve problems one at a time |

## 📊 Test Sets

The competition uses two separate test sets:

| Set | Size | When Used | Order |
|-----|------|-----------|-------|
| **Public** | 50 problems | During competition | Random order |
| **Private** | 50 problems (different) | After deadline | Fixed random order (anti-probe) |

## ⚙️ Submission Requirements

### Format
1. **Notebook submission** is required
2. Must use the **Python evaluation API** (`kaggle_evaluation`)
3. Cannot read test data directly from files
4. Problems are served **one-by-one** via the API
5. Return integer answer in range [0, 99999]

### Environment Constraints
- **Internet disabled** during notebook execution
- **Runtime limits**:
  - CPU notebooks: ≤ 9 hours
  - GPU notebooks: ≤ 5 hours

### Implementation
To participate, you need to:
1. Inherit from `AIMO3InferenceServer` class
2. Implement the `predict()` method that:
   - Takes a problem statement (LaTeX string) as input
   - Returns an integer answer in [0, 99999]

## 📈 Scoring System

### During Competition
- Notebook runs on **50 public test problems**
- Score displayed as number of correct answers

### Final Evaluation (Penalized Accuracy)
After the deadline, your notebook is **rerun twice** on the **50 private test problems**.

**Scoring per problem:**
| Result on 2 Runs | Score |
|------------------|-------|
| Correct both times | **1.0 point** |
| Correct 1 out of 2 times | **0.5 points** |
| Incorrect both times | **0.0 points** |

**Maximum total score: 50 points**

## 🎯 Problem Examples

The reference.csv file contains 10 challenging problems covering:
- **Geometry**: Triangle properties, circle intersections
- **Number Theory**: Modular arithmetic, divisibility
- **Combinatorics**: Tournament rankings, counting problems
- **Algebra**: Functional equations
- **Advanced Topics**: Fibonacci sequences, recursive functions

Example problem difficulty: International Mathematical Olympiad (IMO) level

## 🚀 Getting Started

### 1. Explore Reference Problems
```python
import pandas as pd

# Load reference problems
ref_df = pd.read_csv('reference.csv')
print(f"Number of reference problems: {len(ref_df)}")

# View first problem
print(ref_df.iloc[0]['problem'])
print(f"Answer: {ref_df.iloc[0]['answer']}")
```

### 2. Test with Sample Data
```python
# Load test schema
test_df = pd.read_csv('test.csv')
print(test_df.head())

# Load sample submission format
sample_sub = pd.read_csv('sample_submission.csv')
print(sample_sub.head())
```

### 3. Implement Your Solution
Create a notebook that:
1. Imports the evaluation API
2. Implements a prediction function
3. Processes problems one at a time
4. Returns integer answers

## 📚 Resources

- **Competition Page**: [Kaggle - AIMO3](https://www.kaggle.com/competitions/ai-mathematical-olympiad-progress-prize-3)
- **Reference Solutions**: See `AIMO3_Reference_Problems.pdf` for detailed solutions
- **Evaluation API Documentation**: See `kaggle_evaluation/` directory

## 🔧 Development Tips

1. **Start with reference problems**: Test your approach on the 10 reference problems before submitting
2. **Understand the constraints**: Remember answers must be integers in [0, 99999]
3. **Check for modulo operations**: Read problem statements carefully for modulo requirements
4. **Optimize for runtime**: You have 5-9 hours, but efficient solutions perform better
5. **Handle LaTeX parsing**: Problems are in LaTeX format, ensure proper parsing
6. **Test locally first**: Use the reference problems to validate your approach

## 📝 Notes

- This is a **Code Competition** - your notebook code is what gets evaluated, not pre-computed results
- The evaluation API serves problems in **random order** during public testing
- Private test uses **fixed random order** to prevent probing strategies
- Solutions must use **open-source/open-weight** models at runtime (per competition rules)

## 🤝 Contributing

This repository is for competition purposes. Feel free to:
- Share insights about reference problems
- Improve documentation
- Add utility functions for problem parsing or solving

## 📄 License

Competition data and evaluation code are provided by Kaggle under their competition terms.

---

**Good luck solving challenging Mathematical Olympiad problems with AI! 🎓🤖**

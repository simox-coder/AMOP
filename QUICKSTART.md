# Quick Start Guide - AIMO3 Competition

This guide will help you get started with the AIMO3 competition quickly.

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Explore Reference Problems

Run the analysis script to understand the problem set:

```bash
python analyze_reference.py
```

This will show you:
- Problem length statistics
- Answer distributions
- Problem categorization by topic
- Which problems use modulo operations
- Preview of each problem

### 3. Read Problem Solutions

Open `AIMO3_Reference_Problems.pdf` to see detailed solutions for all 10 reference problems.

## 📝 Development Workflow

### Step 1: Understand a Problem

```python
import pandas as pd

# Load reference problems
df = pd.read_csv('reference.csv')

# Look at first problem
print(df.iloc[0]['problem'])
print(f"Answer: {df.iloc[0]['answer']}")
```

### Step 2: Implement Your Solution

Edit `baseline_solution.py` and implement the `predict()` method:

```python
def predict(self, problem: str) -> int:
    # Your solution logic here
    # 1. Parse the LaTeX problem text
    # 2. Apply mathematical reasoning
    # 3. Compute the answer
    # 4. Return integer in [0, 99999]
    
    answer = your_solve_function(problem)
    return max(0, min(99999, answer))
```

### Step 3: Test Locally

```bash
python baseline_solution.py
```

This will:
- Test your solution on all 10 reference problems
- Show which answers are correct
- Display your accuracy score

### Step 4: Iterate and Improve

1. Check which problems your solution gets wrong
2. Read the detailed solutions in the PDF
3. Improve your implementation
4. Test again

## 🎯 Solution Approaches

### Approach 1: Rule-Based + Symbolic Math

```python
import sympy
from sympy.parsing.latex import parse_latex

def predict(self, problem: str) -> int:
    # Parse LaTeX expressions
    # Use SymPy for symbolic computation
    # Apply mathematical rules
    pass
```

**Pros:** Precise, deterministic
**Cons:** Hard to handle complex word problems

### Approach 2: Large Language Models

```python
def predict(self, problem: str) -> int:
    # Use an LLM to reason about the problem
    # Extract the answer from the response
    # Verify with computational tools
    pass
```

**Pros:** Can handle complex reasoning
**Cons:** May be slow, less precise

### Approach 3: Hybrid Approach (Recommended)

```python
def predict(self, problem: str) -> int:
    # 1. Use LLM to understand the problem
    # 2. Use LLM to generate solution steps
    # 3. Use symbolic math to verify/compute
    # 4. Return verified answer
    pass
```

**Pros:** Combines reasoning and precision
**Cons:** More complex to implement

## 📊 Reference Problem Topics

Based on the analysis:

1. **Problem 1**: Geometry (triangle, circles) + modulo
2. **Problem 2**: Number theory (divisibility, powers of 2)
3. **Problem 3**: Combinatorics (tournament rankings)
4. **Problem 4**: Number theory (base representation)
5. **Problem 5**: Complex geometry + Fibonacci sequences
6. **Problem 6**: Number theory (divisors, "n-Norwegian")
7. **Problem 7**: Algebra (equations with integers)
8. **Problem 8**: Functional equations
9. **Problem 9**: Geometry + combinatorics (tiling)
10. **Problem 10**: Function theory (shifty functions)

## ⚠️ Important Notes

### Answer Range
- All answers must be integers in `[0, 99999]`
- Clamp your answer: `max(0, min(99999, answer))`

### Modulo Operations
7 out of 10 reference problems explicitly require modulo:
- "remainder when ... divided by $10^5$"
- "remainder when ... divided by $99991$"

Make sure to apply the correct modulo operation!

### LaTeX Parsing
Problems are in LaTeX format. Common patterns:
- `$...$` for inline math
- `\begin{equation*}...\end{equation*}` for equations
- `\colon`, `\to`, `\geq`, `\leq` for symbols
- `\left\lfloor...\right\rfloor` for floor function
- `\sum`, `\prod` for summations and products

## 🔧 Debugging Tips

### Problem: Solution is too slow

```python
# Add timing
import time

def predict(self, problem: str) -> int:
    start = time.time()
    answer = your_solution(problem)
    elapsed = time.time() - start
    print(f"Time: {elapsed:.2f}s")
    return answer
```

### Problem: Wrong answer on reference problems

1. Print intermediate steps
2. Compare with the PDF solution
3. Check for modulo operations
4. Verify LaTeX parsing

### Problem: Can't parse LaTeX

```python
# Use regex to extract key information
import re

# Extract numbers
numbers = re.findall(r'\d+', problem)

# Extract variables
variables = re.findall(r'\$([a-zA-Z])\$', problem)

# Extract equations
equations = re.findall(r'\$(.+?)\$', problem)
```

## 📦 Kaggle Submission

### Prepare Your Notebook

1. Copy your implementation to a Kaggle notebook
2. Import the evaluation API:
   ```python
   import sys
   sys.path.append('/kaggle/input/ai-mathematical-olympiad-progress-prize-3/kaggle_evaluation')
   from aimo_3_inference_server import AIMO3InferenceServer
   ```

3. Implement your inference server
4. Add the competition check:
   ```python
   if __name__ == '__main__':
       if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
           inference_server = MyInferenceServer()
           inference_server.serve()
   ```

### Test Before Submission

- Test on all 10 reference problems locally
- Ensure runtime is within limits (CPU: 9h, GPU: 5h)
- Verify answer format (integers in [0, 99999])

### Submit

1. Save your notebook
2. Click "Submit" to enter the competition
3. Your notebook will run on 50 public test problems
4. Check your score on the leaderboard

## 🎓 Learning Resources

1. **AIMO3_Reference_Problems.pdf** - Essential reading!
2. **IMO Problems** - Practice on past International Mathematical Olympiad problems
3. **SymPy Documentation** - For symbolic mathematics
4. **LaTeX Guide** - For parsing problem statements
5. **Competition Forum** - Discuss strategies with other participants

## ✅ Checklist Before First Submission

- [ ] Tested solution on all 10 reference problems
- [ ] Read the PDF solutions for understanding
- [ ] Implemented proper answer clamping [0, 99999]
- [ ] Verified modulo operations are correct
- [ ] Tested LaTeX parsing on all problem types
- [ ] Checked runtime is reasonable
- [ ] Code runs in Kaggle environment (no internet)
- [ ] Verified answer format (integer, not float or string)

## 🏆 Good Luck!

Remember:
- Start simple, then improve iteratively
- Focus on understanding the problems deeply
- Use the reference problems to validate your approach
- Read the PDF solutions - they contain valuable insights!

---

For questions or issues, check the competition forum or open an issue in this repository.

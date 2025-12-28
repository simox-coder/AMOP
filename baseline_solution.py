"""
Example Baseline Solution for AIMO3 Competition

This script demonstrates how to implement a basic inference server
that can be used with the Kaggle evaluation API.

NOTE: This is a placeholder/template. You need to implement actual
mathematical problem-solving logic in the predict() method.
"""

import sys
import os

# Add kaggle_evaluation to path
sys.path.append('/kaggle/input/ai-mathematical-olympiad-progress-prize-3/kaggle_evaluation')

from aimo_3_inference_server import AIMO3InferenceServer


class MyInferenceServer(AIMO3InferenceServer):
    """
    Custom inference server for AIMO3 competition.
    
    You need to implement the predict() method to solve mathematical problems.
    """
    
    def predict(self, problem: str) -> int:
        """
        Solve a mathematical problem and return an integer answer.
        
        Args:
            problem (str): A mathematical problem in LaTeX format
            
        Returns:
            int: The answer as an integer in range [0, 99999]
            
        Example problem format:
            "What is $1+1$?"
            "Let $ABC$ be a triangle with $AB=3$, $BC=4$, $AC=5$. 
             Find the area of triangle $ABC$."
        """
        # TODO: Implement your solution logic here
        # This is just a placeholder that returns 0 for all problems
        
        # Example: Parse the problem, apply mathematical reasoning, compute answer
        # You might want to:
        # 1. Parse LaTeX to extract mathematical expressions
        # 2. Use symbolic math libraries (sympy, etc.)
        # 3. Apply AI models (LLMs) for reasoning
        # 4. Use computational tools for verification
        
        # Placeholder implementation:
        answer = 0
        
        # Ensure answer is in valid range [0, 99999]
        answer = max(0, min(99999, answer))
        
        return answer


def test_on_reference_problems():
    """
    Test your solution on the reference problems locally.
    """
    import pandas as pd
    
    # Load reference problems
    ref_df = pd.read_csv('../reference.csv')
    
    # Create inference server instance
    server = MyInferenceServer()
    
    # Test on each reference problem
    correct = 0
    total = len(ref_df)
    
    print("Testing on reference problems...\n")
    print("=" * 80)
    
    for idx, row in ref_df.iterrows():
        problem_id = row['id']
        problem_text = row['problem']
        true_answer = row['answer']
        
        # Get prediction
        predicted_answer = server.predict(problem_text)
        
        # Check if correct
        is_correct = (predicted_answer == true_answer)
        if is_correct:
            correct += 1
        
        # Print result
        status = "✓" if is_correct else "✗"
        print(f"{status} Problem {idx + 1} (ID: {problem_id})")
        print(f"  Predicted: {predicted_answer}")
        print(f"  Actual:    {true_answer}")
        print()
    
    print("=" * 80)
    print(f"Score: {correct}/{total} ({100 * correct / total:.1f}%)")
    print("=" * 80)


if __name__ == '__main__':
    # Check if running in Kaggle environment
    if os.getenv('KAGGLE_IS_COMPETITION_RERUN'):
        # In competition: run the inference server
        inference_server = MyInferenceServer()
        inference_server.serve()
    else:
        # Local testing: evaluate on reference problems
        print("Running in local/test mode...")
        print("Testing solution on reference problems.\n")
        test_on_reference_problems()

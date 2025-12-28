"""
Analysis of AIMO3 Reference Problems

This script provides utilities to explore and analyze the 10 reference problems.
"""

import pandas as pd
import re


def load_reference_problems():
    """Load the reference problems from CSV."""
    return pd.read_csv('reference.csv')


def analyze_problem_lengths(df):
    """Analyze the length and complexity of problems."""
    print("=" * 80)
    print("PROBLEM LENGTH ANALYSIS")
    print("=" * 80)
    
    df['problem_length'] = df['problem'].str.len()
    
    print(f"\nTotal problems: {len(df)}")
    print(f"Average problem length: {df['problem_length'].mean():.1f} characters")
    print(f"Shortest problem: {df['problem_length'].min()} characters")
    print(f"Longest problem: {df['problem_length'].max()} characters")
    
    print("\nProblem lengths:")
    for idx, row in df.iterrows():
        print(f"  Problem {idx + 1}: {row['problem_length']:4d} chars (Answer: {row['answer']})")
    print()


def analyze_answer_distribution(df):
    """Analyze the distribution of answers."""
    print("=" * 80)
    print("ANSWER DISTRIBUTION ANALYSIS")
    print("=" * 80)
    
    answers = df['answer'].values
    
    print(f"\nAnswer statistics:")
    print(f"  Min answer: {answers.min()}")
    print(f"  Max answer: {answers.max()}")
    print(f"  Mean answer: {answers.mean():.1f}")
    print(f"  Median answer: {pd.Series(answers).median():.1f}")
    
    print(f"\nAnswer range check:")
    print(f"  All answers in [0, 99999]: {all(0 <= a <= 99999 for a in answers)}")
    
    print("\nAnswers by problem:")
    for idx, answer in enumerate(answers, 1):
        print(f"  Problem {idx}: {answer:6d}")
    print()


def extract_math_keywords(problem_text):
    """Extract mathematical keywords from problem text."""
    keywords = {
        'geometry': ['triangle', 'circle', 'angle', 'perpendicular', 'tangent', 'circumcircle', 'incircle'],
        'number_theory': ['divide', 'divisor', 'prime', 'modulo', 'remainder', 'integer'],
        'combinatorics': ['tournament', 'permutation', 'combination', 'count', 'ways'],
        'algebra': ['function', 'equation', 'polynomial', 'sum', 'product'],
        'sequence': ['fibonacci', 'sequence', 'recursive'],
    }
    
    found_categories = []
    text_lower = problem_text.lower()
    
    for category, words in keywords.items():
        if any(word in text_lower for word in words):
            found_categories.append(category)
    
    return found_categories if found_categories else ['other']


def categorize_problems(df):
    """Categorize problems by mathematical topic."""
    print("=" * 80)
    print("PROBLEM CATEGORIZATION")
    print("=" * 80)
    
    print("\nProblem categories based on keywords:")
    for idx, row in df.iterrows():
        problem_id = row['id']
        categories = extract_math_keywords(row['problem'])
        print(f"  Problem {idx + 1} (ID: {problem_id}): {', '.join(categories)}")
    print()


def show_problem_preview(df, max_chars=200):
    """Show a preview of each problem."""
    print("=" * 80)
    print("PROBLEM PREVIEWS")
    print("=" * 80)
    
    for idx, row in df.iterrows():
        problem_id = row['id']
        problem_text = row['problem']
        answer = row['answer']
        
        # Get preview
        preview = problem_text[:max_chars]
        if len(problem_text) > max_chars:
            preview += "..."
        
        print(f"\nProblem {idx + 1} (ID: {problem_id}) - Answer: {answer}")
        print("-" * 80)
        print(preview)
    print("\n" + "=" * 80)


def check_for_modulo_operations(df):
    """Check which problems explicitly mention modulo operations."""
    print("=" * 80)
    print("MODULO OPERATION ANALYSIS")
    print("=" * 80)
    
    modulo_keywords = ['remainder', 'modulo', 'mod ', 'divided by']
    
    print("\nProblems with explicit modulo operations:")
    found_modulo = False
    
    for idx, row in df.iterrows():
        problem_text = row['problem'].lower()
        has_modulo = any(keyword in problem_text for keyword in modulo_keywords)
        
        if has_modulo:
            found_modulo = True
            problem_id = row['id']
            print(f"  ✓ Problem {idx + 1} (ID: {problem_id})")
            # Extract the modulo context
            for keyword in modulo_keywords:
                if keyword in problem_text:
                    # Find context around keyword
                    pos = problem_text.find(keyword)
                    context_start = max(0, pos - 50)
                    context_end = min(len(problem_text), pos + 100)
                    context = problem_text[context_start:context_end]
                    print(f"    Context: ...{context}...")
                    break
    
    if not found_modulo:
        print("  No explicit modulo operations found in any problem.")
    
    print()


def main():
    """Run all analyses."""
    print("\n" + "=" * 80)
    print("AIMO3 REFERENCE PROBLEMS ANALYSIS")
    print("=" * 80 + "\n")
    
    # Load data
    df = load_reference_problems()
    
    # Run analyses
    analyze_problem_lengths(df)
    analyze_answer_distribution(df)
    categorize_problems(df)
    check_for_modulo_operations(df)
    show_problem_preview(df, max_chars=150)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nKey Insights:")
    print("  1. Problems vary significantly in length and complexity")
    print("  2. Answers range from small to large integers (within [0, 99999])")
    print("  3. Problems cover multiple mathematical domains")
    print("  4. Check individual problems for modulo operation requirements")
    print("\nNext steps:")
    print("  - Read AIMO3_Reference_Problems.pdf for detailed solutions")
    print("  - Implement solution logic in baseline_solution.py")
    print("  - Test locally before submitting to Kaggle")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()

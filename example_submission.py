"""
Example: Working with Test Data Format

This script demonstrates how to work with the test.csv and submission format.
"""

import pandas as pd


def load_test_data():
    """Load test data (placeholder in this case)."""
    return pd.read_csv('test.csv')


def create_sample_submission(test_df, answers=None):
    """
    Create a submission file with the correct format.
    
    Args:
        test_df: DataFrame with test problems
        answers: List of answers (default: all 0s)
    
    Returns:
        DataFrame with columns: id, answer
    """
    if answers is None:
        # Default to 0 for all problems
        answers = [0] * len(test_df)
    
    submission = pd.DataFrame({
        'id': test_df['id'],
        'answer': answers
    })
    
    return submission


def validate_submission(submission_df):
    """
    Validate that submission meets all requirements.
    
    Args:
        submission_df: DataFrame with submission data
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Check columns
    required_columns = ['id', 'answer']
    if not all(col in submission_df.columns for col in required_columns):
        print("❌ Missing required columns. Must have: id, answer")
        return False
    
    # Check for missing values
    if submission_df.isnull().any().any():
        print("❌ Submission contains missing values")
        return False
    
    # Check answer types (should be integers)
    if not all(isinstance(ans, (int, float)) for ans in submission_df['answer']):
        print("❌ All answers must be numeric")
        return False
    
    # Check answer range [0, 99999]
    answers = submission_df['answer'].astype(int)
    if not all((0 <= ans <= 99999) for ans in answers):
        print("❌ All answers must be in range [0, 99999]")
        invalid = submission_df[~answers.between(0, 99999)]
        print(f"   Invalid answers: {invalid.to_dict('records')}")
        return False
    
    print("✅ Submission is valid!")
    print(f"   - Number of problems: {len(submission_df)}")
    print(f"   - All answers in range [0, 99999]: ✓")
    print(f"   - No missing values: ✓")
    return True


def main():
    """Demonstrate working with test data format."""
    print("=" * 80)
    print("TEST DATA FORMAT EXAMPLE")
    print("=" * 80)
    
    # Load test data
    print("\n1. Loading test data...")
    test_df = load_test_data()
    print(f"   Loaded {len(test_df)} test problems")
    print("\n   Test data preview:")
    print(test_df.to_string(index=False))
    
    # Load sample submission
    print("\n2. Loading sample submission format...")
    sample_sub = pd.read_csv('sample_submission.csv')
    print("\n   Sample submission:")
    print(sample_sub.to_string(index=False))
    
    # Create a submission with dummy answers
    print("\n3. Creating submission with example answers...")
    example_answers = [0, 0, 0]  # Replace with your predictions
    submission = create_sample_submission(test_df, example_answers)
    print("\n   Created submission:")
    print(submission.to_string(index=False))
    
    # Validate submission
    print("\n4. Validating submission...")
    is_valid = validate_submission(submission)
    
    # Test with invalid answers
    print("\n5. Testing validation with invalid answers...")
    invalid_submission = submission.copy()
    invalid_submission.loc[0, 'answer'] = -1  # Invalid: < 0
    invalid_submission.loc[1, 'answer'] = 100000  # Invalid: > 99999
    print("\n   Modified submission with invalid answers:")
    print(invalid_submission.to_string(index=False))
    print("\n   Validating...")
    validate_submission(invalid_submission)
    
    # Save submission to file
    print("\n6. Saving submission to file...")
    output_file = '/tmp/my_submission.csv'
    submission.to_csv(output_file, index=False)
    print(f"   Saved to: {output_file}")
    
    # Verify saved file
    loaded_submission = pd.read_csv(output_file)
    print("\n   Loaded submission from file:")
    print(loaded_submission.to_string(index=False))
    
    print("\n" + "=" * 80)
    print("KEY POINTS")
    print("=" * 80)
    print("""
1. Submission format:
   - Two columns: 'id' and 'answer'
   - No index column
   - CSV format

2. Answer requirements:
   - Must be integers (or numeric that can convert to int)
   - Must be in range [0, 99999]
   - No missing values allowed

3. In actual competition:
   - Test problems are served one-by-one via API
   - You don't create a CSV directly
   - Your predict() method returns one answer at a time
   - The evaluation system creates the submission for you

4. This example is for:
   - Understanding the data format
   - Local testing and validation
   - Preparing predictions for verification
    """)
    print("=" * 80)


if __name__ == '__main__':
    main()

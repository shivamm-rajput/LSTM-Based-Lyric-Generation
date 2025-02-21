import os
import math

def split_text_file(input_file):
    """
    Splits a .txt file into exactly 20 files with equal number of words in each file.
    
    Args:
        input_file (str): Path to the input .txt file.
    
    Returns:
        None
    """
    # Read the content of the input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split the content into words
    words = content.split()
    total_words = len(words)
    
    # Calculate words per file (rounded up to ensure all words are included)
    num_files = 20
    words_per_file = math.ceil(total_words / num_files)
    
    for i in range(num_files):
        # Calculate start and end indices for this chunk
        start_index = i * words_per_file
        end_index = min((i + 1) * words_per_file, total_words)
        
        # Get the words for this file
        chunk_words = words[start_index:end_index]
        
        # Create the output file name
        base_name, _ = os.path.splitext(input_file)
        output_file = f'lyrics/{base_name}_part_{i + 1}.txt'
        
        # Create the lyrics directory if it doesn't exist
        os.makedirs('lyrics', exist_ok=True)
        
        # Write the words to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(' '.join(chunk_words))

# Example usage
input_file = 'bob dylan.txt'  # Replace with the path to your .txt file
split_text_file(input_file)
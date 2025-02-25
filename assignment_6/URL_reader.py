#Assignment 6 
#Done by: Genrietta Yagudayeva
#Instructions: Modify socket1.py to URL_reader.py by replacing socket with 
#urllib, reading 512-character chunks, and printing only the first 3000 characters 
#while continuing to count the total document size
#named constants, use a single loop, prompt the user for a URL

import urllib.request

# Constants (given by instructor)
CHUNK_SIZE = 512  # Fixed chunk size
PRINT_LIMIT = 3000  # Maximum number of characters to print

def fetch_url_data():
    
    # Step 1: Prompt for a URL
    url = input("Enter the URL of a web server text file resource: ")
    
    try:
        # Step 2: Open URL
        response = urllib.request.urlopen(url)
        total_chars = 0  # Total characters read from the document
        printed_chars = 0  # Characters printed to console
        
        # Step 3: Read and process the document in chunks
        while True:
            chunk = response.read(CHUNK_SIZE)
            if not chunk:
                break  # Stop when no more data is available
            
            chunk_str = chunk.decode('utf-8')
            total_chars += len(chunk_str)  # Count total characters
            
            # Step 4: Print only up to PRINT_LIMIT characters
            if printed_chars < PRINT_LIMIT:
                remaining_chars = PRINT_LIMIT - printed_chars
                print(chunk_str[:remaining_chars], end='')
                printed_chars += len(chunk_str[:remaining_chars])
        
        # Step 5: Print total character count in document to see what amount was printed
        print(f"\nTotal characters in the document: {total_chars}")
    
    except Exception as e:
        # Step 6: Handle errors
        print(f"Error: {e}")

# Step 7: Execute the function when script runs
if __name__ == "__main__":
    fetch_url_data()


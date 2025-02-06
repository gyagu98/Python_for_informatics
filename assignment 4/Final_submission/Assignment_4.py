# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Assignment 4: Files, Lists, and Split
# Made by: Genrietta Yagudayeva
#Directions: Make 1 program to ask for filename, run the program
# and read it. Each line is to be split into list of words
# Each word convert to lowercase
# Same program, make a freqcount() function 

#ensure input works
import sys
if sys.stdin.isatty():
    print("Running in interactive mode")
else:
    print("Running in non-interactive mode.")

#Used to iterate through a list of words and counts
def count_substring_occurrences(substring_to_search, words_list):
  
    for current_word in words_list:
        occurrence_count = 0
        search_position = 0  # Search from the beginning of the word

        while True:
            found_position = current_word.find(substring_to_search, search_position)

            if found_position == -1:
                break  # Exit loop if no occurrences found

            occurrence_count += 1
            search_position = found_position + len(substring_to_search)  # Move past the found substring

        print(f"{current_word} {occurrence_count}")

#This functtion is to rad line by line and extract words, convert to lowercase
def process_file_and_count(filename_to_open, substring_to_search):
 
    unique_words_list = []

    try:
        with open(filename_to_open, 'r') as opened_file:
            for file_line in opened_file:
                words_in_line = file_line.strip().split()  # Split line into words

                for individual_word in words_in_line:
                    word_in_lowercase = individual_word.lower()
                    if word_in_lowercase not in unique_words_list:
                        unique_words_list.append(word_in_lowercase)

        unique_words_list.sort()  # Sort words alphabetically
        count_substring_occurrences(substring_to_search, unique_words_list)

    except FileNotFoundError:
        print(f"The file '{filename_to_open}' was not found.")


#This is to prompt for filename and substring
def main():
  
    print("Script started...")  # Debug message to ensure script starts

    file_name_input = input("Enter filename: ")  # Prompt for filename
    print(f"Filename entered: {file_name_input}")  # Confirm input

    substring_input = input("Enter substring: ")  # Prompt for substring
    print(f"Substring entered: {substring_input}")  # Confirm input

    process_file_and_count(file_name_input, substring_input)


# Execute the main function
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 17:19:34 2025

@author: genriettayagudayeva
"""

# Assignment 3: Looping, Searching, and Slicing
# Full Name: Genrietta Yagudayeva
# Program name: parse_float.py
# Directions: Write a program given: "avg_str = 'Average value read: 0.72903'"
# Use find() method and string slicing to extract the portion
# of the string after the colon and use float () to convert extracted
# string into floating point value
# should be a general solution, no magic numbers

#Locate the colon
def locate_colon(input_string):
    return input_string.find(":")

#extract number as a string after colon
def extract_substring_after_colon(input_string, colon_index):
    if colon_index == -1:
        raise ValueError("Invalid: No colon found.")
    return input_string[colon_index + 1:].strip()

# convert extracted string to a float
def convert_to_float(number_string):
    return float(number_string)

# Handle the extraction process via more functions
def process_extraction(input_string):
    colon_index = locate_colon(input_string)
    number_string = extract_substring_after_colon(input_string, colon_index)
    return convert_to_float(number_string)

# Main execution for example using the number provided
if __name__ == "__main__":
    avg_str = "Average value read: 0.72903"  # Example input
    extracted_value = process_extraction(avg_str)  # Extract float
    
    print(f"Floating-point number: {extracted_value}")  # Result

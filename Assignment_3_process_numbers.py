#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 16:55:45 2025

@author: genriettayagudayeva
"""

# Assignment 3: Looping, Searching, and Slicing
# Full Name: Genrietta Yagudayeva
# Program name: process_numbers.py
# Directions: Write a program that repeatedly reads floating point
# numbers input by the user until the user types done
# After the user entered done, print out the total, count, max, min, and av
# of the numbers (no lists, no max, no min)

#Write out variables

total_sum = 0.0  # Sum of numbers
count_numbers = 0  # Count of numbers
max_number = None  # the maximum
min_number = None  # the minimum

# Start loop to accept user input
while True:
    user_input = input("number (or 'done'): ").strip().lower()
    
    if user_input == "done":
        break  # Exit loop when 'done'
    
    try:
        number = float(user_input)  # Convert input to floating-point number
        total_sum += number  # Add
        count_numbers += 1  # Count
        
        # Maximum and minimum values
        if max_number is None or number > max_number:
            max_number = number
        
        if min_number is None or number < min_number:
            min_number = number
    except ValueError:
        print("Invalid, enter input to be a valid floating point number")  # User gets this if invalid input

#Print results
if count_numbers > 0:
    average_value = total_sum / count_numbers  # Give average
    print("\nResults:")
    print(f"Total: {total_sum}")
    print(f"Count: {count_numbers}")
    print(f"Maximum: {max_number}")
    print(f"Minimum: {min_number}")
    print(f"Average: {average_value}")
else:
    print("No numbers were entered.")  # User gets this if no numbers were input
    


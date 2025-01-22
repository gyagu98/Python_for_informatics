#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 16:57:10 2025

@author: genriettayagudayeva
"""

# Assignment 2: Functions
# Full Name: Genrietta Yagudayeva

# Function 1: Define a function to take a string valuee as a parameter and
# convert it to an int value and return the int value

def to_number(num_str):
    return int(num_str)

# Function 2: Define a function to take two ints, sum them, and return them

def add_two(n1, n2):
    return n1 + n2

# Function 3: Define a function to cube the value and return the result

def cube(n):
    return n ** 3

# Use functions 1-3 to compose 1 statement and specify two string literals
# convert them to ints, add them, cube the result, and print the cubed value
# When you insert the string literals, ensure the strings are convertible to values

print(cube(add_two(to_number('1'), to_number('2'))))
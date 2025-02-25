#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 16:48:29 2025

@author: genriettayagudayeva
"""

# Author: Genrietta Yagudayeva
# Assignment 5: Message Frequency Count

#Open the file with potential if doesn't work
filename = "mbox.txt"
try:
    file_handle = open(filename, 'r')
except FileNotFoundError:
    print(f"Error: The file was not found")
    exit()

#Dictionary for email counts
email_counts = {}

#Read file line by line
for line in file_handle:
    line = line.strip()
    
    # Find  lines that start with 'From'
    if line.startswith("From "):
        words = line.split()
        
        # Take email address and count occurrences
        if len(words) > 1:  
            email = words[1]
            if email not in email_counts:
                email_counts[email] = 1
            else:
                email_counts[email] += 1

#Close file
file_handle.close()

#Convert dictionary to tuples (count, email)
email_list = [(count, email) for email, count in email_counts.items()]

#Sort list in descending based on count
email_list.sort(reverse=True, key=lambda x: x[0])

#Extract and print the person with the highest number of messages
if email_list:
    highest_count, top_sender = email_list[0]
    print(f"The person that has the highest number of messages is {top_sender} with {highest_count} messages")
else:
    print("No emails found")

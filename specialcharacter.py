#!/bin/python3
import re

while True:
    try:
        fname = input("What is the file name: ")

        if fname == "Nuggets":
            fname = "formtestdata.csv"
        #elif fname == "SuperNuggets":
        #    fname = "formtestdata.csv"
        fhand = open(fname)
        break
    except: 
        print("This file does not exist")

# Read all data from file
count = 0
data_list = []
for line in fhand:
    data = line.strip().split(',')
    data_list.append(data)
    count = count + 1
print(f"Total entries read: {count}")

# Process data to find latest entries
count_time = 0
latest_entries = {}
def check_special_characters(text):
    # This regex pattern will match any character that is not a letter, space, hyphen, or apostrophe
    pattern = r'[\[\]\(\)\{\}\<\>\|\~\`\!\@\#\$\%\^\&\*\+\=\_]'

    special_chars = re.findall(pattern, text)
    
    if special_chars:
        return True, special_chars
    else:
        return False, []

# Example usage
# Iterate through your data and check each name
for row in data_list:
    has_special, chars = check_special_characters(row[3])  # First name
    if has_special:
        print(f"Special characters in {str(row)}: {chars}")
        
    has_special, chars = check_special_characters(row[2])  # Last name
    if has_special:
        print(f"Special characters in {str(row)}: {chars}")

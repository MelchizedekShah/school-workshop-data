#!/bin/python3

from datetime import datetime

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

def parse_timestamp(ts_string):
    try:
        cleaned_ts = ts_string.strip().replace('\ufeff', '')
        return datetime.strptime(cleaned_ts, '%m/%d/%Y %H:%M:%S')
    except ValueError as e:
        print(f"Error parsing timestamp '{ts_string}': {e}")
        return None

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

for row in data_list:
    if len(row) < 4:  # Ensure row has enough elements
        print(f"Skipping incomplete row: {row}")
        continue
        
    last_name = row[2].strip().capitalize()
    first_name = row[3].strip().capitalize()

    full_name_normal = f"{first_name} {last_name}"
    full_name_swapped = f"{last_name} {first_name}"

    timestamp = parse_timestamp(row[0])
    if timestamp is None: 
        continue
    
    count_time += 1

    # Determine which key to use (normal or swapped name format)
    key_to_use = None
    if full_name_normal in latest_entries:
        key_to_use = full_name_normal
    elif full_name_swapped in latest_entries:
        key_to_use = full_name_swapped
    else:
        # New person, use normal order as default
        key_to_use = full_name_normal
    
    # Update if this is newer or the first entry
    if key_to_use not in latest_entries:
        latest_entries[key_to_use] = (row, timestamp)
    elif timestamp > latest_entries[key_to_use][1]:
        latest_entries[key_to_use] = (row, timestamp)

print(f"Processed timestamps: {count_time}")

# Extract the cleaned data (only the latest entry for each person)

cleaned_data = []
for entry_data, _ in latest_entries.values():
    cleaned_data.append(entry_data)
    print(f"Latest entry: {entry_data}")

print(f"Total unique individuals: {len(cleaned_data)}")

print("List: " + str(cleaned_data))



try:
    fwrite = open("clean.csv", 'w')
    header = "Timestamp,Class,LastName,FirstName,Round1 (08:00-09:00),Round2 (09:15-10:15),Round3 (10:45-11:45),Round4 (12:00-13:00)"
    fwrite.write(header + '\n')  
    for entry in cleaned_data:
        line = ','.join(str(item) for item in entry)
        fwrite.write(line + '\n')
    print("Successfully wrote to clean.csv")
    fwrite.close()
    fhand.close()  

except IOError as e:
    print(f"Error writing to file: {e}")
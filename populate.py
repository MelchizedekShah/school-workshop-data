import sqlite3
import csv
import sys

# Connect to SQLite database (creates it if it doesn't exist)
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Drop the tables if exist
cursor.execute('DROP TABLE IF EXISTS Schedule')
cursor.execute('DROP TABLE IF EXISTS Students')
cursor.execute('DROP TABLE IF EXISTS Activities')

# Create Students table for unique student information
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        last_name TEXT NOT NULL,
        first_name TEXT NOT NULL,
        class TEXT NOT NULL,
        UNIQUE(last_name, first_name, class)
    )
''')

# Create Activities table for unique activity names
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Activities (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_name TEXT NOT NULL UNIQUE
    )
''')

# Create Schedule table linking students with their activity choices by round
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Schedule (
        schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        timestamp TEXT,
        round1_activity INTEGER,
        round2_activity INTEGER,
        round3_activity INTEGER,
        round4_activity INTEGER,
        FOREIGN KEY (student_id) REFERENCES Students(student_id),
        FOREIGN KEY (round1_activity) REFERENCES Activities(activity_id),
        FOREIGN KEY (round2_activity) REFERENCES Activities(activity_id),
        FOREIGN KEY (round3_activity) REFERENCES Activities(activity_id),
        FOREIGN KEY (round4_activity) REFERENCES Activities(activity_id)
    )
''')

# Get file name and open file
while True:
    try:
        fname = input("What is the file name: ")
        if fname == "Nuggets":
            fname = "clean.csv"
        elif fname == "exit":
            print("Exiting program...")
            conn.close()  # Close database connection before exiting
            sys.exit()
        
        # Open file and create CSV reader
        fhand = open(fname, 'r')
        csv_reader = csv.reader(fhand)
        next(csv_reader)  # Skip header row if it exists
        break
    except FileNotFoundError:
        print("This file does not exist")
    except Exception as e:
        print(f"An error occurred: {e}")

# Insert unique activities into Activities table
unique_activities = set()
for row in csv_reader:
    # Strip whitespace and handle potential empty strings
    activities = [activity.strip() for activity in row[4:8] if activity.strip()]
    unique_activities.update(activities)
unique_activities.discard('')  # Remove empty string if exists

for activity in unique_activities:
    cursor.execute('INSERT OR IGNORE INTO Activities (activity_name) VALUES (?)', (activity,))

# Function to get activity ID
def get_activity_id(activity_name):
    if not activity_name or activity_name.strip() == '':
        return None
    cursor.execute('SELECT activity_id FROM Activities WHERE activity_name = ?', (activity_name.strip(),))
    result = cursor.fetchone()
    return result[0] if result else None

# Reset file pointer to beginning and recreate CSV reader
fhand.seek(0)
csv_reader = csv.reader(fhand)
next(csv_reader)  # Skip header row again

# Insert students and their schedules
for row in csv_reader:
    if len(row) < 8:  # Check if row has enough columns
        print(f"Skipping invalid row: {row}")
        continue
    
    timestamp, class_name, last_name, first_name = row[0:4]
    r1, r2, r3, r4 = row[4:8]
    
    # Insert student (ignore duplicates)
    cursor.execute('''
        INSERT OR IGNORE INTO Students (last_name, first_name, class)
        VALUES (?, ?, ?)
    ''', (last_name.strip(), first_name.strip(), class_name.strip()))
    
    # Get student_id
    cursor.execute('''
        SELECT student_id FROM Students 
        WHERE last_name = ? AND first_name = ? AND class = ?
    ''', (last_name.strip(), first_name.strip(), class_name.strip()))
    student_id = cursor.fetchone()[0]
    
    # Insert schedule
    cursor.execute('''
        INSERT INTO Schedule (student_id, timestamp, round1_activity, round2_activity, 
                            round3_activity, round4_activity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (student_id, timestamp.strip(), 
          get_activity_id(r1), get_activity_id(r2), 
          get_activity_id(r3), get_activity_id(r4)))

# Commit changes and close connections
conn.commit()
fhand.close()
conn.close()

print("Database created and records inserted successfully!")
#!/bin/python3
import sqlite3
import os

conn = sqlite3.connect("data.db")
cur = conn.cursor()


rounds = ["round1_activity", "round2_activity", "round3_activity", "round4_activity"]

for round in rounds:
    cur.execute("SELECT DISTINCT Activities.activity_name FROM Schedule JOIN Activities ON Schedule.{} = Activities.activity_id".format(round),)

    results = cur.fetchall()
    print("These are the " + str(results) + " from " + str(round))
    for row in results:
        activity = row[0].strip()
        print(activity)
    count = len(results)
    print("COUNT: " + str(count))

    if not os.path.exists(round):
        os.makedirs(round)

    for activity in results:
        activity = activity[0].strip()
        cur.execute("""
            SELECT Students.first_name, Students.last_name, Students.class 
            FROM Students 
            JOIN Schedule ON Students.student_id = Schedule.student_id 
            JOIN Activities ON Schedule.{} = Activities.activity_id 
            WHERE Activities.activity_name = ?
        """.format(round), (activity,))

        rows = cur.fetchall()
        student_count = len(rows)

        file_path = os.path.join(round, activity + ".txt")
        fhand = open(file_path, "w")
        fhand.write(activity + "\n")  
        fhand.write("Total Students: " + str(student_count) + "\n")
        fhand.write("\n")

        for info in rows:
            fhand.write(" ".join(info) + "\n") 

        fhand.close()
conn.close()

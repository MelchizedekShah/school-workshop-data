# Workshop Registration Handler

A set of Python scripts designed to streamline the workshop registration process for school events. This tool addresses common data validation issues in Google Forms submissions and provides comprehensive reporting.

## Features

- *Data Cleanup*: Processes raw CSV data from Google Forms, removing duplicates, standardizing input formats, and detecting special characters
- *Database Population*: Transfers validated data into a structured SQLite database for reliable storage
- *Registration Processing*: Generates organized reports showing:
  - Workshop rosters (students registered for each workshop)
  - Student schedules (which workshops each student will attend)
  - Class lists showing all students in each class
  - "Naughty list" identifying students who registered but didn't select any workshops

## Technical Overview

The system consists of five main components:

1. *cleanup.py* - Sanitizes and validates the raw registration data:
   - Removes duplicate entries (keeping only the latest submission)
   - Standardizes name formatting
   - Handles timestamp parsing

2. *specialcharacter.py* - Identifies problematic special characters in student names

3. *populate.py* - Populates a SQLite database with the cleaned data:
   - Creates tables for Students, Activities, and Schedule
   - Maps student selections to appropriate activity IDs
   - Handles validation and error checking

4. *process.py* - Generates workshop rosters by round:
   - Creates a directory for each round
   - Outputs a text file for each workshop listing participants
   - Provides attendance counts for each workshop

5. *process2.py* - Creates additional reports:
   - Class-based lists of all students
   - Special "naughty list" report of students who registered but didn't select workshops

## Usage

1. Run cleanup.py to process raw CSV data
2. Run populate.py to create and fill the database
3. Run process.py to generate workshop rosters
4. Run process2.py to generate class lists and the "naughty list"

This project demonstrates practical application of data processing, validation techniques, and database management to solve a real-world administrative challenge in an educational setting.

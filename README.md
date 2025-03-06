# Workshop Registration Handler

A set of Python scripts designed to streamline the workshop registration process for school events. This tool addresses common data validation issues in Google Forms submissions.

## Features

- *Data Cleanup*: Processes raw CSV data from Google Forms, removing duplicates and standardizing input formats
- *Database Population*: Transfers validated data into a structured database for reliable storage
- *Registration Processing*: Generates organized reports showing:
  - Workshop rosters (students registered for each workshop)
  - Student schedules (which workshops each student will attend)

## Technical Overview

The system consists of three main components:

1. cleanup.py - Sanitizes and validates the raw registration data
2. populate.py - Populates a database with the cleaned data
3. process.py - Processes the database to create organized workshop assignments

This project demonstrates practical application of data processing, validation techniques, and database management to solve a real-world administrative challenge in an educational setting.

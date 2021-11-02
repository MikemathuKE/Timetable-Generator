# Timetable-Generator
A Simple Timetable Generator

## Description
The application works by taking data from existing database and structuring that data into .xls excel sheet.

### How it works
- The allocator for lessons simulates time of the week from the beginning to the end of the week using 1hr timesteps. (Considers weekdays only)
- Each Unit is pre-assigned a Lecturer
- Classroom to be used is generated based on availability of the room and the number of students the classroom can accomodate
- Time from end of a lesson to the next lesson is randomly generated

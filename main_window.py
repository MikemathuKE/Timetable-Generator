import tkinter as tk
from tkinter import messagebox
import modules.database as database
import modules.lesson as ls
import modules.scheduler as sch
from xlwt import Workbook
import os


def main_window():
    db = database.Database("res/school_database.db")

    window = tk.Tk(className="TT")
    window.geometry("1280x720")

    frm_tb_select = tk.Frame(window, relief="raised")
    canvas = tk.Canvas(window)
    vt_scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    hz_scrollbar = tk.Scrollbar(window, orient="horizontal", command=canvas.xview)
    frm_tb_data = tk.Frame(canvas, relief="sunken")
    frm_tb_data.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )
    canvas.create_window((0, 0), window=frm_tb_data, anchor="nw")
    canvas.configure(xscrollcommand=hz_scrollbar.set)
    canvas.configure(yscrollcommand=vt_scrollbar.set)

    def show_table(table_name):
        db.setActiveTable(table_name)
        tb = db.table.get(table_name)
        records = tb.select_record("*", None)
        num_columns = len(tb.get_columns())

        for child in frm_tb_data.winfo_children():
            child.destroy()

        i_ = 0
        title = tk.Label(frm_tb_data, text=table_name, bg="red", font=('Arial', 12, 'bold'))
        title.grid(pady=10, row=i_, columnspan=num_columns + 1)
        i_ += 1
        j = 0
        tk.Label(frm_tb_data, width=3, font=('Arial', 12, 'bold')).grid(row=i_, column=j, padx=10)
        for cols in tb.get_columns().keys():
            j += 1
            tk.Label(frm_tb_data, text=cols, font=('Arial', 12, 'bold')).grid(row=i_, column=j, padx=10)
        for record in records:
            i_ += 1
            j = 0
            tk.Label(frm_tb_data, text=str(i_ - 1), width=3, font=('Arial', 12, 'bold')).grid(row=i_, column=j, padx=10)
            for entry in record:
                j += 1
                data = tk.StringVar()
                data.set(entry)
                ent_field = tk.Entry(frm_tb_data, textvariable=data, state="disabled", font=('Arial', 12, 'bold'))
                ent_field.grid(row=i_, column=j, padx=10)

    i = 0
    btn_table = {}
    for table in db.table.keys():
        btn_table[table] = tk.Button(frm_tb_select, text=table, bg="yellow", font=('Arial', 12, 'bold'))
        btn_table[table].grid(row=2, column=i, padx=10)
        btn_table[table].bind("<Button-1>", lambda event, value=table: show_table(value))
        i += 1

    lessons = {}
    courses = {}
    lecturers = {}
    rooms = {}
    schedulers = {}

    def generate_timetable():
        tb_units = db.table.get("Units")
        tb_lects = db.table.get("Lecturers")
        tb_rooms = db.table.get("Lecture_Room")
        tb_courses = db.table.get("Syllabus")
        rc_units = tb_units.select_record("*", None)
        rc_rooms = tb_rooms.select_record("*", None)

        i = 0
        id_pos = 0
        name_pos = 0
        course_id_pos = 0
        course_year_pos = 0
        lecturer_id_pos = 0
        duration_pos = 0
        students_pos = 0
        for column in tb_units.columns.keys():
            if column == "ID":
                id_pos = i
            if column == "Name":
                name_pos = i
            if column == "Course_ID":
                course_id_pos = i
            if column == "Course_Year":
                course_year_pos = i
            if column == "Lecturer_ID":
                lecturer_id_pos = i
            if column == "Hours_Per_Week":
                duration_pos = i
            if column == "Number_Of_Students":
                students_pos = i
            i += 1

        for room in rc_rooms:
            ls.add_room(rooms, room[0] + str(room[1]), room[2])

        for record in rc_units:
            course = record[course_id_pos] + str(record[course_year_pos])
            lect_id = record[lecturer_id_pos]
            lect_name = tb_lects.select_record("Name", "ID="+str(lect_id))[0][0]
            course_name = tb_courses.select_record("Name", "ID='"+record[course_id_pos]+"' AND " + "Year="+str(record[course_year_pos]))[0][0]
            lessons[record[id_pos]] = ls.Lesson(record[id_pos], record[name_pos], course, lect_id, record[duration_pos], record[students_pos])
            ls.add_course(courses, course, course_name, record[duration_pos])
            ls.add_lecturer(lecturers, lect_id, lect_name, record[duration_pos])

        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        time = [7, 8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        done = True

        wb = Workbook()
        for course in courses.keys():
            max_rest = int(70 / courses[course].time_required) - 1
            min_rest = 1
            column = 0
            row = 0
            schedulers[course] = sch.Scheduler(wb, course, lessons, min_rest, max_rest)

        column += 1
        for t in time:
            for course in courses.keys():
                schedulers[course].sheet.write(row, column, str(t))
            column += 1

        for day in days:
            row += 1
            column = 0
            for course in courses.keys():
                schedulers[course].sheet.write(row, column, day)
            time_remaining = 11

            for t in time:
                time_remaining -= 1
                column += 1

                for schd in schedulers.keys():
                    schedulers[schd].select_active_lesson(rooms, lecturers, time_remaining, row, column)
                    schedulers[schd].simulate_time(rooms, lecturers)

        try:
            wb.save("Timetable.xls")
        except:
            messagebox.showerror("Creating Timetable", "Close Timetable.xls before trying to generate timetable")
            done = False
        lessons.clear()
        courses.clear()
        lecturers.clear()
        rooms.clear()
        if done:
            messagebox.showinfo("Timetable Success",
                                "Timetable has been created and saved as excel workbook in program directory\n" +
                                os.getcwd())
            os.system("start Timetable.xls")

    btn_submit = tk.Button(text="Generate TimeTables", command=generate_timetable, fg="white", bg="blue",
                           font=('Arial', 14, 'bold'))
    frm_tb_select.pack()
    vt_scrollbar.pack(side="right", fill="y")
    canvas.pack(side="top", fill="both", expand=True)
    hz_scrollbar.pack(side="bottom", fill="x")
    btn_submit.pack()
    window.mainloop()

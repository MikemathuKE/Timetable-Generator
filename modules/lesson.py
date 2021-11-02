class Lesson:
    def __init__(self, lesson_id, lesson_name, course_id, lecturer_id, lesson_duration, num_students):
        self.id = lesson_id
        self.name = lesson_name
        self.course_id = course_id
        self.duration = lesson_duration
        self.lect_id = lecturer_id
        self.num_students = num_students

    def use_time(self, time):
        self.duration -= time

    def print(self):
        print("ID: " + str(self.id) + "\nCourse: " + self.course_id + "\nLecturer: " + str(self.lect_id) +
              "\nDuration: " + str(self.duration) + "\nStudents: " + str(self.num_students) + "\n\n")


class Course:

    def __init__(self, id_, name, time):
        self.id = id_
        self.name = name
        self.time_required = time

    def add_time(self, time):
        self.time_required += time

    def use_time(self, time):
        self.time_required -= time


def add_course(courses, new_course, name, time):
    if new_course in courses.keys():
        exists = True
    else:
        exists = False

    if exists:
        courses[new_course].add_time(time)
    else:
        courses[new_course] = Course(new_course, name, time)


class Lecturer:

    def __init__(self, id_, name, time):
        self.id = id_
        self.name = name
        self.time_required = time
        self.active = False

    def add_time(self, time):
        self.time_required += time
        if self.time_required > 0:
            self.active = True

    def use_time(self, time):
        if self.time_required > 0:
            self.time_required -= time

        if self.time_required <= 0:
            self.time_required = 0
            self.active = False


def add_lecturer(lecturers, id_, new_lecturer, time):
    if new_lecturer in lecturers.keys():
        exists = True
    else:
        exists = False

    if exists:
        lecturers[id_].add_time(time)
    else:
        lecturers[id_] = Lecturer(id_, new_lecturer, time)


class Room:
    def __init__(self, id_, capacity):
        self.id = id_
        self.capacity = capacity
        self.hours = 0
        self.active = False

    def assign_hours(self, hours):
        self.hours = hours
        if self.hours > 0:
            self.active = True

    def use_time(self, time):
        if self.hours > 0:
            self.hours -= time

        if self.hours <= 0:
            self.hours = 0
            self.active = False


def add_room(rooms, id_, capacity):
    if id_ in rooms.keys():
        exists = True
    else:
        exists = False

    if not exists:
        rooms[id_] = Room(id_, capacity)


class Session:
    def __init__(self, lesson, active=False):
        self.lesson = lesson
        self.active = active

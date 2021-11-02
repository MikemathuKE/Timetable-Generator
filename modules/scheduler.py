import random as rand
import modules.lesson as ls


class Scheduler:
    def __init__(self, workbook, course_name, lessons, min_rest=0, max_rest=2):
        self.sheet = workbook.add_sheet(course_name)
        self.course_name = course_name
        self.min_rest = min_rest
        self.max_rest = max_rest
        self.active_hours = rand.randint(min_rest, max_rest)
        self.active_lecturer = ""
        self.active_room = ""
        self.active_lesson = ""
        self.available_lessons = {}

        for less in lessons.keys():
            if lessons[less].course_id == course_name:
                self.available_lessons[less] = ls.Session(lessons[less])

    def select_active_lesson(self, rooms, lecturers, time_remaining, row, column):
        if len(self.available_lessons.keys()) <= 0:
            return
        if self.active_hours <= 0:
            lesson = rand.choice(list(self.available_lessons.keys()))
            for lss in self.available_lessons.keys():
                if self.available_lessons[lss].active or self.available_lessons[lss].lesson.duration > time_remaining \
                        or lecturers[self.available_lessons[lss].lesson.lect_id].active \
                        or self.available_lessons[lss].lesson.duration <= 0:
                    lesson = lss
                else:
                    break

            room = rand.choice(list(rooms.keys()))
            for rm in rooms.keys():
                if rooms[room].capacity > self.available_lessons[lesson].lesson.num_students or rooms[room].active:
                    room = rm
                else:
                    break

            if self.available_lessons[lesson].lesson.duration < time_remaining:
                lecturers[self.available_lessons[lesson].lesson.lect_id].active = True
                rooms[room].active = True
                rooms[room].assign_hours(self.available_lessons[lesson].lesson.duration)
                self.active_hours = self.available_lessons[lesson].lesson.duration + \
                    rand.randint(self.min_rest, self.max_rest)
                self.sheet.write_merge(row, row, column, column + self.available_lessons[lesson].lesson.duration - 1,
                                       self.available_lessons[lesson].lesson.name + " (" + room + ") - " +
                                       lecturers[self.available_lessons[lesson].lesson.lect_id].name)
                self.active_lesson = lesson
                self.active_room = room
                self.active_lecturer = self.available_lessons[lesson].lesson.lect_id

    def simulate_time(self, rooms, lecturers, hours=1):
        if self.active_hours > 0:
            self.active_hours -= 1
        if self.active_lesson != '':
            self.available_lessons[self.active_lesson].lesson.use_time(hours)
            rooms[self.active_room].use_time(hours)
            if not rooms[self.active_room].active:
                lecturers[self.active_lecturer].active = False
                self.available_lessons.pop(self.active_lesson)
                self.active_lecturer = ""
                self.active_room = ""
                self.active_lesson = ""

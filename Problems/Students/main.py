class Student:
    def __init__(self, name, last_name, birth_year):
        self.name = name
        self.last_name = last_name
        self.birth_year = birth_year
        # calculate the student_id here
        self.student_id = self.name[0] + self.last_name + str(self.birth_year)


n = input()
last_n = input()
birth_y = int(input())
student = Student(n, last_n, birth_y)
print(student.student_id)

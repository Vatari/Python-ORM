import os
import django
from datetime import date

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Student


def add_students():
    student_data = [
        {
            "student_id": "FC5204",
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "1995-05-15",
            "email": "john.doe@university.com",
        },
        {
            "student_id": "FE0054",
            "first_name": "Jane",
            "last_name": "Smith",
            "birth_date": None,
            "email": "jane.smith@university.com",
        },
        {
            "student_id": "FH2014",
            "first_name": "Alice",
            "last_name": "Johnson",
            "birth_date": "1998-02-10",
            "email": "alice.johnson@university.com",
        },
        {
            "student_id": "FH2015",
            "first_name": "Bob",
            "last_name": "Wilson",
            "birth_date": "1996-11-25",
            "email": "bob.wilson@university.com",
        },
    ]

    for data in student_data:
        student = Student(
            student_id=data["student_id"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            birth_date=data["birth_date"],
            email=data["email"],
        )
        student.save()


add_students()


def get_students_info():
    result = []

    for student in Student.objects.all():
        result.append(
            f"Student №{student.student_id}: {student.first_name} {student.last_name}; Email: {student.email}")

    return '\n'.join(result)


print(get_students_info())


def update_students_emails():
    for student in Student.objects.all():
        mail_split = student.email.split("@")
        mail_split[1] = "uni-students.com"
        student.email = "@".join(mail_split)
        student.save()


update_students_emails()


def truncate_students():
    for student in Student.objects.all():
        student.delete()


truncate_students()
print(Student.objects.all())
print(f"Number of students: {Student.objects.count()}")

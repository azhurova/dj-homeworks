from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from students.models import Student, Course


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'name', 'birth_date')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        if 'students' in data:
            students = data['students']
            if len(students) > settings.MAX_STUDENTS_PER_COURSE:
                raise ValidationError(f"Максимальное число студентов на курсе — {settings.MAX_STUDENTS_PER_COURSE}")

        return data

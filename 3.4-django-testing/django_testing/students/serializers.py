from django.conf import settings
from rest_framework import serializers

from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate_students(self, students):
        """Валидация: не более MAX_STUDENTS_PER_COURSE студентов на курсе."""
        max_students = getattr(settings, 'MAX_STUDENTS_PER_COURSE', 20)
        if len(students) > max_students:
            raise serializers.ValidationError(
                f'На курсе не может быть больше {max_students} студентов'
            )
        return students
        
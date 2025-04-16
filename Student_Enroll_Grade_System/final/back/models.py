from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class newuser(AbstractUser):
    username = models.CharField(max_length=20)
    student_id = models.CharField(max_length=20, unique=True, primary_key=True)
    is_teacher = models.BooleanField(default=False)
    USERNAME_FIELD = 'student_id'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username
    

class course(models.Model):
    course_id = models.CharField(max_length=20, unique=True, primary_key=True)
    course_name = models.CharField(max_length=20)
    teacher = models.ForeignKey(newuser, on_delete=models.CASCADE)
    available = models.ForeignKey('available', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.course_name

class available(models.Model):
    year = models.IntegerField()
    semester = models.CharField(max_length=10)
    capacity = models.IntegerField(default=0)
    registration_deadline = models.DateField(null=True, default=None)

    def __str__(self):
        return str(self.year) + " " + self.semester

class enrollment(models.Model):
    course = models.ForeignKey(course, on_delete=models.CASCADE)
    student = models.ForeignKey(newuser, on_delete=models.CASCADE)
    available = models.ForeignKey(available, on_delete=models.CASCADE, null=True, default=None)
    semester = models.CharField(max_length=10, null=True)  # 添加这一行
    class Meta:
        unique_together = (('student', 'course'),)

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name} - {self.semester}"

    


class grade(models.Model):
    enroll = models.OneToOneField(enrollment, on_delete=models.CASCADE, null=True, default=None)
    score = models.FloatField()
    def __str__(self):
        return f"{self.enroll.student.username} - {self.enroll.course.course_name} - {self.score}"
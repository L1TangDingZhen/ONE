from ninja import Schema
from datetime import date
from typing import Optional
from pydantic import BaseModel

class User(Schema):
    username : str
    password : str
    student_id : str
    # is_teacher : bool=False

class Login(BaseModel):
    student_id : str
    password : str


class Me(Schema):
    username : str
    student_id : str
    is_teacher : bool

class UserChange(Schema):
    username : str
    password : str

class NoMessage(Schema):
    message: str
    username: str = None
    password: str = None
    student_id: str = None

    
class LoginSuccess(Schema):
    student_id: str
    token: str

class ErrorResponse(Schema):
    message: str

class Course(Schema):
    course_id: str
    course_name: str
    teacher_id: str

class CourseChange(Schema):
    course_name: str = None
    year: int = None
    semester: str = None
    capacity: int = None
    registrationDeadline: Optional[date] = None

class Grade(Schema):
    course_id: str
    student_id: str
    score: float

class GradeChange(Schema):
    score: float


class Enrollment(Schema):
    course_id: str
    student_id: str
    semester: str

class EnrollmentDetail(Schema):
    id: int
    course_id: str
    course_name: str
    teacher_name: str
    semester: str


class TeacherCourse(Schema):
    course_id: str
    course_name: str
    semester: str = None
    capacity: int = None
    registration_deadline: Optional[date] = None

class AvailableCourse(Schema):
    course_id: str
    course_name: str
    teacher_name: str
    year: Optional[int] = None  # 将 year 定义为可选的 Optional[int]
    semester: str
    remaining_capacity: int
    registration_deadline: Optional[date] = None

class CreateCourse(Schema):
    name: str
    year: int
    semester: str
    capacity: int

class CreateCourseSchema(Schema):
    name: str
    year: int
    semester: str
    capacity: int
    registrationDeadline: date

class EnrolledStudentInfo(Schema):
    student_id: str
    student_name: str
    score: Optional[float] = None
    grade_id: Optional[int] = None
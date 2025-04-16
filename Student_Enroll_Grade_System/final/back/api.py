from datetime import date, datetime, timedelta
from django.utils import timezone
from ninja import NinjaAPI, Router
from sympy import Sum
from back.scheme import User, NoMessage, LoginSuccess, ErrorResponse, Course, Grade, UserChange, CourseChange, GradeChange, Enrollment, Me, TeacherCourse, CreateCourse, AvailableCourse, CreateCourseSchema, EnrollmentDetail, EnrolledStudentInfo, Login
from back.models import newuser, course, grade, enrollment, available, enrollment
from typing import List
from ninja.security import django_auth, HttpBearer
from ninja.errors import HttpError
from jose import jwt
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI
# config.py
import os
import secrets
import string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password, check_password
from back.permission import IsTeacher
from django.contrib.admin.views.decorators import staff_member_required


teacher_auth = IsTeacher()
router = Router()

# from config import JWT_SECRET_KEY
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 43200


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "supersecret":
            return token


# api = NinjaAPI(auth=GlobalAuth()) #全局验证
api = NinjaExtraAPI(docs_decorator=staff_member_required) #多出来一个token验证类
# authorised to login docs
api.register_controllers(NinjaJWTDefaultController)


# 生成一个随机字符串作为密钥
alphabet = string.ascii_letters + string.digits
secret_key = ''.join(secrets.choice(alphabet) for i in range(32))

# 如果环境变量中有 JWT_SECRET_KEY,就使用环境变量的值
# 否则,使用上面生成的随机字符串
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secret_key)


# def generate_token(username: str, expires_delta = None):
#     to_encode = {"sub": username}.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#         to_encode.update({"exp": expires_delta})
#     else:
#         expire = datetime.utcnow() + datetime.timedelta(minutes=15)
#     to_encode.update(dict(exp=expire))
#     encoded_jwt = jwt.encode(to_encode, "secret", algorithm="HS256")
#     return encoded_jwt



# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         if token == "supersecret":
#             return token

# class AuthBearer(HttpBearer):
#     def authenticate(self, request, token):
#         try:
#             payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
#             username = payload["sub"]
#             exp = payload["exp"]
#             if datetime.utcnow() < datetime.utcfromtimestamp(exp):
#                 user = newuser.objects.get(username=username) #receive the profile of the user
#                 return user
#             else:
#                 # 如果令牌已过期，生成一个新的令牌
#                 new_exp = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#                 new_token = jwt.encode({"sub": username, "exp": new_exp}, JWT_SECRET_KEY, algorithm="HS256")
#                 request.headers["Authorization"] = f"Bearer {new_token}"
#                 user = newuser.objects.get(username=username)
#                 return user
#         except jwt.JWTError:
#             raise HttpError(401, "Invalid token")

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
            user_id = payload["sub"]
            user = newuser.objects.filter(student_id=user_id).first()
            if user:
                return user
        except jwt.JWTError:
            raise HttpError(401, "Invalid token")

    def is_authenticated(self, request):
        return bool(request.auth)

    def is_teacher(self, request):
        return request.auth and request.auth.is_teacher



# @api.post('/refresh_token', response={200: LoginSuccess}, auth=AuthBearer())
# def refresh_token(request):
#     try:
#         payload = jwt.decode(request.auth, JWT_SECRET_KEY, algorithms=["HS256"])
#         username = payload["sub"]
#         expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#         new_token = jwt.encode({"sub": username, "exp": expire}, JWT_SECRET_KEY, algorithm="HS256")
#         return {"username": username, "token": new_token}
#     except jwt.JWTError:
#         raise HttpError(401, "Invalid or expired token")
    

#user section
# @api.post('/register', response={201: User, 409: ErrorResponse}, auth=None)
# def register(request, info: User):
#     if newuser.objects.filter(student_id=info.student_id).exists():
#         return 409, {"message": "User already exists"}
#     new_user = newuser.objects.create(username=info.username, password=info.password, student_id=info.student_id)
#     return 201, {"username": new_user.username, "password": new_user.password, "student_id": new_user.student_id}

@api.post('/register', response={201: Me, 409: ErrorResponse}, auth=None)
def register(request, info: User):
    if newuser.objects.filter(student_id=info.student_id).exists():
        return 409, {"message": "User already exists"}
    hashed_password = make_password(info.password)
    new_user = newuser.objects.create(username=info.username, password=hashed_password, student_id=info.student_id)
    return 201, {"username": new_user.username, "student_id": new_user.student_id}






# @api.post('/login', response={200: LoginSuccess, 401: ErrorResponse}, auth=None)
# def login(request, info: User):
#     if newuser.objects.filter(username=info.username, password=info.password, student_id=info.student_id).exists():
#         expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
#         token = jwt.encode({"sub": info.username, "exp": expire}, JWT_SECRET_KEY, algorithm="HS256")
#         return {"username": info.username, "token": token}
#     return 401, {"message": "username or password is wrong"}


@api.get('/me', response={200: Me}, auth=AuthBearer())
def me(request):
    # username = request.auth
    # user = newuser.objects.get(username=username)
    student_id = request.auth
    user = newuser.objects.get(student_id=student_id)
    return 200, {"username": user.username, "student_id": user.student_id, "is_teacher": user.is_teacher}



@api.post('/login', response={200: LoginSuccess, 401: ErrorResponse}, auth=None)
def login(request, info: Login):
    # user = newuser.objects.filter(username=info.username).first()
    user = newuser.objects.filter(student_id=info.student_id).first()
    if user and check_password(info.password, user.password):
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode({"sub": user.student_id, "exp": expire}, JWT_SECRET_KEY, algorithm="HS256")
        return {"token": token, 'student_id': user.student_id}
    return 401, {"message": "Username or password is incorrect"}




@api.get('/num', response={200: List[User]}, auth=AuthBearer())
def mmm(request):
    return 200, list(newuser.objects.all().values())


@api.get('/num/{user_id}', response={200: User, 404: ErrorResponse}, auth=AuthBearer())
def one_user(request, user_id: int):
    try:
        user = newuser.objects.get(pk=user_id)
    except user.DoesNotExist:
        return 404, {"message": "User not found"}
    except ValueError:
        return 400, {"message": "Invalid user id"}
    return 200, user


@api.delete('/user', response={200: NoMessage, 404: ErrorResponse}, auth=AuthBearer())
def delete_user(request):
    user = request.auth
    user.delete()
    return 200, {"message": "User deleted"}


@api.patch('/user', response={200: User, 404: ErrorResponse}, auth=AuthBearer())
def update_user(request, info: UserChange):
    user = request.auth
    user.username = info.username
    user.password = make_password(info.password)
    user.save()
    return 200, user



#course section
# 所有成绩
# @api.get('/course', response={200: List[Course]}, auth=AuthBearer())
# def all_course(request):
#     return 200, list(course.objects.all().values())

#输入信息搜索课程
@api.get('/course', response={200: List[AvailableCourse]}, auth=AuthBearer())
def all_course(request):
    courses = course.objects.all()
    
    course_data = []
    for c in courses:
        if c.available:
            remaining_capacity = c.available.capacity - c.enrollment_set.count()
            year = c.available.year
            semester = c.available.semester
            registration_deadline = c.available.registration_deadline
        else:
            remaining_capacity = 0
            year = None
            semester = 'N/A'
            registration_deadline = None
        
        course_data.append({
            'course_id': c.course_id,
            'course_name': c.course_name,
            'teacher_name': c.teacher.username,
            'year': year or 0,  # 如果 year 为 None,则替换为 0
            'semester': semester,
            'remaining_capacity': remaining_capacity,
            'registration_deadline': registration_deadline.strftime("%Y-%m-%d") if registration_deadline else None
        })
    
    return 200, course_data

@api.get('/course/{course_id}', response={200: Course, 404: ErrorResponse}, auth=AuthBearer())
def one_course(request, course_id: int):
    try:
        course = course.objects.get(pk=course_id)
    except course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except ValueError:
        return 400, {"message": "Invalid course id"}
    return 200, course

# @api.post('/course', response={200: Course, 409: ErrorResponse}, auth=AuthBearer())
# def create_course(request, info: Course):
#     if course.objects.filter(course_id=info.course_id).exists():
#         return 409, {"message": "Course already exists"}
#     new_course = course.objects.create(course_id=info.course_id, course_name=info.course_name, teacher=user.objects.get(pk=info.teacher_id))
#     return 201, {"course_id": new_course.course_id, "course_name": new_course.course_name, "teacher": new_course.teacher}


# @api.post('/course', response={201: Course, 409: ErrorResponse}, auth=AuthBearer())
# def create_course(request, info: Course):
#     if not request.auth.is_authenticated:
#         raise HttpError(401, "Unauthorized")
#     if not request.auth.is_teacher:
#         raise HttpError(403, "Forbidden")
#     try:
#         # new_course = course.objects.create(course_id=info.course_id, course_name=info.course_name, teacher=request.auth)
#         # new_course = course.objects.create(course_id=info.course_id, course_name=info.course_name, teacher=request.user)
#         course_instance = course.objects.get(course_id=info.course_id)
#         student_instance = newuser.objects.get(student_id=info.student_id)
#     except course.DoesNotExist:
#         return 404, {"message": "Course not found"}
#     except newuser.DoesNotExist:
#         return 404, {"message": "Student not found"}

#     if grade.objects.filter(course=course_instance, student=student_instance).exists():
#         return 409, {"message": "Grade already exists"}

#     new_grade = grade.objects.create(course=course_instance, student=student_instance, score=info.score)
#     return 201, {
#         "course": new_grade.course.course_id,
#         "student": new_grade.student.student_id,
#         "score": new_grade.score
#     }

# how to create the id of course auto
def generate_course_id():
    last_course = course.objects.last()
    if last_course:
        last_id = last_course.course_id
        next_id = int(last_id) + 1
        return f"{next_id:03d}"
    else: 
        return "001"

@api.post('/course', response={201: Course, 409: ErrorResponse}, auth=AuthBearer())
def create_course(request, info: CourseChange):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")
    # if not info.course_id or not info.teacher_id:
    #     raise HttpError(422, "Missing required fields: course_id and teacher_id")

    try:
        new_course = course.objects.create(course_id=generate_course_id(), course_name=info.course_name, teacher=request.auth)
        # new_course = course.objects.create(course_id=info.course_id, course_name=info.course_name, teacher=request.user)
        # course_instance = course.objects.get(course_id=info.course_id)
        # student_instance = newuser.objects.get(student_id=info.student_id)
        return 201, {
            "course_id": new_course.course_id,
            "course_name": new_course.course_name,
            "teacher_id": new_course.teacher.student_id
        }
    except Exception as e:
        raise HttpError(400, str(e))
    # except course.DoesNotExist:
    #     return 404, {"message": "Course not found"}
    # except newuser.DoesNotExist:
    #     return 404, {"message": "Student not found"}

    # if grade.objects.filter(course=course_instance, student=student_instance).exists():
    #     return 409, {"message": "Grade already exists"}

    # new_grade = grade.objects.create(course=course_instance, student=student_instance, score=info.score)
    # return 201, {
    #     "course": new_grade.course.course_id,
    #     "student": new_grade.student.student_id,
    #     "score": new_grade.score
    # }

# user = User.objects.get(pk=info.teacher_id)  # Assuming you have a teacher_id field in the request
# new_course = course.objects.create(
#     course_id=info.course_id, course_name=info.course_name, teacher=user
# )

@api.post('/teacher/create_course', response={201: Course, 400: ErrorResponse}, auth=AuthBearer())
def create_teacher_course(request, info: CreateCourseSchema):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")
    try:
        new_course_id = generate_course_id() 
        available_instance = available(
            year=info.year,
            semester=info.semester,
            capacity=info.capacity,
            registration_deadline=info.registrationDeadline
        )
        available_instance.save()
        new_course = course.objects.create(
            course_id=new_course_id,
            course_name=info.name,
            teacher=request.auth,
            available=available_instance
        )
        return 201, new_course
    except Exception as e:
        return 400, {"message": "Error creating course: " + str(e)}


@api.delete('/course/{course_id}', response={200: NoMessage, 404: ErrorResponse}, auth=AuthBearer())
def delete_course(request, course_id: str):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")
    course_instance = course.objects.get(course_id=course_id)
    if not course_instance:
        return 404, {"message": "Course not found"}
    if course_instance.teacher != request.auth:
        raise HttpError(403, "Forbidden")
    course_instance.delete()
    return 200, {"message": "Course deleted"}


@api.patch('/course/{course_id}', response={200: Course, 404: ErrorResponse, 400: ErrorResponse}, auth=AuthBearer())
def update_course(request, course_id: str, info: CourseChange):
    if not request.auth.is_authenticated:
        return 401, {"message": "Unauthorized"}
    if not request.auth.is_teacher:
        return 403, {"message": "Forbidden"}
    try:
        course_instance = course.objects.get(course_id=course_id)
        if course_instance.teacher != request.auth:
            raise HttpError(403, "Forbidden")
        if info.course_name is not None:
            course_instance.course_name = info.course_name
        if info.year is not None and info.semester is not None:
            # Check if the available instance exists or create/update it
            if course_instance.available:
                available_instance = course_instance.available
            else:
                available_instance = available(year=info.year, semester=info.semester, capacity=info.capacity or 0)
                course_instance.available = available_instance
            available_instance.year = info.year
            available_instance.semester = info.semester
            available_instance.capacity = info.capacity
            available_instance.registration_deadline = info.registrationDeadline
            available_instance.save()
        course_instance.save()
        return 200, {
            "course_id": course_instance.course_id,
            "course_name": course_instance.course_name,
            "teacher_id": course_instance.teacher.student_id
        }
    except course.DoesNotExist:
        return 404, {"message": "Course not found"}
    except ValueError as e:
        return 400, {"message": str(e)}
    except Exception as e:
        return 400, {"message": "Unexpected error: " + str(e)}

#grade section 

# 所有成绩
# @api.get('/grade', response={200: List[Grade]}, auth=AuthBearer())
# def all_grade(request):
#     return 200, list(grade.objects.all().values())
#目前登录用户的成绩
@api.get('/grade', response={200: List[Grade]}, auth=AuthBearer())
def all_grade(request):
    user = request.auth  # Assuming you have access to the authenticated user
    grades = grade.objects.filter(student_id=user.student_id)  # Filter by authenticated user's student record
    return 200, list(grades.values())



@api.get('/grade/{grade_id}', response={200: Grade, 404: ErrorResponse}, auth=AuthBearer())
def one_grade(request, grade_id: int):
    try:
        grade = grade.objects.get(pk=grade_id)
    except grade.DoesNotExist:
        return 404, {"message": "Grade not found"}
    except ValueError:
        return 400, {"message": "Invalid grade id"}
    return 200, grade

@api.post('/grade', response={201: Grade, 409: ErrorResponse}, auth=AuthBearer())
def create_grade(request, info: Grade):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")

    try:
        enrollment_instance = enrollment.objects.get(course_id=info.course_id, student_id=info.student_id)
    except enrollment.DoesNotExist:
        return 404, {"message": "Enrollment not found"}

    grade_instance, created = grade.objects.get_or_create(enroll=enrollment_instance, defaults={'score': info.score})
    if not created:
        return 409, {"message": "Grade already exists"}

    return 201, {
        "course_id": enrollment_instance.course.course_id,
        "student_id": enrollment_instance.student.student_id,
        "score": grade_instance.score
    }
@api.delete('/grade/{grade_id}', response={200: NoMessage, 404: ErrorResponse}, auth=AuthBearer())
def delete_grade(request, grade_id: int):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")
    try:
        grade = grade.objects.get(pk=grade_id)
    except grade.DoesNotExist:
        return 404, {"message": "Grade not found"}
    except ValueError:
        return 400, {"message": "Invalid grade id"}
    grade.delete()
    return 200, {"message": "Grade deleted"}

@api.patch('/grade/{grade_id}', response={200: Grade, 404: ErrorResponse}, auth=AuthBearer())
def update_grade(request, grade_id: int, data: Grade):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")

    try:
        grade_instance = grade.objects.get(pk=grade_id)
    except grade.DoesNotExist:
        return 404, {"message": "Grade not found"}
    except ValueError:
        return 400, {"message": "Invalid grade id"}

    enrollment_instance = grade_instance.enroll
    grade_instance.score = data.score
    grade_instance.save()

    return 200, {
        "course_id": enrollment_instance.course.course_id,
        "student_id": enrollment_instance.student.student_id,
        "score": grade_instance.score
    }

@api.get('/teacher/courses', response={200: List[TeacherCourse]}, auth=AuthBearer())
def teacher_courses(request):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")
    
    courses = course.objects.filter(teacher=request.auth).select_related('available')

    result = []
    for c in courses:
        result.append({
            'course_id': c.course_id,
            'course_name': c.course_name,
            'semester': f"{c.available.year} {c.available.semester}" if c.available else "Not Set",
            'capacity': c.available.capacity if c.available else 0,
            'registration_deadline': c.available.registration_deadline.strftime("%Y-%m-%d") if c.available and c.available.registration_deadline else None
        })
    return 200, result


@api.post('/teacher/course', response={201: Course}, auth=AuthBearer())
def teacher_create_course(request, info: CreateCourse):
    if not request.auth.is_authenticated:
        raise HttpError(401, "Unauthorized")
    if not request.auth.is_teacher:
        raise HttpError(403, "Forbidden")
    
    available_instance = available.objects.create(year=info.year, semester=info.semester, capacity=info.capacity)
    new_course = course.objects.create(course_id=generate_course_id(), course_name=info.name, teacher=request.auth, available=available_instance)
    
    return 201, {
        "course_id": new_course.course_id,
        "course_name": new_course.course_name,
        "teacher_id": new_course.teacher.student_id
    }

@api.get('/course/{course_id}/students', response={200: List[EnrolledStudentInfo]}, auth=AuthBearer())
def get_enrolled_students(request, course_id: str):
    course_instance = course.objects.filter(course_id=course_id).first()
    if not course_instance:
        return 404, {"message": "Course not found"}

    enrolled_students = enrollment.objects.filter(course=course_instance).select_related('student')
    student_info = []
    for enroll in enrolled_students:
        try:
            grade_instance = enroll.grade
            score = grade_instance.score
            grade_id = grade_instance.id
        except enrollment.grade.RelatedObjectDoesNotExist:
            score = None
            grade_id = 0

        student_info.append({
            'student_id': enroll.student.student_id,
            'student_name': enroll.student.username,
            'score': score,
            'grade_id': grade_id
        })
    return 200, student_info
#enrollment section

@api.get('/enroll', response={200: List[EnrollmentDetail]}, auth=AuthBearer())
def all_enrollment(request):
    user = request.auth
    enrollments = enrollment.objects.filter(student_id=user.student_id).select_related('course', 'student', 'available')
    enrollment_data = []
    for enroll in enrollments:
        semester_value = enroll.semester or (enroll.available.semester if enroll.available else 'N/A')
        enrollment_data.append({
            'id': enroll.id,
            'course_id': str(enroll.course.course_id),
            'student_id': enroll.student.student_id,
            'course_name': enroll.course.course_name,  # 添加课程名称
            'teacher_name': enroll.course.teacher.username,  # 添加教师名称
            'semester': semester_value
        })
    return 200, enrollment_data

@api.post('/enroll', response={201: Enrollment, 400: ErrorResponse, 404: ErrorResponse, 409: ErrorResponse}, auth=AuthBearer())
def create_enrollment(request, info: Enrollment):
    course_instance = course.objects.filter(course_id=info.course_id).first()
    student_instance = newuser.objects.filter(student_id=info.student_id).first()
    available_instance = available.objects.filter(course=course_instance).first()

    if not course_instance or not student_instance or not available_instance:
        return 404, {"message": "Course, student, or available course not found"}

    if timezone.now().date() > available_instance.registration_deadline:
        return 400, {"message": "Registration deadline has passed"}

    if enrollment.objects.filter(course=course_instance, student=student_instance).exists():
        return 409, {"message": "Enrollment already exists"}

    if enrollment.objects.filter(course=course_instance).count() >= available_instance.capacity:
        return 400, {"message": "Course capacity reached"}

    new_enrollment = enrollment.objects.create(
    course=course_instance,
    student=student_instance,
    available=available_instance,
    semester=available_instance.semester  # 从 available 实例获取 semester 值
    )
    return 201, {
    "course_id": new_enrollment.course.course_id,
    "student_id": new_enrollment.student.student_id,
    "semester": new_enrollment.semester
    }

@api.delete('/enroll/{enroll_id}', response={200: NoMessage, 400: ErrorResponse, 404: ErrorResponse}, auth=AuthBearer())
def delete_enrollment(request, enroll_id: int):
    try:
        enrollment_instance = enrollment.objects.get(pk=enroll_id)
    except enrollment.DoesNotExist:
        return 404, {"message": "Enrollment not found"}
    
    if timezone.now().date() > enrollment_instance.available.registration_deadline:
        return 400, {"message": "Cannot drop the course after the registration deadline"}
    
    course_instance = enrollment_instance.course
    available_instance = course_instance.available
    
    enrollment_instance.delete()
    
    # 更新课程的剩余容量
    current_enrollment_count = enrollment.objects.filter(course=course_instance).count()
    available_instance.capacity = available_instance.capacity - current_enrollment_count
    available_instance.save()
    
    return 200, {"message": "Enrollment deleted"}

@api.patch('/enroll/{enroll_id}', response={200: Enrollment, 404: ErrorResponse}, auth=AuthBearer())
def update_enrollment(request, enroll_id: int, info: Enrollment):
    try:
        enrollment_instance = enrollment.objects.select_related('available').get(pk=enroll_id)
    except enrollment.DoesNotExist:
        return 404, {"message": "Enrollment not found"}
    except ValueError:
        return 400, {"message": "Invalid enrollment id"}

    # Update fields
    if info.semester:
        enrollment_instance.semester = info.semester
    if hasattr(info, 'registrationDeadline') and enrollment_instance.available:
        enrollment_instance.available.registration_deadline = info.registrationDeadline
        enrollment_instance.available.save()

    enrollment_instance.save()
    return 200, {
        'course_id': enrollment_instance.course.course_id,
        'student_id': enrollment_instance.student.student_id,
        'semester': enrollment_instance.semester,
        'registrationDeadline': enrollment_instance.available.registration_deadline if enrollment_instance.available else None
    }






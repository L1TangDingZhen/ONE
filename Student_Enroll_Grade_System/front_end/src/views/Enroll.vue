<template>
  <div class="enrollment-container">
    <div v-if="userRole === 'student'">
      <h2>Available Courses</h2>
      <table>
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Teacher Name</th>
            <th>Year</th>
            <th>Semester</th>
            <th>Remaining Capacity</th>
            <th>Registration Deadline</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in availableCourses" :key="course.course_id">
            <td>{{ course.course_id }}</td>
            <td>{{ course.course_name }}</td>
            <td>{{ course.teacher_name }}</td>
            <td>{{ course.year }}</td>
            <td>{{ course.semester }}</td>
            <td>{{ course.remaining_capacity }}</td>
            <td>{{ course.registration_deadline }}</td>
            <td>
              <button @click="enroll(course.course_id)" class="enroll-btn">Enroll</button>
            </td>
          </tr>
        </tbody>
      </table>

      <h2>My Courses</h2>
      <table>
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Teacher Name</th>
            <th>Semester</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="enrollment in myCourses" :key="enrollment.id">
            <td>{{ enrollment.courseId }}</td>
            <td>{{ enrollment.courseName }}</td>
            <td>{{ enrollment.teacherName }}</td>
            <td>{{ enrollment.semester }}</td>
            <td>
              <button @click="unenroll(enrollment.id)" class="unenroll-btn">Drop</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="userRole === 'teacher'">
      <h2>My Courses</h2>
      <table>
        <thead>
          <tr>
            <th>Course ID</th>
            <th>Course Name</th>
            <th>Semester</th>
            <th>Capacity</th>
            <th>Registration Deadline</th>

            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="course in teacherCourses" :key="course.course_id">
            <td>{{ course.course_id }}</td>
            <td>{{ course.course_name }}</td>
            <td>{{ course.year }} {{ course.semester }}</td>
            <td>{{ course.capacity }}</td>
            <td>{{ course.registration_deadline }}</td>
            <td>
              <button @click="viewStudents(course.course_id)">View Students</button>
              <button @click="editCourse(course.course_id)">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>

      <button @click="openCreateCourseModal" class="create-course-btn">Create Course</button>
      
      <div v-if="showCreateCourseModal" class="modal">
        <div class="modal-overlay" @click="closeCreateCourseModal"></div>
        <div class="modal-content">
          <h3>Create Course</h3>
          <form @submit.prevent="createCourse">
            <input v-model="newCourse.name" placeholder="Course Name" required>
            <select v-model="newCourse.year" required>
              <option value="">Select Year</option>
              <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
            </select>
            <select v-model="newCourse.semester" required>
              <option value="">Select Semester</option>
              <option value="Semester1">Semester 1</option>
              <option value="Semester2">Semester 2</option>
              <option value="Summer School">Summer School</option>
              <option value="Winter School">Winter School</option>
              <option value="Trimester1">Trimester 1</option>
              <option value="Trimester2">Trimester 2</option>
              <option value="Trimester3">Trimester 3</option>
            </select>
            <input v-model="newCourse.registrationDeadline" type="date" placeholder="Registration Deadline" required>
            <input v-model="newCourse.capacity" type="number" placeholder="Capacity" required>
            <button type="submit">Create</button>
            <button type="button" @click="closeCreateCourseModal">Cancel</button>
          </form>
        </div>
      </div>



      <div v-if="editCourseModal.show" class="modal">
        <div class="modal-content">
          <h3>Edit Course</h3>
          <form @submit.prevent="updateCourse">
            <select v-model="editCourseModal.year" required>
              <option value="">Select Year</option>
              <option v-for="year in availableYears" :key="year" :value="year">{{ year }}</option>
            </select>
            <select v-model="editCourseModal.semester" required>
              <option value="">Select Semester</option>
              <option value="Semester1">Semester 1</option>
              <option value="Semester2">Semester 2</option>
              <option value="Summer School">Summer School</option>
              <option value="Winter School">Winter School</option>
              <option value="Trimester1">Trimester 1</option>
              <option value="Trimester2">Trimester 2</option>
              <option value="Trimester3">Trimester 3</option>
            </select>
          <input v-model="editCourseModal.registrationDeadline" type="date" placeholder="Registration Deadline" required>
            <input v-model="editCourseModal.capacity" type="number" placeholder="Capacity" required>
            <button type="submit">Update</button>
            <button type="button" @click="editCourseModal.show = false">Cancel</button>
          </form>
        </div>
      </div>


      <div v-if="showEnrolledStudentsModal" class="modal">
        <div class="modal-content">
          <h3>Enrolled Students</h3>
          <ul>
            <li v-for="student in enrolledStudents" :key="student">{{ student }}</li>
          </ul>
          <button @click="showEnrolledStudentsModal = false">Close</button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { reqCourseList, reqEnrollList, reqCreateEnroll, reqDeleteEnroll, reqMe, reqTeacherCourses, reqCreateCourse, reqEnrolledStudents, reqUpdateCourseInfo, reqCreateTeacherCourse } from '../api/all';

const availableCourses = ref([]);
const myCourses = ref([]);
const teacherCourses = ref([]);
const userRole = ref('student');
const currentStudentId = ref('');
const showCreateCourseModal = ref(false);
const enrolledStudents = ref([]);
const showEnrolledStudentsModal = ref(false);
const newCourse = ref({
  name: '',
  year: '',
  semester: '',
  capacity: 0,
  registrationDeadline: ''
});

const editCourseModal = ref({
  show: false,
  courseId: '',
  year: '',
  semester: '',
  capacity: 0,
  registrationDeadline: ''
});


const availableYears = ref([2024, 2025]); // 可根据需要调整可选年份

const openCreateCourseModal = () => {
  showCreateCourseModal.value = true;
};

const closeCreateCourseModal = () => {
  showCreateCourseModal.value = false;
};

const fetchTeacherCourses = async () => {
  try {
    const response = await reqTeacherCourses();
    teacherCourses.value = response.data;
  } catch (error) {
    console.error('Error fetching teacher courses:', error);
  }
};


const createCourse = async () => {
  try {
    await reqCreateTeacherCourse({
      name: newCourse.value.name,
      year: newCourse.value.year,
      semester: newCourse.value.semester,
      capacity: newCourse.value.capacity,
      registrationDeadline: newCourse.value.registrationDeadline
    });
    closeCreateCourseModal();
    fetchTeacherCourses();
  } catch (error) {
    console.error('Error creating course:', error);
  }
};


const fetchUserRole = async () => {
  try {
    const response = await reqMe();
    userRole.value = response.data.is_teacher ? 'teacher' : 'student';
    currentStudentId.value = response.data.student_id;
  } catch (error) {
    console.error('Error fetching user role:', error);
  }
};

const fetchCourses = async () => {
  try {
    const response = await reqCourseList();
    availableCourses.value = response.data;
  } catch (error) {
    console.error('Error fetching available courses:', error);
  }
};


const fetchMyCourses = async () => {
  try {
    const response = await reqEnrollList();
    myCourses.value = response.data.map(enrollment => ({
      id: enrollment.id,
      courseId: enrollment.course_id,
      courseName: enrollment.course_name,
      teacherName: enrollment.teacher_name,
      semester: enrollment.semester
    }));
  } catch (error) {
    console.error('Error fetching my courses:', error);
  }
};


const enroll = async (courseId) => {
  try {
    const course = availableCourses.value.find(c => c.course_id === courseId);
    const alreadyEnrolled = myCourses.value.some(enrollment => enrollment.courseId === courseId);

    if (alreadyEnrolled) {
      console.log('You have already enrolled in this course');
      return;
    }

    await reqCreateEnroll({
      course_id: courseId, 
      student_id: currentStudentId.value, 
      semester: course.semester
    });
    fetchMyCourses();
    fetchCourses();
  } catch (error) {
    console.error('Failed to enroll:', error);
  }
};



const unenroll = async (enrollmentId) => {
  try {
    await reqDeleteEnroll(enrollmentId);
    fetchMyCourses();
    fetchCourses();
  } catch (error) {
    console.error('Failed to unenroll:', error);
  }
};

onMounted(async () => {
  await fetchUserRole();
  if (userRole.value === 'student') {
    fetchCourses();
    fetchMyCourses();
  } else if (userRole.value === 'teacher') {
    fetchTeacherCourses();
  }
});

const deleteCourse = async (id) => {
  if (confirm('Are you sure you want to delete this course?')) {
    try {
      await reqDeleteCourse(id);
      await fetchCourses();
    } catch (error) {
      console.error('Error deleting course:', error);
    }
  }
};


const viewStudents = async (courseId) => {
  try {
    const response = await reqEnrolledStudents(courseId);
    enrolledStudents.value = response.data;
    // 显示学生名单的模态框
    showEnrolledStudentsModal.value = true;
  } catch (error) {
    console.error('Error fetching enrolled students:', error);
  }
};


const editCourse = (courseId) => {
  const course = teacherCourses.value.find(c => c.course_id === courseId);
  if (course) {
    editCourseModal.value.show = true;
    editCourseModal.value.courseId = courseId;
    editCourseModal.value.name = course.course_name;
    editCourseModal.value.year = course.semester.split(' ')[0]; // 提取年份
    editCourseModal.value.semester = course.semester.split(' ')[1]; // 提取学期
    editCourseModal.value.capacity = course.capacity;
    editCourseModal.value.registrationDeadline = course.registration_deadline;
  }
};



const updateCourse = async () => {
  try {
    await reqUpdateCourseInfo(editCourseModal.value.courseId, {
      course_name: editCourseModal.value.name,
      year: editCourseModal.value.year,
      semester: editCourseModal.value.semester,
      capacity: editCourseModal.value.capacity,
      registrationDeadline: editCourseModal.value.registrationDeadline
    });
    editCourseModal.value.show = false;
    await fetchTeacherCourses(); // 重新获取教师的课程列表
  } catch (error) {
    console.error('Error updating course:', error);
  }
};



</script>

<style scoped>

table {
  width: 100%;
  border-collapse: collapse; /* Ensures that the border spacing is collapsed */
  background-color: #111;
  /* You can also remove the cell padding if needed */
  /* padding: 0; */
}


tbody tr td:first-child {
  border-left: none;
}


tbody td {
  border: none;
}


thead th {
  /* border-bottom: 2px solid #222; */
  border-bottom: none;
}
  /* the line top of course id  */
thead th:first-child {
  border-top: 1px solid #fff;
}

/* the line top of course name */
thead th:not(:first-child) {
  border-top: 1px solid #fff;
}


tbody {
  background-color: #111;

}

table thead th {
  background-color: #111; /*black background */
  /* color: #111; white text color */
}


/* Add your styles here */
tbody tr:nth-child(odd) {
  background-color: #111;
}

tbody tr:nth-child(even) {
  background-color: #111;
}

.enrollment-container {
  display: flex;
  flex-direction: column;
  background-color: #111;
  gap: 20px;
}

table {
  width: 100%;
  border-collapse: collapse; /* Collapses the border so it becomes one single line instead of two */
  background-color: #111;
  /* No border spacing */
}

/* Remove borders from all table cells */
th, td {
  border: none;
}

/* the line under course id*/
thead th {
  border-bottom: none; 
}

/* Ensure the first row cells in tbody do not have any borders */
tbody tr:first-child td {
  border-top: none;
}


.modal-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
  background-color: #111;
  padding: 20px;
  border-radius: 4px;
  z-index: 1000;
}
</style>
<template>
  <div class="teacher-grades-container">
    <h1>My Courses</h1>
    <table>
      <thead>
        <tr>
          <th>Course ID</th>
          <th>Course Name</th>
          <th>Semester</th>
          <th>Capacity</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in teacherCourses" :key="course.course_id">
          <td>{{ course.course_id }}</td>
          <td>{{ course.course_name }}</td>
          <td>{{ course.semester }}</td>
          <td>{{ course.capacity }}</td>
          <td>
            <button @click="viewStudents(course.course_id)">View Students</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="showStudentsModal" class="modal">
      <div class="modal-content">
        <h3>Students</h3>
        <table>
          <thead>
            <tr>
              <th>Student ID</th>
              <th>Student Name</th>
              <th>Score</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in enrolledStudents" :key="student.student_id">
              <td>{{ student.student_id }}</td>
              <td>{{ student.student_name }}</td>
              <td>{{ student.score }}</td>
              <td>
                <button @click="editScore(student.student_id, student.grade_id)">Edit Score</button>
              </td>
            </tr>
          </tbody>
        </table>
        <button @click="closeModal">Close</button>
      </div>
    </div>

    <div v-if="showEditScoreModal" class="modal">
      <div class="modal-content">
        <h3>Edit Score</h3>
        <form @submit.prevent="updateScore">
          <label>
            Score:
            <input v-model="editedScore" type="number" step="0.01" required>
          </label>
          <button type="submit">Save</button>
          <button type="button" @click="closeEditScoreModal">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { reqTeacherCourses, reqEnrolledStudents, reqUpdateGrade, reqCreateGrade } from '../api/all';

const teacherCourses = ref([]);
const enrolledStudents = ref([]);
const showStudentsModal = ref(false);
const showEditScoreModal = ref(false);
const editedStudentId = ref('');
const editedScore = ref(0);
const editedGradeId = ref('');

onMounted(async () => {
  try {
    const response = await reqTeacherCourses();
    teacherCourses.value = response.data;
  } catch (error) {
    console.error('Error fetching teacher courses:', error);
  }
});

const viewStudents = async (courseId) => {
  try {
    const response = await reqEnrolledStudents(courseId);
    enrolledStudents.value = response.data.map(student => ({
      student_id: student.student_id,
      student_name: student.student_name,
      score: student.score,
      course_id: courseId,
      grade_id: student.grade_id  // 添加 grade_id 字段
    }));
    showStudentsModal.value = true;
  } catch (error) {
    console.error('Error fetching enrolled students:', error);
  }
};

const editScore = (studentId, gradeId) => {
  const student = enrolledStudents.value.find(s => s.student_id === studentId);
  if (student) {
    editedStudentId.value = studentId;
    editedScore.value = student.score;
    editedGradeId.value = gradeId;
    showEditScoreModal.value = true;
  }
};

const closeEditScoreModal = () => {
  showEditScoreModal.value = false;
  editedStudentId.value = '';
  editedScore.value = 0;
};

const updateScore = async () => {
  try {
    const studentId = editedStudentId.value;
    const student = enrolledStudents.value.find(s => s.student_id === studentId);
    const courseId = student.course_id;

    const data = {
      course_id: courseId,
      student_id: studentId,
      score: editedScore.value
    };

    if (student.grade_id) {
      // 使用 PATCH 请求更新成绩
      await reqUpdateGrade(data, student.grade_id);
    } else {
      // 使用 POST 请求创建成绩
      await reqCreateGrade(data);
    }

    // 更新前端展示的成绩
    if (student) {
      student.score = editedScore.value;
    }
    closeEditScoreModal();
  } catch (error) {
    console.error('Error updating score:', error);
  }
};

</script>

<style scoped>
/* Add your styles here */
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

.teacher-grades-container {
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




<template>
  <div class="courses-container">
    <select v-model="searchField">
      <option value="course_id">Course ID</option>
      <option value="course_name">Course Name</option>
      <option value="teacher_id">Teacher ID</option>
    </select>
    <input v-model="searchTerm" @input="filterCourses" placeholder="Search courses..." class="search-bar">
    <button v-if="userRole === 'teacher'" @click="showAddCourseModal" class="add-course-btn">Add Course</button>
    <table>
      <thead>
        <tr>
          <th>Course ID</th>
          <th>Course Name</th>
          <th>Teacher Name</th>
          <th v-if="userRole === 'teacher'">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="course in filteredCourses" :key="course.course_id">
          <td>{{ course.course_id }}</td>
          <td>{{ course.course_name }}</td>
          <td>{{ course.teacher_name  }}</td>
          <td v-if="userRole === 'teacher'">
            <button v-if="course.teacher_name === userInfo.username" @click="editCourse(course.course_id)" class="edit-btn">Edit</button>
            <button v-if="course.teacher_name === userInfo.username" @click="confirmDelete(course.course_id)" class="delete-btn">Delete</button>
          </td>
        </tr>
      </tbody>
      <div v-if="showEditModal" class="modal">
        <div class="modal-content">
          <h2>Edit Course</h2>
          <span class="close" @click="closeEditModal">&times;</span>
          <form @submit.prevent="updateCourse(editedCourseId)">
            <input v-model="editedCourseName" placeholder="Course Name" required>
            <button type="submit" class="save-btn">Update</button>
          </form>
        </div>
      </div>
    </table>

    <!-- Add this modal for creating a new course -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Add Course</h2>
        <span class="close" @click="closeModal">&times;</span>
        <form @submit.prevent="addCourse">
          <input v-model="newCourseName" placeholder="Course Name" required>
          <button type="submit" class="add-btn">Add</button>
        </form>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import { reqMe, reqCourseList, reqDeleteCourse, reqCreateCourse, reqUpdateCourse } from '../api/all';

const courses = ref([]);
const filteredCourses = ref([]);
const searchTerm = ref('');
const userRole = ref('student');
const userInfo = ref(null);
const showModal = ref(false);
const newCourseName = ref('');
const searchField = ref('course_name');
const showEditModal = ref(false);
const editedCourseId = ref('');
const editedCourseName = ref('');

const fetchUserRole = async () => {
  try {
    const response = await reqMe();
    userRole.value = response.data.is_teacher ? 'teacher' : 'student';
  } catch (error) {
    console.error('Error fetching user role:', error);
  }
};

const fetchCourses = async () => {
  try {
    const response = await reqCourseList();
    courses.value = response.data;
    filterCourses();
  } catch (error) {
    console.error('Error fetching courses:', error);
  }
};

onMounted(async () => {
  await fetchUserRole();
  await fetchCourses();
  await fetchUserInfo();
});


const filterCourses = () => {
  filteredCourses.value = courses.value.filter(course =>
    course[searchField.value].toString().toLowerCase().includes(searchTerm.value.toLowerCase())
  );
};

const fetchUserInfo = async () => {
  try {
    const response = await reqMe();
    userInfo.value = response.data;
  } catch (error) {
    console.error('Error fetching user info:', error);
  }
};

const addCourse = async () => {
  try {
    await reqCreateCourse({ course_name: newCourseName.value, teacher_id: userInfo.value.student_id });
    // await reqCreateCourse({ course_name: newCourseName.value});
    newCourseName.value = '';
    showModal.value = false;
    await fetchCourses();
  } catch (error) {
    console.error('Error creating course:', error);
  }
};


const showAddCourseModal = () => {
  // Logic to display a modal for adding a course
  showModal.value = true;
  console.log('Show add course modal');
};


const deleteCourse = async (id) => {
  try {
    await reqDeleteCourse(id);
    await fetchCourses(); // Refresh list after deletion
  } catch (error) {
    console.error('Error deleting course:', error);
  }
};

const closeModal = () => {
  showModal.value = false;
};

const editCourse = (courseId) => {
  const courseToEdit = courses.value.find((course) => course.course_id === courseId);
  if (courseToEdit) {
    editedCourseId.value = courseId;
    editedCourseName.value = courseToEdit.course_name;
    showEditModal.value = true;
  } else {
    console.error('Course with id ' + courseId + ' not found.');
  }
};


const updateCourse = async (courseId) => {
  try {
    await reqUpdateCourse({ course_name: editedCourseName.value }, courseId);
    editedCourseName.value = ''; // Clear the input after successful update
    showEditModal.value = false;
    await fetchCourses();
  } catch (error) {
    console.error('Error updating course:', error);
  }
};
const closeEditModal = () => {
  showEditModal.value = false;
};
const confirmDelete = async (courseId) => {
  if (confirm('Are you sure you want to delete this course?')) {
    await deleteCourse(courseId);
  }
};


</script>

<style scoped>
body {
  background-color: #222;
  color: #222;
}

table {
  background-color: #222 ;
  width: 100%;
  border-collapse: collapse;

}

.courses-container {
  margin-bottom: 20px;
}

.search-bar {
  margin-bottom: 10px;
}

/* tbody tr:nth-child(odd) {
  background-color: #111;
} */

tbody tr:nth-child(odd) {
  background-color: #222;
}
tbody tr:nth-child(even) {
  background-color: #222;
}

.add-course-btn {
  background-color: green;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #111; /* 设置表格背景颜色与页面背景一致 */
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #222;
}

thead th {
  border-bottom: 2px solid #222;
  background-color: #222; /* 设置表头背景颜色 */
}

tbody td {
  border-bottom: 1px solid #222; /* Make bottom border the same as background */
}

thead th:last-child {
  border-bottom: none;
}

td {
  border: none; /* Remove all borders from table cells */
}

tbody tr:last-child td {
  border-bottom: none; /* Removes the border from the last row */
}



/* You may also want to remove the left and right borders on all cells */
th, td {
  border-left: none;
  border-right: none;
}

.edit-btn {
  background-color: yellow;
  color: black;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
}

.delete-btn {
  background-color: red;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  color: #000;
}

.close {
  color: #aaaaaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}


.edit-btn {
  background-color: #ffc107;
  color: black;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 5px;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.save-btn {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

.add-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}

</style>
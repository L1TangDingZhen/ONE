<template>
  <div class="my-container">
    <h1>My Profile</h1>
    <div v-if="userInfo" class="user-info">
      <p><strong>Username:</strong> {{ userInfo.username }}</p>
      <p><strong>Student ID:</strong> {{ userInfo.student_id }}</p>
      <!-- 其他用户信息 -->
    </div>
    <div class="navigation-buttons">
    <button @click="goToCourses" class="nav-button">My Courses</button>
    <button @click="goToEnroll" class="nav-button">Enroll</button>
    <button @click="goToGrades" class="nav-button">My Grades</button>
  </div>
  <div class="action-buttons">
    <button @click="updateAccount" class="nav-button">Update Profile</button>
    <button @click="deleteAccount" class="delete-button">Delete Account</button>
    <button @click="logout" class="logout-button">Log Out</button>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { reqMe, reqDelete, reqUpdate } from '../api/all';

const userInfo = ref(null);
const router = useRouter();

onMounted(async () => {
  try {
    const response = await reqMe();
    userInfo.value = response.data;  // 假设后端直接返回用户信息对象
  } catch (error) {
    console.error('Error fetching user info:', error);
    // 处理错误，比如跳转到登录页
    router.push('/login');
  }
});


const deleteAccount = async () => {
  if (confirm("Are you sure you want to delete your account?")) {
    try {
      await reqDelete();
      localStorage.removeItem('token');
      router.push('/login');
    } catch (error) {
      console.error('Error deleting account:', error);
      // 处理错误,如显示错误消息
    }
  }
};

const updateAccount = async () => {
  const newUsername = prompt("Enter new username:");
  const newPassword = prompt("Enter new password:");
  const confirmPassword = prompt("Confirm new password:");

  if (newPassword !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  try {
    await reqUpdate({ username: newUsername, password: newPassword });
    alert("Account updated successfully!");
  } catch (error) {
    console.error('Error updating account:', error);
    // 处理错误,如显示错误消息
  }
};

const logout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

const goToCourses = () =>  router.push({ name: 'course' });
const goToEnroll = () =>  router.push({ name: 'enroll' });
const goToGrades = () => router.push({ name: 'grade' });
</script>

<style scoped>
.my-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  text-align: center;
  color: #333; /* Default text color */
}

/* 更新了导航和行动按钮的样式 */
.navigation-buttons,
.action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 0px; /* Add some space above the button group */
}

.nav-button,
.delete-button {
  flex: 1; /* Make buttons take equal space */
  margin: 5px; /* Add space between buttons */
  padding: 10px; /* Add padding for better appearance */
  cursor: pointer;
  border: none; /* Remove border */
}

.nav-button {
  background-color: #42b983; /* Green background */
  color: white; /* White text */
}

.nav-button:hover {
  background-color: #333; /* Darker background on hover */
}

.delete-button {
  background-color: #d9534f; /* Bootstrap's btn-danger color */
  color: white; /* White text */
}

.delete-button:hover {
  background-color: #c9302c; /* Darker red on hover */
}

/* 用户信息的样式 */
.user-info {
  margin-bottom: 20px; /* Space below user info */
}

.user-info strong {
  color: #333; /* Same color as the container text */
}

/* 移除了p元素的color属性，因为不再需要特别指定红色 */
p {
  margin-top: 10px;
}


.logout-button {
  background-color: #ffc107; /* Bootstrap's yellow color for warning buttons */
  color: #333; /* Dark text for contrast */
  border: none; /* No border for consistency with other buttons */
  margin: 5px; /* Same margin as other buttons for consistent spacing */
  padding: 10px; /* Same padding as other buttons for consistent size */
  cursor: pointer; /* Cursor pointer to indicate it's clickable */
}

.logout-button:hover {
  background-color: #e0a800; /* Darker yellow on hover */
}
/* 其他样式保持不变 */
</style>

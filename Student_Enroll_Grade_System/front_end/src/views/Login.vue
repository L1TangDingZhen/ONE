<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div class="form-group">
          <label for="student-id">Student ID:</label>
          <input id="student-id" v-model="credentials.student_id" type="text" placeholder="Enter student ID" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input id="password" v-model="credentials.password" type="password" placeholder="Enter password" required>
      </div>
      <button type="submit">Login</button>
      <button type = 'button' @click="register">Register</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { reqLogin, reqRegister } from '../api/all.ts';  // 确保路径正确
import { useRouter } from 'vue-router';

const router = useRouter();

const credentials = ref({
  password: '',
  student_id: ''  // 添加 student_id
});
const errorMessage = ref('');


// const router = useRouter();

const login = async () => {
  try {
    const response = await reqLogin(credentials.value);
    // 处理登录成功，如保存 token，跳转等
    localStorage.setItem('token', response.data.token); // 保存 token
    router.push('/my');  // 导航到 home 路由
  } catch (error) {
    console.error('Login error:', error);
    // 在界面上显示错误提示
    errorMessage.value = 'Login failed, please try again';
    console.error('Login error:', error);
  }
};

const register = async () => {
  try {
    router.push('/register'); // Redirect to Register.vue route
  } catch (error) {
    console.error('Register error:', error);
    // 在界面上显示错误提示
    errorMessage.value = 'Register failed, please try again';
  }
};

</script>

<style scoped>
.login-container {
  max-width: 300px;
  margin: auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #333;
}

p {
  color: red;
  margin-top: 10px;
}
</style>

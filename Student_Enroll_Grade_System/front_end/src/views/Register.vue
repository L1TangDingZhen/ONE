<template>
    <div class="register-container">
      <h1>Register</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="student-id">Student ID:</label>
          <input id="student-id" v-model="userInfo.student_id" type="text" placeholder="Enter student ID" required>
        </div>
        <div class="form-group">
          <label for="username">Username:</label>
          <input id="username" v-model="userInfo.username" type="text" placeholder="Enter username" required>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input id="password" v-model="userInfo.password" type="password" placeholder="Enter password" required>
        </div>
        <div class="form-group">
          <label for="confirm-password">Confirm Password:</label>
          <input id="confirm-password" v-model="confirmPassword" type="password" placeholder="Confirm password" required>
        </div>
        <button type="submit">Register</button>
        <p v-if="errorMessage">{{ errorMessage }}</p>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { reqRegister } from '../api/all.ts';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  const userInfo = ref({
    student_id: '',
    username: '',
    password: '',
  });
  const confirmPassword = ref('');
  const errorMessage = ref('');
  
  const handleRegister = async () => {
    if (userInfo.value.password !== confirmPassword.value) {
      errorMessage.value = "Passwords do not match";
      return;
    }
  
    try {
      const response = await reqRegister(userInfo.value);
      console.log('Registration successful:', response);
      // Assume token is part of the successful response
      router.push({ name: 'login' }); // Stay on the registration page
    } catch (error) {
      console.error('Registration error:', error);
      errorMessage.value = error.response.data.message || 'Registration failed, please try again';
    }
  };
  </script>
  
  <style scoped>
  .register-container {
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
  
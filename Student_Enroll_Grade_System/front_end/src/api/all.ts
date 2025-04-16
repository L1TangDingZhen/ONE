
import request from "./request"
import axios from 'axios';

console.log("^^^^^^^6666^^^^^^^")
// console.log('Base API URL:', process.env.VUE_APP_API_BASE_URL);

// 获取环境变量中的API基础URL
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/student';

// 修改apiClient配置
const apiClient = axios.create({
    headers: {
        'Content-Type': 'application/json'
    }
});

export default apiClient;


// 账户
export function reqRegister(data:any){
    return apiClient.post(`${API_BASE_URL}/register`, data);
}

export function reqLogin(credentials:any){
    return apiClient.post(`${API_BASE_URL}/login`, credentials);
}

export function reqMe(){
    return apiClient.get(`${API_BASE_URL}/me`,
    {headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}});
}

export function reqAll(){
    return apiClient.get(`${API_BASE_URL}/num`,
    {headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}});
}

export function reqDelete(id:number){
    return apiClient.delete(`${API_BASE_URL}/user`,
    {headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}});
    // return request({url:`/api/num/${id}`, method:'delete'})
}

export function reqUpdate(data:any){
    return apiClient.patch(`${API_BASE_URL}/user`, data,
    {headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}});
    // return request({url:`/api/num`, method:'patch', data:data})
}

//课程

export function reqCourseList(){
    return apiClient.get(`${API_BASE_URL}/course`, {
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
}

export function reqCourseListOne(id:number){
    return apiClient.get(`${API_BASE_URL}/course/${id}`, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
}

export function reqCreateCourse(data:any){

    return apiClient.post(`${API_BASE_URL}/course`, data, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/course`, method:'post', data:data})
}

export function reqDeleteCourse(id:number){
    return apiClient.delete(`${API_BASE_URL}/course/${id}`, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/course/${id}`, method:'delete'})
}


export function reqUpdateCourse(data:any, id:number){
    return apiClient.patch(`${API_BASE_URL}/course/${id}`, data, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/course/${id}`, method:'patch', data:data})
}

//grade

export function reqGradeList(){
    return apiClient.get(`${API_BASE_URL}/grade`, {
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/grade`, method:'get'})
}

export function reqGradeListOne(id:number){
    return apiClient.get(`${API_BASE_URL}/grade/${id}`, {
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/grade/${id}`, method:'get'})
}

export function reqCreateGrade(data: any) {
    return apiClient.post(`${API_BASE_URL}/grade`, data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
  }

export function reqDeleteGrade(id:number){

    return apiClient.delete(`${API_BASE_URL}/grade/${id}`, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/grade/${id}`, method:'delete'})
}
export function reqUpdateGrade(data: any, gradeId: number) {
    return apiClient.patch(`${API_BASE_URL}/grade/${gradeId}`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
}

//enroll
export function reqEnrollList(){
    return apiClient.get(`${API_BASE_URL}/enroll`, {
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/enroll`, method:'get'})
}

export function reqCreateEnroll(data:any){
    return apiClient.post(`${API_BASE_URL}/enroll`, data, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
}

export function reqDeleteEnroll(id:number){
    return apiClient.delete(`${API_BASE_URL}/enroll/${id}`, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    }); 

    // return request({url:`/api/enroll/${id}`, method:'delete'})
}

export function reqUpdateEnroll(data:any, id:number){
    return apiClient.patch(`${API_BASE_URL}/enroll/${id}`, data, { 
        headers: {Authorization: `Bearer ${localStorage.getItem('token')}`}
    });
    // return request({url:`/api/enroll/${id}`, method:'patch', data:data})
}

export function reqTeacherCourses(){
    // Replace with your actual endpoint and logic to fetch the teacher's courses
    return apiClient.get(`${API_BASE_URL}/teacher/courses`, { 
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
}

export function reqEnrolledStudents(courseId: string) {
    return apiClient.get(`${API_BASE_URL}/course/${courseId}/students`,{
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
}

export function reqUpdateCourseInfo(courseId: string, data: any) {
    return apiClient.patch(`${API_BASE_URL}/course/${courseId}`, data, {
      headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
  }

export function reqCreateTeacherCourse(data: any) {
    return apiClient.post(`${API_BASE_URL}/teacher/create_course`, data, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
    });
    }
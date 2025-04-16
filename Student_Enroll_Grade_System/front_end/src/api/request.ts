import axios from 'axios'
import { ElMessageBox, ElMessage } from 'element-plus'

// 创建axios实例
const service = axios.create({
  // baseURL: 'http://127.0.0.1:8000/api', // url = base url + request url
  // withCredentials: true, // send cookies when cross-domain requests
  timeout: 5000 // request timeout
})

//请求拦截器：携带的token字段
service.interceptors.request.use(
  config => {
    // do something before request is sent
    config.headers = config.headers || {}
    if (localStorage.getItem('token')) {
      config.headers.token = localStorage.getItem('token') || ''
    }
    return config
  },
  error => {
    // do something with request error
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

//响应拦截器
service.interceptors.response.use(
  async response => {
    if (response.status !== 201 && response.status != 200) {
      ElMessage({
        message: response.statusText || 'Error',
        type: 'error',
        duration: 5 * 1000
      })

      if (response.status === 404 || response.status === 50012 || response.status === 50014) {
        await ElMessageBox.confirm('You have been logged out, you can cancel to stay on this page, or log in again', 'Confirm logout', {
          confirmButtonText: 'Re-Login',
          cancelButtonText: 'Cancel',
          type: 'warning'
        })
        localStorage.dispatch('user/resetToken').then(() => {
          location.reload()
        })
      }
      return Promise.reject(new Error('Response error'))
    } else {
      return Promise.resolve(response)
    }
  },

  error => {
    console.log('err' + error) // for debug
    ElMessage({
      message: error.message,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service

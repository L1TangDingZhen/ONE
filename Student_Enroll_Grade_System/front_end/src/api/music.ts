// 获取音乐列表的接口
import request from "./request"
// /api/musics
export function reqMusicList() {
    return request({url: `/musics`, method: `get`})
}

// 查询单个
export function reqMusicListOne(id:number) {
    return request({url: `/musics/${id}`, method: `get`})
}

// 删除
export function reqDeleteMusic(id:number) {
    return request({url: `/musics/${id}`, method: `delete`})
}

// 增加或者修改
export function reqAddOrUpdateMusic(music:any, index:number){
    if (index != 0){
        return request({url:`musics/update/${index}`, method:'put', data:music})
    }else{
      //新增品牌
      return request({ url: '/musics', method: 'post', data: music });  
    }
}



// 账户
export function reqRegister(data:any){
    return request({url:`/register`, method:'post', data:data})
}

export function reqLogin(data:any){
    return request({url:`/login`, method:'post', data:data})
}

export function reqDelete(id:number){
    return request({url:`/num/${id}`, method:'delete'})
}

export function reqUpdate(data:any){
    return request({url:`/num`, method:'patch', data:data})
}

//课程

export function reqCourseList(){
    return request({url:`/course`, method:'get'})
}

export function reqCourseListOne(id:number){
    return request({url:`/course/${id}`, method:'get'})
}

export function reqCreateCourse(data:any){
    return request({url:`/course`, method:'post', data:data})
}

export function reqDeleteCourse(id:number){
    return request({url:`/course/${id}`, method:'delete'})
}


export function reqUpdateCourse(data:any, id:number){
    return request({url:`/course/${id}`, method:'patch', data:data})
}

//grade

export function reqGradeList(){
    return request({url:`/grade`, method:'get'})
}

export function reqGradeListOne(id:number){
    return request({url:`/grade/${id}`, method:'get'})
}

export function reqCreateGrade(data:any){
    return request({url:`/grade`, method:'post', data:data})
}

export function reqDeleteGrade(id:number){
    return request({url:`/grade/${id}`, method:'delete'})
}

export function reqUpdateGrade(data:any, id:number){
    return request({url:`/grade/${id}`, method:'patch', data:data})
}

//enroll
export function reqEnrollList(){
    return request({url:`/enroll`, method:'get'})
}

export function reqCreateEnroll(data:any){
    return request({url:`/enroll`, method:'post', data: data})
}

export function reqDeleteEnroll(id:number){
    return request({url:`/enroll/${id}`, method:'delete'})
}

export function reqUpdateEnroll(data:any, id:number){
    return request({url:`/enroll/${id}`, method:'patch', data:data})
}


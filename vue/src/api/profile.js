import request from '@/utils/request'

/**
 * 获取用户信息
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回用户信息
 */
export function getProfile(params) {
  return request.get('/getProfile/', { params })
}

/**
 * 修改密码
 * @param {Object} params - 修改参数
 * @param {string} params.oldPass - 旧密码
 * @param {string} params.newPass - 新密码
 * @returns {Promise} 返回修改结果
 */
export function changePass(params) {
  return request.get(`/changePass/?${new URLSearchParams(params)}`)
}

/**
 * 修改用户信息
 * @param {Object} params - 修改参数
 * @param {string} params.name - 姓名
 * @param {string} params.phone - 电话
 * @param {string} params.email - 邮箱
 * @returns {Promise} 返回修改结果
 */
export function changeProfile(params) {
  return request.get(`/changeProfile/?${new URLSearchParams(params)}`)
}
import request from '@/utils/request'

/**
 * 用户登录
 * @param {Object} params - 登录参数
 * @param {string} params.name - 用户名
 * @param {string} params.pass - 密码
 * @returns {Promise} 返回登录结果，包含用户类型和用户信息
 */
export function login(params) {
  return request.get('/login', { params })
}

/**
 * 用户注册
 * @param {Object} data - 注册数据
 * @returns {Promise} 返回注册结果
 */
export function register(data) {
  return request.post('/register/', data)
}
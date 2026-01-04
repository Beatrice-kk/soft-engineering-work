import request from '@/utils/request'

/**
 * 获取账号列表
 * @param {Object} params - 查询参数
 * @param {string} params.username - 用户名筛选
 * @returns {Promise} 返回账号列表数据，包含accounts数组
 */
export function getAccount(params) {
  return request.get('/getAccount/', { params })
}

/**
 * 重置账号密码
 * @param {Object} params - 重置参数
 * @param {string|number} params.p_id - 用户ID
 * @returns {Promise} 返回重置结果
 */
export function resetAccount(params) {
  return request.get('/resetAccount/', { params })
}

/**
 * 删除单个账号
 * @param {Object} params - 删除参数
 * @param {string|number} params.p_id - 用户ID
 * @returns {Promise} 返回删除结果
 */
export function delAccount(params) {
  return request.get('/delAccount/', { params })
}

/**
 * 批量删除账号
 * @param {Object} params - 删除参数
 * @param {string} params.p_ids - 用户ID列表，多个ID用逗号分隔
 * @returns {Promise} 返回批量删除结果
 */
export function delAccountBatch(params) {
  return request.get('/delAccountBatch', { params })
}
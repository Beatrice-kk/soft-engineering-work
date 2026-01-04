import request from '@/utils/request'

/**
 * 获取关系列表
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回关系列表数据
 */
export function getRelation(params) {
  return request.get('/getRelation/', { params })
}

/**
 * 添加关系
 * @param {Object} params - 添加参数
 * @param {string} params.relation_name - 关系名称
 * @returns {Promise} 返回添加结果
 */
export function addRelation(params) {
  return request.get(`/addRelation/?${new URLSearchParams(params)}`)
}

/**
 * 删除关系
 * @param {Object} params - 删除参数
 * @param {string|number} params.r_id - 关系ID
 * @returns {Promise} 返回删除结果
 */
export function delRelation(params) {
  return request.get('/delRelation/', { params })
}
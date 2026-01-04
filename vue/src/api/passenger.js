import request from '@/utils/request'

/**
 * 获取乘客列表
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页大小
 * @returns {Promise} 返回乘客列表数据
 */
export function mgetPassenger(params) {
  return request.get('/mgetPassenger/', { params })
}

/**
 * 删除单个乘客
 * @param {Object} params - 删除参数
 * @param {string|number} params.p_id - 乘客ID
 * @returns {Promise} 返回删除结果
 */
export function delPassenger(params) {
  return request.get('/delPassenger/', { params })
}

/**
 * 批量删除乘客
 * @param {Object} params - 删除参数
 * @param {string} params.p_ids - 乘客ID列表，多个ID用逗号分隔
 * @returns {Promise} 返回批量删除结果
 */
export function delPassengerBatch(params) {
  return request.get('/delPassengerBatch', { params })
}
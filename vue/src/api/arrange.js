import request from '@/utils/request'

/**
 * 获取排班列表
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页大小
 * @returns {Promise} 返回排班列表数据
 */
export function getArrange(params) {
  return request.get('/getArrange/', { params })
}

/**
 * 修改排班信息
 * @param {Object} params - 修改参数
 * @param {string|number} params.a_id - 排班ID
 * @param {string} params.flight_number - 航班号
 * @param {string} params.departure_time - 出发时间
 * @param {string} params.arrival_time - 到达时间
 * @param {number} params.price - 价格
 * @param {number} params.seats - 座位数
 * @returns {Promise} 返回修改结果
 */
export function changeArrange(params) {
  return request.get('/changeArrange/', { params })
}

/**
 * 删除排班信息
 * @param {Object} params - 删除参数
 * @param {string|number} params.a_id - 排班ID
 * @returns {Promise} 返回删除结果
 */
export function delArrange(params) {
  return request.get('/delArrange/', { params })
}
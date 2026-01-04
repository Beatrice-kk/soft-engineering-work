import request from '@/utils/request'

/**
 * 获取排班信息用于预订
 * @param {Object} params - 查询参数
 * @param {string} params.start - 起始地
 * @param {string} params.end - 目的地
 * @param {string} params.date - 日期
 * @returns {Promise} 返回可预订的排班信息
 */
export function getArrange(params) {
  return request.get('/getArrange/', { params })
}

/**
 * 获取乘客信息
 * @param {Object} params - 查询参数
 * @param {string|number} params.p_id - 乘客ID
 * @returns {Promise} 返回乘客详细信息
 */
export function getPassenger(params) {
  return request.get('/getPassenger/', { params })
}

/**
 * 保存订单
 * @param {Object} params - 订单参数
 * @param {string|number} params.a_id - 排班ID
 * @param {string|number} params.p_id - 乘客ID
 * @param {string} params.seat - 座位号
 * @returns {Promise} 返回订单保存结果
 */
export function saveOrder(params) {
  return request.get('/saveOrder/', { params })
}
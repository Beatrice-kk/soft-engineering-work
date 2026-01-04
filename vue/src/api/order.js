import request from '@/utils/request'

/**
 * 获取已预订票务
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回已预订票务列表
 */
export function bookedTickets(params) {
  return request.get('/bookedTickets/', { params })
}

/**
 * 购买票务
 * @param {Object} params - 购买参数
 * @param {string|number} params.t_id - 票务ID
 * @returns {Promise} 返回购买结果
 */
export function purchase(params) {
  return request.get('/purchase/', { params })
}

/**
 * 取消票务
 * @param {Object} params - 取消参数
 * @param {string|number} params.t_id - 票务ID
 * @returns {Promise} 返回取消结果
 */
export function cancelTicket(params) {
  return request.get('/cancelTicket/', { params })
}
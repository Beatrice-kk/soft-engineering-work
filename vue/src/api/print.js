import request from '@/utils/request'

/**
 * 获取已订票务用于打印
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回已订票务数据
 */
export function orderedTickets(params) {
  return request.get('/orderedTickets/', { params })
}
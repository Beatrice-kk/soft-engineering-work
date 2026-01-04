import request from '@/utils/request'

/**
 * 获取票务列表
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页大小
 * @param {string} params.start - 起始地
 * @param {string} params.end - 目的地
 * @param {string} params.date - 日期 (yyyy-MM-dd格式)
 * @param {string} params.status - 状态 ('已支付' 或 '未支付')
 * @returns {Promise} 返回票务列表数据，包含tickets数组和total总数
 */
export function getTicket(params) {
  return request.get('/getTicket/', { params })
}

/**
 * 删除单个票务
 * @param {Object} params - 删除参数
 * @param {string|number} params.t_id - 票务ID
 * @returns {Promise} 返回删除结果
 */
export function delTicket(params) {
  return request.get('/delTicket/', { params })
}

/**
 * 获取票务详细信息
 * @param {Object} params - 查询参数
 * @param {string|number} params.t_id - 票务ID
 * @returns {Promise} 返回票务详细信息，包含乘客姓名(p_name)、付款方账号(p_account)、付款时间(t_paytime)等
 */
export function getTicketMore(params) {
  return request.get('/getTicketMore/', { params })
}

/**
 * 批量删除票务
 * @param {Object} params - 删除参数
 * @param {string} params.t_ids - 票务ID列表，多个ID用逗号分隔
 * @returns {Promise} 返回批量删除结果
 */
export function delTicketBatch(params) {
  return request.get('/delTicketBatch/', { params })
}
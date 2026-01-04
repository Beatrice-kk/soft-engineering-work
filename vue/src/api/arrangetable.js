import request from '@/utils/request'

/**
 * 获取列车信息用于排班
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回列车信息数据
 */
export function mgetTrain(params) {
  return request.get('/mgetTrain/', { params })
}

/**
 * 保存排班信息
 * @param {Object} params - 保存参数
 * @returns {Promise} 返回保存结果
 */
export function saveArrange(params) {
  return request.get('/saveArrange/', { params })
}
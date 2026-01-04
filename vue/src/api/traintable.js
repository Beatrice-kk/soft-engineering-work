import request from '@/utils/request'

/**
 * 保存列车信息
 * @param {Object} params - 保存参数
 * @returns {Promise} 返回保存结果
 */
export function saveTrain(params) {
  return request.get('/saveTrain/', { params })
}
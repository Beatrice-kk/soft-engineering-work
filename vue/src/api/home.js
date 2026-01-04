import request from '@/utils/request'

/**
 * 获取航班时刻表
 * @param {Object} params - 查询参数
 * @returns {Promise} 返回航班时刻表数据
 */
export function getSchedule(params) {
  return request.get('/getSchedule/', { params })
}
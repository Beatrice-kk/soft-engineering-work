import request from '@/utils/request'

/**
 * 获取列车信息列表
 * @param {Object} params - 查询参数
 * @param {number} params.pageNum - 页码
 * @param {number} params.pageSize - 每页大小
 * @param {string} params.start - 起始地
 * @param {string} params.end - 目的地
 * @returns {Promise} 返回列车信息列表数据，包含train_list数组和total总数
 */
export function getTrain(params) {
  return request.get('/getTrain/', { params })
}

/**
 * 修改列车信息
 * @param {Object} params - 修改参数
 * @param {string|number} params.f_id - 列车ID
 * @param {string} params.startField - 起始机场
 * @param {string} params.endField - 目的机场
 * @returns {Promise} 返回修改结果
 */
export function changeTrain(params) {
  return request.get('/changeTrain/', { params })
}

/**
 * 删除列车信息
 * @param {Object} params - 删除参数
 * @param {string|number} params.f_id - 列车ID
 * @returns {Promise} 返回删除结果
 */
export function delTrain(params) {
  return request.get('/delTrain/', { params })
}
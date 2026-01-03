<template>
  <div class="home-container">
    <el-card class="calendar-card" shadow="never">
      <div slot="header" class="card-header">
        <span class="title"><i class="el-icon-date"></i> 航班/日程提醒</span>
        <el-tag size="small" type="info">今日：{{ today }}</el-tag>
      </div>

      <el-calendar v-model="value">
        <template slot="dateCell" slot-scope="{date, data}">
          <div class="calendar-item">
            <div class="date-number" :class="data.isSelected ? 'active-day' : ''">
              {{ data.day.split('-').slice(2).join('') }}
              <i v-if="data.isSelected" class="el-icon-check selected-icon"></i>
            </div>
            
            <div class="schedule-content">
              <div v-for="(item, index) in getDaySchedule(data.day)" :key="index">
                <el-tooltip class="item" effect="dark" :content="item.content" placement="top">
                  <el-tag size="mini" :type="getTagType(item)" class="schedule-tag">
                    {{ item.content }}
                  </el-tag>
                </el-tooltip>
              </div>
            </div>
          </div>
        </template>
      </el-calendar>
    </el-card>
  </div>
</template>

<script>
export default {
  name: "Home",
  data() {
    return {
      value: new Date(),
      scheduleData: [],
      type: localStorage.getItem('user'),
      p_id: localStorage.getItem('p_id'),
      today: new Date().toLocaleDateString()
    }
  },
  methods: {
    load() {
      // 这里的接口地址请保持你原来的
      this.request.get("/getSchedule/", {
        params: {
          type: this.type,
          p_id: this.p_id
        }
      }).then(response => {
        // 假设后端返回的数据在 res 字段
        this.scheduleData = response.res || [];
      })
    },
    // 优化渲染性能：根据日期筛选日程
    getDaySchedule(day) {
      return this.scheduleData.filter(item => item.scheduleDay === day);
    },
    // 根据内容类型返回不同的标签颜色（可选）
    getTagType(item) {
      if (item.content.includes('航班')) return 'primary';
      if (item.content.includes('紧急')) return 'danger';
      return 'warning';
    }
  },
  created() {
    this.load();
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
  background-color: #f0f2f5;
  min-height: calc(100vh - 60px);
}

.calendar-card {
  border-radius: 8px;
  border: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header .title {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

/* 日历内部样式优化 */
.calendar-item {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.date-number {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.active-day {
  color: #409EFF;
  font-weight: bold;
}

.selected-icon {
  font-size: 12px;
  margin-left: 2px;
}

.schedule-content {
  flex: 1;
  overflow-y: auto;
}

.schedule-tag {
  width: 100%;
  margin-top: 2px;
  border-radius: 4px;
  text-overflow: ellipsis;
  overflow: hidden;
  white-space: nowrap;
  display: block;
  border: none;
}

/* 缩小日历单元格默认高度，使其更紧凑 */
::v-deep .el-calendar-table .el-calendar-day {
  height: 85px !important;
  padding: 8px;
}

/* 隐藏日历原生自带的 P 标签样式 */
::v-deep .el-calendar-table thead th {
  padding: 12px 0;
  color: #606266;
}
</style>
<template>
  <div class="book-container">
    <el-card class="search-card" shadow="never">
      <div class="search-flex-bar">
        <div class="input-item">
          <el-input v-model="start" placeholder="起始城市" prefix-icon="el-icon-position" clearable></el-input>
        </div>
        <div class="input-connector"><i class="el-icon-sort-inner"></i></div>
        <div class="input-item">
          <el-input v-model="end" placeholder="到达城市" prefix-icon="el-icon-location-outline" clearable></el-input>
        </div>
        <div class="input-item date-picker">
          <el-date-picker
            v-model="date"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="出发日期"
            style="width: 100%"
          ></el-date-picker>
        </div>
        <div class="button-group">
          <el-button type="primary" icon="el-icon-search" @click="load">搜索航班</el-button>
          <el-button icon="el-icon-refresh" @click="reset">重置</el-button>
        </div>
      </div>
    </el-card>

    <el-table 
      :data="tableData" 
      stripe 
      class="flight-table"
      :header-cell-style="{ background: '#f8f9fb', color: '#606266', fontWeight: 'bold', textAlign: 'center' }"
    >
      <el-table-column prop="航班编号" label="航班号" width="100" align="center">
        <template slot-scope="scope">
          <span class="flight-no">{{ scope.row.航班编号 }}</span>
        </template>
      </el-table-column>
      
      <el-table-column label="行程详情" min-width="400" align="center">
        <template slot-scope="scope">
          <div class="route-display-container">
            <div class="route-station departure">
              <div class="station-time">{{ scope.row.起飞时间 }}</div>
              <div class="station-name">{{ scope.row.起始地 }}</div>
              <div class="airport-info">{{ scope.row.起始机场 }}</div>
            </div>
            
            <div class="route-axis">
              <div class="axis-tag">直飞</div>
              <div class="axis-line">
                <i class="el-icon-caret-right arrow"></i>
              </div>
            </div>

            <div class="route-station arrival">
              <div class="station-time">{{ scope.row.到达时间 }}</div>
              <div class="station-name">{{ scope.row.目的地 }}</div>
              <div class="airport-info">{{ scope.row.目的机场 }}</div>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column prop="日期" label="日期" width="120" align="center"></el-table-column>

      <el-table-column label="价格" width="140" align="center">
        <template slot-scope="scope">
          <span class="price-value"><small>¥</small>{{ scope.row.航班价格 }}</span>
        </template>
      </el-table-column>

      <el-table-column label="余票状态" width="120" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.剩余 < 10 ? 'danger' : 'success'" size="small" effect="dark">
            仅剩 {{ scope.row.剩余 }} 张
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="150">
        <template v-slot="scope">
          <el-button type="primary" size="small" round icon="el-icon-tickets" @click="handleEdit(scope.row)">
            立即预订
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-footer">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pageNum"
        :page-sizes="[5, 10, 20]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background
      ></el-pagination>
    </div>

    </div>
</template>

<script>
export default {
  name: "BookFlight",
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 5,
      start: "",
      end: "",
      date: "",
      form: {},
      passengers: [],
      dialogFormVisible: false,
      multipleSelection: [],
      p_id: localStorage.getItem('p_id'),
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/getArrange/", {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          start: this.start,
          end: this.end,
          date: this.date,
        }
      }).then(res => {
        this.tableData = res.tickets;
        this.total = res.total;
      })
    },
    reset() {
      this.start = ""; this.end = ""; this.date = "";
      this.load();
    },
    handleEdit(row) {
      this.form = row;
      this.request.get("/getPassenger/", { params: { p_id: this.p_id } }).then(res => {
        this.passengers = res.passengers;
        this.dialogFormVisible = true;
      });
    },
    handleSizeChange(pageSize) { this.pageSize = pageSize; this.load(); },
    handleCurrentChange(pageNum) { this.pageNum = pageNum; this.load(); },
    handleSelectionChange(val) { this.multipleSelection = val; }
  }
}
</script>

<style scoped>
/* 容器背景与基础布局 */
.book-container { padding: 25px; background-color: #f6f8fb; min-height: 100vh; }

/* 搜索栏布局优化 */
.search-card { border-radius: 12px; margin-bottom: 20px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.search-flex-bar { display: flex; align-items: center; justify-content: flex-start; gap: 12px; }
.input-item { width: 180px; }
.input-connector { color: #C0C4CC; font-size: 20px; transform: rotate(90deg); }
.date-picker { width: 220px; }
.button-group { margin-left: auto; }

/* 核心对齐：行程展示 */
.route-display-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 10px 0;
}

.route-station {
  flex: 1; /* 关键：左右两部分平分剩余空间 */
  display: flex;
  flex-direction: column;
}

.departure { text-align: right; } /* 起点文字右对齐，向中心靠拢 */
.arrival { text-align: left; }    /* 终点文字左对齐，向中心靠拢 */

.station-time { font-size: 26px; font-weight: 800; color: #303133; line-height: 1.1; }
.station-name { font-size: 16px; font-weight: 600; color: #444; margin: 4px 0; }
.airport-info { font-size: 12px; color: #909399; }

/* 中间轴线 */
.route-axis {
  width: 110px; /* 固定轴线宽度，确保对齐不抖动 */
  margin: 0 25px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.axis-tag { font-size: 11px; color: #409EFF; background: #ecf5ff; padding: 2px 8px; border-radius: 10px; margin-bottom: 5px; }
.axis-line {
  width: 100%;
  height: 2px;
  background: #DCDFE6;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.arrow { color: #DCDFE6; position: absolute; right: -6px; font-size: 14px; }

/* 其他样式 */
.flight-table { border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.05); }
.price-value { color: #f5222d; font-size: 22px; font-weight: bold; }
.flight-no { color: #409EFF; font-weight: bold; font-family: 'Arial'; }
.pagination-footer { margin-top: 25px; display: flex; justify-content: flex-end; }
</style>
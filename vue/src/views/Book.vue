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
<<<<<<< HEAD
          <el-tag :type="scope.row.剩余 < 10 ? 'danger' : 'success'" size="small" effect="dark">
            仅剩 {{ scope.row.剩余 }} 张
=======
          <el-tag :type="scope.row.剩余 <= 0 ? 'info' : (scope.row.剩余 < 10 ? 'danger' : 'success')" size="small" effect="dark">
            {{ scope.row.剩余 > 0 ? `仅剩 ${scope.row.剩余} 张` : '已售罄' }}
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="150">
        <template v-slot="scope">
          <el-button 
<<<<<<< HEAD
            type="primary" 
            size="small" 
            round 
            icon="el-icon-tickets" 
=======
            :type="scope.row.剩余 <= 0 ? 'info' : 'primary'" 
            size="small" 
            round 
            :icon="scope.row.剩余 <= 0 ? 'el-icon-circle-close' : 'el-icon-tickets'" 
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
            @click="handleEdit(scope.row)"
            :disabled="scope.row.剩余 <= 0"
          >
            {{ scope.row.剩余 <= 0 ? '已售罄' : '立即预订' }}
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

<<<<<<< HEAD
    <el-dialog title="确认订单" :visible.sync="dialogFormVisible" width="450px" center>
=======
    <el-dialog title="确认订单信息" :visible.sync="dialogFormVisible" width="450px" center>
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
      <div class="booking-dialog-content">
        <div class="ticket-preview">
          <div class="preview-row">
            <span class="label">航班号:</span>
            <span class="val">{{ form.航班编号 }}</span>
          </div>
          <div class="preview-row">
            <span class="label">航程:</span>
<<<<<<< HEAD
            <span class="val">{{ form.起始地 }} —— {{ form.目的地 }}</span>
          </div>
          <div class="preview-row">
            <span class="label">日期:</span>
            <span class="val">{{ form.日期 }} {{ form.起飞时间 }}</span>
          </div>
          <div class="preview-row">
            <span class="label">价格:</span>
=======
            <span class="val">{{ form.起始地 }} 到 {{ form.目的地 }}</span>
          </div>
          <div class="preview-row">
            <span class="label">起飞时间:</span>
            <span class="val">{{ form.日期 }} {{ form.起飞时间 }}</span>
          </div>
          <div class="preview-row">
            <span class="label">应付金额:</span>
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
            <span class="val price-color">¥ {{ form.航班价格 }}</span>
          </div>
        </div>

        <el-form label-width="80px" style="margin-top: 20px;">
          <el-form-item label="乘机人">
<<<<<<< HEAD
            <el-input :value="passengerName" disabled></el-input>
=======
            <el-input :value="passengerName" disabled prefix-icon="el-icon-user"></el-input>
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
          </el-form-item>
        </el-form>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
<<<<<<< HEAD
        <el-button type="primary" @click="confirmBooking">提交订单并支付</el-button>
=======
        <el-button type="primary" @click="confirmBooking">立即支付并订票</el-button>
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
      </span>
    </el-dialog>

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
<<<<<<< HEAD
      form: {}, // 存储选中的航班信息
      passengerName: "", // 存储查出来的乘客姓名
=======
      form: {},
      passengerName: "",
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
      dialogFormVisible: false,
      p_id: localStorage.getItem('p_id'),
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      // 此接口需确保后端返回的数据中包含由 count(*) 算出的“剩余”字段
      this.request.get("/getArrange/", {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          start: this.start,
          end: this.end,
          date: this.date,
        }
      }).then(res => {
        this.tableData = res.tickets || [];
        this.total = res.total || 0;
      })
    },
    reset() {
      this.start = ""; this.end = ""; this.date = "";
      this.load();
    },
    // 点击“立即预订”时触发
    handleEdit(row) {
      this.form = row;
<<<<<<< HEAD
      // 1. 先根据当前登录的 p_id 获取乘客姓名
      this.request.get("/getPassenger/", { params: { p_id: this.p_id } }).then(res => {
        // 假设返回的 res.passengers 是个对象或者数组
        const passenger = Array.isArray(res.passengers) ? res.passengers[0] : res.passengers;
        this.passengerName = passenger ? passenger.p_name : "未知用户";
        
        // 2. 显示弹窗
        this.dialogFormVisible = true;
      }).catch(() => {
        this.$message.error("无法获取乘客信息，请重新登录");
      });
    },
    // 对话框点击“确认支付”时触发
    confirmBooking() {
      this.request.get("/saveOrder/", {
        params: {
          p_id: this.p_id,
          f_id: this.form.排班编号, // 注意后端接收的字段名
          price: this.form.航班价格
        }
      }).then(res => {
        this.$message.success("恭喜！订票成功");
        this.dialogFormVisible = false;
        this.load(); // 重新加载列表，更新余票
      }).catch(err => {
        this.$message.error("预订失败，请稍后再试");
      })
    },
    handleSizeChange(pageSize) { this.pageSize = pageSize; this.load(); },
    handleCurrentChange(pageNum) { this.pageNum = pageNum; this.load(); },
=======
      // 预订前再次核对余票状态
      if (row.剩余 <= 0) {
        this.$message.warning("手慢了！该航班刚刚售罄");
        this.load();
        return;
      }
      this.request.get("/getPassenger/", { params: { p_id: this.p_id } }).then(res => {
        const passenger = Array.isArray(res.passengers) ? res.passengers[0] : res.passengers;
        this.passengerName = passenger ? passenger.p_name : "未登录用户";
        this.dialogFormVisible = true;
      });
    },
    confirmBooking() {
      // 这里的接口会触发后端的“查票-改状态-创订单”事务
      this.request.get("/saveOrder/", {
        params: {
          p_id: this.p_id,
          f_id: this.form.航班编号, 
          price: this.form.航班价格
        }
      }).then(res => {
        this.$message.success("订票成功！");
        this.dialogFormVisible = false;
        this.load(); // 支付后刷新，触发数据库重新统计余票
      }).catch(err => {
        this.$message.error("系统繁忙，请重试");
      })
    },
    handleSizeChange(val) { this.pageSize = val; this.load(); },
    handleCurrentChange(val) { this.pageNum = val; this.load(); },
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
  }
}
</script>

<style scoped>
<<<<<<< HEAD
.book-container { padding: 25px; background-color: #f6f8fb; min-height: 100vh; }
.search-card { border-radius: 12px; margin-bottom: 20px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.search-flex-bar { display: flex; align-items: center; justify-content: flex-start; gap: 12px; }
.input-item { width: 180px; }
.input-connector { color: #C0C4CC; font-size: 20px; transform: rotate(90deg); }
.date-picker { width: 220px; }
.button-group { margin-left: auto; }

.route-display-container { display: flex; align-items: center; justify-content: center; width: 100%; padding: 10px 0; }
.route-station { flex: 1; display: flex; flex-direction: column; }
.departure { text-align: right; }
.arrival { text-align: left; }
.station-time { font-size: 26px; font-weight: 800; color: #303133; }
.station-name { font-size: 16px; font-weight: 600; color: #444; margin: 4px 0; }
.airport-info { font-size: 12px; color: #909399; }

.route-axis { width: 110px; margin: 0 25px; display: flex; flex-direction: column; align-items: center; }
.axis-tag { font-size: 11px; color: #409EFF; background: #ecf5ff; padding: 2px 8px; border-radius: 10px; margin-bottom: 5px; }
.axis-line { width: 100%; height: 2px; background: #DCDFE6; position: relative; display: flex; align-items: center; justify-content: flex-end; }
.arrow { color: #DCDFE6; position: absolute; right: -6px; font-size: 14px; }

.flight-table { border-radius: 12px; overflow: hidden; box-shadow: 0 8px 24px rgba(0,0,0,0.05); }
.price-value { color: #f5222d; font-size: 22px; font-weight: bold; }
.flight-no { color: #409EFF; font-weight: bold; }
.pagination-footer { margin-top: 25px; display: flex; justify-content: flex-end; }

/* 弹窗样式 */
.ticket-preview { background: #f8f9fb; padding: 15px; border-radius: 8px; }
.preview-row { margin-bottom: 8px; font-size: 14px; }
.preview-row .label { color: #909399; width: 60px; display: inline-block; }
.preview-row .val { color: #303133; font-weight: bold; }
=======
/* 容器及基础卡片 */
.book-container { padding: 25px; background-color: #f6f8fb; min-height: 100vh; }
.search-card { border-radius: 12px; margin-bottom: 20px; border: none; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.search-flex-bar { display: flex; align-items: center; gap: 12px; }
.input-item { width: 180px; }
.input-connector { color: #C0C4CC; transform: rotate(90deg); }
.button-group { margin-left: auto; }

/* 航线展示：灵感来自各大航司官网 */
.route-display-container { display: flex; align-items: center; justify-content: center; width: 100%; }
.route-station { flex: 1; display: flex; flex-direction: column; }
.departure { text-align: right; }
.arrival { text-align: left; }
.station-time { font-size: 24px; font-weight: bold; color: #303133; }
.station-name { font-size: 15px; font-weight: 500; margin: 2px 0; }
.airport-info { font-size: 12px; color: #909399; }

.route-axis { width: 120px; margin: 0 30px; display: flex; flex-direction: column; align-items: center; }
.axis-tag { font-size: 10px; color: #409EFF; border: 1px solid #d9ecff; background: #ecf5ff; padding: 0 6px; border-radius: 4px; margin-bottom: 4px; }
.axis-line { width: 100%; height: 2px; background: #E4E7ED; position: relative; }
.arrow { position: absolute; right: -5px; top: -6px; color: #E4E7ED; font-size: 14px; }

/* 表格及文字 */
.flight-table { border-radius: 12px; overflow: hidden; box-shadow: 0 8px 20px rgba(0,0,0,0.04); }
.flight-no { color: #409EFF; font-weight: bold; }
.price-value { color: #f5222d; font-size: 22px; font-weight: bold; }
.pagination-footer { margin-top: 25px; display: flex; justify-content: flex-end; }

/* 弹窗预览 */
.ticket-preview { background: #fdfdfd; padding: 15px; border-radius: 8px; border: 1px dashed #DCDFE6; }
.preview-row { margin-bottom: 10px; display: flex; justify-content: space-between; }
.preview-row .label { color: #909399; }
.preview-row .val { font-weight: bold; color: #303133; }
>>>>>>> 9dd416ef474c0f7cc841a0d9d9811ad58392e19d
.price-color { color: #f5222d; font-size: 18px; }
</style>
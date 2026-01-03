<template>
  <div class="manage-container">
    <el-card class="search-card" shadow="never">
      <div class="toolbar">
        <div class="search-inputs">
          <el-input v-model="start" placeholder="起始地" prefix-icon="el-icon-search" class="w-150" clearable></el-input>
          <el-input v-model="end" placeholder="目的地" prefix-icon="el-icon-location" class="w-150 ml-10" clearable></el-input>
          <el-date-picker
            v-model="date"
            type="date"
            value-format="yyyy-MM-dd"
            placeholder="航班日期"
            class="w-200 ml-10"
          ></el-date-picker>
        </div>
        <div class="action-buttons">
          <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
          <el-button icon="el-icon-refresh" @click="reset">重置</el-button>
        </div>
      </div>
    </el-card>

    <el-table 
      :data="tableData" 
      border 
      stripe 
      class="manage-table"
      :header-cell-style="{ background: '#F5F7FA', color: '#606266', fontWeight: 'bold', textAlign: 'center' }"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="50" align="center"></el-table-column>
      <el-table-column prop="航班编号" label="编号" width="70" align="center"></el-table-column>

      <el-table-column label="行程安排 (起飞 - 到达)" min-width="380" align="center">
        <template slot-scope="scope">
          <div class="admin-route-wrapper">
            <div class="route-point departure">
              <span class="time">{{ scope.row.起飞时间 }}</span>
              <span class="info">{{ scope.row.起始地 }} {{ scope.row.起始机场 }}</span>
            </div>
            
            <div class="route-divider">
              <span class="date-tag">{{ scope.row.日期 }}</span>
              <div class="line"></div>
            </div>

            <div class="route-point arrival">
              <span class="time">{{ scope.row.到达时间 }}</span>
              <span class="info">{{ scope.row.目的地 }} {{ scope.row.目的机场 }}</span>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="航班价格" width="120" align="center">
        <template slot-scope="scope">
          <span class="price-text">¥{{ scope.row.航班价格 }}</span>
        </template>
      </el-table-column>

      <el-table-column label="上座统计 (已售/剩余)" width="160" align="center">
        <template slot-scope="scope">
          <div class="seat-stats">
            <span class="sold">{{ scope.row.已售 }}</span>
            <span class="slash">/</span>
            <span class="remain" :class="{ 'danger': scope.row.剩余 < 10 }">{{ scope.row.剩余 }}</span>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="管理操作" align="center" width="180">
        <template v-slot="scope">
          <el-button type="text" size="small" icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
          <el-divider direction="vertical"></el-divider>
          <el-popconfirm
            confirm-button-text='确定'
            cancel-button-text='取消'
            title="确定下架该航班排班吗？"
            @confirm="handleDel(scope.row.航班编号)"
          >
            <el-button type="text" size="small" icon="el-icon-delete" slot="reference" style="color: #F56C6C">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-container">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pageNum"
        :page-sizes="[5, 10, 20]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background>
      </el-pagination>
    </div>

    <el-dialog title="航班动态编辑" :visible.sync="dialogFormVisible" width="420px" :close-on-click-modal="false">
      <el-form label-width="100px" size="medium">
        <el-form-item label="航班 ID">
          <el-input :value="form.航班编号" disabled style="width: 240px"></el-input>
        </el-form-item>
        <el-form-item label="起飞时间">
          <el-time-picker v-model="form.起飞时间" value-format="HH:mm:ss" style="width: 240px"></el-time-picker>
        </el-form-item>
        <el-form-item label="到达时间">
          <el-time-picker v-model="form.到达时间" value-format="HH:mm:ss" style="width: 240px"></el-time-picker>
        </el-form-item>
        <el-form-item label="航班价格">
          <el-input-number v-model="form.航班价格" :min="0" :precision="2" style="width: 240px"></el-input-number>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="traceBack">取 消</el-button>
        <el-button type="primary" @click="save">保存并同步</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 10,
      start: "",
      end: "",
      date: "",
      select: "",
      form: {},
      dialogFormVisible: false,
      multipleSelection: []
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
    save() {
      this.request.get("/changeArrange/", {
        params: {
          a_id: this.select,
          startTime: this.form.起飞时间,
          endTime: this.form.到达时间,
          price: this.form.航班价格
        }
      }).then(res => {
        this.load()
        this.dialogFormVisible = false
        this.$message.success("航班信息已更新")
      })
    },
    reset() {
      this.start = ""; this.end = ""; this.date = "";
      this.load()
    },
    traceBack() {
      this.dialogFormVisible = false;
      this.load()
    },
    handleDel(a_id) {
      this.request.get("/delArrange/", { params: { a_id: a_id } }).then(res => {
        this.load()
        this.$message.info("已成功下架该航班")
      })
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = Object.assign({}, row); // 使用浅拷贝防止同步修改
      this.select = this.form.航班编号
    },
    handleSizeChange(pageSize) { this.pageSize = pageSize; this.load(); },
    handleCurrentChange(pageNum) { this.pageNum = pageNum; this.load(); },
    handleSelectionChange(val) { this.multipleSelection = val; }
  }
}
</script>

<style scoped>
.manage-container { padding: 20px; background-color: #f0f2f5; min-height: 100vh; }
.search-card { margin-bottom: 20px; border-radius: 8px; border: none; }
.toolbar { display: flex; justify-content: space-between; align-items: center; }
.w-150 { width: 150px !important; }
.w-200 { width: 200px !important; }
.ml-10 { margin-left: 10px; }

/* 居中对齐样式 */
.admin-route-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px 0;
}
.route-point {
  flex: 1; /* 左右平分 */
  display: flex;
  flex-direction: column;
}
.departure { text-align: right; }
.arrival { text-align: left; }

.time { font-size: 18px; font-weight: bold; color: #2c3e50; }
.info { font-size: 12px; color: #909399; margin-top: 4px; }

.route-divider {
  width: 100px;
  margin: 0 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.date-tag { font-size: 11px; color: #409EFF; margin-bottom: 4px; }
.line { width: 100%; height: 1px; background: #E4E7ED; position: relative; }
.line::after {
  content: '';
  position: absolute;
  right: -2px;
  top: -4px;
  border: 5px solid transparent;
  border-left-color: #E4E7ED;
}

/* 统计与价格 */
.seat-stats { font-family: 'Monaco', monospace; font-size: 15px; }
.sold { color: #67C23A; font-weight: bold; }
.remain.danger { color: #F56C6C; font-weight: bold; }
.slash { margin: 0 4px; color: #DCDFE6; }
.price-text { color: #E6A23C; font-weight: bold; font-size: 16px; }

.pagination-container { margin-top: 20px; display: flex; justify-content: flex-end; }
.manage-table { border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
</style>
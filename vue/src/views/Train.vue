<template>
  <div class="manage-container">
    <el-card class="search-card" shadow="never">
      <div class="toolbar">
        <div class="input-group">
          <el-input v-model="start" placeholder="起始城市" prefix-icon="el-icon-search" class="w-200" clearable></el-input>
          <el-input v-model="end" placeholder="目的地" prefix-icon="el-icon-location" class="w-200 ml-10" clearable></el-input>
          <el-button type="primary" icon="el-icon-search" @click="load" class="ml-10">查询航线</el-button>
          <el-button type="warning" icon="el-icon-refresh" @click="reset">重置</el-button>
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
      <el-table-column type="selection" width="55" align="center"></el-table-column>
      
      <el-table-column prop="排班编号" label="航线编号" width="120" align="center">
        <template slot-scope="scope">
          <el-tag size="small" effect="plain">{{ scope.row.排班编号 }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column label="航线路径 (始发地 - 目的地)" min-width="400" align="center">
        <template slot-scope="scope">
          <div class="route-box">
            <div class="station departure">
              <span class="city">{{ scope.row.起始地 }}</span>
              <span class="airport">{{ scope.row.起始机场 }}</span>
            </div>
            
            <div class="route-icon">
              <i class="el-icon-position plane-icon"></i>
              <div class="line"></div>
            </div>

            <div class="station arrival">
              <span class="city">{{ scope.row.目的地 }}</span>
              <span class="airport">{{ scope.row.目的机场 }}</span>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="220">
        <template v-slot="scope">
          <el-button type="primary" size="mini" plain icon="el-icon-edit" @click="handleEdit(scope.row)">编辑</el-button>
          
          <el-popconfirm
            confirm-button-text='确定'
            cancel-button-text='取消'
            icon="el-icon-info"
            icon-color="red"
            title="确定要永久删除该航线吗？"
            @confirm="handleDel(scope.row.排班编号)"
            class="ml-10"
          >
            <el-button type="danger" size="mini" plain icon="el-icon-delete" slot="reference">删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination-wrapper">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pageNum"
        :page-sizes="[5, 10, 15, 20]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
        background>
      </el-pagination>
    </div>

    <el-dialog title="修改航线基础信息" :visible.sync="dialogFormVisible" width="400px">
      <el-form label-width="100px" size="medium">
        <el-form-item label="航线编号">
          <el-input v-model="select" disabled></el-input>
        </el-form-item>
        <el-form-item label="起始机场">
          <el-input v-model="form.起始机场" placeholder="请输入完整机场名称"></el-input>
        </el-form-item>
        <el-form-item label="目的机场">
          <el-input v-model="form.目的机场" placeholder="请输入完整机场名称"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <el-button @click="traceBack">取 消</el-button>
        <el-button type="primary" @click="save">保存修改</el-button>
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
      pageSize: 5,
      start: "",
      end: "",
      select: "",
      form: {},
      dialogFormVisible: false,
      multipleSelection: [],
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/getTrain/", {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          start: this.start,
          end: this.end,
        }
      }).then(res => {
        this.tableData = res.train_list;
        this.total = res.total;
      })
    },
    reset() {
      this.start = ""; this.end = "";
      this.load()
    },
    traceBack() {
      this.dialogFormVisible = false;
      this.load()
    },
    save() {
      this.request.get("/changeTrain/", {
        params: {
          f_id: this.select,
          startField: this.form.起始机场,
          endField: this.form.目的机场,
        }
      }).then(res => {
        this.load()
        this.dialogFormVisible = false
        this.$message.success("航线机场信息已更新")
      })
    },
    handleDel(f_id) {
      this.request.get("/delTrain/", { params: { f_id: f_id } }).then(res => {
        this.$message.info("航线已删除")
        this.load()
      })
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = Object.assign({}, row)
      this.select = row.排班编号
    },
    handleSizeChange(pageSize) { this.pageSize = pageSize; this.load(); },
    handleCurrentChange(pageNum) { this.pageNum = pageNum; this.load(); },
    handleSelectionChange(val) { this.multipleSelection = val; }
  }
}
</script>

<style scoped>
.manage-container { padding: 20px; background-color: #f9fafc; min-height: 100vh; }
.search-card { margin-bottom: 20px; border-radius: 8px; border: none; }
.w-200 { width: 200px !important; }
.ml-10 { margin-left: 10px; }

/* 航线路径布局 */
.route-box {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px 0;
}
.station {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.departure { text-align: right; }
.arrival { text-align: left; }

.city { font-size: 18px; font-weight: bold; color: #303133; }
.airport { font-size: 12px; color: #909399; margin-top: 5px; }

/* 飞机图标样式优化 */
.route-icon {
  width: 100px;
  margin: 0 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #409EFF;
}
.plane-icon { 
  font-size: 22px; 
  transform: rotate(90deg); /* 让小飞机头朝右飞 */
  margin-bottom: -5px;
}
.route-icon .line { 
  width: 100%; 
  height: 1px; 
  background: #DCDFE6; 
  margin-top: 8px; 
  position: relative; 
}
.route-icon .line::after {
  content: '';
  position: absolute;
  right: 0; top: -3px;
  border: 4px solid transparent;
  border-left-color: #DCDFE6;
}

.manage-table { border-radius: 8px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); }
.pagination-wrapper { margin-top: 20px; display: flex; justify-content: flex-end; }
</style>
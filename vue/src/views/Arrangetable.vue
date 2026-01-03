<template>
  <div class="create-flight-container">
    <div class="page-header">
      <div class="header-content">
        <img src="../../public/plane1.png" class="logo">
        <h2 class="title">创建航班排班计划</h2>
      </div>
      <p class="subtitle">请先从下方列表中选择基础航线，再配置详细时间价格</p>
    </div>

    <div class="main-layout">
      <el-card class="step-card" shadow="hover">
        <div slot="header" class="card-title">
          <i class="el-icon-search"></i> 第一步：检索并选择基础航线
        </div>
        
        <div class="search-bar">
          <el-input v-model="startPlace" placeholder="起始地" prefix-icon="el-icon-position" class="w-200" clearable></el-input>
          <el-input v-model="endPlace" placeholder="目的地" prefix-icon="el-icon-location-outline" class="w-200 ml-10" clearable></el-input>
          <el-button type="primary" icon="el-icon-search" @click="load" class="ml-10">查询航线</el-button>
          <el-button icon="el-icon-refresh" @click="reset">重置</el-button>
        </div>

        <el-table
          ref="singleTable"
          :data="tableData"
          highlight-current-row
          @current-change="handleCurrentChange"
          class="route-table"
          height="280"
          :header-cell-style="{ background: '#f5f7fa', color: '#606266' }"
        >
          <el-table-column type="index" width="55" label="序号" align="center"></el-table-column>
          <el-table-column property="起始地" label="起始城市" align="center"></el-table-column>
          <el-table-column property="目的地" label="到达城市" align="center"></el-table-column>
          <el-table-column property="起始机场" label="始发机场" align="center"></el-table-column>
          <el-table-column property="目的机场" label="到达机场" align="center"></el-table-column>
        </el-table>
      </el-card>

      <el-card class="step-card config-card" shadow="hover" v-if="currentRow">
        <div slot="header" class="card-title">
          <i class="el-icon-date"></i> 第二步：配置排班参数 
          <el-tag size="small" type="success" class="ml-10">已选：{{currentRow.起始地}} - {{currentRow.目的地}}</el-tag>
        </div>

        <el-form :model="form" label-width="80px" label-position="top">
          <el-row :gutter="20">
            <el-col :span="6">
              <el-form-item label="执行日期">
                <el-date-picker 
                  type="date" 
                  placeholder="选择日期" 
                  v-model="form.date" 
                  style="width: 100%" 
                  value-format="yyyy-MM-dd"
                ></el-date-picker>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="起飞时间">
                <el-time-picker 
                  placeholder="选择时间" 
                  v-model="form.start" 
                  style="width: 100%" 
                  format="HH:mm:ss"
                  value-format="HH:mm:ss"
                ></el-time-picker>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="到达时间">
                <el-time-picker 
                  placeholder="选择时间" 
                  v-model="form.end" 
                  style="width: 100%" 
                  format="HH:mm:ss"
                  value-format="HH:mm:ss"
                ></el-time-picker>
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="设定票价 (元)">
                <el-input-number v-number v-model="form.price" :min="0" :precision="2" style="width: 100%" controls-position="right"></el-input-number>
              </el-form-item>
            </el-col>
          </el-row>
          
          <div class="submit-section">
            <el-button type="success" size="large" icon="el-icon-circle-plus-outline" @click="save" :loading="loading">确认发布该航班</el-button>
          </div>
        </el-form>
      </el-card>

      <div v-else class="empty-hint">
        <i class="el-icon-info"></i> 请先从上方表格选择一条航线以继续配置
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: false,
      tableData: [],
      currentRow: null,
      startPlace: '',
      endPlace: '',
      form: {
        f_id: '',
        date: null,  // 必须为 null，避免 Invalid Date 报错
        start: null, // 必须为 null
        end: null,   // 必须为 null
        price: 500.0,
      }
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/mgetTrain/", {
        params: {
          start: this.startPlace,
          end: this.endPlace
        }
      }).then(res => {
        this.tableData = res.train_list || [];
      })
    },
    save() {
      // 严格检查必填项
      if (!this.form.f_id || !this.form.date || !this.form.start || !this.form.end) {
        this.$message.warning("请完整填写所有航班参数");
        return;
      }
      
      this.loading = true;
      this.request.get("/saveArrange/", {
        params: {
          f_id: this.form.f_id,
          date: this.form.date,
          start: this.form.start,
          end: this.form.end,
          price: this.form.price
        }
      }).then(response => {
        this.loading = false;
        // 兼容不同后端的成功码
        if (response === 'success' || response.code === '200' || response.code === 200 || response.message === 'success') {
          this.$message.success("航班排班发布成功");
          this.resetForm();
        } else {
          this.$message.error(response.message || "添加失败");
        }
      }).catch(() => { this.loading = false; });
    },
    reset() {
      this.startPlace = "";
      this.endPlace = "";
      this.currentRow = null; // 重置选中行
      this.load();
    },
    resetForm() {
      // 发布成功后，清空输入内容，保留当前选中行的ID（如果需要连发）或全部清空
      this.form = { 
        f_id: this.currentRow ? this.currentRow.排班编号 : '', 
        date: null, 
        start: null, 
        end: null, 
        price: 500.0 
      };
    },
    handleCurrentChange(val) {
      if (val) {
        this.currentRow = val;
        // 切换行时，重置表单避免旧数据的格式干扰
        this.form.f_id = val.排班编号;
        this.form.date = null;
        this.form.start = null;
        this.form.end = null;
      }
    }
  }
}
</script>

<style scoped>
.create-flight-container {
  padding: 20px;
  background-color: #f8f9fa;
  min-height: 100vh;
}

/* 头部样式 */
.page-header {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 20px 30px;
  border-radius: 12px;
  color: white;
  margin-bottom: 25px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.header-content { display: flex; align-items: center; }
.logo { height: 45px; filter: brightness(0) invert(1); }
.title { margin-left: 15px; font-size: 22px; font-weight: 500; letter-spacing: 1px; }
.subtitle { margin: 10px 0 0 60px; opacity: 0.8; font-size: 14px; }

/* 卡片样式 */
.step-card {
  margin-bottom: 20px;
  border-radius: 10px;
  border: none;
}
.card-title {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
  display: flex;
  align-items: center;
}
.card-title i { margin-right: 8px; color: #409EFF; }

/* 搜索栏 */
.search-bar { margin-bottom: 20px; }
.w-200 { width: 200px !important; }
.ml-10 { margin-left: 10px; }

/* 配置卡片 */
.config-card {
  background-color: #ffffff;
  border-top: 4px solid #67C23A;
}
.submit-section {
  text-align: center;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px dashed #dcdfe6;
}

.empty-hint {
  text-align: center;
  padding: 40px;
  color: #909399;
  background: #fdfdfd;
  border: 2px dashed #ebeef5;
  border-radius: 10px;
}

/* 覆盖 Element UI 选中行样式 */
::v-deep .el-table__body tr.current-row > td {
  background-color: #ecf5ff !important;
  color: #409EFF;
  font-weight: bold;
}
</style>
<template>
  <div class="main-container">
    <div class="header-banner">
      <div class="header-content">
        <img src="../../public/plane1.png" class="header-logo">
        <span class="header-title">航班管理系统</span>
      </div>
    </div>

    <div class="content-body">
      <div class="search-section">
        <el-input prefix-icon="el-icon-location-outline" v-model="startPlace" placeholder="起始地" class="search-item"></el-input>
        <el-input prefix-icon="el-icon-position" v-model="endPlace" placeholder="目的地" class="search-item ml-10"></el-input>
        <el-button type="primary" icon="el-icon-search" @click="load" class="ml-10">查询路线</el-button>
        <el-button type="info" plain icon="el-icon-refresh" @click="reset">重置</el-button>
      </div>

      <el-card class="table-card" shadow="never">
        <div slot="header" class="card-header">
          <span><i class="el-icon-guide"></i> 第一步：选择航线路线</span>
        </div>
        <el-table
            ref="singleTable"
            :data="tableData"
            highlight-current-row
            @current-change="handleCurrentChange"
            :row-class-name="rowClassName"
            height="220"
            style="width: 100%">
          <el-table-column type="index" label="序号" width="60"></el-table-column>
          <el-table-column property="起始地" label="起始地" align="center"></el-table-column>
          <el-table-column property="目的地" label="目的地" align="center"></el-table-column>
          <el-table-column property="起始机场" label="起始机场" align="center" show-overflow-tooltip></el-table-column>
          <el-table-column property="目的机场" label="目的机场" align="center" show-overflow-tooltip></el-table-column>
        </el-table>
      </el-card>

      <el-card class="form-card" shadow="never">
        <div slot="header" class="card-header">
          <span><i class="el-icon-edit-outline"></i> 第二步：完善排班及票价信息</span>
          <el-tag v-if="form.f_id" type="success" size="small">当前选择航线 ID: {{ form.f_id }}</el-tag>
        </div>
        
        <div class="form-grid">
          <div class="form-item">
            <span class="label">排班编号:</span>
            <el-input placeholder="如: A001" v-model="form.a_id"></el-input>
          </div>
          <div class="form-item">
            <span class="label">出发日期:</span>
            <el-date-picker type="date" placeholder="选择日期" v-model="form.date" style="width: 100%;"></el-date-picker>
          </div>
          <div class="form-item">
            <span class="label">起飞时间:</span>
            <el-time-picker placeholder="起飞时间" v-model="form.start" style="width: 100%;"></el-time-picker>
          </div>
          <div class="form-item">
            <span class="label">到达时间:</span>
            <el-time-picker placeholder="到达时间" v-model="form.end" style="width: 100%;"></el-time-picker>
          </div>
          <div class="form-item">
            <span class="label">航班票价:</span>
            <el-input placeholder="金额" v-model="form.price">
              <template slot="prepend">￥</template>
            </el-input>
          </div>
        </div>

        <div class="submit-area">
          <el-button type="success" icon="el-icon-check" size="medium" @click="save" round>确认创建航班任务</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
/* 整体容器 */
.main-container {
  background-color: #f5f7fa;
  min-height: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* 顶部 Banner */
.header-banner {
  background: linear-gradient(135deg, #409EFF 0%, #1e80e1 100%);
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 25px;
}
.header-logo {
  height: 35px;
  filter: brightness(0) invert(1); /* 图片变白色 */
}
.header-title {
  color: white;
  margin-left: 15px;
  font-size: 20px;
  font-weight: bold;
  letter-spacing: 1px;
}

/* 内容体 */
.content-body {
  padding: 20px;
}

/* 搜索区 */
.search-section {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
}
.search-item {
  width: 180px;
}
.ml-10 { margin-left: 10px; }

/* 卡片样式 */
.table-card, .form-card {
  margin-bottom: 15px;
  border-radius: 8px;
}
.card-header {
  font-size: 15px;
  font-weight: bold;
  color: #303133;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 网格表单 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}
.form-item .label {
  display: block;
  font-size: 13px;
  color: #606266;
  margin-bottom: 8px;
}

/* 提交按钮 */
.submit-area {
  margin-top: 25px;
  text-align: center;
  border-top: 1px dashed #ebeef5;
  padding-top: 20px;
}

/* 选中行样式 */
::v-deep .selected-row {
  background-color: #f0f9eb !important;
}
</style>

<script>
// 脚本逻辑保持完全不变
export default {
  data() {
    return {
      tableData: [],
      currentRow: null,
      startPlace: '',
      endPlace: '',
      form: {
        a_id: '',
        f_id: '',
        date: '',
        start: '',
        end: '',
        price: '',
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
        this.tableData = res.train_list
      })
    },
    save() {
      if(!this.form.a_id || !this.form.f_id || !this.form.date || !this.form.start || !this.form.end || !this.form.price) {
        this.$message.warning("请完整填写所有信息（包括排班编号）");
        return;
      }

      let dateFromPicker = new Date(this.form.date);
      let startFromPicker = new Date(this.form.start);
      let endFromPicker = new Date(this.form.end);

      dateFromPicker.setHours(dateFromPicker.getHours() + 8);
      startFromPicker.setHours(startFromPicker.getHours() + 8);
      endFromPicker.setHours(endFromPicker.getHours() + 8);

      this.request.get("/saveArrange/", {
        params: {
          a_id: this.form.a_id,
          f_id: this.form.f_id,
          date: dateFromPicker,
          start: startFromPicker,
          end: endFromPicker,
          price: this.form.price
        }
      }).then(response => {
        if (response.status === 'success') {
          this.$message.success("添加航班信息成功");
          this.form.a_id = '';
          this.form.price = '';
        } else {
          this.$message.error(response.message || "添加失败");
        }
      })
    },
    reset() {
      this.startPlace = "";
      this.endPlace = "";
      this.load();
    },
    handleCurrentChange(val) {
      if (val) {
        this.currentRow = val;
        this.form.f_id = this.currentRow.排班编号;
      }
    },
    rowClassName({row}) {
      return row === this.currentRow ? 'selected-row' : '';
    }
  }
}
</script>
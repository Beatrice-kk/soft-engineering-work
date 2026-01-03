<template>
  <div class="add-route-container">
    <el-card class="form-card" :body-style="{ padding: '0px' }">
      <div class="card-header">
        <div class="header-main">
          <img src="../../public/plane1.png" class="header-logo">
          <div class="header-text">
            <h3>录入新航线</h3>
            <p>请输入航线的基础地理位置与机场信息</p>
          </div>
        </div>
      </div>

      <div class="card-body">
        <el-form label-position="top" :model="form" class="custom-form">
          <el-row :gutter="40">
            <el-col :span="12">
              <el-form-item label="起始城市">
                <el-input 
                  v-model="form.startPlace" 
                  placeholder="例如：北京" 
                  prefix-icon="el-icon-position">
                </el-input>
              </el-form-item>
              
              <el-form-item label="目的城市">
                <el-input 
                  v-model="form.endPlace" 
                  placeholder="例如：上海" 
                  prefix-icon="el-icon-location-outline">
                </el-input>
              </el-form-item>
            </el-col>

            <el-col :span="12">
              <el-form-item label="起始机场">
                <el-input 
                  v-model="form.startField" 
                  placeholder="例如：大兴国际机场" 
                  prefix-icon="el-icon-office-building">
                </el-input>
              </el-form-item>
              
              <el-form-item label="目的机场">
                <el-input 
                  v-model="form.endField" 
                  placeholder="例如：虹桥国际机场" 
                  prefix-icon="el-icon-school">
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>

          <div class="form-footer">
            <el-button @click="resetForm" icon="el-icon-refresh-right">重置内容</el-button>
            <el-button 
              type="primary" 
              class="submit-btn" 
              @click="save" 
              icon="el-icon-circle-plus">
              立即发布航线
            </el-button>
          </div>
        </el-form>
      </div>
    </el-card>

    <div class="bg-tips">
      <i class="el-icon-warning-outline"></i> 注意：航线一经发布，即可在排班调度中进行时间分配。
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        startPlace: '',
        endPlace: '',
        startField: '',
        endField: ''
      }
    }
  },
  methods: {
    save() {
      // 基础判空校验
      if (!this.form.startPlace || !this.form.endPlace || !this.form.startField || !this.form.endField) {
        this.$message.warning("请完整填写所有航线信息");
        return;
      }

      this.request.get("/saveTrain/", {
        params: {
          startPlace: this.form.startPlace,
          endPlace: this.form.endPlace,
          startField: this.form.startField,
          endField: this.form.endField,
        }
      }).then(res => {
        this.$message.success("新航线信息保存成功");
        this.resetForm();
      }).catch(error => {
        console.error("Save failed:", error);
        this.$message.error("保存失败，请检查网络或联系管理员");
      });
    },
    resetForm() {
      this.form = {
        startPlace: '',
        endPlace: '',
        startField: '',
        endField: ''
      };
    }
  }
}
</script>

<style scoped>
.add-route-container {
  height: 100%;
  background-color: #f0f2f5;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.form-card {
  width: 100%;
  max-width: 800px;
  border-radius: 16px;
  overflow: hidden;
  border: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08) !important;
}

/* 头部渐变 */
.card-header {
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  padding: 30px;
  color: white;
}

.header-main {
  display: flex;
  align-items: center;
}

.header-logo {
  height: 60px;
  filter: brightness(0) invert(1);
}

.header-text {
  margin-left: 20px;
}

.header-text h3 {
  margin: 0;
  font-size: 24px;
  letter-spacing: 1px;
}

.header-text p {
  margin: 5px 0 0;
  opacity: 0.8;
  font-size: 14px;
}

/* 表单主体样式 */
.card-body {
  padding: 40px;
  background: white;
}

.custom-form ::v-deep .el-form-item__label {
  font-weight: bold;
  color: #444;
  padding-bottom: 8px;
}

.custom-form ::v-deep .el-input__inner {
  height: 48px;
  border-radius: 8px;
  background-color: #f8f9fb;
  border-color: #eef0f5;
}

.custom-form ::v-deep .el-input__inner:focus {
  background-color: #fff;
}

/* 底部操作 */
.form-footer {
  margin-top: 40px;
  display: flex;
  justify-content: flex-end;
  gap: 15px;
}

.submit-btn {
  padding: 12px 30px;
  font-size: 16px;
  border-radius: 8px;
}

.bg-tips {
  margin-top: 25px;
  color: #909399;
  font-size: 14px;
}
</style>
<template>
  <div class="main-container">
    <el-card class="box-card" :body-style="{ padding: '40px' }">
      <div slot="header" class="clearfix">
        <div class="header-content">
          <img src="../../public/plane1.png" class="logo">
          <span class="title">新建基础航班线路</span>
        </div>
      </div>

      <el-form label-position="top" :model="form" ref="formRef" class="flight-form">
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="航班编号 (f_id)" required>
              <el-input v-model="form.f_id" placeholder="例如：CA1234" prefix-icon="el-icon-key"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="起始城市">
              <el-input v-model="form.startPlace" placeholder="请输入城市名" prefix-icon="el-icon-position"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到达城市">
              <el-input v-model="form.endPlace" placeholder="请输入城市名" prefix-icon="el-icon-location-outline"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="起始机场">
              <el-input v-model="form.startField" placeholder="请输入机场全称" prefix-icon="el-icon-office-building"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="目的机场">
              <el-input v-model="form.endField" placeholder="请输入机场全称" prefix-icon="el-icon-school"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <div class="button-group">
          <el-button type="primary" size="medium" icon="el-icon-check" @click="save" style="width: 200px;">提交创建</el-button>
          <el-button size="medium" @click="resetForm">重置表单</el-button>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        f_id: '', // 新增主键字段
        startPlace: '',
        endPlace: '',
        startField: '',
        endField: ''
      }
    }
  },
  methods: {
    save() {
      // 前端校验：主键不能为空
      if (!this.form.f_id) {
        this.$message.error("航班编号是必填项！");
        return;
      }

      this.request.get("/saveTrain/", {
        params: {
          // 这里必须和后端获取的参数名一一对应
          f_id: this.form.f_id,
          startPlace: this.form.startPlace,
          endPlace: this.form.endPlace,
          startField: this.form.startField,
          endField: this.form.endField,
        }
      }).then(res => {
        // 增加逻辑判断：如果后端返回 status 为 error，说明主键冲突或保存失败
        if (res.status === 'success') {
          this.$message.success("航线保存成功");
          this.resetForm();
        } else {
          this.$message.error("保存失败：" + res.message);
        }
      }).catch(error => {
        console.error("请求失败:", error);
        this.$message.error("服务器异常");
      });
    },
    resetForm() {
      this.form = {
        f_id: '',
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
.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.box-card {
  width: 100%;
  max-width: 700px;
  border-radius: 12px;
}

.header-content {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px;
  margin-right: 15px;
}

.title {
  font-size: 22px;
  font-weight: 600;
  color: #303133;
}

.flight-form {
  margin-top: 10px;
}

/* 按钮居中显示 */
.button-group {
  margin-top: 30px;
  text-align: center;
}

/* 调整输入框内部文字颜色 */
::v-deep .el-input__inner {
  color: #333;
}
</style>
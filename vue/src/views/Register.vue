<template>
  <div class="register-container">
    <div class="main-layout">
      
      <div class="left-section">
        <img class="full-bg" src="../../public/background-4.png" alt="Illustration"/>
        
        <div class="form-wrapper">
          <div class="header">
            <h1 class="page-title">用 户 注 册</h1>
          </div>

          <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="85px" class="custom-form">
            <el-form-item label="用户名" prop="account">
              <el-input size="medium" placeholder="请输入用户名" v-model="ruleForm.account"></el-input>
            </el-form-item>
            
            <el-form-item label="密码" prop="pass">
              <el-input size="medium" type="password" placeholder="请输入密码" v-model="ruleForm.pass" autocomplete="off"></el-input>
            </el-form-item>
            
            <el-form-item label="确认密码" prop="checkPass">
              <el-input size="medium" type="password" placeholder="请再次确认密码" v-model="ruleForm.checkPass" autocomplete="off"></el-input>
            </el-form-item>
            
            <el-form-item label="真实姓名" prop="name">
              <el-input size="medium" placeholder="请输入真实姓名" v-model="ruleForm.name"></el-input>
            </el-form-item>
            
            <el-form-item label="性别" prop="sex">
              <el-radio-group v-model="ruleForm.sex" class="white-radio">
                <el-radio label="1">男</el-radio>
                <el-radio label="2">女</el-radio>
              </el-radio-group>
            </el-form-item>
            
            <el-form-item label="年龄" prop="age">
              <el-input size="medium" placeholder="请输入年龄" v-model.number="ruleForm.age"></el-input>
            </el-form-item>
            
            <el-form-item label="联系电话" prop="phone">
              <el-input size="medium" placeholder="请输入联系电话" v-model="ruleForm.phone"></el-input>
            </el-form-item>
            
            <el-form-item label="身份证号" prop="card">
              <el-input
                size="medium"
                placeholder="请输入身份证号"
                v-model="ruleForm.card"
                maxlength="18"
                show-word-limit
              ></el-input>
            </el-form-item>
          </el-form>

          <div class="footer-btn">
            <button class="submit-btn" @click="register">提 交 注 册 申 请</button>
          </div>
        </div>
      </div>

      <div class="right-section">
        <img class="full-bg" src="../../public/background-3.png" alt="Background"/>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "register",
  data() {
    const validateField = (msg) => (rule, value, callback) => {
      if (!value) {
        this.errorInfo = msg;
        callback(new Error(msg));
      } else { callback(); }
    };
    const validatePass2 = (rule, value, callback) => {
      if (!value) {
        this.errorInfo = '请再次输入密码';
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.pass) {
        this.errorInfo = '两次密码不一致';
        callback(new Error('两次密码不一致'));
      } else { callback(); }
    };

    return {
      errorInfo: '',
      ruleForm: {
        account: '', pass: '', checkPass: '', name: '', sex: '1', age: '', phone: '', card: ''
      },
      rules: {
        account: [{ validator: validateField('请输入用户名'), trigger: 'blur' }],
        pass: [{ validator: validateField('请输入密码'), trigger: 'blur' }],
        checkPass: [{ validator: validatePass2, trigger: 'blur' }],
        name: [{ validator: validateField('请输入姓名'), trigger: 'blur' }],
        age: [{ validator: validateField('请输入年龄'), trigger: 'blur' }],
        phone: [{ validator: validateField('请输入电话'), trigger: 'blur' }],
        card: [{ validator: validateField('请输入身份证号'), trigger: 'blur' }]
      }
    };
  },
  methods: {
    register() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {
          this.request.post("/register/", this.ruleForm).then(res => {
            if (res.res === 3) {
              this.$message.success("注册成功");
              this.$router.push("/login");
            } else {
              this.$message.error(res.res === 1 ? "用户名已占用" : "身份证已占用");
            }
          })
        } else {
          this.$message.error(this.errorInfo || "请完善表单");
        }
      });
    }
  }
};
</script>

<style scoped>
.register-container {
  width: 100vw;
  height: 100vh;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.main-layout {
  display: flex;
  width: 100%;
  height: 100%;
}

/* 通用背景图设置 */
.full-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

/* 左侧：背景4 + 表单内容 */
.left-section {
  flex: 1.3; 
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow-y: auto;
}

/* 右侧：背景3 (纯背景) */
.right-section {
  flex: 1;
  position: relative;
}

/* 表单容器样式 */
.form-wrapper {
  position: relative;
  z-index: 10;
  width: 85%;
  max-width: 420px;
  /* 增加轻微半透明背景，确保在复杂插图背景上文字清晰 */
  background: rgba(0, 0, 0, 0.15);
  padding: 30px;
  border-radius: 20px;
  backdrop-filter: blur(5px);
}

.page-title {
  color: #ffffff;
  font-size: 52px;
  font-weight: 500;
  text-align: center;
  margin-bottom: 25px;
  letter-spacing: 4px;
}

.custom-form >>> .el-form-item__label {
  color: rgba(255, 255, 255, 0.95) !important;
}

.white-radio >>> .el-radio__label {
  color: white !important;
}

.footer-btn {
  margin-top: 30px;
  text-align: center;
}

.submit-btn {
  width: 100%;
  height: 46px;
  background-color: #31cde2;
  border: none;
  border-radius: 23px;
  color: #ffffff;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
}

.submit-btn:hover {
  background-color: #2bb8cc;
}
</style>
<template>
  <div class="login-container">
    <div class="main-box">
      <div class="image-section">
        <img src="./img/background-1.png" alt="Decoration" />
      </div>

      <div class="form-section">
        <img class="bg-overlay" src="./img/background-2.png" alt="Background" />
        
        <div class="login-content">
          <div class="title-area">
            <h1 class="main-title">软件工程大作业</h1>
            <h2 class="sub-title">机票预订系统</h2>
            <p class="eng-title">Plane Ticketing System</p>
          </div>

          <el-form :model="ruleForm" :rules="rules" ref="userForm" class="custom-form">
            <el-form-item prop="username">
              <el-input 
                size="medium" 
                prefix-icon="el-icon-user" 
                v-model="ruleForm.username"
                placeholder="请输入登录ID">
              </el-input>
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input 
                size="medium" 
                prefix-icon="el-icon-lock" 
                show-password
                v-model="ruleForm.password" 
                placeholder="请输入密码">
              </el-input>
            </el-form-item>

            <Vcode :show="isShow" @success="success" @close="close"/>
          </el-form>

          <div class="button-group">
            <button class="btn btn-login" @click="submit">登录</button>
            <button class="btn btn-register" @click="register">注册</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vcode from "vue-puzzle-vcode";

export default {
  name: "Login",
  components: { Vcode },
  data() {
    return {
      isShow: false,
      ruleForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [{ required: true, message: '请输入登录名', trigger: 'blur' }],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
      }
    }
  },
  methods: {
    submit() { this.isShow = true; },
    register() { this.$router.push("/register"); },
    login() {
      this.$refs['userForm'].validate((valid) => {
        if (valid) {
          this.axios.get("/login", {
            params: { name: this.ruleForm.username, pass: this.ruleForm.password }
          }).then((response) => {
            if (response.res === 0) {
              this.$message.error("用户名不存在或密码错误");
            } else {
              this.$message.success(response.res === 2 ? "管理员登录成功" : "用户登录成功");
              localStorage.setItem('user', JSON.stringify(response.res));
              localStorage.setItem('id', this.ruleForm.username);
              localStorage.setItem('p_id', response.p_id);
              this.$router.push("/home");
            }
          })
        }
      });
    },
    success() {
      this.isShow = false;
      this.login();
    },
    close() { this.isShow = false; }
  }
}
</script>

<style scoped>
/* 基础复位 */
.login-container {
  margin: 0;
  padding: 0;
  width: 100vw;
  height: 100vh;
  display: flex;
  overflow: hidden;
  background-color: #f0f2f5;
}

.main-box {
  display: flex;
  width: 100%;
  height: 100%;
}

/* 左侧图片区域 */
.image-section {
  flex: 1.2; /* 比例，可以根据实际图片调整 */
  display: block;
}

.image-section img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 保持图片比例填充 */
}

/* 右侧表单区域 */
.form-section {
  flex: 1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-width: 350px;
}

.bg-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  object-fit: cover;
  z-index: 1;
}

.login-content {
  position: relative;
  z-index: 2;
  width: 80%;
  max-width: 400px;
  padding: 20px;
  text-align: center;
}

/* 标题样式 */
.title-area {
  color: #ffffff;
  margin-bottom: 30px;
  text-align: left;
}

.main-title { font-size: 2.5rem; margin: 0; }
.sub-title { font-size: 1.8rem; margin: 5px 0; }
.eng-title { font-size: 1rem; opacity: 0.8; }

/* 表单控件间距 */
.custom-form .el-form-item {
  margin-bottom: 20px;
}

/* 按钮样式重构 */
.button-group {
  display: flex;
  gap: 20px;
  margin-top: 20px;
}

.btn {
  flex: 1;
  height: 45px;
  border-radius: 25px;
  border: none;
  font-size: 16px;
  color: white;
  cursor: pointer;
  background-color: #31cde2;
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: #2bb8cc;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(49, 205, 226, 0.3);
}

/* 响应式媒体查询：手机端适配 */
@media (max-width: 768px) {
  .image-section {
    display: none; /* 窄屏隐藏左侧图 */
  }
  
  .form-section {
    flex: 1;
  }
  
  .main-title { font-size: 2rem; }
  .sub-title { font-size: 1.5rem; }
}

/* 针对超大屏幕的限制 */
@media (min-width: 1920px) {
  .login-content {
    max-width: 500px;
  }
}
</style>
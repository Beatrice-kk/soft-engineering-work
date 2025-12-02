<template>
  <div class="center-1">
    <div class="box">
      <div class="box-2">
        <img src="./img/background-1.png" alt=""/>
      </div>
      <div class="box-3">
        <img src="./img/background-2.png" alt=""/>
        <div class="box-4">
          <div class="title" style="margin-bottom: 10px">
            <p><span class="title-text">软件工程大作业<br><span style="font-size: 40px"></span></span></p>
            <p><span class="title-text">机票预订系统<br><span style="font-size: 33px">Train Ticketing System</span></span></p>
          </div>
          <el-form :model="ruleForm" :rules="rules" ref="userForm">
            <el-form-item prop="name">
              <el-input size="medium" style="margin: 10px 0" prefix-icon="el-icon-user" v-model="ruleForm.username"
                        placeholder="请输入登录ID"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input size="medium" style="margin: 10px 0" prefix-icon="el-icon-lock" show-password
                        v-model="ruleForm.password" placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item style="margin: 10px 0; text-align: right">
              <Vcode :show="isShow" @success="success" @close="close"/>
            </el-form-item>
          </el-form>
          <div class="btn-1">
            <button id="btn-login" @click="submit" style="margin-right: 20px">登录</button>
            <button id="btn-register" @click="register">注册</button>
          </div>
          <!--
          <div class="btn-2">
            <button id="btn-forget" @click="forget">忘记密码</button>
          </div>
          -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Vcode from "vue-puzzle-vcode";

export default {
  name: "Login",
  components: {
    Vcode
  },
  data() {
    return {
      isShow: false,
      ruleForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          {required: true, message: '请输入登录名', trigger: 'blur'},
          //{min: 1, max: 20, message: '长度在1 到 10个字符', trigger: 'blur'}
        ],
        password: [
          {required: true, message: '请输入密码', trigger: 'blur'},
          //{min: 1, max: 20, message: '长度在 1 到 20 个字符', trigger: 'blur'}
        ],
      }
    }
  },
  methods: {
    submit() {
      this.isShow = true;
    },
    register() {
      this.$router.push("/register")
    },
    forget() {
      this.$router.push("/forget")
    },
    login() {
      this.$refs['userForm'].validate((valid) => {
        if (valid) {
          this.axios.get("/login", {     //登录接口返回p_id
            params: {
              name: this.ruleForm.username ,
              pass: this.ruleForm.password
            }
          }).then((response) => {
            if (response.res === 0) {
              this.$message.error("用户名不存在或密码错误")
            } else{
              if(response.res === 1){
                this.$message.success("用户登录成功")
                localStorage.setItem('user', JSON.stringify(response.res))//获取信息到用户浏览器
                localStorage.setItem('id', this.ruleForm.username)
                localStorage.setItem('p_id', response.p_id)
                this.$router.push("/home")
              }
              if(response.res === 2) {
                this.$message.success("管理员登录成功")
                localStorage.setItem('user', JSON.stringify(response.res))//获取信息到用户浏览器
                localStorage.setItem('id', this.ruleForm.username)
                localStorage.setItem('p_id', response.p_id)
                this.$router.push("/home")
              }
            }
          })
        }
      });
    },
    success(msg) {
      this.isShow = false; // 通过验证后，需要手动隐藏模态框
      this.login()
    },
    // 用户点击遮罩层，应该关闭模态框
    close() {
      this.isShow = false;
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.box {
  display: flex;
  height: 750px;
}

.box-2 {
  height: 750px;
  width: 1000px;
}

.box-3 img {
  height: 750px;
  width: 1126px;
}

.title {
  font-family: "微软雅黑", Times, serif;
  text-align: left;
  position: relative;
  font-size: 50px;
  color: #ffffff;
}

.box-4 {
  z-index: 4;
  margin-top: -25px;
}

button#btn-login {
  position: relative;
  background-color: #31cde2;
  width: 117px;
  height: 41px;
  font-size: 18px;
  border-radius: 25px;
  border: none;
  color: #fff;
  margin-top: 0px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button#btn-login:hover {
  background-color: #31cde2;
}

button#btn-register {
  position: relative;
  background-color: #31cde2;
  width: 117px;
  height: 41px;
  font-size: 18px;
  border-radius: 25px;
  border: none;
  color: #fff;
  margin-top: 0px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button#btn-register:hover {
  background-color: #31cde2;
}

button#btn-forget {
  position: relative;
  background-color: #31cde2;
  width: 189px;
  height: 41px;
  font-size: 18px;
  border-radius: 25px;
  border: none;
  color: #fff;
  margin-top: 30px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button#btn-forget:hover {
  background-color: #31cde2;
}

.form-control {
  margin-top: 20px;
  width: 258px;
  height: 20px;
  border: 1px solid #ffffff;
  font-size: 16px;
  padding: 10px;
  border-radius: 25px;
  background-color: transparent
}

.form-control:focus {
  border-color: #a6a6a6;
  outline: none;
}

.box-3 {
  position: relative;

}

.box-4 {
  position: absolute;
  top: 45%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1;

}

.box-2 img {
  position: relative;
  max-width: 1000px;
  width: 100%;
  max-height: 750px;
  height: 100%;
}

</style>
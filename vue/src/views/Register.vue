<template>
  <div class="center-2">
    <div class="box">
      <div class="box-2">
        <img src="../../public/background-4.png" alt=""/>
      </div>
      <div class="box-3">
        <img src="../../public/background-3.png" alt=""/>
      </div>
      <div class="box-4">
        <div class="title">
          <p><span class="title-text" style="margin-bottom: 20px">用 户 注 册</span></p>
        </div>

        <!-- Vue 表单代码 -->
        <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="70px" class="demo-ruleForm">
          <el-form-item label="用户名" prop="account">
            <el-input size="medium" placeholder="请确认用户名" v-model="ruleForm.account" ></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="pass">
            <el-input size="medium" type="password" placeholder="请确认密码" v-model="ruleForm.pass"
                      autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass">
            <el-input size="medium" type="password" placeholder="请再次确认密码" v-model="ruleForm.checkPass"
                      autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item label="真实姓名" prop="name">
            <el-input size="medium" placeholder="请确认真实姓名" v-model.number="ruleForm.name"></el-input>
          </el-form-item>
          <el-form-item label="性别" prop="sex">
            <div style="margin-top: 4px">
              <el-radio v-model="ruleForm.sex" label="1" style="margin-right: 10px">男</el-radio>
              <el-radio v-model="ruleForm.sex" label="2">女</el-radio>
            </div>
          </el-form-item>
          <el-form-item label="年龄" prop="age">
            <el-input size="medium" placeholder="请确认年龄" v-model.number="ruleForm.age"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input size="medium" placeholder="请确认联系电话" v-model.number="ruleForm.phone"></el-input>
          </el-form-item>
          <el-form-item label="身份证号" prop="card">
            <el-input
                type="text"
                size="medium"
                placeholder="请输入内容"
                v-model="ruleForm.card"
                maxlength="18"
                show-word-limit
            ></el-input>
          </el-form-item>
        </el-form>
        <!-- 结束 Vue 表单代码 -->
        <div class="btn-1">
          <button id="btn-register" @click="register()">提交注册申请</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script>
import Vcode from "vue-puzzle-vcode";

export default {
  name: "register",
  components: {
    Vcode
  },
  data() {
    var validateAccount = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请输入用户名'
          console.log("请输入用户名")
        }
        callback(new Error('请输入用户名'));
      } else {
        if (this.errorInfo === '请输入用户名')
          this.errorInfo = ''
        callback();
      }
    };
    var validateName = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请输入真实姓名'
        }
        callback(new Error('请输入真实姓名'));
      } else {
        if (this.errorInfo === '请输入真实姓名')
          this.errorInfo = ''
        callback();
      }
    };
    var validatePass = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请输入密码'
        }
        callback(new Error('请输入密码'));
      } else {
        if (this.errorInfo === '请输入密码')
          this.errorInfo = ''
        callback();
      }
    };
    var validatePass2 = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请再次输入密码'
        }
        callback(new Error('请再次输入密码'));
      } else if (value !== this.ruleForm.pass) {
        if (this.errorInfo === '' || this.errorInfo === '请再次输入密码') {
          this.errorInfo = '两次输入密码不一致'
        }
        callback(new Error('两次输入密码不一致'));
      } else {
        if (this.errorInfo === '请再次输入密码' || this.errorInfo === '两次输入密码不一致')
          this.errorInfo = ''
        callback();
      }
    };
    var validatePhone = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请输入电话'
        }
        callback(new Error('请输入电话'));
      } else {
        if (this.errorInfo === '请输入电话')
          this.errorInfo = ''
        callback();
      }
    };
    var validateAge = (rule, value, callback) => {
      const regex = /^\d+$/;
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请输入年龄'
        }
        callback(new Error('请输入年龄'));
      } else if(!regex.test(value)){
        if (this.errorInfo === '' || this.errorInfo === '请输入年龄') {
          this.errorInfo = '年龄必须为非负整数'
        }
        callback(new Error('年龄必须为非负整数'));
      } else{
        if (this.errorInfo === '请输入年龄'|| this.errorInfo === '年龄必须为非负整数')
          this.errorInfo = ''
        callback();
      }
    };
    var validateSex = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请选择性别'
        }
        callback(new Error('请选择性别'));
      } else {
        if (this.errorInfo === '请选择性别')
          this.errorInfo = ''
        callback();
      }
    };
    var validateCard = (rule, value, callback) => {
      if (value === '') {
        if (this.errorInfo === '') {
          this.errorInfo = '请输入身份证号'
        }
        callback(new Error('请输入身份证号'));
      } else if (value.length !== 18) {
        if (this.errorInfo === '' || this.errorInfo === '请输入身份证号') {
          this.errorInfo = '身份证号不为18位'
        }
        callback(new Error('身份证号不为18位'));
      } else {
        if (this.errorInfo === '请输入身份证号' || this.errorInfo === '身份证号不为18位')
          this.errorInfo = ''
        callback();
      }
    };
    return {
      errorInfo: '',
      ruleForm: {
        account: '',
        pass: '',
        checkPass: '',
        card: '',
        phone: '',
        age: '',
        name: '',
        sex: '',
      },
      rules: {
        account: [
          {validator: validateAccount, trigger: 'blur'}
        ],
        pass: [
          {validator: validatePass, trigger: 'blur'}
        ],
        checkPass: [
          {validator: validatePass2, trigger: 'blur'}
        ],
        name: [
          {validator: validateName, trigger: 'blur'}
        ],
        sex: [
          {validator: validateSex, trigger: 'blur'}
        ],
        age: [
          {validator: validateAge, trigger: 'blur'}
        ],
        phone: [
          {validator: validatePhone, trigger: 'blur'}
        ],
        card: [
          {validator: validateCard, trigger: 'blur'}
        ]
      }
    };
  },
  methods: {
    register() {
      this.$refs['ruleForm'].validate((valid) => {
        if (valid) {  // 表单校验合法
          console.log("valid!")
          this.request.post("/register/", this.ruleForm).then(response => {
            if (response.res === 3) {
              this.$message.success("新用户注册成功")
              this.$router.push("/login")
            } else if (response.res === 2) {
              this.$message.error("该身份证已被注册")
            } else if (response.res === 1) {
              this.$message.error("该用户名已被注册")
            }
          })
        } else {
          this.$message.error(this.errorInfo)
        }
      });
    }
  }
};
</script>
<style>
.el-form-item label {
  color: white
}
</style>


<style scoped>
* {
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.box {
  display: flex;
  height: 750px;
}

.box-2 img {
  height: 750px;
  width: 1050px;
}

.title {
  font-family: "微软雅黑", Times, serif;
  text-align: center;
  position: relative;
  font-size: 64px;
  color: #ffffff;
  margin-bottom: 20px;

}

.form-control {
  margin-top: 30px;
  width: 258px;
  height: 20px;
  border: 1px solid #ffffff;
  font-size: 16px;
  padding: 10px;
  border-radius: 25px;
  background-color: transparent;
}

.form-control:focus {
  border: 1px solid #ffffff;

}

button#btn-obtain {
  position: relative;
  background-color: #31cde2;
  width: 117px;
  height: 41px;
  font-size: 18px;
  border-radius: 25px;
  border: none;
  color: #fff;
  margin-top: 30px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button#btn-obtain:hover {
  background-color: #31cde2;
}

button#btn-register {
  position: relative;
  background-color: #31cde2;
  width: 266px;
  height: 41px;
  font-size: 18px;
  border-radius: 25px;
  border: none;
  color: #fff;

  cursor: pointer;
  transition: background-color 0.3s ease;
}

button#btn-register:hover {
  background-color: #31cde2;
}

input#code {
  width: 133px;
}

.box-2 {
  position: relative;

}

.box-4 {
  position: absolute;
  top: 48%;
  left: 23%;
  transform: translate(-50%, -50%);
  z-index: 1;
}

.box-3 img {
  position: relative;
  max-width: 1000px;
  width: 100%;
  max-height: 750px;
  height: 100%;
}

.form-control:focus {
  border-color: #a6a6a6;
  outline: none;
}

label.el-form-item__label {
  text-align: center;
}

.btn-1 {

  text-align: center;
}
</style>
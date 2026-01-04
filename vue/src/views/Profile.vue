<template>
  <div>
    <el-card class="box-card">
      <el-form label-width="80px" size="large">
        <el-form-item label="姓名" style="width: 400px;margin-left: 160px">
          <el-input v-model="user.p_name" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="性别" style="width: 400px;margin-left: 160px">
          <el-input v-model="user.p_sex" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="年龄" style="width: 400px;margin-left: 160px">
          <el-input v-model="user.p_age" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" style="width: 400px;margin-left: 160px">
          <el-input v-model="user.p_tel" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="身份证号" style="width: 400px;margin-left: 160px">
          <el-input v-model="user.p_card" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item style="width: 400px;margin-left: 160px">
          <el-button type="success" @click="editProfile" style="padding-right: 17px">修改个人资料</el-button>
          <el-button type="primary" @click="editPassword" style="padding-right: 17px">修改密码</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-dialog title="修改密码" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="旧密码">
          <el-input v-model="passform.upassword" autocomplete="off" show-password></el-input>
        </el-form-item>
        <el-form-item label="新密码">
          <el-input v-model="passform.newpassword" autocomplete="off" show-password></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="cancelPass">取 消</el-button>
        <el-button type="primary" @click="savePass">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog title="个人资料" :visible.sync="profileFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="姓名">
          <el-input v-model="profileForm.p_name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="性别">
          <el-input v-model="profileForm.p_sex" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input v-model="profileForm.p_age" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="联系电话">
          <el-input v-model="profileForm.p_tel" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="身份证号">
          <el-input v-model="profileForm.p_card" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="profileFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="saveProfile">确 定</el-button>
      </div>
    </el-dialog>
  </div>

</template>

<script>
import MiddleUtil from "@/utils/MiddleUtil";

export default {
  name: "Person",
  data() {
    return {
      passform: {
        upassword: "",
        newpassword: "",
      },
      user: {
        p_name: "",
        p_sex: "",
        p_age: "",
        p_tel: "",
        p_card: "",
      },
      profileForm: {
        p_name: "",
        p_sex: "",
        p_age: "",
        p_tel: "",
        p_card: "",
      },
      id: "",
      name: "",
      type: "",
      upassword: "",
      newpassword: "",
      p_id: localStorage.getItem('p_id'),
      dialogFormVisible: false,
      profileFormVisible: false,
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/getProfile/", {
        params: {p_id: this.p_id}
      }).then(res => {
        if (res.status === 'success') {
          const userInfo = res.user_info;
          this.user.p_name = userInfo.p_name;
          this.user.p_sex = userInfo.p_sex;
          this.user.p_age = userInfo.p_age;
          this.user.p_tel = userInfo.p_tel;
          this.user.p_card = userInfo.p_card;
          this.profileForm = userInfo
        } else {
          // 处理错误情况
          this.$message.error(res.message);
        }
      }).catch(error => {
        console.error('Request failed:', error);
      });
    },
    cancelPass(){
      this.dialogFormVisible = false
      this.passform.upassword=""
      this.passform.newpassword=""
    },
    savePass() {
      // 构建查询参数
      const params = new URLSearchParams({
        p_id: this.p_id,
        upassword: this.passform.upassword,
        newpassword: this.passform.newpassword
      }).toString();

      // 使用GET请求发送密码更改信息
      this.request.get(`/changePass/?${params}`)
          .then(res => {
            if (res.status === 'success') {
              this.$message.success(res.message);
              this.dialogFormVisible=false
              this.passform.upassword=""
              this.passform.newpassword=""
              this.load()
            } else {
              this.$message.error(res.message);
            }
          }).catch(error => {
        console.error('Request failed:', error);
      });
    },

    saveProfile() {
      // 构建查询参数
      const params = new URLSearchParams({
        p_id: this.p_id,
        p_name: this.profileForm.p_name,
        p_sex: this.profileForm.p_sex,
        p_age: this.profileForm.p_age,
        p_tel: this.profileForm.p_tel,
        p_card: this.profileForm.p_card
      }).toString();

      // 使用GET请求发送个人资料更改信息
      this.request.get(`/changeProfile/?${params}`)
          .then(res => {
            // 根据返回的状态显示相应的消息
            if (res.status === 'success') {
              this.$message.success(res.message);
              this.profileFormVisible=false
            } else {
              this.$message.error(res.message);
            }
            this.load()
          }).catch(error => {
        console.error('Request failed:', error);
      });
    },

    editPassword() {
      this.dialogFormVisible = true;
    },
    editProfile() {
      this.profileFormVisible = true;
    },
  }


}
</script>

<style scoped>

</style>

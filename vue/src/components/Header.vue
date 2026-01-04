<template>
  <div class="header-container">
    <div class="left-box">
      <div class="collapse-btn" @click="collapse">
        <i :class="collapseBtnClass"></i>
      </div>
      <el-breadcrumb separator="/" class="breadcrumb-nav">
        <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item v-if="currentPathName !== '首页'">{{ currentPathName }}</el-breadcrumb-item>
      </el-breadcrumb>
    </div>

    <div class="right-box">
      <div class="user-info">
        <i class="el-icon-user"></i>
        <span class="label">当前用户：</span>
        <span class="username">{{ id }}</span>
      </div>

      <el-dropdown trigger="click">
        <div class="avatar-wrapper">
          <img src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" class="user-avatar">
          <i class="el-icon-arrow-down el-icon--right"></i>
        </div>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item icon="el-icon-user" @click.native="$router.push('/profile')">个人信息</el-dropdown-item>
          <el-dropdown-item icon="el-icon-switch-button" divided @click.native="logout">退出登录</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import MiddleUtil from "@/utils/MiddleUtil";

export default {
  name: "Header",
  props: {
    collapseBtnClass: String,
    collapse: Function
  },
  data() {
    return {
      id: ""
    }
  },
  created() {
    this.id = localStorage.getItem('id');
    // 监听逻辑建议放在 created 或 mounted 其中一处即可，避免重复挂载
    MiddleUtil.$on("click", (name) => {
      this.id = name; // 这里建议直接更新 id 或者对应的用户信息字段
    });
  },
  computed: {
    currentPathName() {
      return this.$store.state.currentPathName;
    }
  },
  methods: {
    logout() {
      this.$confirm('确认退出系统吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        localStorage.removeItem("user");
        localStorage.removeItem("id");
        this.$router.push("/login");
        this.$message.success("退出成功");
      }).catch(() => {});
    }
  },
  // 销毁组件前解绑事件，防止内存泄漏
  beforeDestroy() {
    MiddleUtil.$off("click");
  }
}
</script>

<style scoped>
.header-container {
  height: 60px;
  line-height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #fff;
  box-shadow: 0 1px 4px rgba(0,21,41,.08); /* 增加底部细微阴影 */
  padding: 0 20px;
}

.left-box {
  display: flex;
  align-items: center;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  margin-right: 15px;
  color: #606266;
  transition: color .3s;
}

.collapse-btn:hover {
  color: #409EFF;
}

.breadcrumb-nav {
  margin-left: 10px;
}

.right-box {
  display: flex;
  align-items: center;
}

.user-info {
  margin-right: 20px;
  font-size: 14px;
  color: #606266;
}

.user-info .username {
  font-weight: bold;
  color: #303133;
}

.avatar-wrapper {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  margin-right: 5px;
  border: 1px solid #eee;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
}
</style>
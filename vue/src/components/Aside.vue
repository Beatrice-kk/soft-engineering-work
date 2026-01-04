<template>
  <el-menu
    :default-active="$route.path"
    class="el-menu-vertical"
    :collapse="isCollapse"
    :collapse-transition="false"
    background-color="#304156"
    text-color="#bfcbd9"
    active-text-color="#409EFF"
    router
  >
    <div class="logo-container">
      <img src="../../public/plane.png" alt="logo" class="logo-img">
      <transition name="fade">
        <span v-show="!isCollapse" class="logo-title">机票预订系统</span>
      </transition>
    </div>

    <el-menu-item index="/home">
      <i class="el-icon-s-home"></i>
      <span slot="title">系统主页</span>
    </el-menu-item>

    <div v-show="adminShow">
      <el-submenu index="1">
        <template slot="title">
          <i class="el-icon-message-solid"></i>
          <span slot="title">基础信息管理</span>
        </template>
        <el-menu-item index="/arrange">
          <i class="el-icon-s-data"></i>
          <span>航班信息总览</span>
        </el-menu-item>
        <el-menu-item index="/arrangetable">
          <i class="el-icon-plus"></i>
          <span>添加航班信息</span>
        </el-menu-item>
      </el-submenu>

      <el-submenu index="2">
        <template slot="title">
          <i class="el-icon-s-promotion"></i>
          <span slot="title">排班信息管理</span>
        </template>
        <el-menu-item index="/train">
          <i class="el-icon-tickets"></i>
          <span>排班信息总览</span>
        </el-menu-item>
        <el-menu-item index="/traintable">
          <i class="el-icon-edit-outline"></i>
          <span>添加排班信息</span>
        </el-menu-item>
      </el-submenu>

      <el-submenu index="4">
        <template slot="title">
          <i class="el-icon-s-custom"></i>
          <span slot="title">用户信息管理</span>
        </template>
        <el-menu-item index="/passenger">
          <i class="el-icon-user"></i>
          <span>用户信息总览</span>
        </el-menu-item>
        <el-menu-item index="/account">
          <i class="el-icon-key"></i>
          <span>用户账号总览</span>
        </el-menu-item>
      </el-submenu>
    </div>

    <div v-show="userShow">
      <el-menu-item index="/profile">
        <i class="el-icon-user-solid"></i>
        <span slot="title">个人资料</span>
      </el-menu-item>

      <el-menu-item index="/relation">
        <i class="el-icon-share"></i>
        <span slot="title">关联旅客</span>
      </el-menu-item>

      <el-menu-item index="/book">
        <i class="el-icon-s-claim"></i>
        <span slot="title">航班预订</span>
      </el-menu-item>

      <el-menu-item index="/order">
        <i class="el-icon-menu"></i>
        <span slot="title">我的订单</span>
      </el-menu-item>

      <el-menu-item index="/print">
        <i class="el-icon-printer"></i>
        <span slot="title">打印航班</span>
      </el-menu-item>
    </div>
  </el-menu>
</template>

<script>
export default {
  name: "Aside",
  props: {
    isCollapse: Boolean,
  },
  data() {
    return {
      adminShow: false,
      userShow: false
    }
  },
  created() {
    this.checkPermission();
  },
  methods: {
    checkPermission() {
      const userRole = localStorage.getItem('user');
      // 假设 '2' 是管理员，'1' 是普通用户
      this.adminShow = userRole === '2';
      this.userShow = userRole === '1';
    }
  }
}
</script>

<style scoped>
/* 侧边栏整体高度 */
.el-menu-vertical:not(.el-menu--collapse) {
  width: 200px;
  min-height: 100vh;
}

.el-menu-vertical {
  min-height: 100vh;
  border: none;
}

/* Logo 容器样式 */
.logo-container {
  height: 60px;
  line-height: 60px;
  background-color: #2b2f3a; /* 比侧边栏稍深的背景 */
  text-align: center;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.logo-img {
  width: 24px;
  height: 24px;
}

.logo-title {
  margin-left: 12px;
  color: white;
  font-weight: bold;
  font-size: 16px;
  white-space: nowrap;
}

/* 菜单文字和激活效果 */
.el-menu-item i, .el-submenu__title i {
  color: #bfcbd9;
  margin-right: 10px;
}

.el-menu-item:hover, .el-submenu__title:hover {
  background-color: #263445 !important;
}

.el-menu-item.is-active {
  background-color: #263445 !important;
}

/* 渐变过渡动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>
<template>
  <el-menu :default-openeds="[]" style="min-height: 100%; overflow-x: hidden"
           background-color="rgb(0, 191, 255)"
           text-color="#fff"
           active-text-color="#ffd04b"
           :collapse-transition="false"
           :collapse="isCollapse"
           router
  ><!--router实现路由-->
    <div style="height: 90px; line-height: 90px; text-align: center">
      <img src="../../public/plane.png" alt="" style="width: 35px; position: relative; top: 12px; right: 5px;margin-right: 2px">
      <b style="color: white" >航班预订系统</b>
    </div>
      <el-menu-item index="/home" >
        <template slot="title">
        <i class="el-icon-s-home"></i>
        <span slot="title" >系统主页</span>
        </template>
      </el-menu-item>

    <el-submenu index="1" v-show="adminShow">
      <template slot="title">
        <i class="el-icon-message-solid"></i>
        <span slot="title" >航班信息管理</span>
      </template>
      <el-menu-item index="/arrange">
        <template slot="title">
          <i class="el-icon-s-data"></i>
          <span slot="title" >航班信息总览</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/arrangetable">
        <template slot="title">
          <i class="el-icon-s-order"></i>
          <span slot="title" >添加航班信息</span>
        </template>
      </el-menu-item>
    </el-submenu>

    <el-submenu index="2" v-show="adminShow">
      <template slot="title">
        <i class="el-icon-s-promotion"></i>
        <span slot="title" >排班信息管理</span>
      </template>
      <el-menu-item index="/train">
        <template slot="title">
          <i class="el-icon-s-data"></i>
          <span slot="title" >排班信息总览</span>
        </template>
      </el-menu-item>
      <el-menu-item index="/traintable">
        <template slot="title">
          <i class="el-icon-s-order"></i>
          <span slot="title" >添加排班信息</span>
        </template>
      </el-menu-item>
    </el-submenu>

    <el-submenu index="3" v-show="adminShow">
      <template slot="title">
        <i class="el-icon-s-grid"></i>
        <span slot="title" >航班信息管理</span>
      </template>

      <el-menu-item index="/ticket">
        <template slot="title">
          <i class="el-icon-s-data"></i>
          <span slot="title" >航班信息总览</span>
        </template>
      </el-menu-item>
    </el-submenu>

    <el-submenu index="4" v-show="adminShow">
      <template slot="title">
        <i class="el-icon-s-custom"></i>
        <span slot="title">用户信息管理</span>
      </template>

      <el-menu-item index="/passenger">
        <template slot="title">
          <i class="el-icon-s-data"></i>
          <span slot="title" >用户信息总览</span>
        </template>
      </el-menu-item>

      <el-menu-item index="/account">
        <template slot="title">
          <i class="el-icon-s-data"></i>
          <span slot="title" >用户账号总览</span>
        </template>
      </el-menu-item>
    </el-submenu>

    <el-menu-item index="/profile" v-show="userShow">
        <template slot="title">
        <i class="el-icon-user-solid"></i>
        <span slot="title" >个人资料</span>
        </template>
      </el-menu-item>

    <el-menu-item index="/relation" v-show="userShow">
        <template slot="title">
        <i class="el-icon-share"></i>
        <span slot="title" >关联旅客</span>
        </template>
      </el-menu-item>


    <el-menu-item index="/book" v-show="userShow">
        <template slot="title">
        <i class="el-icon-s-claim"></i>
        <span slot="title" >航班预订</span>
        </template>
      </el-menu-item>

    <el-menu-item index="/order" v-show="userShow">
        <template slot="title">
        <i class="el-icon-menu"></i>
        <span slot="title" >我的订单</span>
        </template>
      </el-menu-item>

    <el-menu-item index="/print" v-show="userShow">
        <template slot="title">
        <i class="el-icon-s-check"></i>
        <span slot="title" >打印航班</span>
        </template>
      </el-menu-item>
  </el-menu>
</template>


<script>
import MiddleUtil from "@/utils/MiddleUtil";

export default {
  name: "Aside",
  data(){
    return {
      form: {},
      adminShow:false,
      userShow:false
    }
  },
  props:{
    isCollapse:Boolean,
    logoTextShow:Boolean
  },
  methods:{

  },
  created(){
    let res=localStorage.getItem('user')
    if(res === '2')this.adminShow=true
    if(res === '1') this.userShow=true
  }
}
</script>

<style scoped>

</style>
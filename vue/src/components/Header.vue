
<template>
<div style=" line-height: 60px; display: flex">
  <div style="flex: 1;">
    <span :class="collapseBtnClass" style="cursor: pointer; font-size: 18px" @click="collapse"></span>

    <el-breadcrumb separator="/" style="display: inline-block;margin-left: 10px">
    <el-breadcrumb-item :to="'/'">首页</el-breadcrumb-item>
      <el-breadcrumb-item>{{ currentPathName}}</el-breadcrumb-item>
  </el-breadcrumb>
  </div>
  <div style="margin-right: 30px;font-size: 14px">
  <span style="font-weight: bold;">当前用户 : </span>
  <span >{{ id }}</span>
  </div>
  <div>
    <el-button type="primary" style="height: 40px " @click="logout">退出登录</el-button>
  </div>
</div>
</template>

<script>
import MiddleUtil from "@/utils/MiddleUtil";
export default {
  name: "Header",
  props:{
    collapseBtnClass:String,
    collapse:Function
  },
  data(){
    return{
      paths:[],
      form:{},
      id:""
    }
  },
  created() {
    MiddleUtil.$on("click",(name)=>{
      this.changeUsername(name);
    });
    this.id=localStorage.getItem('id')
  },
  computed:{
    currentPathName(){
      return this.$store.state.currentPathName;　　//需要监听的数据
    }
  },

  methods:{
   logout(){
     this.$router.push("/login")
     localStorage.removeItem("user")
     localStorage.removeItem("id")
     this.$message.success("退出成功")//清空数据
   },
    changeUsername(name) {//动态修改昵称
      this.$set(this.user, 'name',name);
       },
  },
   mounted() {
   MiddleUtil.$on("click",(name)=>{
     this.changeUsername(name);
   });
  },
    watch: {
    currentPathName(newVal, oldVal) {
      console.log(newVal)
    }
  },


}
</script>

<style scoped>

</style>
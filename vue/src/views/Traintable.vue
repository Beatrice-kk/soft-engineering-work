<template>
  <div style="box-shadow: 0 2px 4px rgba(0, 0, 0,.10), 0 0 6px rgba(0, 0, 0, .4);height: 80%">
    <div class="header"
         style="background: #cccccc; height: 15%; display: flex; align-items: center; justify-content: center;">
      <div style="height: 100%; width: 100%; display: flex; align-items: center;">
        <img src="../../public/plane1.png" style="height: 50px; margin-left: 8px;">
        <span style="margin-left: 8px;font-size: 20px">排班信息表</span>
      </div>
    </div>

        <div style="height: 250px;margin-top:50px;margin-left:100px">
      <el-form label-position="left" label-width="80px" :model="form">
        <el-form-item label="起始地" style="color: black;">
          <el-input v-model="form.startPlace" size="large" style="width: 300px; color: black;"></el-input>
        </el-form-item>
        <el-form-item label="目的地" style="color: black;">
          <el-input v-model="form.endPlace" size="large" style="width: 300px; color: black;"></el-input>
        </el-form-item>
        <el-form-item label="起始机场" style="color: black;">
          <el-input v-model="form.startField" size="large" style="width: 300px; color: black;"></el-input>
        </el-form-item>
        <el-form-item label="目的机场" style="color: black;">
          <el-input v-model="form.endField" size="large" style="width: 300px; color: black;"></el-input>
        </el-form-item>
      </el-form>
    </div>
    <div style="margin-left: 100px;">
      <el-button type="success" size="large" @click="save" >创建排班</el-button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      currentRow: null,
      form: {
        startPlace: '',
        endPlace: '',
        startField: '',
        endField: ''
      }
    }
  },

  methods: {
    save() {
  this.request.get("/saveTrain/", {
    params: {
      startPlace: this.form.startPlace,
      endPlace: this.form.endPlace,
      startField: this.form.startField,
      endField: this.form.endField,
    }
  }).then(res => {
    // 处理成功保存后的动作
    console.log("Save successful:", res);
    this.form.startPlace=''
    this.form.endPlace=''
    this.form.startField=''
    this.form.endField=''
    this.$message.success("排班信息保存成功")
  }).catch(error => {
    // 处理保存失败的动作
    console.error("Save failed:", error);
  });
},


  }
}
</script>

<style>
.headerBg {
  background: #eee !important;
}

</style>>
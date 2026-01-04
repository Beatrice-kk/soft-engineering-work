<template>
  <div style="box-shadow: 0 2px 4px rgba(0, 0, 0,.10), 0 0 6px rgba(0, 0, 0, .4);height: 83%">
    <div class="header"
         style="background: #cccccc; height: 15%; display: flex; align-items: center; justify-content: center;">
      <div style="height: 100%; width: 100%; display: flex; align-items: center;">
        <img src="../../public/plane1.png" style="height: 50px; margin-left: 8px;">
        <span style="margin-left: 8px;font-size: 20px">航班信息表</span>
      </div>
    </div>

    <div style="margin: 20px">
      <div style="margin: 10px 0">
        <el-input style="width: 200px" placeholder="请输入起始地" suffix-icon="el-icon-search"
                  v-model="startPlace"></el-input>
        <el-input style="width: 200px" placeholder="请输入目的地" suffix-icon="el-icon-message" class="ml-5"
                  v-model="endPlace"></el-input>
        <el-button class="ml-5" type="primary" @click="load">搜索</el-button>
        <el-button class="ml-5" type="warning" @click="reset">重置</el-button>
      </div>
      <div style="height:250px;margin-top: 10px">
        <el-table
            ref="singleTable"
            :data="tableData"
            highlight-current-row
            @current-change="handleCurrentChange"
            :row-class-name="rowClassName"
            style="width: 100%; max-height: 250px; overflow-y: auto;">>
          <el-table-column
              type="index"
              width="50">
          </el-table-column>
          <el-table-column
              property="起始地"
              label="起始地"
              width="120">
          </el-table-column>
          <el-table-column
              property="目的地"
              label="目的地"
              width="120">
          </el-table-column>
          <el-table-column
              property="起始机场"
              label="起始机场"
              width="120">
          </el-table-column>
          <el-table-column
              property="目的机场"
              label="目的机场">
          </el-table-column>
        </el-table>
      </div>
    </div>

    <div style="height:50px;width: 100%;margin-top:10px">
      <el-date-picker type="date" placeholder="选择日期" v-model="form.date"
                      style="width: 200px;margin-left: 20px"></el-date-picker>
      <el-time-picker placeholder="选择起飞时间" v-model="form.start" style="width: 200px;margin-left: 5px"></el-time-picker>
      <el-time-picker placeholder="选择到达时间" v-model="form.end" style="width: 200px;margin-left: 5px"></el-time-picker>
      <el-input placeholder="请输入票价" v-model="form.price" autocomplete="off"
                style="width: 200px;margin-left: 5px"></el-input>
    </div>

    <div>
      <el-button type="success" size="large" style="margin-left: 20px;" @click="save">创建航班</el-button>
    </div>

  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      currentRow: null,
      startPlace: '',
      endPlace: '',
      form: {
        f_id: '',
        date: '',
        start: '',
        end: '',
        price: '',
      }
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/mgetTrain/", {
        params: {
          start: this.startPlace,  // 传递起始地
          end: this.endPlace       // 传递目的地
        }
      }).then(res => {
        this.tableData = res.train_list
      })
    },
    save() {
      let dateFromPicker = new Date(this.form.date);
      let startFromPicker = new Date(this.form.start);
      let endFromPicker = new Date(this.form.end);

      dateFromPicker.setHours(dateFromPicker.getHours() + 8);
      startFromPicker.setHours(startFromPicker.getHours() + 8);
      endFromPicker.setHours(endFromPicker.getHours() + 8);
      this.request.get("/saveArrange/", {
        params: {
          f_id: this.form.f_id,
          date: dateFromPicker,
          start: startFromPicker,
          end: endFromPicker,
          price: this.form.price
        }
      }).then(response => {
        console.log(response);
        if (response.message === 'All fields must be provided') {
          this.$message.error("请完整填写航班信息表")
        } else if (response.message === 'Invalid date or time format') {
          this.$message.error("错误的日期或时间格式")
        } else if (response.message === 'Failed to create new Arrange') {
          this.$message.error("未知错误 添加失败")
        } else {
          this.$message.success("添加航班信息成功")
        }
      })
    },
    reset() {
      this.startPlace = ""
      this.endPlace = ""
      this.load()
    },
    setCurrent(row) {
      this.$refs.singleTable.setCurrentRow(row);
    },
    handleCurrentChange(val) {
      this.currentRow = val;
      this.form.f_id = this.currentRow.排班编号
    },
    rowClassName({row}) {
      // 根据条件判断当前行是否为被选中行，返回相应的类名
      return row === this.currentRow ? 'selected-row' : '';
    }
  }
}
</script>

<style>
.headerBg {
  background: #eee !important;
}

.selected-row {
  color: #3192F2;
}
</style>>
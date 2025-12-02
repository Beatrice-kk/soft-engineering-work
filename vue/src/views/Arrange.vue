<template>
  <div>
    <div style="margin: 10px 0">
      <el-input style="width: 200px" placeholder="请输入起始地" suffix-icon="el-icon-search" v-model="start"></el-input>
      <el-input style="width: 200px" placeholder="请输入目的地" suffix-icon="el-icon-message" class="ml-5"
                v-model="end"></el-input>
      <el-date-picker
          style="margin-left: 5px"
          v-model="date"
          type="date"
          value-format="yyyy-MM-dd"
          placeholder="选择日期">
      </el-date-picker>
      <el-button class="ml-5" type="primary" @click="load">搜索</el-button>
      <el-button class="ml-5" type="warning" @click="reset">重置</el-button>
    </div>
    <el-table :data="tableData" border stripe :header-cell-class-name="headerBg"
              @selection-change="handleSelectionChange">
      <el-table-column
          type="selection"
          width="55">
      </el-table-column>
      <el-table-column prop="航班编号" label="航班编号" width="70">
      </el-table-column>
      <el-table-column prop="起始地" label="起始地" width="100">
      </el-table-column>
      <el-table-column prop="目的地" label="目的地" width="100">
      </el-table-column>
      <el-table-column prop="起始机场" label="起始机场" width="70">
      </el-table-column>
      <el-table-column prop="目的机场" label="目的机场" width="70">
      </el-table-column>
      <el-table-column prop="日期" label="日期" width="90">
      </el-table-column>
      <el-table-column prop="起飞时间" label="起飞时间" width="70">
      </el-table-column>
      <el-table-column prop="到达时间" label="到达时间" width="70">
      </el-table-column>
      <el-table-column prop="航班价格" label="航班价格" width="100">
      </el-table-column>
      <el-table-column prop="已售" label="已售" width="60">
      </el-table-column>
      <el-table-column prop="剩余" label="剩余" width="60">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-button type="success" @click="handleEdit(scope.row)">编辑 <i class="el-icon-edit"></i></el-button>
          <el-popconfirm
              confirm-button-text='确定'
              cancel-button-text='我再想想'
              icon="el-icon-info"
              icon-color="red"
              title="你确定删除吗？"
              @confirm="handleDel(scope.row.航班编号)"
              class="ml-5"
          >
            <el-button type="danger" slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
    <div style="padding: 10px 0">
      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pageNum"
          :page-sizes="[5, 10, 15, 20]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total">
      </el-pagination>
    </div>
    <el-dialog title="航班信息" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="航班编号">
          <el-input v-model="form.航班编号" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="起飞时间">
          <el-input v-model="form.起飞时间" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="到达时间">
          <el-input v-model="form.到达时间" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="航班价格">
          <el-input v-model="form.航班价格" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="traceBack">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 5,
      start: "",
      end: "",
      date: "",
      select: "",
      form: {},
      dialogFormVisible: false,
      multipleSelection: [],
      headerBg: 'headerBg'
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/getArrange/", {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          start: this.start,
          end: this.end,
          date: this.date,
        }
      }).then(res => {
        this.tableData = res.tickets;
        this.total = res.total;
      })
    },
    save() {
      this.request.get("/changeArrange/", {
        params: {
          a_id: this.select,
          startTime: this.form.起飞时间,
          endTime: this.form.到达时间,
          price: this.form.航班价格
        }
      }).then(res => {
          this.load()
          this.dialogFormVisible = false
          this.$message.success("修改已提交！")
      })
    },
    reset() {
      this.start = ""
      this.end = ""
      this.date = ""
      this.load()
    },
    traceBack() {
      this.dialogFormVisible = false;
      this.load()
    },
    handleAdd() {
      this.dialogFormVisible = true//看见表单
      this.form = {}
    },
    handleDel(a_id) {
      console.log(a_id)
      this.request.get("/delArrange/", {
        params: {
          a_id: a_id,
        }
      }).then(res => {
        this.load()
      })
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = row  //已经绑定过save（）
      this.select = this.form.航班编号
    },
    handleSizeChange(pageSize) {
      console.log(pageSize)//控制台输出相关数据
      this.pageSize = pageSize
      this.load()
    },
    handleCurrentChange(pageNum) {
      console.log(pageNum)
      this.pageNum = pageNum
      this.load()
    },
    handleSelectionChange(val) {
      console.log(val)
      this.multipleSelection = val;
    }
  }
}
</script>

<style>
.headerBg {
  background: #eee !important;
}
</style>>

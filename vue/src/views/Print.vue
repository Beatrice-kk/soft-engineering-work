<template>
  <div>

    <el-table :data="tableData" border stripe :header-cell-class-name="headerBg">//表格数据需要绑定
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
      <el-table-column prop="航班价格" label="航班价格" width="70">
      </el-table-column>
      <el-table-column prop="座位号" label="座位号" width="60">
      </el-table-column>
      <el-table-column prop="乘客姓名" label="乘客姓名" width="70">
      </el-table-column>
      <el-table-column prop="状态" label="状态" width="58">
      </el-table-column>
      <el-table-column prop="支付时间" label="支付时间" width="139">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-button type="success" @click="moreInfo(scope.row)">打印<i class="el-icon-edit"></i></el-button>
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
    <el-dialog title="订单详情" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="起始地">
          <el-input v-model="form.起始地" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="目的地">
          <el-input v-model="form.目的地" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="起始机场">
          <el-input v-model="form.起始机场" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="目的机场">
          <el-input v-model="form.目的机场" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="起飞时间">
          <el-input v-model="form.起飞时间" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="到达时间">
          <el-input v-model="form.到达时间" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="航班价格">
          <el-input v-model="form.航班价格" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="座位号">
          <el-input v-model="form.座位号" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="乘客姓名">
          <el-input v-model="form.乘客姓名" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
      </el-form>
      <div style="display: flex;justify-content: flex-end;">
        <el-button @click="traceBack">取 消</el-button>
        <el-button type="primary" @click="save">确认打印</el-button>
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
      select: "",
      form: {},
      p_id: localStorage.getItem('p_id'),
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
      this.request.get("/orderedTickets/", {
        params: {
          p_id: this.p_id
        }
      }).then(res => {
        this.tableData = res.tickets;
      })
    },
    traceBack() {
      this.dialogFormVisible = false;
      this.load()
    },
    save(row) {
      this.dialogFormVisible = false;
      this.$message.success("航班打印成功！")
    },
    moreInfo(row) {
      this.dialogFormVisible = true
      this.form = row//已经绑定过save（）
      this.select = this.form.t_id
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
  }
}
</script>

<style>
.headerBg {
  background: #eee !important;
}
</style>>

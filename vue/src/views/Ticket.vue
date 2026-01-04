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
          placeholder="选择日期"
          value-format="yyyy-MM-dd">
      </el-date-picker>
      <el-select v-model="value" placeholder="请选择" style="margin-left: 5px">
        <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value">
        </el-option>
      </el-select>
      <el-button class="ml-5" type="primary" @click="load">搜索</el-button>
      <el-button class="ml-5" type="warning" @click="reset">重置</el-button>
    </div>

    <div style="margin: 10px 0">
      <el-popconfirm
          class="ml-5"
          confirm-button-text='确定'
          cancel-button-text='我再想想'
          icon="el-icon-info"
          icon-color="red"
          title="你确定删除吗？"
          @confirm="delBatch"
      >
        <el-button type="danger" slot="reference">批量删除 <i class="el-icon-remove-outline"></i></el-button>
      </el-popconfirm>
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
      <el-table-column prop="日期" label="日期" width="100">
      </el-table-column>
      <el-table-column prop="起飞时间" label="起飞时间" width="70">
      </el-table-column>
      <el-table-column prop="到达时间" label="到达时间" width="70">
      </el-table-column>
      <el-table-column prop="航班价格" label="航班价格" width="70">
      </el-table-column>
      <el-table-column prop="座位号" label="座位号" width="60">
      </el-table-column>
      <el-table-column prop="状态" label="状态" width="70">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-button type="success" @click="moreInfo(scope.row)">查看<i class="el-icon-edit"></i></el-button>
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
    <el-dialog title="购买详情" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="乘客姓名">
          <el-input v-model="form.t_name" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="付款方">
          <el-input v-model="form.p_name" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="付款时间">
          <el-input v-model="form.p_time" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="traceBack">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getTicket, delTicket, getTicketMore, delTicketBatch } from '@/api/ticket'

export default {
  data() {
    return {
      options: [{
        value: '已支付',
        label: '已售'
      }, {
        value: '未支付',
        label: '空闲'
      }],
      value: '',
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
      getTicket({
        pageNum: this.pageNum,
        pageSize: this.pageSize,
        start: this.start,
        end: this.end,
        date: this.date,
        status: this.value
      }).then(res => {
        // 假设服务器返回的数据格式是 { tickets: [], total: 0 }
        // 分页查询航班信息给tabledata和total赋值
        this.tableData = res.tickets; // 存储票务数据
        this.total = res.total; // 存储数据总数，用于分页
      })
    },

    reset() {
      this.start = ""
      this.end = ""
      this.date = ""
      this.value = ""
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
    handleDel(t_id) {
      delTicket({
        t_id: t_id,
      }).then(res => {
        this.load()
        this.$message.success("航班删除成功")
      })
    },
    moreInfo(row) {
      this.form = row//已经绑定过save（）
      this.select = row.航班编号
      getTicketMore({
        t_id: this.select,
      }).then(res => {
        this.form.t_name = res.p_name;
        this.form.p_name = res.p_account;
        this.form.p_time = res.t_paytime;
        this.reset()
      })
      this.dialogFormVisible = true
    },
    delBatch() {
      let t_ids = this.multipleSelection.map(v => v.航班编号).join(",");
      delTicketBatch({
        t_ids: t_ids,
      }).then(res => {
        this.load()
        this.$message.success("航班批量删除成功")
      }).catch(error => {
        console.error("删除失败:", error);
      });
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

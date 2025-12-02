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
          <el-button type="success" @click="handleEdit(scope.row)">购买<i class="el-icon-edit"></i></el-button>
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
    <el-dialog title="选择乘客" :visible.sync="dialogFormVisible" width="30%">
      <el-table :data="passengers" border stripe :header-cell-class-name="headerBg"
                @selection-change="handleSelectionChange">
        <el-table-column
            type="selection"
            width="55">
        </el-table-column>
        <el-table-column prop="姓名" label="姓名" width="100">
        </el-table-column>
        <el-table-column prop="身份证号" label="身份证号">
        </el-table-column>
      </el-table>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-popconfirm
            confirm-button-text='确定'
            cancel-button-text='我再想想'
            icon="el-icon-check"
            icon-color="red"
            title="你确定购买吗？"
            @confirm="save"
            class="ml-5"
        >
          <el-button type="primary" slot="reference">确认<i class="el-icon-remove-outline"></i></el-button>
        </el-popconfirm>
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
      passengers: [],
      dialogFormVisible: false,
      multipleSelection: [],
      headerBg: 'headerBg',
      p_id: localStorage.getItem('p_id'),
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
    handleEdit(row) {
      this.form = row; // 已经绑定过save（）
      this.select = this.form.航班编号;
      this.request.get("/getPassenger/", {
        params: {
          p_id: this.p_id
        }
      }).then(res => {
        this.passengers = res.passengers; // 更新passengers数据
      })
      this.dialogFormVisible = true;
    },
    save() {
      if (this.form.剩余 < this.multipleSelection.length) {
        this.$message.error("余票不足")
      } else {
        let p_ids = this.multipleSelection.map(v => v.用户编号).join(','); // 将数组转换为逗号分隔的字符串
        this.request.get("/book/", {
          params: {
            p_main: this.p_id,
            p_ids: p_ids,
            a_id: this.select
          }
        }).then(res => {
          if (res.message === 'Already') {
            this.$message.error("有乘客已购买过本次航班的航班")
          } else if (res.message === 'Ticket not found') {
            this.$message.error("余票不足")
          } else {
            this.$message.success("航班预订成功")
            this.dialogFormVisible = false
            this.load()
          }
        })
      }
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
      console.log(this.multipleSelection)
    }
  }
}
</script>

<style>
.headerBg {
  background: #eee !important;
}
</style>>

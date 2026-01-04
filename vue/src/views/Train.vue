<template>
  <div>
    <div style="margin: 10px 0">
      <el-input style="width: 200px" placeholder="请输入起始地" suffix-icon="el-icon-search" v-model="start"></el-input>
      <el-input style="width: 200px" placeholder="请输入目的地" suffix-icon="el-icon-message" class="ml-5"
                v-model="end"></el-input>
      <el-button class="ml-5" type="primary" @click="load">搜索</el-button>
      <el-button class="ml-5" type="warning" @click="reset">重置</el-button>
    </div>
    <el-table :data="tableData" border stripe :header-cell-class-name="headerBg"
              @selection-change="handleSelectionChange">//表格数据需要绑定
      <el-table-column
          type="selection"
          width="55">
      </el-table-column>
      <el-table-column prop="排班编号" label="排班编号" width="150">
      </el-table-column>
      <el-table-column prop="起始地" label="起始地" width="150">
      </el-table-column>
      <el-table-column prop="目的地" label="目的地" width="150">
      </el-table-column>
      <el-table-column prop="起始机场" label="起始机场" width="150">
      </el-table-column>
      <el-table-column prop="目的机场" label="目的机场" width="150">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-button type="success" @click="handleEdit(scope.row)">编辑<i class="el-icon-edit"></i></el-button>
          <el-popconfirm
              confirm-button-text='确定'
              cancel-button-text='我再想想'
              icon="el-icon-info"
              icon-color="red"
              title="你确定删除吗？"
              @confirm="handleDel(scope.row.排班编号)"
              class="ml-5"
          >
            <el-button type="danger" slot="reference">删除 <i class="el-icon-remove-outline"></i></el-button>
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
    <el-dialog title="排班信息" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="排班编号">
          <el-input v-model="this.select" autocomplete="off" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="起始机场">
          <el-input v-model="form.起始机场" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="目的机场">
          <el-input v-model="form.目的机场" autocomplete="off"></el-input>
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
import { getTrain, changeTrain, delTrain } from '@/api/train'

export default {
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 5,
      start: "",
      end: "",
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
      getTrain({
        pageNum: this.pageNum,
        pageSize: this.pageSize,
        start: this.start,
        end: this.end,
      }).then(res => {
        this.tableData = res.train_list; // 更新航班数据
        this.total = res.total; // 更新总数据量
      })
    },
    reset() {
      this.start = ""
      this.end = ""
      this.area = ""
      this.load()
    },
    traceBack() {
      this.dialogFormVisible = false;
      this.load()
    },
    save() {
      console.log("Saving:", this.select, this.form.startField, this.form.endField); // 添加日志以确认值
      changeTrain({
        f_id: this.select,
        startField: this.form.起始机场,  // 注意这里改成了 this.form.startField
        endField: this.form.目的机场,      // 注意这里改成了 this.form.endField
      }).then(res => {
        console.log("Save successful:", res); // 添加成功日志
        this.load()
        this.dialogFormVisible=false
        this.$message.success("排班信息修改成功")
      }).catch(error => {
        console.error("Save failed:", error); // 添加错误日志
      });
    },
    handleDel(f_id) {
      delTrain({
        f_id: f_id
      }).then(res => {
        this.reset()
      })
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = row
      this.select = row.排班编号
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

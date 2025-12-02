<template>
  <div>
    <div style="margin: 10px 0">
      <el-input style="width: 200px" placeholder="请输入用户姓名" suffix-icon="el-icon-search" v-model="name"></el-input>
      <el-input style="width: 200px" placeholder="请输入联系方式" suffix-icon="el-icon-message" class="ml-5"
                v-model="phone"></el-input>
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
      <el-table-column prop="p_id" label="用户编号" width="120">
      </el-table-column>
      <el-table-column prop="p_name" label="用户姓名" width="100">
      </el-table-column>
      <el-table-column prop="p_sex" label="性别" width="100">
      </el-table-column>
      <el-table-column prop="p_age" label="年龄" width="100">
      </el-table-column>
      <el-table-column prop="p_tel" label="联系电话" width="150">
      </el-table-column>
      <el-table-column prop="p_card" label="身份证号" width="200">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-popconfirm
              confirm-button-text='确定'
              cancel-button-text='我再想想'
              icon="el-icon-info"
              icon-color="red"
              title="你确定删除吗？"
              @confirm="handleDel(scope.row.p_id)"
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
      name: "",
      phone: "",
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
      this.request.get("/mgetPassenger/", {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          name: this.name,
          phone: this.phone,
        }
      }).then(res => {
        this.tableData = res.passengers;
        this.total = res.total;
      }).catch(error => {
        console.error("加载失败:", error);
      });
    },
    reset() {
      this.name = ""
      this.phone = ""
      this.load()
    },
    handleDel(p_id) {
      this.request.get("/delPassenger/", {
        params: {
          p_id: p_id,
        }
      }).then(res => {
        this.load(),
        this.$message.success("删除用户成功")
      })
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = row//已经绑定过save（）
      this.select = row.p_id
    },
    delBatch() {
      let p_ids = this.multipleSelection.map(v => v.p_id).join(",");  // 将p_ids数组转换成以逗号分隔的字符串
      this.request.get("/delPassengerBatch", {
        params: {
          p_ids: p_ids,  // 将p_ids作为参数传递
        }
      }).then(res => {
        this.load()
        this.$message.success("批量删除用户成功")
      }).catch(error => {
        console.error("批量删除失败:", error);
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

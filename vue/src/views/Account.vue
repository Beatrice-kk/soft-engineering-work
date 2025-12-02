<template>

  <div>
    <div style="margin: 10px 0">
      <el-input style="width: 200px" placeholder="请输入用户名" suffix-icon="el-icon-search" v-model="username"></el-input>
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
      <el-table-column prop="p_id" label="用户编号" width="200">
      </el-table-column>
      <el-table-column prop="p_account" label="用户名" width="200">
      </el-table-column>
      <el-table-column prop="p_password" label="密码" width="200">
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
            <el-button type="danger" slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>
          </el-popconfirm>

          <el-popconfirm
              confirm-button-text='确定'
              cancel-button-text='我再想想'
              icon="el-icon-info"
              icon-color="red"
              title="你确定重置吗？"
              @confirm="handleReset(scope.row.p_id)"
              class="ml-5"
          >
            <el-button type="success" slot="reference">重置密码 <i class="el-icon-remove-outline"></i></el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  name: "account",
  data() {
    return {
      tableData: [],
      username: "",
      form: {},
      dialogFormVisible: false,
      multipleSelection: [],
      headerBg: 'headerBg',
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/getAccount/", {
        params: {
          username: this.username
        }
      }).then(res => {
        this.tableData = res.accounts;  // 更新你的data中的accounts数组
      }).catch(error => {
        console.error("查询失败:", error);
      });
    },

    handleReset(id) {
      this.request.get("/resetAccount/", {
        params: {
          p_id: id,
        }
      }).then(res => {
        this.reset()

      })
    },
    handleDel(p_id) {
      this.request.get("/delAccount/", {
        params: {
          p_id: p_id,
        }
      }).then(res => {
        this.load()
      }).catch(error => {
        console.error("删除失败:", error);
      });
    },

    delBatch() {
      let p_ids = this.multipleSelection.map(v => v.p_id).join(","); // 将p_ids数组转换成以逗号分隔的字符串
      this.request.get("/delAccountBatch", {
        params: {
          p_ids: p_ids,  // 将p_ids作为参数传递
        }
      }).then(res => {
        // 批量删除账号信息后的逻辑
      }).catch(error => {
        console.error("批量删除失败:", error);
      });
    },
    reset() {
      this.username = ""
      this.load()
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
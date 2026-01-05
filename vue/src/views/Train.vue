<template>
  <div class="manage-container">
    <el-card class="search-card" shadow="never">
      <div class="search-form">
        <el-input 
          v-model="start" 
          placeholder="起始地" 
          prefix-icon="el-icon-location-outline"
          class="search-input"
          clearable
        ></el-input>
        <el-input 
          v-model="end" 
          placeholder="目的地" 
          prefix-icon="el-icon-position"
          class="search-input ml-10"
          clearable
        ></el-input>
        <el-button type="primary" icon="el-icon-search" class="ml-10" @click="load">搜索</el-button>
        <el-button type="warning" icon="el-icon-refresh" @click="reset">重置</el-button>
      </div>
    </el-card>

    <el-card class="table-card" shadow="never">
      <el-table 
        :data="tableData" 
        stripe 
        highlight-current-row
        :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }"
        @selection-change="handleSelectionChange"
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" align="center"></el-table-column>
        <el-table-column prop="航线编号" label="航线编号" width="120">
          <template v-slot="scope">
            <el-tag size="small" effect="plain">{{ scope.row.航线编号 }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="起始地" label="起始地" align="center"></el-table-column>
        <el-table-column prop="目的地" label="目的地" align="center"></el-table-column>
        <el-table-column prop="起始机场" label="起始机场" show-overflow-tooltip></el-table-column>
        <el-table-column prop="目的机场" label="目的机场" show-overflow-tooltip></el-table-column>
        
        <el-table-column label="操作" align="center" width="200">
          <template v-slot="scope">
            <el-button 
              type="primary" 
              size="mini" 
              icon="el-icon-edit"
              plain
              @click="handleEdit(scope.row)"
            >编辑</el-button>
            <el-popconfirm
              confirm-button-text='确定'
              cancel-button-text='取消'
              icon="el-icon-warning"
              icon-color="#f56c6c"
              title="确定要删除这条航线记录吗？"
              @confirm="handleDel(scope.row.航线编号)"
              class="ml-10"
            >
              <el-button 
                type="danger" 
                size="mini" 
                icon="el-icon-delete"
                slot="reference"
              >删除</el-button>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="pageNum"
          :page-sizes="[5, 10, 15, 20]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
          background
        >
        </el-pagination>
      </div>
    </el-card>

    <el-dialog 
      title="修改航线详细信息" 
      :visible.sync="dialogFormVisible" 
      width="35%"
      custom-class="custom-dialog"
    >
      <el-form :model="form" label-width="100px" size="medium">
        <el-form-item label="航线编号">
          <el-input v-model="select" disabled prefix-icon="el-icon-key"></el-input>
        </el-form-item>
        <el-form-item label="起始机场">
          <el-input v-model="form.起始机场" placeholder="请输入起始机场全称"></el-input>
        </el-form-item>
        <el-form-item label="目的机场">
          <el-input v-model="form.目的机场" placeholder="请输入目的机场全称"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="traceBack" size="medium">取 消</el-button>
        <el-button type="primary" @click="save" size="medium" icon="el-icon-check">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.manage-container {
  padding: 20px;
  background-color: #f9fafc;
  min-height: 100vh;
}

.search-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.search-form {
  display: flex;
  align-items: center;
}

.search-input {
  width: 220px;
}

.table-card {
  border-radius: 8px;
}

.pagination-container {
  padding: 20px 0 10px 0;
  display: flex;
  justify-content: flex-end;
}

.ml-10 {
  margin-left: 10px;
}

/* 覆盖一些 Element UI 的默认样式 */
::v-deep .el-table__row {
  height: 55px;
}

::v-deep .custom-dialog .el-dialog__header {
  border-bottom: 1px solid #ebeef5;
  padding: 20px;
}

::v-deep .custom-dialog .el-dialog__footer {
  border-top: 1px solid #ebeef5;
  padding: 15px 20px;
}
</style>

<script>
export default {
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 10, // 初始每页显示设为 10 较美观
      start: "",
      end: "",
      select: "",
      form: {},
      dialogFormVisible: false,
      multipleSelection: [],
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      this.request.get("/getTrain/", {
        params: {
          pageNum: this.pageNum,
          pageSize: this.pageSize,
          start: this.start,
          end: this.end,
        }
      }).then(res => {
        this.tableData = res.train_list;
        this.total = res.total;
      })
    },
    reset() {
      this.start = ""
      this.end = ""
      this.load()
    },
    traceBack() {
      this.dialogFormVisible = false;
      this.load()
    },
    save() {
      this.request.get("/changeTrain/", {
        params: {
          f_id: this.select,
          startField: this.form.起始机场,
          endField: this.form.目的机场,
        }
      }).then(res => {
        this.load()
        this.dialogFormVisible = false
        this.$message.success("航线信息修改成功")
      })
    },
    handleDel(f_id) {
      this.request.get("/delTrain/", {
        params: { f_id: f_id }
      }).then(res => {
        this.$message.success("删除成功")
        this.load()
      })
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = Object.assign({}, row); // 使用拷贝防止直接修改表格数据
      this.select = row.航线编号
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize
      this.load()
    },
    handleCurrentChange(pageNum) {
      this.pageNum = pageNum
      this.load()
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    }
  }
}
</script>
<template>
  <div class="manage-wrapper">
    <el-card class="search-card" shadow="never">
      <div class="toolbar-layout">
        <div class="search-inputs">
          <el-input 
            v-model="name" 
            placeholder="姓名" 
            prefix-icon="el-icon-user" 
            class="w-200"
            clearable
            @keyup.enter.native="load"
          ></el-input>
          <el-input 
            v-model="phone" 
            placeholder="联系电话" 
            prefix-icon="el-icon-mobile-phone" 
            class="w-200 ml-10"
            clearable
            @keyup.enter.native="load"
          ></el-input>
          <el-button type="primary" icon="el-icon-search" class="ml-10" @click="load">查询</el-button>
          <el-button type="warning" icon="el-icon-refresh" @click="reset">重置</el-button>
        </div>

        <div class="batch-actions">
          <el-popconfirm
            confirm-button-text='确定'
            cancel-button-text='取消'
            icon="el-icon-warning"
            icon-color="red"
            title="确定要批量删除选中的乘客吗？"
            @confirm="delBatch"
          >
            <el-button 
              type="danger" 
              slot="reference" 
              :disabled="multipleSelection.length === 0"
              icon="el-icon-delete"
            >
              批量删除 ({{ multipleSelection.length }})
            </el-button>
          </el-popconfirm>
        </div>
      </div>
    </el-card>

    <el-table 
      :data="tableData" 
      border 
      stripe 
      class="data-table"
      :header-cell-style="{ background: '#F5F7FA', color: '#606266', fontWeight: 'bold' }"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" align="center"></el-table-column>
      
      <el-table-column prop="p_id" label="编号" width="80" align="center"></el-table-column>
      
      <el-table-column prop="p_name" label="用户姓名" width="120" align="center">
        <template slot-scope="scope">
          <span class="user-name">{{ scope.row.p_name }}</span>
        </template>
      </el-table-column>
      
      <el-table-column prop="p_sex" label="性别" width="80" align="center">
        <template slot-scope="scope">
          <el-tag :type="scope.row.p_sex === '男' ? '' : 'danger'" size="small">
            {{ scope.row.p_sex || '未知' }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column prop="p_age" label="年龄" width="80" align="center"></el-table-column>
      
      <el-table-column prop="p_tel" label="联系电话" width="140" align="center"></el-table-column>
      
      <el-table-column prop="p_card" label="身份证号" min-width="180" align="center">
        <template slot-scope="scope">
          <span class="card-text">{{ scope.row.p_card }}</span>
        </template>
      </el-table-column>

      <el-table-column label="管理" align="center" width="120">
        <template v-slot="scope">
          <el-popconfirm
            title="确定移除该乘客信息吗？"
            @confirm="handleDel(scope.row.p_id)"
          >
            <el-button type="text" size="small" icon="el-icon-delete" slot="reference" style="color: #F56C6C">删除</el-button>
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
        background>
      </el-pagination>
    </div>
  </div>
</template>

<script>
import { mgetPassenger, delPassenger, delPassengerBatch } from '@/api/passenger'

export default {
  data() {
    return {
      tableData: [],
      total: 0,
      pageNum: 1,
      pageSize: 10,
      name: "",
      phone: "",
      multipleSelection: []
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      mgetPassenger({
        pageNum: this.pageNum,
        pageSize: this.pageSize,
        name: this.name,
        phone: this.phone,
      }).then(res => {
        this.tableData = res.passengers || [];
        this.total = res.total || 0;
      }).catch(err => {
        this.$message.error("数据加载失败");
      });
    },
    reset() {
      this.name = "";
      this.phone = "";
      this.pageNum = 1;
      this.load();
    },
    handleDel(p_id) {
      delPassenger({ p_id: p_id }).then(res => {
        this.$message.success("信息已删除");
        this.load();
      });
    },
    delBatch() {
      if (!this.multipleSelection.length) return;
      let p_ids = this.multipleSelection.map(v => v.p_id).join(",");
      delPassengerBatch({ p_ids: p_ids }).then(res => {
        this.$message.success("批量删除成功");
        this.load();
      });
    },
    handleSizeChange(pageSize) {
      this.pageSize = pageSize;
      this.load();
    },
    handleCurrentChange(pageNum) {
      this.pageNum = pageNum;
      this.load();
    },
    handleSelectionChange(val) {
      this.multipleSelection = val;
    }
  }
}
</script>

<style scoped>
.manage-wrapper { padding: 20px; background-color: #f9fafc; min-height: 100vh; }
.search-card { margin-bottom: 20px; border: none; border-radius: 8px; }
.toolbar-layout { display: flex; justify-content: space-between; align-items: center; }
.search-inputs { display: flex; align-items: center; }
.w-200 { width: 200px !important; }
.ml-10 { margin-left: 10px; }

.data-table { border-radius: 8px; box-shadow: 0 2px 12px 0 rgba(0,0,0,0.05); }
.user-name { font-weight: bold; color: #409EFF; }
.card-text { font-family: monospace; color: #606266; }

.pagination-container { padding: 20px 0; display: flex; justify-content: flex-end; }

/* 深度选择器，优化Element表格表头 */
::v-deep .el-table th {
  padding: 12px 0;
}
</style>
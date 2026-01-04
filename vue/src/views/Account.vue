<template>
  <div class="user-manage-container">
    <el-card class="box-card toolbar-card" shadow="never">
      <div class="toolbar-content">
        <div class="search-group">
          <el-input 
            v-model="username" 
            placeholder="按用户名搜索" 
            prefix-icon="el-icon-user"
            class="search-input"
            clearable
            @keyup.enter.native="load"
          ></el-input>
          <el-button type="primary" icon="el-icon-search" @click="load">查询</el-button>
          <el-button icon="el-icon-refresh" @click="reset">重置</el-button>
        </div>

        <div class="action-group">
          <el-popconfirm
            confirm-button-text='确定'
            cancel-button-text='我再想想'
            icon="el-icon-warning"
            icon-color="red"
            title="确定要批量删除选中的用户吗？"
            @confirm="delBatch"
          >
            <el-button 
              type="danger" 
              slot="reference" 
              :disabled="multipleSelection.length === 0"
              icon="el-icon-delete-solid"
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
      class="user-table"
      :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: 'bold' }"
      @selection-change="handleSelectionChange"
    >
      <el-table-column type="selection" width="55" align="center"></el-table-column>
      
      <el-table-column prop="p_id" label="用户 ID" width="100" align="center">
        <template slot-scope="scope">
          <code class="id-tag">{{ scope.row.p_id }}</code>
        </template>
      </el-table-column>
      
      <el-table-column prop="p_account" label="用户名" min-width="150">
        <template slot-scope="scope">
          <span style="font-weight: 500">{{ scope.row.p_account }}</span>
        </template>
      </el-table-column>
      
      <el-table-column prop="p_password" label="当前密码状态" width="180" align="center">
        <template slot-scope="scope">
          <el-tooltip content="出于安全考虑，密码已加密显示" placement="top">
            <span class="password-shield">
              <i class="el-icon-lock"></i> ●●●●●●
            </span>
          </el-tooltip>
        </template>
      </el-table-column>
      
      <el-table-column label="管理操作" align="center" width="220">
        <template v-slot="scope">
          <el-popconfirm
            title="确定将该用户密码重置为初始状态吗？"
            @confirm="handleReset(scope.row.p_id)"
            class="action-btn"
          >
            <el-button type="text" size="small" icon="el-icon-refresh-left" slot="reference">重置密码</el-button>
          </el-popconfirm>

          <el-divider direction="vertical"></el-divider>

          <el-popconfirm
            confirm-button-text='确定'
            cancel-button-text='取消'
            title="删除后用户将无法登录，确定吗？"
            @confirm="handleDel(scope.row.p_id)"
            class="action-btn"
          >
            <el-button 
              type="text" 
              size="small" 
              icon="el-icon-delete" 
              slot="reference" 
              style="color: #F56C6C"
            >删除</el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { getAccount, resetAccount, delAccount, delAccountBatch } from '@/api/account'

export default {
  name: "account",
  data() {
    return {
      tableData: [],
      username: "",
      multipleSelection: [],
    }
  },
  created() {
    this.load()
  },
  methods: {
    load() {
      getAccount({ username: this.username }).then(res => {
        // 假设返回结构为 { accounts: [...] }
        this.tableData = res.accounts || [];
      }).catch(error => {
        this.$message.error("获取账号列表失败");
      });
    },

    handleReset(id) {
      this.request.get("/resetAccount/", {
        params: { p_id: id }
      }).then(res => {
        this.$message.success("密码重置成功");
        this.load();
      });
    },

    handleDel(p_id) {
      this.request.get("/delAccount/", {
        params: { p_id: p_id }
      }).then(res => {
        this.$message.success("用户已成功注销");
        this.load();
      });
    },

    delBatch() {
      if (!this.multipleSelection.length) return;
      
      let p_ids = this.multipleSelection.map(v => v.p_id).join(",");
      this.request.get("/delAccountBatch", {
        params: { p_ids: p_ids }
      }).then(res => {
        this.$message.success(`成功批量删除 ${this.multipleSelection.length} 个账号`);
        this.load();
      }).catch(err => {
        this.$message.error("批量删除失败");
      });
    },

    reset() {
      this.username = "";
      this.load();
    },

    handleSelectionChange(val) {
      this.multipleSelection = val;
    }
  }
}
</script>

<style scoped>
.user-manage-container {
  padding: 20px;
  background-color: #f9fafc;
  min-height: 100%;
}

.toolbar-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.toolbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-group {
  display: flex;
  gap: 10px;
}

.search-input {
  width: 240px !important;
}

.user-table {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.id-tag {
  background-color: #f0f2f5;
  padding: 2px 6px;
  border-radius: 4px;
  color: #909399;
  font-family: monospace;
}

.password-shield {
  color: #C0C4CC;
  font-size: 12px;
}

.action-btn {
  display: inline-block;
  margin: 0 5px;
}

/* 覆盖 Element UI 原生样式 */
::v-deep .el-table__row:hover {
  cursor: default;
}
</style>
<template>
  <div>
    <el-button type="primary" style="margin-bottom: 10px" @click="addRelation">新增关联人</el-button>
    <el-table :data="tableData" border stripe :header-cell-class-name="headerBg"
              @selection-change="handleSelectionChange">//表格数据需要绑定
      <el-table-column prop="name" label="关联人姓名" width="150">
      </el-table-column>
      <el-table-column prop="phone" label="关联人联系电话" width="200">
      </el-table-column>
      <el-table-column prop="card" label="关联人身份证号" width="300">
      </el-table-column>
      <el-table-column label="操作" align="center">
        <template v-slot="scope">
          <el-popconfirm
              confirm-button-text='确定'
              cancel-button-text='我再想想'
              icon="el-icon-info"
              icon-color="red"
              title="你确定删除吗？"
              @confirm="handleDel(scope.row.card)"
              class="ml-5"
          >
            <el-button type="danger" slot="reference">删除<i class="el-icon-remove-outline"></i></el-button>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="关联人信息" :visible.sync="dialogFormVisible" width="30%">
      <el-form label-width="80px" size="small">
        <el-form-item label="姓名">
          <el-input v-model="form.name" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="save">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "ScoreLog",
  data() {
    return {
      tableData: [],
      form: {},
      select: '',
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
      this.request.get("/getRelation/", {
        params: {p_id: this.p_id}
      }).then(res => {
        if (res.status === 'success' && res.data.relation) {
          this.tableData = res.data.relation;
        } else {
          this.$message.error(res.message);
        }
      });
    },

    save() {
      // 将表单数据编码为查询字符串
      const params = new URLSearchParams({
        p_main: this.p_id,
        p_name: this.form.name  // 展开form对象作为查询参数
      }).toString();

      // 发送GET请求
      this.request.get(`/addRelation/?${params}`).then(res => {
        if (res.status === 'success') {
          this.$message.success('关联人信息添加成功！');
          this.dialogFormVisible = false; // 关闭对话框
          this.load()
        } else {
          this.$message.error('添加失败: ' + res.message);
          this.load()
        }
      })
    },

    handleDel(card) {
      this.request.get("/delRelation/", {
        params: {
          p_main: this.p_id,
          card: card  // 被关联人的姓名
        }
      }).then(res => {
        if (res.status === 'success') {
          this.$message.success('关联人删除成功');
        } else {
          this.$message.error('删除失败: ' + res.message);
        }
        this.load()
      }).catch(error => {
        this.$message.error('请求失败: ' + error);
      });
    },
    handleEdit(row) {
      this.dialogFormVisible = true
      this.form = row//已经绑定过save（）
      this.select = row.card
      this.load()
    },
    addRelation() {
      this.dialogFormVisible = true
    }
  }
}
</script>

<style>
.headerBg {
  background: #eee !important;
}
</style>>
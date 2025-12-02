<template>
  <div>
    <el-calendar>
      <template
          slot="dateCell"
          slot-scope="{date, data}">
        <p :class="data.isSelected ? 'is-selected' : ''">
          {{ data.day.split('-').slice(1).join('-') }} {{ data.isSelected ? '✔️' : '' }}
        </p>
        <div style="width:100%;" v-for="item in scheduleData" :key="item">
          <el-tag type="danger" v-if="item.scheduleDay==data.day">
            {{ item.content }}
          </el-tag>
        </div>
      </template>
    </el-calendar>
  </div>
</template>

<script>
import MiddleUtil from "@/utils/MiddleUtil";

export default {
  name: "Home",
  data() {
    return {
      value: new Date(),
      adminShow: false,
      userShow: false,
      headerBg: 'headerBg',
      scheduleData: [],
      type:localStorage.getItem('user'),
      p_id: localStorage.getItem('p_id'),
    }
  },
  methods: {
    load() {
      this.request.get("/getSchedule/", {
        params: {
          type: this.type,
          p_id:this.p_id
        }
      }).then(response => {
        this.scheduleData=response.res
      })
    },
    mounted() {

    }
  },
  created() {
    let res = localStorage.getItem('user')
    if (res === '2') this.adminShow = true
    if (res === '1') this.userShow = true
    this.load()
  }
}
</script>

<style scoped>

</style>
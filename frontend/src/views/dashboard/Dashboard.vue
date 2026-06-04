<template>
  <div>
    <el-row :gutter="20" class="overview-cards">
      <el-col :span="6" v-for="card in cards" :key="card.title">
        <el-card shadow="hover">
          <div class="card-content">
            <div class="card-info">
              <div class="card-value">{{ card.value }}</div>
              <div class="card-title">{{ card.title }}</div>
            </div>
            <el-icon :size="40" :color="card.color"><component :is="card.icon" /></el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="16">
        <el-card>
          <template #header>近7天出入趋势</template>
          <v-chart :option="trendOption" style="height:300px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>楼栋通行排名</template>
          <v-chart :option="rankOption" style="height:300px" autoresize />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="12">
        <el-card>
          <template #header>今日时段分布</template>
          <v-chart :option="hourlyOption" style="height:280px" autoresize />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>告警类型统计</template>
          <v-chart :option="alertOption" style="height:280px" autoresize />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart, PieChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, TitleComponent } from 'echarts/components'
import { getOverview, getAccessTrend, getBuildingRank, getHourly, getAlertsSummary } from '../../api/statistics'

use([CanvasRenderer, LineChart, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

const overview = ref({})
const trend = ref([])
const rank = ref([])
const hourly = ref([])
const alerts = ref([])

const cards = computed(() => [
  { title: '学生总数', value: overview.value.total_students || 0, icon: 'User', color: '#409EFF' },
  { title: '宿舍楼栋', value: overview.value.total_buildings || 0, icon: 'School', color: '#67C23A' },
  { title: '今日通行', value: overview.value.today_access || 0, icon: 'Tickets', color: '#E6A23C' },
  { title: '未处理告警', value: overview.value.unread_alerts || 0, icon: 'Warning', color: '#F56C6C' },
])

const trendOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: trend.value.map(i => i.date.slice(5)) },
  yAxis: { type: 'value' },
  series: [{ data: trend.value.map(i => i.count), type: 'line', smooth: true, areaStyle: {} }]
}))

const rankOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'value' },
  yAxis: { type: 'category', data: rank.value.map(i => i.name).reverse() },
  series: [{ data: rank.value.map(i => i.count).reverse(), type: 'bar', colorBy: 'data' }]
}))

const hourlyOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  xAxis: { type: 'category', data: hourly.value.map(i => i.hour + ':00') },
  yAxis: { type: 'value' },
  series: [{ data: hourly.value.map(i => i.count), type: 'bar' }]
}))

const alertTypeMap = { unknown_face: '未识别人脸', unauthorized: '未授权通行', forced: '强行闯入', tailgate: '尾随进入' }
const alertOption = computed(() => ({
  tooltip: { trigger: 'item' },
  series: [{
    type: 'pie', radius: ['40%', '70%'],
    data: alerts.value.map(i => ({ name: alertTypeMap[i.type] || i.type, value: i.count }))
  }]
}))

onMounted(async () => {
  const [r1, r2, r3, r4, r5] = await Promise.all([
    getOverview(), getAccessTrend({ days: 7 }), getBuildingRank(), getHourly(), getAlertsSummary()
  ])
  overview.value = r1.data || {}
  trend.value = r2.data || []
  rank.value = r3.data || []
  hourly.value = r4.data || []
  alerts.value = r5.data || []
})
</script>

<style scoped>
.card-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}
.card-title {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}
</style>

<template>
  <el-card>
    <template #header>
      <el-form inline>
        <el-form-item label="楼栋">
          <el-select v-model="filters.building_id" placeholder="全部" clearable @change="fetchData">
            <el-option v-for="b in buildings" :key="b.id" :label="b.name" :value="b.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="方向">
          <el-select v-model="filters.direction" placeholder="全部" clearable @change="fetchData">
            <el-option label="进入" value="in" />
            <el-option label="离开" value="out" />
          </el-select>
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker v-model="dateRange" type="daterange" start-placeholder="开始" end-placeholder="结束"
            value-format="YYYY-MM-DD" @change="handleDateChange" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="filters.keyword" placeholder="姓名" clearable @keyup.enter="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">查询</el-button>
        </el-form-item>
      </el-form>
    </template>

    <el-table :data="logs" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="user_name" label="姓名" width="100" />
      <el-table-column prop="building_name" label="楼栋" width="100" />
      <el-table-column label="方向" width="70">
        <template #default="{ row }">
          <el-tag :type="row.direction === 'in' ? 'success' : 'warning'" size="small">
            {{ row.direction === 'in' ? '进入' : '离开' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="method" label="方式" width="80">
        <template #default="{ row }">{{ {face:'人脸',manual:'手动',visitor:'访客'}[row.method] || row.method }}</template>
      </el-table-column>
      <el-table-column label="置信度" width="80">
        <template #default="{ row }">{{ row.confidence ? (row.confidence * 100).toFixed(0) + '%' : '-' }}</template>
      </el-table-column>
      <el-table-column label="授权" width="70">
        <template #default="{ row }">
          <el-tag :type="row.is_authorized ? 'success' : 'danger'" size="small">
            {{ row.is_authorized ? '通过' : '拒绝' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" width="170" />
    </el-table>

    <el-pagination
      style="margin-top:16px;justify-content:flex-end"
      v-model:current-page="page"
      :page-size="perPage"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="fetchData"
    />
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getAccessLogs } from '../../api/access'
import { getBuildings } from '../../api/buildings'

const logs = ref([])
const buildings = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = 20
const total = ref(0)
const dateRange = ref(null)
const filters = reactive({ building_id: '', direction: '', keyword: '', start_date: '', end_date: '' })

function handleDateChange(val) {
  filters.start_date = val ? val[0] : ''
  filters.end_date = val ? val[1] : ''
  fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getAccessLogs({ page: page.value, per_page: perPage, ...filters })
    logs.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const res = await getBuildings()
  buildings.value = res.data || []
  fetchData()
})
</script>

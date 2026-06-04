<template>
  <el-card>
    <template #header>我的出入记录</template>

    <el-table :data="logs" stripe v-loading="loading">
      <el-table-column prop="building_name" label="楼栋" width="120" />
      <el-table-column label="方向" width="80">
        <template #default="{ row }">
          <el-tag :type="row.direction === 'in' ? 'success' : 'warning'" size="small">
            {{ row.direction === 'in' ? '进入' : '离开' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="method" label="方式" width="80">
        <template #default="{ row }">{{ {face:'人脸',manual:'手动'}[row.method] || row.method }}</template>
      </el-table-column>
      <el-table-column label="结果" width="80">
        <template #default="{ row }">
          <el-tag :type="row.is_authorized ? 'success' : 'danger'" size="small">
            {{ row.is_authorized ? '通过' : '拒绝' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" />
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
import { ref, onMounted } from 'vue'
import { getMyAccessLogs } from '../../api/access'

const logs = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = 20
const total = ref(0)

async function fetchData() {
  loading.value = true
  try {
    const res = await getMyAccessLogs({ page: page.value, per_page: perPage })
    logs.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

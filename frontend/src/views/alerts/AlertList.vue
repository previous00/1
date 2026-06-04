<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>异常告警</span>
        <el-form inline>
          <el-form-item>
            <el-select v-model="filterStatus" placeholder="状态" clearable @change="fetchData">
              <el-option label="未读" value="unread" />
              <el-option label="已读" value="read" />
              <el-option label="已处理" value="resolved" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-select v-model="filterType" placeholder="类型" clearable @change="fetchData">
              <el-option label="未识别人脸" value="unknown_face" />
              <el-option label="未授权通行" value="unauthorized" />
            </el-select>
          </el-form-item>
        </el-form>
      </div>
    </template>

    <el-table :data="alerts" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column label="类型" width="120">
        <template #default="{ row }">
          <el-tag :type="row.alert_type === 'unknown_face' ? 'danger' : 'warning'" size="small">
            {{ {unknown_face:'未识别人脸', unauthorized:'未授权通行', forced:'强行闯入'}[row.alert_type] || row.alert_type }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="building_name" label="楼栋" width="100" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="{unread:'danger',read:'warning',resolved:'success'}[row.status]" size="small">
            {{ {unread:'未读',read:'已读',resolved:'已处理'}[row.status] }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="时间" width="170" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleRead(row)" v-if="row.status === 'unread'">标记已读</el-button>
          <el-button size="small" type="success" @click="handleResolve(row)" v-if="row.status !== 'resolved'">处理</el-button>
        </template>
      </el-table-column>
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
import { ElMessage } from 'element-plus'
import { getAlerts, markAlertRead, resolveAlert } from '../../api/alerts'

const alerts = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = 20
const total = ref(0)
const filterStatus = ref('')
const filterType = ref('')

async function fetchData() {
  loading.value = true
  try {
    const res = await getAlerts({ page: page.value, per_page: perPage, status: filterStatus.value, alert_type: filterType.value })
    alerts.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function handleRead(row) {
  await markAlertRead(row.id)
  ElMessage.success('已标记')
  fetchData()
}

async function handleResolve(row) {
  await resolveAlert(row.id)
  ElMessage.success('已处理')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

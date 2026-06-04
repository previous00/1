<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <el-form inline>
          <el-form-item>
            <el-select v-model="filterStatus" placeholder="状态" clearable @change="fetchData">
              <el-option label="待审批" value="pending" />
              <el-option label="已批准" value="approved" />
              <el-option label="已拒绝" value="rejected" />
              <el-option label="已完成" value="completed" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchData">查询</el-button>
          </el-form-item>
        </el-form>
      </div>
    </template>

    <el-table :data="visitors" stripe v-loading="loading">
      <el-table-column prop="name" label="访客姓名" width="100" />
      <el-table-column prop="phone" label="电话" width="120" />
      <el-table-column prop="reason" label="来访事由" />
      <el-table-column prop="visit_target_name" label="拜访对象" width="100" />
      <el-table-column prop="building_name" label="楼栋" width="100" />
      <el-table-column prop="applicant_name" label="申请人" width="100" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="170" />
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button size="small" type="success" @click="handleApprove(row)">批准</el-button>
            <el-button size="small" type="danger" @click="handleReject(row)">拒绝</el-button>
          </template>
          <el-button size="small" type="warning" @click="handleComplete(row)" v-if="row.status === 'approved'">结束访问</el-button>
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
import { getVisitors, approveVisitor, rejectVisitor, completeVisitor } from '../../api/visitors'

const visitors = ref([])
const loading = ref(false)
const page = ref(1)
const perPage = 20
const total = ref(0)
const filterStatus = ref('')

const statusLabel = (s) => ({ pending: '待审批', approved: '已批准', rejected: '已拒绝', completed: '已完成' }[s] || s)
const statusType = (s) => ({ pending: 'warning', approved: 'success', rejected: 'danger', completed: 'info' }[s] || '')

async function fetchData() {
  loading.value = true
  try {
    const res = await getVisitors({ page: page.value, per_page: perPage, status: filterStatus.value })
    visitors.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function handleApprove(row) {
  await approveVisitor(row.id)
  ElMessage.success('已批准')
  fetchData()
}

async function handleReject(row) {
  await rejectVisitor(row.id)
  ElMessage.success('已拒绝')
  fetchData()
}

async function handleComplete(row) {
  await completeVisitor(row.id)
  ElMessage.success('访问已结束')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

<template>
  <div>
    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="学生账号" name="student">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <el-tag type="primary" size="large">学生账号 ({{ studentTotal }}人)</el-tag>
              <el-form inline>
                <el-form-item>
                  <el-input v-model="keyword" placeholder="搜索学号/姓名" clearable @keyup.enter="fetchData" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="fetchData">搜索</el-button>
                </el-form-item>
              </el-form>
            </div>
          </template>

          <el-table :data="users" stripe v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="username" label="用户名/学号" width="130" />
            <el-table-column prop="real_name" label="姓名" width="100" />
            <el-table-column prop="phone" label="手机" width="130" />
            <el-table-column label="角色" width="80">
              <template #default>
                <el-tag>学生</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '正常' : '禁用' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="注册时间" width="170" />
            <el-table-column label="操作" width="160" fixed="right">
              <template #default="{ row }">
                <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="toggleStatus(row)">
                  {{ row.is_active ? '禁用' : '启用' }}
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="宿管账号" name="manager">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <el-tag type="warning" size="large">宿管账号 ({{ managerTotal }}人)</el-tag>
              <el-form inline>
                <el-form-item>
                  <el-input v-model="keyword" placeholder="搜索姓名" clearable @keyup.enter="fetchData" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="fetchData">搜索</el-button>
                </el-form-item>
              </el-form>
            </div>
          </template>

          <el-table :data="users" stripe v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="username" label="用户名" width="130" />
            <el-table-column prop="real_name" label="姓名" width="100" />
            <el-table-column prop="phone" label="手机" width="130" />
            <el-table-column label="角色" width="80">
              <template #default>
                <el-tag type="warning">宿管</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '正常' : '禁用' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="注册时间" width="170" />
            <el-table-column label="操作" width="160" fixed="right">
              <template #default="{ row }">
                <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="toggleStatus(row)">
                  {{ row.is_active ? '禁用' : '启用' }}
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>

      <el-tab-pane label="管理员账号" name="admin">
        <el-card shadow="never">
          <template #header>
            <div class="card-header">
              <el-tag type="danger" size="large">管理员账号 ({{ adminTotal }}人)</el-tag>
              <el-form inline>
                <el-form-item>
                  <el-input v-model="keyword" placeholder="搜索姓名" clearable @keyup.enter="fetchData" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="fetchData">搜索</el-button>
                </el-form-item>
              </el-form>
            </div>
          </template>

          <el-table :data="users" stripe v-loading="loading">
            <el-table-column prop="id" label="ID" width="60" />
            <el-table-column prop="username" label="用户名" width="130" />
            <el-table-column prop="real_name" label="姓名" width="100" />
            <el-table-column prop="phone" label="手机" width="130" />
            <el-table-column label="角色" width="80">
              <template #default>
                <el-tag type="danger">管理员</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'info'">{{ row.is_active ? '正常' : '禁用' }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="注册时间" width="170" />
            <el-table-column label="操作" width="160" fixed="right">
              <template #default="{ row }">
                <el-button size="small" :type="row.is_active ? 'warning' : 'success'" @click="toggleStatus(row)">
                  {{ row.is_active ? '禁用' : '启用' }}
                </el-button>
                <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <el-pagination
      style="margin-top:16px;justify-content:flex-end"
      v-model:current-page="page"
      :page-size="perPage"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="fetchData"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsers, toggleUserStatus, deleteUser } from '../../api/users'

const users = ref([])
const loading = ref(false)
const keyword = ref('')
const activeTab = ref('student')
const page = ref(1)
const perPage = 20
const total = ref(0)
const studentTotal = ref(0)
const managerTotal = ref(0)
const adminTotal = ref(0)

function handleTabChange() {
  page.value = 1
  keyword.value = ''
  fetchData()
}

async function fetchData() {
  loading.value = true
  try {
    const res = await getUsers({ page: page.value, per_page: perPage, keyword: keyword.value, role: activeTab.value })
    users.value = res.data.items
    total.value = res.data.total

    if (activeTab.value === 'student') studentTotal.value = res.data.total
    else if (activeTab.value === 'manager') managerTotal.value = res.data.total
    else if (activeTab.value === 'admin') adminTotal.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function fetchCounts() {
  const [s, m, a] = await Promise.all([
    getUsers({ page: 1, per_page: 1, role: 'student' }),
    getUsers({ page: 1, per_page: 1, role: 'manager' }),
    getUsers({ page: 1, per_page: 1, role: 'admin' }),
  ])
  studentTotal.value = s.data.total
  managerTotal.value = m.data.total
  adminTotal.value = a.data.total
}

async function toggleStatus(row) {
  await toggleUserStatus(row.id, { is_active: !row.is_active })
  ElMessage.success('状态已更新')
  fetchData()
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除用户"${row.real_name}"吗？`, '提示', { type: 'warning' })
  await deleteUser(row.id)
  ElMessage.success('已删除')
  fetchData()
  fetchCounts()
}

onMounted(() => {
  fetchData()
  fetchCounts()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

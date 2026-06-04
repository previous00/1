<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span>楼栋管理</span>
        <el-button type="primary" @click="showDialog = true">新增楼栋</el-button>
      </div>
    </template>

    <el-table :data="buildings" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="楼栋名称" width="120" />
      <el-table-column prop="address" label="地址" />
      <el-table-column prop="floors" label="层数" width="80" />
      <el-table-column prop="manager_name" label="负责宿管" width="100" />
      <el-table-column prop="room_count" label="房间数" width="80" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" :title="editId ? '编辑楼栋' : '新增楼栋'" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="地址"><el-input v-model="form.address" /></el-form-item>
        <el-form-item label="层数"><el-input-number v-model="form.floors" :min="1" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDialog = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getBuildings, createBuilding, updateBuilding, deleteBuilding } from '../../api/buildings'

const buildings = ref([])
const loading = ref(false)
const submitting = ref(false)
const showDialog = ref(false)
const editId = ref(null)
const form = reactive({ name: '', address: '', floors: 6 })

async function fetchData() {
  loading.value = true
  try {
    const res = await getBuildings()
    buildings.value = res.data || []
  } finally {
    loading.value = false
  }
}

function handleEdit(row) {
  editId.value = row.id
  form.name = row.name
  form.address = row.address
  form.floors = row.floors
  showDialog.value = true
}

async function submitForm() {
  submitting.value = true
  try {
    if (editId.value) {
      await updateBuilding(editId.value, form)
    } else {
      await createBuilding(form)
    }
    ElMessage.success(editId.value ? '更新成功' : '创建成功')
    showDialog.value = false
    editId.value = null
    form.name = ''; form.address = ''; form.floors = 6
    fetchData()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除"${row.name}"吗？`, '提示', { type: 'warning' })
  await deleteBuilding(row.id)
  ElMessage.success('已删除')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

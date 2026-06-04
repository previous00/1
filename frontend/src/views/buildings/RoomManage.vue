<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <el-form inline>
          <el-form-item label="楼栋">
            <el-select v-model="buildingId" placeholder="选择楼栋" @change="fetchRooms">
              <el-option v-for="b in buildings" :key="b.id" :label="b.name" :value="b.id" />
            </el-select>
          </el-form-item>
        </el-form>
        <el-button type="primary" @click="showDialog = true" :disabled="!buildingId">新增房间</el-button>
      </div>
    </template>

    <el-table :data="rooms" stripe v-loading="loading">
      <el-table-column prop="room_number" label="房间号" width="100" />
      <el-table-column prop="floor" label="楼层" width="80" />
      <el-table-column prop="capacity" label="容量" width="80" />
      <el-table-column prop="current_count" label="已住" width="80" />
      <el-table-column label="入住率" width="120">
        <template #default="{ row }">
          <el-progress :percentage="Math.round(row.current_count / row.capacity * 100)" :status="row.current_count >= row.capacity ? 'exception' : ''" />
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="showDialog" title="新增房间" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="房间号"><el-input v-model="form.room_number" placeholder="如：301" /></el-form-item>
        <el-form-item label="楼层"><el-input-number v-model="form.floor" :min="1" /></el-form-item>
        <el-form-item label="容量"><el-input-number v-model="form.capacity" :min="1" :max="8" /></el-form-item>
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
import { getBuildings, getBuildingRooms, createRoom, deleteRoom } from '../../api/buildings'

const buildings = ref([])
const rooms = ref([])
const loading = ref(false)
const submitting = ref(false)
const buildingId = ref(null)
const showDialog = ref(false)
const form = reactive({ room_number: '', floor: 1, capacity: 4 })

async function fetchBuildings() {
  const res = await getBuildings()
  buildings.value = res.data || []
  if (buildings.value.length) {
    buildingId.value = buildings.value[0].id
    fetchRooms()
  }
}

async function fetchRooms() {
  if (!buildingId.value) return
  loading.value = true
  try {
    const res = await getBuildingRooms(buildingId.value)
    rooms.value = res.data || []
  } finally {
    loading.value = false
  }
}

async function submitForm() {
  submitting.value = true
  try {
    await createRoom({ ...form, building_id: buildingId.value })
    ElMessage.success('创建成功')
    showDialog.value = false
    form.room_number = ''; form.floor = 1; form.capacity = 4
    fetchRooms()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row) {
  await ElMessageBox.confirm(`确定删除房间"${row.room_number}"吗？`, '提示', { type: 'warning' })
  await deleteRoom(row.id)
  ElMessage.success('已删除')
  fetchRooms()
}

onMounted(fetchBuildings)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>

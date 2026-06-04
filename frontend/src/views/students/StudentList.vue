<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <el-form inline>
          <el-form-item>
            <el-input v-model="keyword" placeholder="搜索学号/姓名" clearable @clear="fetchData" @keyup.enter="fetchData" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="fetchData">搜索</el-button>
          </el-form-item>
          <el-form-item>
            <el-button type="success" @click="showCreate = true">新增学生</el-button>
          </el-form-item>
        </el-form>
      </div>
    </template>

    <el-table :data="students" stripe v-loading="loading">
      <el-table-column prop="student_no" label="学号" width="130" />
      <el-table-column label="姓名" width="100">
        <template #default="{ row }">{{ row.user?.real_name }}</template>
      </el-table-column>
      <el-table-column prop="gender" label="性别" width="60" />
      <el-table-column prop="college" label="学院" />
      <el-table-column prop="major" label="专业" />
      <el-table-column prop="class_name" label="班级" width="100" />
      <el-table-column label="宿舍" width="150">
        <template #default="{ row }">
          {{ row.room ? `${row.room.building_name} ${row.room.room_number}` : '未分配' }}
        </template>
      </el-table-column>
      <el-table-column prop="check_in_date" label="入住日期" width="110" />
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleEdit(row)">编辑</el-button>
          <el-button size="small" type="success" @click="handleCheckin(row)" v-if="!row.room_id">入住</el-button>
          <el-button size="small" type="warning" @click="handleCheckout(row)" v-else>退宿</el-button>
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

    <el-dialog v-model="showCreate" title="新增学生" width="500px">
      <el-form :model="createForm" label-width="80px">
        <el-form-item label="学号"><el-input v-model="createForm.student_no" /></el-form-item>
        <el-form-item label="姓名"><el-input v-model="createForm.real_name" /></el-form-item>
        <el-form-item label="性别">
          <el-radio-group v-model="createForm.gender">
            <el-radio value="男">男</el-radio>
            <el-radio value="女">女</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="学院"><el-input v-model="createForm.college" /></el-form-item>
        <el-form-item label="专业"><el-input v-model="createForm.major" /></el-form-item>
        <el-form-item label="班级"><el-input v-model="createForm.class_name" /></el-form-item>
        <el-form-item label="入学年份"><el-input v-model.number="createForm.enrollment_year" /></el-form-item>
        <el-form-item label="手机号"><el-input v-model="createForm.phone" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreate = false">取消</el-button>
        <el-button type="primary" @click="submitCreate" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="showCheckin" title="入住分配" width="400px">
      <el-form label-width="80px">
        <el-form-item label="选择楼栋">
          <el-select v-model="checkinBuildingId" @change="loadRooms" style="width:100%">
            <el-option v-for="b in buildings" :key="b.id" :label="b.name" :value="b.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="选择房间">
          <el-select v-model="checkinRoomId" style="width:100%">
            <el-option v-for="r in rooms" :key="r.id"
              :label="`${r.room_number} (${r.current_count}/${r.capacity})`"
              :value="r.id" :disabled="r.current_count >= r.capacity" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCheckin = false">取消</el-button>
        <el-button type="primary" @click="submitCheckin" :loading="submitting">确定入住</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getStudents, createStudent, checkinStudent, checkoutStudent } from '../../api/students'
import { getBuildings, getBuildingRooms } from '../../api/buildings'

const students = ref([])
const loading = ref(false)
const submitting = ref(false)
const keyword = ref('')
const page = ref(1)
const perPage = 20
const total = ref(0)

const showCreate = ref(false)
const createForm = reactive({
  student_no: '', real_name: '', gender: '男', college: '', major: '',
  class_name: '', enrollment_year: new Date().getFullYear(), phone: ''
})

const showCheckin = ref(false)
const checkinStudentId = ref(null)
const checkinBuildingId = ref(null)
const checkinRoomId = ref(null)
const buildings = ref([])
const rooms = ref([])

async function fetchData() {
  loading.value = true
  try {
    const res = await getStudents({ page: page.value, per_page: perPage, keyword: keyword.value })
    students.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

async function submitCreate() {
  submitting.value = true
  try {
    await createStudent(createForm)
    ElMessage.success('创建成功')
    showCreate.value = false
    fetchData()
  } finally {
    submitting.value = false
  }
}

function handleEdit(row) {
  ElMessage.info('编辑功能待完善')
}

async function handleCheckin(row) {
  checkinStudentId.value = row.id
  checkinBuildingId.value = null
  checkinRoomId.value = null
  rooms.value = []
  if (!buildings.value.length) {
    const res = await getBuildings()
    buildings.value = res.data || []
  }
  showCheckin.value = true
}

async function loadRooms() {
  if (checkinBuildingId.value) {
    const res = await getBuildingRooms(checkinBuildingId.value)
    rooms.value = res.data || []
  }
}

async function submitCheckin() {
  if (!checkinRoomId.value) return ElMessage.warning('请选择房间')
  submitting.value = true
  try {
    await checkinStudent(checkinStudentId.value, { room_id: checkinRoomId.value })
    ElMessage.success('入住成功')
    showCheckin.value = false
    fetchData()
  } finally {
    submitting.value = false
  }
}

async function handleCheckout(row) {
  await ElMessageBox.confirm('确定要办理退宿吗？', '提示')
  await checkoutStudent(row.id)
  ElMessage.success('退宿成功')
  fetchData()
}

onMounted(fetchData)
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>

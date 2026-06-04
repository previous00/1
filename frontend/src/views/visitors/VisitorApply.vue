<template>
  <el-card>
    <template #header>访客申请</template>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" style="max-width:500px">
      <el-form-item label="访客姓名" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      <el-form-item label="身份证号">
        <el-input v-model="form.id_card" />
      </el-form-item>
      <el-form-item label="联系电话">
        <el-input v-model="form.phone" />
      </el-form-item>
      <el-form-item label="来访楼栋" prop="building_id">
        <el-select v-model="form.building_id" style="width:100%">
          <el-option v-for="b in buildings" :key="b.id" :label="b.name" :value="b.id" />
        </el-select>
      </el-form-item>
      <el-form-item label="来访事由" prop="reason">
        <el-input v-model="form.reason" type="textarea" :rows="3" />
      </el-form-item>
      <el-form-item label="预计到访">
        <el-date-picker v-model="form.visit_start" type="datetime" placeholder="开始时间" value-format="YYYY-MM-DDTHH:mm:ss" />
      </el-form-item>
      <el-form-item label="预计离开">
        <el-date-picker v-model="form.visit_end" type="datetime" placeholder="结束时间" value-format="YYYY-MM-DDTHH:mm:ss" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm" :loading="submitting">提交申请</el-button>
      </el-form-item>
    </el-form>

    <el-divider />
    <h4>我的申请记录</h4>
    <el-table :data="myVisitors" stripe size="small">
      <el-table-column prop="name" label="访客" width="80" />
      <el-table-column prop="building_name" label="楼栋" width="80" />
      <el-table-column prop="reason" label="事由" />
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)" size="small">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="申请时间" width="170" />
    </el-table>
  </el-card>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { createVisitor, getMyVisitors } from '../../api/visitors'
import { getBuildings } from '../../api/buildings'

const buildings = ref([])
const myVisitors = ref([])
const formRef = ref()
const submitting = ref(false)

const form = reactive({
  name: '', id_card: '', phone: '', building_id: null, reason: '',
  visit_start: '', visit_end: ''
})
const rules = {
  name: [{ required: true, message: '请输入访客姓名', trigger: 'blur' }],
  building_id: [{ required: true, message: '请选择楼栋', trigger: 'change' }],
  reason: [{ required: true, message: '请填写来访事由', trigger: 'blur' }],
}

const statusLabel = (s) => ({ pending: '待审批', approved: '已批准', rejected: '已拒绝', completed: '已完成' }[s] || s)
const statusType = (s) => ({ pending: 'warning', approved: 'success', rejected: 'danger', completed: 'info' }[s] || '')

async function submitForm() {
  await formRef.value.validate()
  submitting.value = true
  try {
    await createVisitor(form)
    ElMessage.success('申请已提交')
    Object.assign(form, { name: '', id_card: '', phone: '', building_id: null, reason: '', visit_start: '', visit_end: '' })
    fetchMyVisitors()
  } finally {
    submitting.value = false
  }
}

async function fetchMyVisitors() {
  const res = await getMyVisitors({ page: 1, per_page: 10 })
  myVisitors.value = res.data?.items || []
}

onMounted(async () => {
  const res = await getBuildings()
  buildings.value = res.data || []
  fetchMyVisitors()
})
</script>

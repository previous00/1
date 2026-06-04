<template>
  <el-card>
    <template #header>门禁模拟</template>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-form label-width="80px">
          <el-form-item label="选择楼栋">
            <el-select v-model="buildingId" style="width:100%">
              <el-option v-for="b in buildings" :key="b.id" :label="b.name" :value="b.id" />
            </el-select>
          </el-form-item>
          <el-form-item label="通行方向">
            <el-radio-group v-model="direction">
              <el-radio value="in">进入</el-radio>
              <el-radio value="out">离开</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-form>

        <div class="capture-area">
          <el-upload action="#" :auto-upload="false" :show-file-list="false" :on-change="handleFile" accept="image/*">
            <template #trigger>
              <el-button type="primary" :icon="Upload">选择图片</el-button>
            </template>
          </el-upload>
          <el-button type="success" @click="captureFromCamera" :icon="Camera">摄像头拍照</el-button>
        </div>

        <video ref="videoRef" v-show="showCamera" autoplay style="width:100%;max-width:400px;margin-top:12px" />
        <canvas ref="canvasRef" style="display:none" />

        <div class="preview" v-if="previewUrl">
          <img :src="previewUrl" />
        </div>

        <el-button type="primary" size="large" style="margin-top:20px;width:100%" @click="submitAccess" :loading="loading" :disabled="!selectedFile || !buildingId">
          验证通行
        </el-button>
      </el-col>

      <el-col :span="12">
        <div class="result-panel" v-if="result" :class="result.authorized ? 'success' : 'denied'">
          <el-icon :size="60">
            <CircleCheckFilled v-if="result.authorized" />
            <CircleCloseFilled v-else />
          </el-icon>
          <h2>{{ result.authorized ? '通行成功' : '通行拒绝' }}</h2>
          <p v-if="result.user_name">身份: {{ result.user_name }}</p>
          <p>置信度: {{ (result.confidence * 100).toFixed(1) }}%</p>
          <p>{{ result.message }}</p>
        </div>
        <el-empty v-else description="请进行人脸验证" />
      </el-col>
    </el-row>
  </el-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Upload, Camera, CircleCheckFilled, CircleCloseFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { faceAccess } from '../../api/faces'
import { getBuildings } from '../../api/buildings'

const buildings = ref([])
const buildingId = ref(null)
const direction = ref('in')
const selectedFile = ref(null)
const previewUrl = ref('')
const loading = ref(false)
const result = ref(null)
const showCamera = ref(false)
const videoRef = ref(null)
const canvasRef = ref(null)
let stream = null

async function fetchBuildings() {
  const res = await getBuildings()
  buildings.value = res.data || []
}

function handleFile(file) {
  selectedFile.value = file.raw
  previewUrl.value = URL.createObjectURL(file.raw)
  showCamera.value = false
  stopCamera()
}

async function captureFromCamera() {
  showCamera.value = true
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 } })
    videoRef.value.srcObject = stream
    setTimeout(() => {
      const canvas = canvasRef.value
      canvas.width = 640
      canvas.height = 480
      canvas.getContext('2d').drawImage(videoRef.value, 0, 0)
      canvas.toBlob(blob => {
        selectedFile.value = new File([blob], 'capture.jpg', { type: 'image/jpeg' })
        previewUrl.value = URL.createObjectURL(blob)
      }, 'image/jpeg')
      stopCamera()
      showCamera.value = false
    }, 2000)
  } catch {
    ElMessage.error('无法访问摄像头')
    showCamera.value = false
  }
}

function stopCamera() {
  if (stream) { stream.getTracks().forEach(t => t.stop()); stream = null }
}

async function submitAccess() {
  if (!selectedFile.value || !buildingId.value) return
  loading.value = true
  result.value = null
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('building_id', buildingId.value)
    formData.append('direction', direction.value)
    const res = await faceAccess(formData)
    result.value = res.data
  } finally {
    loading.value = false
  }
}

onMounted(fetchBuildings)
onUnmounted(stopCamera)
</script>

<style scoped>
.capture-area { display: flex; gap: 12px; margin-top: 12px; }
.preview { margin-top: 12px; }
.preview img { max-width: 100%; max-height: 300px; border-radius: 8px; border: 1px solid #eee; }
.result-panel {
  text-align: center;
  padding: 40px;
  border-radius: 12px;
  margin-top: 20px;
}
.result-panel.success { background: #f0f9eb; color: #67c23a; }
.result-panel.denied { background: #fef0f0; color: #f56c6c; }
.result-panel h2 { margin: 16px 0 8px; }
.result-panel p { color: #606266; margin: 4px 0; }
</style>

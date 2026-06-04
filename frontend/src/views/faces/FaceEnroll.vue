<template>
  <div>
    <el-card>
      <template #header>人脸录入</template>
      <el-row :gutter="20">
        <el-col :span="12">
          <div class="upload-area">
            <el-upload
              ref="uploadRef"
              action="#"
              :auto-upload="false"
              :show-file-list="false"
              :on-change="handleFileChange"
              accept="image/*"
            >
              <template #trigger>
                <el-button type="primary" :icon="Upload">选择图片</el-button>
              </template>
            </el-upload>
            <el-button type="success" style="margin-left:12px" @click="captureFromCamera" :icon="Camera">
              摄像头拍照
            </el-button>
            <div class="preview" v-if="previewUrl">
              <img :src="previewUrl" alt="预览" />
            </div>
            <video ref="videoRef" v-show="showCamera" autoplay style="width:100%;max-width:400px;margin-top:12px" />
            <canvas ref="canvasRef" style="display:none" />
          </div>
          <el-button type="primary" style="margin-top:16px" @click="submitEnroll" :loading="submitting" :disabled="!selectedFile">
            确认录入
          </el-button>
        </el-col>
        <el-col :span="12">
          <h4>已录入的人脸</h4>
          <el-empty v-if="!faces.length" description="暂未录入人脸" />
          <div v-for="face in faces" :key="face.id" class="face-item">
            <el-tag>{{ face.is_primary ? '主要' : '备用' }}</el-tag>
            <span>{{ face.created_at }}</span>
            <el-button size="small" type="danger" text @click="handleDelete(face)">删除</el-button>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Upload, Camera } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { enrollFace, getMyFaces, deleteFace } from '../../api/faces'

const faces = ref([])
const selectedFile = ref(null)
const previewUrl = ref('')
const submitting = ref(false)
const showCamera = ref(false)
const videoRef = ref(null)
const canvasRef = ref(null)
let stream = null

async function fetchFaces() {
  const res = await getMyFaces()
  faces.value = res.data || []
}

function handleFileChange(file) {
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
  } catch (e) {
    ElMessage.error('无法访问摄像头')
    showCamera.value = false
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(t => t.stop())
    stream = null
  }
}

async function submitEnroll() {
  if (!selectedFile.value) return
  submitting.value = true
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    await enrollFace(formData)
    ElMessage.success('人脸录入成功')
    selectedFile.value = null
    previewUrl.value = ''
    fetchFaces()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(face) {
  await deleteFace(face.id)
  ElMessage.success('已删除')
  fetchFaces()
}

onMounted(fetchFaces)
onUnmounted(stopCamera)
</script>

<style scoped>
.upload-area { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 12px; }
.preview { width: 100%; margin-top: 12px; }
.preview img { max-width: 400px; border-radius: 8px; border: 1px solid #eee; }
.face-item { display: flex; align-items: center; gap: 12px; padding: 8px 0; border-bottom: 1px solid #f0f0f0; }
</style>

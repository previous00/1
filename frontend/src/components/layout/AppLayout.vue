<template>
  <el-container class="app-layout">
    <el-aside :width="isCollapse ? '64px' : '220px'">
      <div class="logo">
        <el-icon :size="24"><HomeFilled /></el-icon>
        <span v-show="!isCollapse">智能门禁系统</span>
      </div>
      <el-menu
        :default-active="$route.path"
        :collapse="isCollapse"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/dashboard" v-if="hasRole('manager', 'admin')">
          <el-icon><DataLine /></el-icon>
          <template #title>数据概览</template>
        </el-menu-item>

        <el-sub-menu index="dorm" v-if="hasRole('manager', 'admin')">
          <template #title>
            <el-icon><School /></el-icon>
            <span>宿舍管理</span>
          </template>
          <el-menu-item index="/buildings" v-if="hasRole('admin')">楼栋管理</el-menu-item>
          <el-menu-item index="/rooms">房间管理</el-menu-item>
          <el-menu-item index="/students">学生管理</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="face">
          <template #title>
            <el-icon><Camera /></el-icon>
            <span>人脸门禁</span>
          </template>
          <el-menu-item index="/face-enroll">人脸录入</el-menu-item>
          <el-menu-item index="/face-verify">门禁模拟</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="access">
          <template #title>
            <el-icon><Tickets /></el-icon>
            <span>出入管理</span>
          </template>
          <el-menu-item index="/access-logs" v-if="hasRole('manager', 'admin')">出入记录</el-menu-item>
          <el-menu-item index="/my-access">我的出入</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="visitor">
          <template #title>
            <el-icon><User /></el-icon>
            <span>访客管理</span>
          </template>
          <el-menu-item index="/visitors" v-if="hasRole('manager', 'admin')">访客列表</el-menu-item>
          <el-menu-item index="/visitor-apply">访客申请</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/alerts" v-if="hasRole('manager', 'admin')">
          <el-icon><Warning /></el-icon>
          <template #title>
            异常告警
            <el-badge v-if="unreadAlerts > 0" :value="unreadAlerts" class="alert-badge" />
          </template>
        </el-menu-item>

        <el-menu-item index="/users" v-if="hasRole('admin')">
          <el-icon><UserFilled /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header>
        <div class="header-left">
          <el-icon class="collapse-btn" @click="isCollapse = !isCollapse">
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          <span class="page-title">{{ $route.meta.title }}</span>
        </div>
        <div class="header-right">
          <span class="user-name">{{ authStore.userName }}</span>
          <el-tag size="small" :type="roleTagType">{{ roleLabel }}</el-tag>
          <el-button type="danger" text @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { getUnreadCount } from '../../api/alerts'

const router = useRouter()
const authStore = useAuthStore()
const isCollapse = ref(false)
const unreadAlerts = ref(0)

const roleLabel = computed(() => {
  const map = { admin: '管理员', manager: '宿管', student: '学生' }
  return map[authStore.userRole] || ''
})

const roleTagType = computed(() => {
  const map = { admin: 'danger', manager: 'warning', student: '' }
  return map[authStore.userRole] || ''
})

function hasRole(...roles) {
  return roles.includes(authStore.userRole)
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}

async function fetchAlertCount() {
  if (hasRole('manager', 'admin')) {
    try {
      const res = await getUnreadCount()
      unreadAlerts.value = res.data?.count || 0
    } catch {}
  }
}

onMounted(() => {
  fetchAlertCount()
  setInterval(fetchAlertCount, 60000)
})
</script>

<style scoped>
.app-layout {
  height: 100vh;
}
.el-aside {
  background-color: #304156;
  transition: width 0.3s;
  overflow-x: hidden;
}
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  border-bottom: 1px solid #3d4c5c;
}
.el-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
  padding: 0 20px;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.collapse-btn {
  cursor: pointer;
  font-size: 20px;
}
.page-title {
  font-size: 16px;
  font-weight: 500;
}
.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}
.user-name {
  font-size: 14px;
  color: #606266;
}
.el-main {
  background-color: #f5f7fa;
  padding: 20px;
}
.alert-badge {
  margin-left: 8px;
}
</style>

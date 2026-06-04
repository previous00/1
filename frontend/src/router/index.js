import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/',
    component: () => import('../components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/Dashboard.vue'),
        meta: { title: '数据概览', roles: ['manager', 'admin'] }
      },
      {
        path: 'students',
        name: 'Students',
        component: () => import('../views/students/StudentList.vue'),
        meta: { title: '学生管理', roles: ['manager', 'admin'] }
      },
      {
        path: 'buildings',
        name: 'Buildings',
        component: () => import('../views/buildings/BuildingList.vue'),
        meta: { title: '楼栋管理', roles: ['admin'] }
      },
      {
        path: 'rooms',
        name: 'Rooms',
        component: () => import('../views/buildings/RoomManage.vue'),
        meta: { title: '房间管理', roles: ['manager', 'admin'] }
      },
      {
        path: 'face-enroll',
        name: 'FaceEnroll',
        component: () => import('../views/faces/FaceEnroll.vue'),
        meta: { title: '人脸录入', roles: ['student', 'manager', 'admin'] }
      },
      {
        path: 'face-verify',
        name: 'FaceVerify',
        component: () => import('../views/faces/FaceVerify.vue'),
        meta: { title: '门禁模拟', roles: ['student', 'manager', 'admin'] }
      },
      {
        path: 'access-logs',
        name: 'AccessLogs',
        component: () => import('../views/access/AccessLog.vue'),
        meta: { title: '出入记录', roles: ['manager', 'admin'] }
      },
      {
        path: 'my-access',
        name: 'MyAccess',
        component: () => import('../views/access/MyAccess.vue'),
        meta: { title: '我的出入', roles: ['student', 'manager', 'admin'] }
      },
      {
        path: 'visitors',
        name: 'Visitors',
        component: () => import('../views/visitors/VisitorList.vue'),
        meta: { title: '访客管理', roles: ['manager', 'admin'] }
      },
      {
        path: 'visitor-apply',
        name: 'VisitorApply',
        component: () => import('../views/visitors/VisitorApply.vue'),
        meta: { title: '访客申请', roles: ['student', 'manager', 'admin'] }
      },
      {
        path: 'alerts',
        name: 'Alerts',
        component: () => import('../views/alerts/AlertList.vue'),
        meta: { title: '异常告警', roles: ['manager', 'admin'] }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('../views/students/UserList.vue'),
        meta: { title: '用户管理', roles: ['admin'] }
      },
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (to.meta.guest && authStore.isLoggedIn) {
    next('/dashboard')
  } else if (to.meta.roles && !to.meta.roles.includes(authStore.userRole)) {
    if (authStore.userRole === 'student') {
      next('/face-enroll')
    } else {
      next('/dashboard')
    }
  } else {
    next()
  }
})

export default router

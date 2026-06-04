# 智能宿舍人脸门禁管理系统

基于 Flask + Vue 3 + Element Plus 的前后端分离智能门禁管理系统，支持人脸识别、多角色管理、访客管理和数据统计分析。

## 技术栈

- **后端**: Flask + SQLAlchemy + Flask-JWT-Extended + SQLite
- **前端**: Vue 3 + Vite + Element Plus + Pinia + ECharts
- **人脸识别**: OpenCV (Haar Cascade 人脸检测 + 特征编码)

## 功能模块

- 多角色认证 (学生/宿管/管理员)
- 宿舍楼栋和房间管理
- 学生信息管理与入住/退宿
- 人脸录入与门禁模拟验证
- 出入记录自动登记与查询
- 访客申请与审批工作流
- 异常通行告警管理
- 数据统计仪表盘

## 快速开始

### 1. 后端启动

```bash
cd backend

# 创建虚拟环境 (已创建可跳过)
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化演示数据
python seed.py

# 启动服务
python run.py
```

后端运行在 http://127.0.0.1:5000

### 2. 前端启动

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173

### 3. 访问系统

打开浏览器访问 http://localhost:5173

## 演示账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 宿管 | manager1 | 123456 |
| 宿管 | manager2 | 123456 |
| 学生 | 2021001 ~ 2021008 | 123456 |

## 项目结构

```
├── backend/               # Flask 后端
│   ├── app/
│   │   ├── models/        # 数据模型
│   │   ├── api/           # REST API 接口
│   │   ├── services/      # 业务逻辑
│   │   └── utils/         # 工具函数
│   ├── uploads/faces/     # 人脸图片存储
│   ├── instance/          # SQLite 数据库
│   ├── run.py             # 启动入口
│   └── seed.py            # 演示数据
├── frontend/              # Vue 3 前端
│   ├── src/
│   │   ├── api/           # 接口封装
│   │   ├── components/    # 组件
│   │   ├── views/         # 页面
│   │   ├── router/        # 路由
│   │   └── stores/        # 状态管理
│   └── vite.config.js
└── README.md
```

## API 接口

| 模块 | 前缀 | 说明 |
|------|------|------|
| 认证 | /api/auth | 登录/注册/Token |
| 用户 | /api/users | 用户管理(管理员) |
| 学生 | /api/students | 学生CRUD/入住 |
| 楼栋 | /api/buildings | 楼栋管理 |
| 房间 | /api/rooms | 房间管理 |
| 人脸 | /api/faces | 录入/验证/门禁 |
| 出入 | /api/access | 记录查询 |
| 访客 | /api/visitors | 申请/审批 |
| 告警 | /api/alerts | 异常管理 |
| 统计 | /api/statistics | 数据分析 |

# 图书管理系统

前后端分离的图书管理系统，支持读者注册登录、图书浏览借阅，管理员图书及分类管理。

## 技术栈

- **后端**: Python Flask + SQLAlchemy + JWT + SQLite
- **前端**: Vue 3 (CDN) + 原生 CSS
- **接口**: RESTful API

## 项目结构

```
├── backend/                # 后端
│   ├── app/
│   │   ├── __init__.py     # 应用工厂
│   │   ├── models.py       # 数据模型
│   │   └── api/            # API蓝图
│   │       ├── auth.py     # 认证（注册/登录）
│   │       ├── books.py    # 图书CRUD
│   │       ├── categories.py  # 分类管理
│   │       └── borrows.py  # 借阅管理
│   ├── run.py              # 入口文件
│   ├── requirements.txt    # 依赖
│   └── venv/               # 虚拟环境
├── frontend/               # 前端
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
└── serve_frontend.py       # 前端静态服务启动脚本
```

## 快速启动

```bash
# 1. 进入后端目录，激活虚拟环境，启动后端API
cd backend
venv\Scripts\activate       # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python run.py               # 后端运行在 http://localhost:5000

# 2. 新开一个终端，在项目根目录启动前端
python serve_frontend.py    # 前端运行在 http://localhost:8080
```

浏览器访问 http://localhost:8080 即可使用。

## 默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |

读者可自行注册。

## 功能说明

### 读者功能
- 注册/登录
- 浏览图书（分页、搜索、分类筛选）
- 查看图书详情
- 借阅图书
- 查看借阅记录

### 管理员功能
- 图书管理（新增/编辑/删除）
- 分类管理（新增/编辑/删除）
- 借阅管理（查看所有记录、处理归还）

## API 接口

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | /api/auth/register | 注册 | 公开 |
| POST | /api/auth/login | 登录 | 公开 |
| GET | /api/auth/me | 当前用户 | 登录 |
| GET | /api/books | 图书列表(分页/搜索) | 公开 |
| GET | /api/books/:id | 图书详情 | 公开 |
| POST | /api/books | 新增图书 | 管理员 |
| PUT | /api/books/:id | 修改图书 | 管理员 |
| DELETE | /api/books/:id | 删除图书 | 管理员 |
| GET | /api/categories | 分类列表 | 公开 |
| POST | /api/categories | 新增分类 | 管理员 |
| PUT | /api/categories/:id | 修改分类 | 管理员 |
| DELETE | /api/categories/:id | 删除分类 | 管理员 |
| GET | /api/borrows | 借阅记录 | 登录 |
| POST | /api/borrows | 借阅图书 | 登录 |
| POST | /api/borrows/:id/return | 归还图书 | 管理员 |

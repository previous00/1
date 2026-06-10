"""
图书管理系统 - 启动后端服务

使用方法:
    cd backend
    ../venv/Scripts/activate  (或 source ../venv/bin/activate)
    python run.py

服务地址: http://localhost:5000
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 40)
    print("  图书管理系统 - 后端API服务")
    print("  http://localhost:5000")
    print("=" * 40)
    app.run(debug=True, port=5000)

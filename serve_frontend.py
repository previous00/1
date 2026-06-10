"""
图书管理系统 - 前端静态文件服务

使用方法:
    python serve_frontend.py          # 默认 8080 端口
    python serve_frontend.py 3000     # 指定端口
"""
import http.server
import socketserver
import os
import sys


def get_frontend_dir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    directory = get_frontend_dir()

    if not os.path.isdir(directory):
        print(f"[ERROR] 前端目录不存在: {directory}")
        sys.exit(1)

    if not os.path.isfile(os.path.join(directory, 'index.html')):
        print(f"[ERROR] 前端入口文件不存在: {os.path.join(directory, 'index.html')}")
        sys.exit(1)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=directory, **kwargs)

        def log_message(self, format, *args):
            print(f"  {self.address_string()} - {format % args}")

    socketserver.TCPServer.allow_reuse_address = True

    try:
        httpd = socketserver.TCPServer(("0.0.0.0", port), Handler)
    except OSError as e:
        if "address already in use" in str(e).lower() or e.errno == 10048:
            print(f"[ERROR] 端口 {port} 已被占用，请更换端口或关闭占用进程")
            print(f"        尝试: python serve_frontend.py {port + 1}")
        else:
            print(f"[ERROR] 无法启动服务: {e}")
        sys.exit(1)

    print("=" * 40)
    print("  图书管理系统 - 前端服务")
    print(f"  http://localhost:{port}")
    print("=" * 40)
    print(f"  静态目录: {directory}")
    print(f"  按 Ctrl+C 停止服务\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] 服务已停止")
    finally:
        httpd.server_close()


if __name__ == '__main__':
    main()

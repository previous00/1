from flask import jsonify


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return jsonify(code=400, message='请求参数错误'), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify(code=401, message='未授权，请先登录'), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify(code=403, message='权限不足'), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(code=404, message='资源不存在'), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify(code=500, message='服务器内部错误'), 500

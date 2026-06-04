from flask import jsonify


def success(data=None, message='操作成功'):
    return jsonify(code=200, message=message, data=data)


def created(data=None, message='创建成功'):
    return jsonify(code=201, message=message, data=data), 201


def error(message='操作失败', code=400):
    return jsonify(code=code, message=message), code

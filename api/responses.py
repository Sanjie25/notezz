from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    response = {
        "success": True,
        "message": message,
        "status_code": status_code,
        "data": data,
    }
    return jsonify(response)


def error_response(message="Error", status_code=200):
    response = {"success": False, "message": message, "status_code": status_code}
    return jsonify(response)

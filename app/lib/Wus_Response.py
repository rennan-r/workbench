def return_response(data={}, message="操作成功"):
    return {"code": 200, "message": message, "data": data, "success": True}

def return_response_page(data, page, per_page, pages, total):
    return {"code": 200, "message": "操作成功", "data": data, "success": True,
            "meta": {"page": page, "per_page": per_page, "pages": pages, "total": total}}

def return_error(error_code, error_message):
    return {"code": error_code, "message": error_message, "data": None, "success": False}

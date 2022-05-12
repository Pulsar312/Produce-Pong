from flask import render_template


def simple_error_page(title: str, message: str, code: int = 404):
    data = {
        "title": title,
        "message": message
    }
    return render_template("error.html", **data), code

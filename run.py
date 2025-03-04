from app import create_app
from flask import jsonify
from marshmallow import ValidationError

app = create_app()

@app.errorhandler(ValidationError)
def handle_validation_error(err):
    return jsonify({
        "code": 400,
        "message": "请求数据不合法",
        "errors": err.messages
    }), 400

if __name__ == '__main__':
    app.run(debug=True)
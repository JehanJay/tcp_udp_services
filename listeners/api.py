from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/device/save_log', methods=['POST'])
def device():
    data1 = request.data
    test = data1.decode()
    print(test)
    val = request.form
    print(val)
    return 'ok',200



if __name__ == '__main__':
    app.run(host="0.0.0.0",port = int(1141),debug=True)


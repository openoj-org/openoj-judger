from flask import Flask, request, jsonify
from celery import Celery
from judger.judger import judge_entrance

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def judge_code(data):
    result = judge_entrance(data)
    print(result)
    return result

@app.route('/submit_code', methods=['POST'])
def submit_code():
    data = request.get_json()

    task = judge_code.apply_async(args=[data])

    # return jsonify({'task_id': task.id}), 202
    return {'id':task.id}

@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    task = judge_code.AsyncResult(task_id)

    if task.state == 'SUCCESS':
        result = task.result
    else:
        result = {'ok': False}

    return jsonify(result)
    # return result

if __name__ == '__main__':
    app.run(debug=True)

import celery.states as states
from flask import Flask, request
from flask import url_for, jsonify
from worker import celery

dev_mode = True
app = Flask(__name__)


@app.route('/submit_code', methods=['POST'])
def submit_code():
    data = request.get_json()
    task = celery.send_task('tasks.judge_code', args=[data], kwargs={})
    return {'id':task.id}

@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    # task = judge_code.AsyncResult(task_id)
    task = celery.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        result = task.result
    else:
        result = {'ok': False}

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

import os
import time
from celery import Celery
from judger.judger import judge_entrance


CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)


@celery.task(name='tasks.judge_code')
def judge_code(data):
    result = judge_entrance(data)
    print(result)
    return result

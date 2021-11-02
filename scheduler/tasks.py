try:
    from flask import Flask
    from celery import Celery
    from datetime import timedelta
    import os, glob, PyPDF2
    from shutil import copyfile
except Exception as e:
    print("Error : {} ".format(e))


def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app = Flask(__name__)
app.config['CELERY_BACKEND'] = "redis://redis:6379/0"
app.config['CELERY_BROKER_URL'] = "redis://redis:6379/0"

app.config['CELERYBEAT_SCHEDULE'] = {
    'say-every-5-seconds': {
        'task': 'return_something',
        'schedule': timedelta(seconds=5)
    },
}


app.config['CELERY_TIMEZONE'] = 'UTC'
celery_app = make_celery(app)


@celery_app.task(name='return_something')
#def return_something():
#    print ('something')
#    return 'something'

def return_something():
    print ('something')
    print(os.getcwd())
    folder='input'
    img_files=glob.glob(folder+'/*.jpeg')
    print(img_files)
    for f in img_files:
        #f='/home/gaurav/Python-Flask-Redis-Celery-Docker/part 4/MyScheduler/'+f
        #img=cv2.imread(f)
        #cv2.imwrite(f.replace('input','output'),img)
        #print(f.replace('input','output'))
        #f=f.replace('/usr/src/app/','/usr/share/')
        print(f)
        if os.path.exists(f.replace('input','output')):
            continue
        copyfile(f, f.replace('input','output'))

from celery import Celery

def make_celery(app):
    celery = Celery('worker',
            backend='redis://redis:6379',
            broker='redis://redis:6379')
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
from celery import Celery

# 创建celery类的对象
celery_app = Celery('celery_tasks')


# 加载配置
celery_app.config_from_object('celery_tasks.config')

# 让celery worker启动时自动发现有哪些任务函数
celery_app.autodiscover_tasks(['celery_tasks.sms'])
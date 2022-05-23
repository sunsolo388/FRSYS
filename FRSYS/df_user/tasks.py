from celery import Celery
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "ihome.settings"

# 放到celery服务器上时将注释打开
# import django
# django.setup()

from django.core.mail import send_mail
from django.conf import settings
#from goods.models import GoodsCategory, IndexGoodsBanner, IndexPromotionBanner
#from goods.models import IndexCategoryGoodsBanner
from django.template import loader

# celery -A celery_tasks.tasks worker -l info


# 创建celery应用对象
app = Celery("celery_tasks.tasks", broker="redis://192.168.108.57/4")


@app.task
def send_active_email(to_email):#, user_name, token):
    """发送激活邮件"""
    subject = "生鲜码盒用户激活"  # 标题
    body = ""  # 文本邮件体
    sender = settings.EMAIL_FROM  # 发件人
    receiver = [to_email]  # 接收人
    html_body = '<h1>尊敬的用户 %s, 感谢您注册生鲜生鲜码盒可溯源生鲜！</h1>' \
                #'<br/><p>请点击此链接激活您的帐号<a href="http://127.0.0.1:8000/users/active/%s">' \
                #'http://127.0.0.1:8000/users/active/%s</a></p>' % (user_name, token, token)
    send_mail(subject, body, sender, receiver, html_message=html_body)
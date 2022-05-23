from django.core.mail import send_mail
from django.conf import settings

def send_active_email(to_email, user_name):#, token):
    """发送激活邮件"""
    subject = "生鲜码盒用户注册通知"  # 标题
    body = ""  # 文本邮件体
    sender = settings.EMAIL_HOST_USER  # 发件人
    receiver = [to_email]  # 接收人
    html_body = '<h1>尊敬的用户 %s, 感谢您注册生鲜生鲜码盒可溯源生鲜！</h1>'%user_name
    send_mail(subject, body, sender, receiver, html_message=html_body)
"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     emailset.py
@Author:   shenfan
@Time:     2021/2/2 9:09
"""
import chardet
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from socket import gaierror, error
from src.common.log import Logger
from src.common.config import Config

logger = Logger(logger_name="EmailSet").get_logger()

class EmailSet:
    def __init__(self):
        self.title = Config().get('mail').get('title')
        self.message = Config().get('mail').get('message')
        self.files = Config().get('mail').get('path')
        self.msg = MIMEMultipart('related')
        self.server = Config().get('mail').get('server')
        self.sender = Config().get('mail').get('sender')
        self.receiver = Config().get('mail').get('receiver')
        self.password = Config().get('mail').get('password')

    def attach_file(self, att_file):
        att = MIMEText(open(att_file, 'rb').read(), 'bsae64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        file_name = re.split(r'[\\|/]', att_file)
        filename = file_name[-1]
        att["Content-Disposition"] = 'attachment; filename="%s"' % filename
        self.msg.attach(att)

    def send(self):
        self.msg['Subject'] = self.title
        self.msg['From'] = self.sender
        self.msg['To'] = self.receiver
        # 邮件正文
        if self.message:
            self.msg.attach(MIMEText(self.message, "html", "utf-8"))

        try:
            smtp_server = smtplib.SMTP_SSL(self.server,465)
        except (gaierror and error) as e:
            logger.exception('发送邮件失败,无法连接到SMTP服务器，检查网络以及SMTP服务器. %s', e)
        else:
            try:
                smtp_server.login(self.sender, self.password)
            except smtplib.SMTPAuthenticationError as e:
                logger.exception('用户名密码验证失败！%s', e)
            else:
                smtp_server.sendmail(self.sender, self.receiver.split(','), self.msg.as_string())
            finally:
                smtp_server.quit()
                logger.info('发送邮件"{0}"成功! 收件人：{1}。如果没有收到邮件，请检查垃圾箱，'
                            '同时检查收件人地址是否正确'.format(self.title, self.receiver))

if __name__ == "__main__":
    e = EmailSet()
    e.send()










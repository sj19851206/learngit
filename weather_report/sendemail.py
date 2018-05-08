#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 28 16:06:13 2018

@author: shenjing
"""

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import poplib
import time
import datetime
from email.parser import Parser
import base64

def SendMail(path = '',subject='',content='',send='11522857@qq.com',passwd='noojviljspeqbjaj',touser='11522857@qq.com'):
    msg = MIMEMultipart()
    msg['From'] = formataddr([send.split(('@'))[0],send])
    msg['To'] = formataddr([touser.split('@')[0],touser])
    msg['Subject'] = subject
    content = content
    text = MIMEText(content,'plain','utf-8')
    msg.attach(text)
    if path != '':
        part = MIMEApplication(open(path,'rb').read())
        part.add_header('Content-Disposition','attachment',filename=os.path.basename(path))
        msg.attach(part)
    server = smtplib.SMTP_SSL('smtp.qq.com',465)
    server.login(send,passwd)
    server.sendmail(send,[touser,],msg.as_string())
    server.quit()
    print('Done')

def get_parsed_msg():
    useracount = '11522857@qq.com'
    password = 'noojviljspeqbjaj'
    pop3_server = 'pop.qq.com'
    server = poplib.POP3_SSL(pop3_server)
    server.user(useracount)
    server.pass_(password)
    resp, mails, octets = server.list()
    print('邮件总数: {}'.format(len(mails)))
    total_mail_numbers = len(mails)
    response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
    msg_content = b'\r\n'.join(mail_message_lines).decode('gbk')
    msg = Parser().parsestr(text=msg_content)
    print('解码后的邮件信息:\n{}'.format(msg))
    server.close()
    return msg




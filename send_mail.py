#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, string, socket
import smtplib

#导入smtplib和MIMEText
import smtplib
from email.mime.text import MIMEText
from config import mailto_list, mail_host, mail_user, mail_pass, mail_postfix

def send_mail(sub,content):
    me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(me, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

if __name__ == '__main__':
    if send_mail("subject","content"):
        print "发送成功"
    else:
        print "发送失败"

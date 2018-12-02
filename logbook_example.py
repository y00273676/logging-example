# -*- coding: utf-8 -*-

import sys

from logbook import Logger, StreamHandler, FileHandler, MailHandler

handler = StreamHandler(sys.stdout)
log = Logger('test')


def main():
    log.info('something logging')


def test1():
    with handler.applicationbound():
        main()


StreamHandler(sys.stdout, level='DEBUG').push_application()
FileHandler('app.log', bubble=True, level='INFO').push_application()


def test2():
    main()


sender = 'Logger<dongdong@163.com>'
recipients = ['dongdong@qq.com']
email_user = 'dongdong@163.com'
email_pass = 'password'

mail_handler = MailHandler(sender, recipients,
                           server_addr='smtp.163.com',
                           starttls=True,
                           secure=False,
                           credentials=(email_user, email_pass),
                           format_string=u'''\
            Subject: {record.level_name} on My Application

            Message type: {record.level_name}
            Location: {record.filename}:{record.lineno}
            Module: {record.module}
            Function: {record.func_name}
            Time: {record.time:%Y-%m-%d %H:%M:%S}
            Remote IP: {record.extra[ip]}
            Request: {record.extra[url]} [{record.extra[method]}]
            Message: {record.message}
            ''',
                           bubble=True)


def test3():
    with mail_handler.threadbound():
        main()

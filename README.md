# logbook

## threadbound与applicationbound

从最开始的例子来看，可以使用两种方式来记录日志，一种是在最开始使用push_*来激活，另一种是使用的时候用with构造上下文，现在进行一些补充

| push	| with	| pop |
| ------ | ------ | ------ |
| push_application()	| applicationbound()	| pop_application() |
| push_thread()	| threadbound()	| pop_threadbound() |
| push_greenlet()	| greenletbound()	| pop_greenlet() |

使用pop_* 可以取消记录的上下文
application作用于整个应用，thread只针对当前线程

    handler = MyHandler()
    handler.push_application()
    # all here goes to that handler
    handler.pop_application()
    
消除嵌套
使用多个Handler的时候，使用push_方式启动的上下文不会形成嵌套，但是使用with启动的上下文会形成嵌套，可以使用nested handler

    import os
    from logbook import NestedSetup, NullHandler, FileHandler, \
    MailHandler, Processor

    def inject_information(record):
       record.extra['cwd'] = os.getcwd()

    setup = NestedSetup([
       # NullHandler避免stderr接受消息
       NullHandler(),
       FileHandler('application.log', level='WARNING'),
       MailHandler('servererrors@example.com', ['admin@example.com'],
            level='ERROR', bubble=True),

       Processor(inject_information)
    ])
    
    with setup.threadbound():
    log.info('something logging')
    
    
  ## 日期格式
上边在介绍的自定义日志格式的时候使用的时间是虽然指定了格式但是是UTC格式，跟北京时间是差了8个小时的。所以需要设置让它记录本地的时间

在刚才的例子前面加上如下代码即可

    logbook.set_datetime_format('local') 

    handler = StreamHandler(sys.stdout)
    handler.format_string = '[{record.time:%Y-%m-%d %H:%M:%S}] IP:{record.extra[ip]} {record.level_name}: {record.channel}: {record.message}'
    handler.formatter
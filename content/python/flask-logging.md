Title: Flask中通过fileConfig配置多个logger
Date: 2015-02-11 00:05
Tags: flask, logging
Slug: flask-logging
Author: crazygit
Summary: Flask中通过config文件配置多个logger


## Flask中如何通过配置文件配置logger

1. 创建`app.py`文件

        $ cat app.py
        from flask import Flask
        import logging
        import logging.config

        def configure_logger(app):
            logging.config.fileConfig("log.conf")
            # 获取当前所有的logger
            print logging.Logger.manager.loggerDict.keys()
            app.logger.info("logger start")

        def app_factory():
            app = Flask('root')
            configure_logger(app)
            return app

2. 创建`run.py`文件

        $ cat run.py
        from app import app_factory

        app = app_factory()
        @app.route('/')
        def index():
            return "index"

        if __name__ == '__main__':
            app.run(debug=True)

3. 创建logger的配置文件`log.conf`

        $ cat log.conf
        # https://docs.python.org/2/library/logging.config.html#logging-config-fileformat

        # configure loggers
        [loggers]
        keys=root, other_logger

        [logger_root]
        level=DEBUG
        handlers=root_handler
        qualname=root

        [logger_other_logger]
        level=DEBUG
        handlers=root_handler
        qualname=root.other_logger

        # configure handlers
        [handlers]
        keys=root_handler

        [handler_root_handler]
        class=FileHandler
        level=INFO
        formatter=root_formatter
        args=('app.log', 'w+')

        # configure formatters
        [formatters]
        keys=root_formatter

        [formatter_root_formatter]
        format=%(asctime)s %(levelname)s %(message)s
        datefmt=
        class=logging.Formatter

4. 运行`run.py`

        $ python run.py 
        ['root', 'root.other_logger']
        ['root', 'root.other_logger']

    可以看出当前已经配置了两个logger

5. Flask中的默认logger名

    Flask默认以import_name作为logger的默认名

        app = Flask('root')

    本例就是以root作为logger名字，并配置了新的logger: root.other_logger,

6. 使用建议

    * 为Flask配置多个模块时，建议通过设置'qualname'为'import_name.sub_name'做为新的logger名,
    * level设置时, logger的level等级应该小于handler的level等级，最终是以handler的设置为准， 反之，则起作用的是logger的level


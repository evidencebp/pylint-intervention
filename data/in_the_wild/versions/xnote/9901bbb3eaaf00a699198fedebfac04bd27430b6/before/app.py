# encoding=utf-8
# @since 2016/12/04
# @modified 2022/04/03 21:46:38
"""xnote - Xnote is Not Only Text Editor
Copyright (C) 2016-2022  xupingmao 578749341@qq.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function
import os, socket, sys
import json
import time
import webbrowser
import posixpath
import socket
import logging
import traceback
import argparse
# insert after working dir
sys.path.insert(1, "lib")
sys.path.insert(1, "core")
import web
import xutils
import xconfig
import xtables
import xmanager
import xtemplate
import signal
import logging
from xutils import *
from xutils import mem_util
from xutils.mem_util import log_mem_info_deco
from xutils.lockutil import FileLock
from autoreload import AutoReloadThread

FILE_LOCK = FileLock("pid.lock")

# 配置日志模块
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s')


def print_debug_info(*args):
    logging.info("%s" % args)

def get_bool_by_sys_arg(value):
    return value == "yes" or value == "true"

def get_int_by_sys_arg(value):
    if value is None:
        return value
    return int(value)

def handle_args_and_init_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default = "./config/boot/boot.default.properties")
    parser.add_argument("--data", default="")
    parser.add_argument("--delay", default="0")
    parser.add_argument("--debug", default="yes")
    parser.add_argument("--minthreads", default="15")
    parser.add_argument("--useCacheSearch", default="no")
    parser.add_argument("--useUrlencode", default="no")
    parser.add_argument("--devMode", default="no")
    parser.add_argument("--initScript", default="init.py")
    parser.add_argument("--test", default="no")

    web.config.debug = False
    args = parser.parse_args()

    if args.data != "":
        logging.error("--data配置已经废弃，请使用--config配置")
        sys.exit(1)

    # 处理Data目录，创建各种目录
    xconfig.init(args.config)

    # 延迟加载，避免定时任务重复执行
    delay = int(args.delay)
    time.sleep(delay)
    

    xconfig.MIN_THREADS   = int(args.minthreads)
    xconfig.INIT_SCRIPT   = args.initScript
    web.config.minthreads = xconfig.MIN_THREADS

    xconfig.USE_CACHE_SEARCH = get_bool_by_sys_arg(args.useCacheSearch)
    xconfig.USE_URLENCODE    = get_bool_by_sys_arg(args.useUrlencode)
    xconfig.DEV_MODE         = get_bool_by_sys_arg(args.devMode)
    xconfig.IS_TEST          = get_bool_by_sys_arg(args.test)
    # 调试配置
    xconfig.DEBUG            = get_bool_by_sys_arg(args.debug)
    web.config.debug         = xconfig.DEBUG

    start_time = xutils.format_datetime()
    xconfig.set_global_config("start_time", start_time)
    xconfig.set_global_config("system.start_time", start_time)

def handle_signal(signum, frame):
    """处理系统消息
    @param {int} signum
    @param {frame} current stack frame
    """
    xutils.log("Signal received: %s" % signum)
    if signum == signal.SIGALRM:
        # 时钟信号
        return
    # 优雅下线
    xmanager.fire("sys.exit")
    sys.exit(0)


@log_mem_info_deco("try_init_sqlite")
def try_init_sqlite():
    try:
        # 初始化数据库
        xtables.init()
    except:
        xutils.print_exc()
        xconfig.errors.append("初始化sqlite失败")

@log_mem_info_deco("try_init_ldb")
def try_init_ldb():
    try:

        block_cache_size = xconfig.get_global_config("system.block_cache_size")
        write_buffer_size = xconfig.get_global_config("system.write_buffer_size")
        max_open_files = xconfig.get_global_config("system.max_open_files")

        leveldb_kw = dict(block_cache_size = block_cache_size, 
            write_buffer_size = write_buffer_size, 
            max_open_files = max_open_files)

        db_instance = None
        db_driver = xconfig.get_global_config("system.db_driver")

        if db_driver == "sqlite":
            from xutils.db.driver_sqlite import SqliteKV
            db_file = os.path.join(xconfig.DB_DIR, "sqlite", "kv_store.db")
            db_instance = SqliteKV(db_file)

        if db_driver == "leveldbpy":
            from xutils.db.driver_leveldbpy import LevelDBProxy
            db_instance = LevelDBProxy(xconfig.DB_DIR, **leveldb_kw)

        if db_driver == "lmdb":
            from xutils.db.driver_lmdb import LmdbKV
            db_dir = os.path.join(xconfig.DB_DIR, "lmdb")
            db_instance = LmdbKV(db_dir)

        # 默认使用leveldb启动
        if db_instance is None:
            try:
                import leveldb
                from xutils.db.driver_leveldb import LevelDBImpl
                db_instance = LevelDBImpl(xconfig.DB_DIR, **leveldb_kw)
            except ImportError:
                if xutils.is_windows():
                    logging.warning("检测到Windows环境，自动切换到leveldbpy驱动")
                    from xutils.db.driver_leveldbpy import LevelDBProxy
                    db_instance = LevelDBProxy(xconfig.DB_DIR, **leveldb_kw)
                    # 更新驱动名称
                    xconfig.set_global_config("system.db_driver", "leveldbpy")
                else:
                    logging.error("启动失败,请安装leveldb依赖")
                    sys.exit(1)

        # 初始化leveldb数据库
        dbutil.init(xconfig.DB_DIR, db_instance = db_instance, db_cache = cacheutil)
    except:
        xutils.print_exc()
        logging.error("初始化数据库失败...")
        sys.exit(1)

def init_autoreload():
    def reload_callback():
        # 重新加载handlers目录下的所有模块
        if xconfig.get_global_config("system.fast_reload"):
            xmanager.reload()
        else:
            xmanager.restart()
        
        autoreload_thread.clear_watched_files()
        autoreload_thread.watch_dir(xconfig.HANDLERS_DIR, recursive=True)

    # autoreload just reload models
    autoreload_thread = AutoReloadThread(reload_callback)
    autoreload_thread.watch_dir(xconfig.HANDLERS_DIR, recursive=True)
    autoreload_thread.watch_file("core/xtemplate.py")
    autoreload_thread.start()

def init_cluster():
    # 初始化集群配置
    if xconfig.get_global_config("system.node_role") == "follower":
        logging.info("当前系统以从节点身份运行")

@log_mem_info_deco("init_web_app")
def init_web_app():
    # 关闭autoreload使用自己实现的版本
    var_env = dict()
    app = web.application(list(), var_env, autoreload=False)

    # 初始化模板管理
    xtemplate.init()

    # 初始化主管理器，包括用户及权限、定时任务、各功能模块
    xmanager.init(app, var_env)
    return app


def init_app_no_lock():
    global app

    # 处理初始化参数
    handle_args_and_init_config()

    # 初始化数据库
    try_init_sqlite()
    try_init_ldb()
    
    # 初始化工具箱
    xutils.init(xconfig)

    app = init_web_app()

    # 初始化自动加载功能
    init_autoreload()

    # 初始化集群
    init_cluster()

    # 触发handler里面定义的启动函数
    xmanager.fire("sys.init", None)

    # 注册信号响应
    # 键盘终止信号
    if not xutils.is_windows():
        signal.signal(signal.SIGINT, handle_signal)
        # kill终止信号
        signal.signal(signal.SIGTERM, handle_signal)
        # 时钟信号
        # signal.signal(signal.SIGALRM, handle_signal)
        # signal.alarm(5)

    # 记录已经启动
    xconfig.mark_started()
    logging.info("app started")

def init_app():
    return init_app_no_lock()

def count_worker_thread():
    count = 0
    for t in threading.enumerate():
        if t.isDaemon():
            continue
        count += 1
    return count

def wait_thread_exit():
    while True:
        count = count_worker_thread()
        logging.debug("线程数量:%s", count)
        if count > 1:
            time.sleep(0.1)
        else:
            return

def main():
    global app
    global FILE_LOCK

    try:
        if FILE_LOCK.acquire():
            # 初始化
            init_app_no_lock()
            # 监听端口
            app.run()
            logging.info("服务器已关闭")
            wait_thread_exit()
            sys.exit(xconfig.EXIT_CODE)
        else:
            logging.error("get lock failed")
            logging.error("xnote进程已启动，请不要重复启动!")
            sys.exit(1)
    finally:
        FILE_LOCK.release()



class LogMiddleware:
    """WSGI middleware for logging the status.

    中间件的实现参考 web/httpservers.py
    """

    PROFILE_SET = set()

    def __init__(self, app):
        self.app = app
        self.format = '%s - - [%s] "%s %s %s" - %s %s ms'
    
        f = BytesIO()
        
        class FakeSocket:
            def makefile(self, *a):
                return f
        
        # take log_date_time_string method from BaseHTTPRequestHandler
        self.log_date_time_string = BaseHTTPRequestHandler(FakeSocket(), None, None).log_date_time_string
        
    def invoke_app(self, environ, start_response):
        start_time = time.time()
        def xstart_response(status, response_headers, *args):
            out = start_response(status, response_headers, *args)
            self.log(status, environ, time.time() - start_time)
            return out
        return self.app(environ, xstart_response)

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '_')
        if path in LogMiddleware.PROFILE_SET:
            vars = dict(f=self.invoke_app, environ=environ, start_response=start_response)
            profile.runctx("r=f(environ, start_response)", globals(), vars, sort="time")
            return vars["r"]
        else:
            return self.invoke_app(environ, start_response)
             
    def log(self, status, environ, cost_time):
        outfile = environ.get('wsgi.errors', web.debug)
        req = environ.get('PATH_INFO', '_') 
        query_string = environ.get("QUERY_STRING", '')
        if query_string != '':
            req += '?' + query_string
        protocol = environ.get('ACTUAL_SERVER_PROTOCOL', '-')
        method = environ.get('REQUEST_METHOD', '-')
        x_forwarded_for = environ.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for is not None:
            host = x_forwarded_for.split(",")[0]
        else:
            host = "%s:%s" % (environ.get('REMOTE_ADDR','-'), 
                              environ.get('REMOTE_PORT','-'))

        time = self.log_date_time_string()

        msg = self.format % (host, time, protocol, method, req, status, int(1000 * cost_time))
        print(utils.safestr(msg), file=outfile)

if __name__ == '__main__':
    main()

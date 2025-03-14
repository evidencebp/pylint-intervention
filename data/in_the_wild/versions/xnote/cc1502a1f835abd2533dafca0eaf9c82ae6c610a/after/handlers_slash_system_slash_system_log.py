# -*- coding:utf-8 -*-
# @author xupingmao <578749341@qq.com>
# @since 2018/03/03 12:46:20
# @modified 2022/04/20 22:50:10
import os
import time
from collections import deque

import xauth
import xutils
import xconfig
import xmanager
from xutils import logutil
from xutils.imports import *
from xtemplate import BasePlugin
from xutils.functions import iter_exists

OPTION_HTML = '''
<script src="/static/js/base/jq-ext.js"></script>

<div class="card">
    <div class="x-tab-box row" data-tab-key="log_type" data-tab-default="file">
        <a class="x-tab" data-tab-value="file">文件日志</a>
        <a class="x-tab" data-tab-value="mem">内存日志</a>
    </div>
</div>

<div class="card">
    {% if log_type == "file" %}
        <div class="x-tab-box btn-style dark row" data-tab-key="type" data-tab-default="tail">
            <a class="x-tab" data-tab-value="tail">最新</a>
            <a class="x-tab" data-tab-value="head">最早</a>
            <a class="x-tab" data-tab-value="all">全部</a>
        </div>

        <div class="row">
            <span>直接查看文件</span>
            <a href="/code/edit?path={{info_log_path}}">INFO日志</a>
            <span>|</span>
            <a href="/code/edit?path={{warn_log_path}}">WARN日志</a>
            <span>|</span>
            <a href="/code/edit?path={{error_log_path}}">ERROR日志</a>
            <span>|</span>
            <a href="/code/edit?path={{trace_log_path}}">TRACE日志</a>
        </div>
    {% end %}

    {% if log_type == "mem" %}
        {% init log_name = "" %}
        {% init log_not_found = False %}

        <span>日志名称</span>
        <select value="{{log_name}}" class="logger-name-select">
            {% for logger in mem_loggers %}
                <option value="{{logger.name}}">{{logger.name}}</option>
            {% end %}

            {% if log_not_found and log_name != "" %}
                <option value="{{log_name}}">{{log_name}}</option>
            {% end %}
        </select>
    {% end %}
</div>
<script>
$(function () {
    $(".output-textarea").scrollBottom();
    $(".logger-name-select").change(function (e) {
        var oldHref = window.location.href;
        var newHref = addUrlParam(oldHref, "log_name", $(e.target).val());
        window.location.href = newHref;
    });
})
</script>
'''


def readlines(fpath):
    if not os.path.exists(fpath):
        return []
    with open(fpath, encoding="utf-8") as fp:
        return fp.readlines()


def get_log_path(date, level="INFO"):
    month = "-".join(date.split("-")[:2])
    dirname = os.path.join(xconfig.LOG_DIR, month)
    fname = "xnote.%s.%s.log" % (date, level)
    return os.path.join(dirname, fname)


def read_tail_lines(fpath, lines):
    if not os.path.exists(fpath):
        return []

    q = deque()

    with open(fpath, encoding="utf-8") as fp:
        while True:
            line = fp.readline(1024)
            if line is None or len(line) == 0:
                break
            q.append(line)
            if len(q) > lines:
                q.popleft()

    return "".join(q)


class LogHandler(BasePlugin):

    title = 'xnote系统日志'
    # description = "查看系统日志"
    show_category = False
    category = 'system'
    editable = False
    rows = 0

    def get_arg_date(self):
        date = xutils.get_argument("date")

        if not date:
            date = time.strftime("%Y-%m-%d")

        return date

    def handle_mem_log(self):
        log_name = xutils.get_argument("log_name", "")
        loggers = logutil.MemLogger.list_loggers()
        for logger in loggers:
            if logger.name == log_name:
                return logger.text()

        if len(loggers) > 0 and log_name == "":
            return loggers[0].text()

        return "<empty>"

    def handle_file_log(self):
        type = xutils.get_argument("type", "tail")
        date = self.get_arg_date()

        fpath = get_log_path(date)

        if type == "tail":
            return read_tail_lines(fpath, 100)

        if type == "head":
            return ''.join(readlines(fpath)[:100])

        return xutils.readfile(fpath, limit=1024 * 1024)

    def handle(self, content):
        user_name = xauth.current_name()
        xmanager.add_visit_log(user_name, "/system/log")

        log_type = xutils.get_argument("log_type", "file")
        date = self.get_arg_date()

        self.render_options(date)

        if log_type == "mem":
            return self.handle_mem_log()

        if log_type == "file":
            return self.handle_file_log()

        return ""

    def render_options(self, date):
        log_type = xutils.get_argument("log_type", "file")
        log_name = xutils.get_argument("log_name", "")
        loggers = logutil.MemLogger.list_loggers()
        log_not_found = not iter_exists(lambda x: x.name == log_name, loggers)

        self.writehtml(OPTION_HTML,
                       log_type=log_type,
                       mem_loggers=loggers,
                       info_log_path=get_log_path(date),
                       log_name=log_name,
                       log_not_found=log_not_found,
                       warn_log_path=get_log_path(date, "WARN"),
                       error_log_path=get_log_path(date, "ERROR"),
                       trace_log_path=get_log_path(date, "TRACE"))


xurls = (
    r"/system/log", LogHandler,
)

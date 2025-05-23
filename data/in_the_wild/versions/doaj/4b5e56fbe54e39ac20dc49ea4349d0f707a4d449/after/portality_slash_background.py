import traceback
from copy import deepcopy

from flask_login import login_user
from huey import RedisHuey

from portality import constants
from portality import models
from portality.bll import DOAJ
from portality.core import app
from portality.decorators import write_required
from portality.tasks.redis_huey import schedule, configure


class BackgroundException(Exception):
    pass


class RetryException(Exception):
    pass


class BackgroundSummary(object):
    def __init__(self, job_id, affected=None, error=None):
        self.job_id = job_id
        self.affected = affected if affected is not None else {}
        self.error = error

    def as_dict(self):
        return {
            "job_id": self.job_id,
            "affected": self.affected,
            "error": self.error
        }


class BackgroundApi(object):
    """
    ~~BackgroundTasks:Feature~~
    """

    @classmethod
    def execute(self, background_task):
        # ~~->BackgroundTask:Process~~
        # ~~->BackgroundJob:Model~~
        job = background_task.background_job
        ctx = None
        acc = None
        if job.user is not None:
            ctx = app.test_request_context("/")
            ctx.push()
            # ~~-> Account:Model~~
            acc = models.Account.pull(job.user)  # FIXME: what happens when this is the "system" user
            if acc is not None:
                login_user(acc)

        job.start()
        job.add_audit_message("Job Started")
        job.save()

        try:
            background_task.run()
        except RetryException:
            if job.reference is None:
                job.reference = {}
            retries = job.reference.get("retries", 0)
            job.reference["retries"] = retries + 1
            job.save()
            raise
        except Exception as e:
            job.fail()
            job.add_audit_message("Error in Job Run")
            job.add_audit_message("Caught in job runner during run: " + traceback.format_exc())
        job.add_audit_message("Job Run Completed")

        job.add_audit_message("Cleanup Started")
        try:
            background_task.cleanup()
        except Exception as e:
            job.fail()
            job.add_audit_message("Error in Cleanup Run")
            job.add_audit_message("Caught in job runner during cleanup: " + traceback.format_exc())
        job.add_audit_message("Job Cleanup Completed")

        job.add_audit_message("Job Finished")
        if not job.is_failed():
            job.success()
        job.save()

        # trigger a status change event
        jdata = deepcopy(job.data)
        del jdata["audit"]
        eventsSvc = DOAJ.eventsService()
        eventsSvc.trigger(models.Event(constants.BACKGROUND_JOB_FINISHED, job.user, {
            "job": jdata
        }))

        if ctx is not None:
            ctx.pop()


class BackgroundTask(object):
    """
    All background tasks should extend from this object and override at least the following methods:

    - run
    - cleanup
    - prepare (class method)

    ~~BackgroundTask:Process~~
    """

    __action__ = None
    """ static member variable defining the name of this task """

    def __init__(self, background_job):
        self._background_job = background_job

    @property
    def background_job(self):
        return self._background_job

    def run(self):
        """
        Execute the task as specified by the background_job
        :return:
        """
        raise NotImplementedError()

    def cleanup(self):
        """
        Cleanup after a successful OR failed run of the task
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def prepare(cls, username, **kwargs):
        """
        Take an arbitrary set of keyword arguments and return an instance of a BackgroundJob,
        or fail with a suitable exception

        :param username: the user creating the job
        :param kwargs: arbitrary keyword arguments pertaining to this task type
        :return: a BackgroundJob instance representing this task
        """
        raise NotImplementedError()

    @classmethod
    def submit(cls, background_job):
        """
        Submit the specified BackgroundJob to the background queue

        :param background_job: the BackgroundJob instance
        :return:
        """
        raise NotImplementedError()

    @classmethod
    def get_param(cls, params, param_name, default=None):
        return params.get('{}__{}'.format(cls.__action__, param_name), default)

    @classmethod
    def set_param(cls, params, param_name, value):
        params['{}__{}'.format(cls.__action__, param_name)] = value

    @classmethod
    def set_reference(cls, refs, ref_name, value):
        refs['{}__{}'.format(cls.__action__, ref_name)] = value

    @classmethod
    def create_huey_helper(cls, task_queue: RedisHuey):
        return RedisHueyTaskHelper(task_queue, cls.__action__)


class AdminBackgroundTask(BackgroundTask):
    """~~AdminBackgroundTask:Process->BackgroundTask:Process~~"""

    @classmethod
    def check_admin_privilege(cls, username):
        # ~~->Account:Model~~
        a = models.Account.pull(username)
        if a is None:
            # very unlikely, as they would have had to log in to get to here..
            raise BackgroundException('Admin account that is being used to prepare this job does not exist.')

        if not a.has_role('admin'):
            raise BackgroundException('Account {} is not permitted to run this background task.'.format(username))

    @classmethod
    def prepare(cls, username, **kwargs):
        cls.check_admin_privilege(username)


class RedisHueyTaskHelper:
    def __init__(self, task_queue: RedisHuey, task_name: str):
        self.task_queue = task_queue
        self.task_name = task_name

    @property
    def queue_type(self):
        from portality.tasks.helpers import background_helper
        return background_helper.get_queue_type_by_task_queue(self.task_queue)

    def register_schedule(self, fn):
        fn = write_required(script=True)(fn)
        fn = self.task_queue.periodic_task(schedule(self.task_name))(fn)
        return fn

    def register_execute(self, is_load_config=False):
        def wrapper(fn):
            if is_load_config:
                conf = configure(self.task_name)
            else:
                conf = {}

            fn = write_required(script=True)(fn)
            fn = self.task_queue.task(**conf)(fn)
            return fn

        return wrapper

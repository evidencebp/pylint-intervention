from datetime import datetime

from django.contrib.auth.models import User
from django.template import Library

from astrobin.models import Image
from astrobin_apps_iotd.models import Iotd
from astrobin_apps_iotd.permissions import may_toggle_submission_image, may_toggle_vote_image, may_elect_iotd, \
    may_unelect_iotd
from astrobin_apps_iotd.services import IotdService

register = Library()


# Roles

@register.filter
def is_iotd_submitter(user):
    return user.groups.filter(name='iotd_submitters').exists()


@register.filter
def is_iotd_reviewer(user):
    return user.groups.filter(name='iotd_reviewers').exists()


@register.filter
def is_iotd_judge(user):
    return user.groups.filter(name='iotd_judges').exists()


# Permissions

@register.filter
def may_toggle_submission(user, image):
    may, reason = may_toggle_submission_image(user, image)
    return may


@register.filter
def may_not_toggle_submission_reason(user, image):
    may, reason = may_toggle_submission_image(user, image)
    return reason


@register.filter
def may_toggle_vote(user, image):
    may, reason = may_toggle_vote_image(user, image)
    return may


@register.filter
def may_not_toggle_vote_reason(user, image):
    may, reason = may_toggle_vote_image(user, image)
    return reason


@register.filter
def may_elect(user, image):
    may, reason = may_elect_iotd(user, image)
    return may


@register.filter
def may_unelect(user, image):
    may, reason = may_unelect_iotd(user, image)
    return may


@register.filter
def may_not_elect_reason(user, image):
    may, reason = may_elect_iotd(user, image)
    return reason


@register.filter
def may_not_unelect_reason(user, image):
    may, reason = may_unelect_iotd(user, image)
    return reason


@register.filter
def may_submit_to_iotd_tp_process(user: User, image: Image) -> bool:
    may, reason = IotdService.may_submit_to_iotd_tp_process(user, image)
    return may


@register.filter
def may_submit_to_iotd_tp_process_reason(user: User, image: Image) -> str:
    may, reason = IotdService.may_submit_to_iotd_tp_process(user, image)
    return reason

# Statuses


@register.filter
def is_iotd(image):
    return Iotd.objects.filter(image=image).exists()


@register.filter
def is_current_or_past_iotd(image):
    return Iotd.objects.filter(image=image, date__lte=datetime.now().date())


@register.filter
def iotd_elections_today(user):
    return Iotd.objects.filter(judge=user, created__contains=datetime.now().date()).count()


# Getters

@register.filter
def iotd_date_for_image(image):
    try:
        iotd = Iotd.objects.get(image=image)
        return iotd.date
    except Iotd.DoesNotExist:
        return ""


@register.simple_tag
def get_iotd():
    iotds = Iotd.objects.filter(date__lte=datetime.now().date()).order_by('-date')
    if iotds:
        return iotds[0]
    return None


@register.filter
def judge_cannot_select_now_reason(judge):
    # type: (User) -> Union[str, None]
    return IotdService().judge_cannot_select_now_reason(judge)


@register.filter
def get_next_available_selection_time_for_judge(judge):
    # type: (User) -> datetime
    return IotdService().get_next_available_selection_time_for_judge(judge)

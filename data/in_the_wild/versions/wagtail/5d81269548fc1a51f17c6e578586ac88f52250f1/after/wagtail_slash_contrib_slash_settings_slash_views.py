from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.lru_cache import lru_cache
from django.utils.text import capfirst
from django.utils.translation import ugettext as _

from wagtail.wagtailadmin import messages
from wagtail.wagtailadmin.edit_handlers import (
    ObjectList, extract_panel_definitions_from_model_class)
from wagtail.wagtailcore.models import Site

from .forms import SiteSwitchForm
from .permissions import user_can_edit_setting_type
from .registry import registry


def get_model_from_url_params(app_name, model_name):
    """
    retrieve a content type from an app_name / model_name combo.
    Throw Http404 if not a valid setting type
    """
    model = registry.get_by_natural_key(app_name, model_name)
    if model is None:
        raise Http404
    return model


@lru_cache()
def get_setting_edit_handler(model):
    panels = extract_panel_definitions_from_model_class(model, ['site'])
    return ObjectList(panels).bind_to_model(model)


def edit_current_site(request, app_name, model_name):
    # Redirect the user to the edit page for the current site
    return redirect('wagtailsettings_edit', request.site.pk, app_name, model_name)


def edit(request, site_pk, app_name, model_name):
    model = get_model_from_url_params(app_name, model_name)
    if not user_can_edit_setting_type(request.user, model):
        raise PermissionDenied
    site = get_object_or_404(Site, pk=site_pk)

    setting_type_name = model._meta.verbose_name

    instance = model.for_site(site)
    edit_handler_class = get_setting_edit_handler(model)
    form_class = edit_handler_class.get_form_class(model)

    if request.POST:
        form = form_class(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                _("{setting_type} updated.").format(
                    setting_type=capfirst(setting_type_name),
                    instance=instance
                )
            )
            return redirect('wagtailsettings_edit', site.pk, app_name, model_name)
        else:
            messages.error(request, _("The setting could not be saved due to errors."))
            edit_handler = edit_handler_class(instance=instance, form=form)
    else:
        form = form_class(instance=instance)
        edit_handler = edit_handler_class(instance=instance, form=form)

    # Show a site switcher form if there are multiple sites
    site_switcher = None
    if Site.objects.count() > 1:
        site_switcher = SiteSwitchForm(site, model)

    return render(request, 'wagtailsettings/edit.html', {
        'opts': model._meta,
        'setting_type_name': setting_type_name,
        'instance': instance,
        'edit_handler': edit_handler,
        'site': site,
        'site_switcher': site_switcher,
    })

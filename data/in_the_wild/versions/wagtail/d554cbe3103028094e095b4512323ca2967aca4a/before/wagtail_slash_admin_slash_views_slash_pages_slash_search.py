from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import InvalidPage, Paginator
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from django.views.generic import View

from wagtail.admin.auth import user_has_any_page_permission, user_passes_test
from wagtail.admin.forms.search import SearchForm
from wagtail.models import Page
from wagtail.search.query import MATCH_ALL
from wagtail.search.utils import parse_query_string


def page_filter_search(q, pages, all_pages=None, ordering=None):
    # Parse query
    filters, query = parse_query_string(q, operator="and", zero_terms=MATCH_ALL)

    # Live filter
    live_filter = filters.get("live") or filters.get("published")
    live_filter = live_filter and live_filter.lower()

    if live_filter in ["yes", "true"]:
        if all_pages is not None:
            all_pages = all_pages.filter(live=True)
        pages = pages.filter(live=True)
    elif live_filter in ["no", "false"]:
        if all_pages is not None:
            all_pages = all_pages.filter(live=False)
        pages = pages.filter(live=False)

    # Search
    if all_pages is not None:
        all_pages = all_pages.search(query, order_by_relevance=not ordering)
    pages = pages.search(query, order_by_relevance=not ordering)

    return pages, all_pages


class SearchView(View):
    @method_decorator(vary_on_headers("X-Requested-With"))
    @method_decorator(user_passes_test(user_has_any_page_permission))
    def get(self, request):
        pages = all_pages = (
            Page.objects.all().prefetch_related("content_type").specific()
        )
        show_locale_labels = getattr(settings, "WAGTAIL_I18N_ENABLED", False)
        if show_locale_labels:
            pages = pages.select_related("locale")

        q = MATCH_ALL
        content_types = []
        ordering = None

        if "ordering" in request.GET:
            if request.GET["ordering"] in [
                "title",
                "-title",
                "latest_revision_created_at",
                "-latest_revision_created_at",
                "live",
                "-live",
            ]:
                ordering = request.GET["ordering"]

                if ordering == "title":
                    pages = pages.order_by("title")
                elif ordering == "-title":
                    pages = pages.order_by("-title")

                if ordering == "latest_revision_created_at":
                    pages = pages.order_by("latest_revision_created_at")
                elif ordering == "-latest_revision_created_at":
                    pages = pages.order_by("-latest_revision_created_at")

                if ordering == "live":
                    pages = pages.order_by("live")
                elif ordering == "-live":
                    pages = pages.order_by("-live")

        if "content_type" in request.GET:
            try:
                app_label, model_name = request.GET["content_type"].split(".")
            except ValueError:
                raise Http404

            try:
                selected_content_type = ContentType.objects.get_by_natural_key(
                    app_label, model_name
                )
            except ContentType.DoesNotExist:
                raise Http404

            pages = pages.filter(content_type=selected_content_type)
        else:
            selected_content_type = None

        if "q" in request.GET:
            form = SearchForm(request.GET)
            if form.is_valid():
                q = form.cleaned_data["q"]

                # Parse query and filter
                pages, all_pages = page_filter_search(q, pages, all_pages, ordering)

                # Facets
                if pages.supports_facet:
                    content_types = [
                        (ContentType.objects.get(id=content_type_id), count)
                        for content_type_id, count in all_pages.facet(
                            "content_type_id"
                        ).items()
                    ]

        else:
            form = SearchForm()

        paginator = Paginator(pages, per_page=20)
        try:
            pages = paginator.page(request.GET.get("p", 1))
        except InvalidPage:
            raise Http404

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return TemplateResponse(
                request,
                "wagtailadmin/pages/search_results.html",
                {
                    "pages": pages,
                    "all_pages": all_pages,
                    "query_string": q,
                    "content_types": content_types,
                    "selected_content_type": selected_content_type,
                    "ordering": ordering,
                    "show_locale_labels": show_locale_labels,
                },
            )
        else:
            return TemplateResponse(
                request,
                "wagtailadmin/pages/search.html",
                {
                    "search_form": form,
                    "pages": pages,
                    "all_pages": all_pages,
                    "query_string": q,
                    "content_types": content_types,
                    "selected_content_type": selected_content_type,
                    "ordering": ordering,
                    "show_locale_labels": show_locale_labels,
                },
            )

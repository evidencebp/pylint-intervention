"User web interface modules."

import tornado.web

from publications import constants
from publications import settings
from publications import utils


class Authors(tornado.web.UIModule):
    "HTML for authors list, including links to researcher page when available."

    def render(self, authors, complete=False):
        if (
            not complete
            and len(authors)
            > settings["NUMBER_FIRST_AUTHORS"] + settings["NUMBER_LAST_AUTHORS"]
        ):
            authors = (
                authors[: settings["NUMBER_FIRST_AUTHORS"]]
                + [None]
                + authors[-settings["NUMBER_LAST_AUTHORS"] :]
            )
        result = []
        for author in authors:
            if not author:
                result.append("...")
                continue
            name = "%s %s" % (author["family"], author.get("initials") or "")
            if author.get("researcher"):
                url = self.handler.reverse_url("researcher", author["researcher"])
                result.append(f'<a href="{url}">{name}</a>')
            else:
                result.append(name)
        return ", ".join(result)


class Journal(tornado.web.UIModule):
    "HTML for journal reference."

    def render(self, publication):
        journal = publication["journal"]
        title = journal.get("title")
        if title:
            url = self.handler.reverse_url("journal", title)
            result = ['<a href="%s">%s</a>' % (url, title)]
        else:
            result = ["-"]
        result.append("<strong>%s</strong>" % (journal.get("volume") or "-"))
        result.append("(%s)" % (journal.get("issue") or "-"))
        result.append(journal.get("pages") or "-")
        return " ".join(result)


class Published(tornado.web.UIModule):
    "Published date, and online, if present."

    def render(self, publication):
        result = publication["published"]
        epub = publication.get("epublished")
        if epub:
            result += "; online " + epub
        return "[%s]" % result


class OpenAccess(tornado.web.UIModule):
    "Open Access marker."

    def render(self, publication):
        if publication.get("open_access"):
            url = self.handler.static_url("open_access.png")
            return f'<img src="{url}" title="Open Access">'
        else:
            return ""


class Xref(tornado.web.UIModule):
    "HTML for a general external database entry."

    ICON = '<span class="glyphicon glyphicon-share"></span>'
    ATTRS = 'target="_" style="margin-right: 1em;"'

    def render(self, xref, full=False):
        db = xref["db"]
        key = xref["key"]
        description = xref.get("description") or ""
        if db.lower() == "url":
            url = key
            title = description or key
        elif key.lower().startswith("http"):
            url = key
            title = description or key
        else:
            try:
                url = settings["XREF_TEMPLATE_URLS"][db.lower()]
            except KeyError:
                url = None
                title = f"{xref['db']}: {key}"
                if full and description:
                    title += f" {description}"
            else:
                if "%-s" in url:  # Use lowercase key
                    url.replace("%-s", "%s")
                    key = key.lower()
                url = url % key
                title = f"{xref['db']}: {key}"
                if full and description:
                    title += f" {description}"
        if url:
            result = (
                f'<a target="_" style="margin-right: 1em;" href="{url}">'
                f"{self.ICON} <small>{title}</small></a>"
            )
        else:
            result = f"<span {self.ATTRS}>{self.ICON} <small>{title}</small></span>"
        return result


class ExternalButton(tornado.web.UIModule):
    "HTML for a button to an external publication page."

    ICON = '<span class="glyphicon glyphicon-link"></span>'
    ATTRS = 'class="btn btn-default btn-xs" role="button" target="_"'
    NAME = None
    URL = None

    def render(self, key, full=False):
        assert self.NAME
        assert self.URL
        if key:
            url = self.URL % key
            result = '<a %s href="%s">%s %s</a>' % (
                self.ATTRS,
                url,
                self.ICON,
                self.NAME,
            )
            if full:
                result = "<p>" + result + " " + key + "</p>"
            return result
        else:
            return ""


class PubmedButton(ExternalButton):
    NAME = "PubMed"
    URL = constants.PUBMED_URL


class DoiButton(ExternalButton):
    NAME = "DOI"
    URL = constants.DOI_URL


class CrossrefButton(ExternalButton):
    NAME = "Crossref"
    URL = constants.CROSSREF_URL


class OrcidButton(ExternalButton):
    NAME = "ORCID"
    URL = constants.ORCID_URL


class Translate(tornado.web.UIModule):
    "Translate the term, or keep as is."

    def render(self, term):
        istitle = term.istitle()
        try:
            term = settings["DISPLAY_TRANSLATIONS"][term.lower()]
            if istitle:
                term = term.title()
        except KeyError:
            pass
        return term

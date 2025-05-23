import re

from django.urls import NoReverseMatch, reverse
from django.utils.safestring import mark_safe

from crispy_forms.exceptions import FormHelpersException
from crispy_forms.layout import Layout
from crispy_forms.layout_slice import LayoutSlice
from crispy_forms.utils import TEMPLATE_PACK, flatatt, list_difference, render_field


class DynamicLayoutHandler:
    def _check_layout(self):
        if self.layout is None:
            raise FormHelpersException("You need to set a layout in your FormHelper")

    def _check_layout_and_form(self):
        self._check_layout()
        if self.form is None:
            raise FormHelpersException("You need to pass a form instance to your FormHelper")

    def all(self):
        """
        Returns all layout objects of first level of depth
        """
        self._check_layout()
        return LayoutSlice(self.layout, slice(0, len(self.layout.fields), 1))

    def filter(self, *LayoutClasses, max_level=0, greedy=False):
        """
        Returns a LayoutSlice pointing to layout objects of type `LayoutClass`
        """
        self._check_layout()
        filtered_layout_objects = self.layout.get_layout_objects(LayoutClasses, max_level=max_level, greedy=greedy)

        return LayoutSlice(self.layout, filtered_layout_objects)

    def filter_by_widget(self, widget_type):
        """
        Returns a LayoutSlice pointing to fields with widgets of `widget_type`
        """
        self._check_layout_and_form()
        layout_field_names = self.layout.get_field_names()

        # Let's filter all fields with widgets like widget_type
        filtered_fields = []
        for pointer in layout_field_names:
            if isinstance(self.form.fields[pointer[1]].widget, widget_type):
                filtered_fields.append(pointer)

        return LayoutSlice(self.layout, filtered_fields)

    def exclude_by_widget(self, widget_type):
        """
        Returns a LayoutSlice pointing to fields with widgets NOT matching `widget_type`
        """
        self._check_layout_and_form()
        layout_field_names = self.layout.get_field_names()

        # Let's exclude all fields with widgets like widget_type
        filtered_fields = []
        for pointer in layout_field_names:
            if not isinstance(self.form.fields[pointer[1]].widget, widget_type):
                filtered_fields.append(pointer)

        return LayoutSlice(self.layout, filtered_fields)

    def __getitem__(self, key):
        """
        Return a LayoutSlice that makes changes affect the current instance of the layout
        and not a copy.
        """
        # when key is a string containing the field name
        if isinstance(key, str):
            # Django templates access FormHelper attributes using dictionary [] operator
            # This could be a helper['form_id'] access, not looking for a field
            if hasattr(self, key):
                return getattr(self, key)

            self._check_layout()
            layout_field_names = self.layout.get_field_names()

            filtered_field = []
            for pointer in layout_field_names:
                # There can be an empty pointer
                if len(pointer) == 2 and pointer[1] == key:
                    filtered_field.append(pointer)

            return LayoutSlice(self.layout, filtered_field)

        return LayoutSlice(self.layout, key)

    def __setitem__(self, key, value):
        self.layout[key] = value

    def __delitem__(self, key):
        del self.layout.fields[key]

    def __len__(self):
        if self.layout is not None:
            return len(self.layout.fields)
        else:
            return 0


class FormHelper(DynamicLayoutHandler):
    """
    This class controls the form rendering behavior of the form passed to
    the `{% crispy %}` tag. For doing so you will need to set its attributes
    and pass the corresponding helper object to the tag::

        {% crispy form form.helper %}

    Let's see what attributes you can set and what form behaviors they apply to:

        **form_method**: Specifies form method attribute.
            You can set it to 'POST' or 'GET'. Defaults to 'POST'

        **form_action**: Applied to the form action attribute:
            - Can be a named url in your URLconf that can be executed via the `{% url %}` template tag. \
            Example: 'show_my_profile'. In your URLconf you could have something like::

                path('show/profile/', 'show_my_profile_view', name = 'show_my_profile')

            - It can simply point to a URL '/whatever/blabla/'.

        **form_id**: Generates a form id for dom identification.
            If no id provided then no id attribute is created on the form.

        **form_class**: String containing separated CSS classes to be applied
            to form class attribute.

        **form_group_wrapper_class**: String containing separated CSS classes to be applied
            to each row of inputs.

        **form_tag**: It specifies if <form></form> tags should be rendered when using a Layout.
            If set to False it renders the form without the <form></form> tags. Defaults to True.

        **form_error_title**: If a form has `non_field_errors` to display, they
            are rendered in a div. You can set title's div with this attribute.
            Example: "Oooops!" or "Form Errors"

        **formset_error_title**: If a formset has `non_form_errors` to display, they
            are rendered in a div. You can set title's div with this attribute.

        **include_media**: Whether to automatically include form media. Set to False if
            you want to manually include form media outside the form. Defaults to True.

    Public Methods:

        **add_input(input)**: You can add input buttons using this method. Inputs
            added using this method will be rendered at the end of the form/formset.

        **add_layout(layout)**: You can add a `Layout` object to `FormHelper`. The Layout
            specifies in a simple, clean and DRY way how the form fields should be rendered.
            You can wrap fields, order them, customize pretty much anything in the form.

    Best way to add a helper to a form is adding a property named helper to the form
    that returns customized `FormHelper` object::

        from crispy_forms.helper import FormHelper
        from crispy_forms.layout import Submit

        class MyForm(forms.Form):
            title = forms.CharField(_("Title"))

            @property
            def helper(self):
                helper = FormHelper()
                helper.form_id = 'this-form-rocks'
                helper.form_class = 'search'
                helper.add_input(Submit('save', 'save'))
                [...]
                return helper

    You can use it in a template doing::

        {% load crispy_forms_tags %}
        {% crispy form %}
    """

    _form_method = "post"
    _form_action = ""

    form = None
    form_id = ""
    form_class = ""
    form_group_wrapper_class = ""
    layout = None
    form_tag = True
    form_error_title = ""
    formset_error_title = ""
    form_show_errors = True
    render_unmentioned_fields = False
    render_hidden_fields = False
    render_required_fields = False
    _help_text_inline = False
    _error_text_inline = True
    form_show_labels = True
    template = None
    field_template = None
    disable_csrf = False
    use_custom_control = True
    label_class = ""
    field_class = ""
    include_media = True

    def __init__(self, form=None):
        self.attrs = {}
        self.inputs = []

        if form is not None:
            self.form = form
            self.layout = self.build_default_layout(form)

    def build_default_layout(self, form):
        return Layout(*form.fields.keys())

    @property
    def form_method(self):
        return self._form_method

    @form_method.setter
    def form_method(self, method):
        if method.lower() not in ("get", "post"):
            raise FormHelpersException(
                "Only GET and POST are valid in the \
                    form_method helper attribute"
            )

        self._form_method = method.lower()

    @property
    def form_action(self):
        try:
            return reverse(self._form_action)
        except NoReverseMatch:
            return self._form_action

    @form_action.setter
    def form_action(self, action):
        self._form_action = action

    @property
    def help_text_inline(self):
        return self._help_text_inline

    @help_text_inline.setter
    def help_text_inline(self, flag):
        self._help_text_inline = flag
        self._error_text_inline = not flag

    @property
    def error_text_inline(self):
        return self._error_text_inline

    @error_text_inline.setter
    def error_text_inline(self, flag):
        self._error_text_inline = flag
        self._help_text_inline = not flag

    def add_input(self, input_object):
        self.inputs.append(input_object)

    def add_layout(self, layout):
        self.layout = layout

    def render_layout(self, form, context, template_pack=TEMPLATE_PACK):
        """
        Returns safe html of the rendering of the layout
        """
        form.rendered_fields = set()
        form.crispy_field_template = self.field_template

        # This renders the specified Layout strictly
        html = self.layout.render(form, context, template_pack=template_pack)

        # Rendering some extra fields if specified
        if self.render_unmentioned_fields or self.render_hidden_fields or self.render_required_fields:
            fields = tuple(form.fields.keys())
            left_fields_to_render = list_difference(fields, form.rendered_fields)
            for field in left_fields_to_render:
                if (
                    self.render_unmentioned_fields
                    or (self.render_hidden_fields and form.fields[field].widget.is_hidden)
                    or (self.render_required_fields and form.fields[field].widget.is_required)
                ):
                    html += render_field(field, form, context, template_pack=template_pack)

        return mark_safe(html)

    def get_attributes(self, template_pack=TEMPLATE_PACK):  # noqa: C901
        """
        Used by crispy_forms_tags to get helper attributes
        """
        items = {
            "disable_csrf": self.disable_csrf,
            "error_text_inline": self.error_text_inline,
            "field_class": self.field_class,
            "field_template": self.field_template or "%s/field.html" % template_pack,
            "form_error_title": self.form_error_title.strip(),
            "form_method": self.form_method.strip(),
            "form_show_errors": self.form_show_errors,
            "form_show_labels": self.form_show_labels,
            "form_tag": self.form_tag,
            "formset_error_title": self.formset_error_title.strip(),
            "help_text_inline": self.help_text_inline,
            "include_media": self.include_media,
            "label_class": self.label_class,
            "use_custom_control": self.use_custom_control,
        }

        if template_pack == "bootstrap4":
            if "form-horizontal" in self.form_class.split():
                bootstrap_size_match = re.findall(r"col(-(xl|lg|md|sm))?-(\d+)", self.label_class)
                if bootstrap_size_match:
                    offset_pattern = "offset%s-%s"
                    items["bootstrap_checkbox_offsets"] = [
                        offset_pattern % (m[0], m[-1]) for m in bootstrap_size_match
                    ]
        else:
            bootstrap_size_match = re.findall(r"col-(lg|md|sm|xs)-(\d+)", self.label_class)
            if bootstrap_size_match:
                offset_pattern = "col-%s-offset-%s"
                items["bootstrap_checkbox_offsets"] = [offset_pattern % m for m in bootstrap_size_match]

        items["attrs"] = {}
        if self.attrs:
            items["attrs"] = self.attrs.copy()
        if self.form_action:
            items["attrs"]["action"] = self.form_action.strip()
        if self.form_id:
            items["attrs"]["id"] = self.form_id.strip()
        if self.form_class:
            items["attrs"]["class"] = self.form_class.strip()
        if self.form_group_wrapper_class:
            items["attrs"]["form_group_wrapper_class"] = self.form_group_wrapper_class

        items["flat_attrs"] = flatatt(items["attrs"])

        if self.inputs:
            items["inputs"] = self.inputs

        for attribute_name, value in self.__dict__.items():
            if (
                attribute_name not in items
                and attribute_name not in ["layout", "inputs"]
                and not attribute_name.startswith("_")
            ):
                items[attribute_name] = value

        return items

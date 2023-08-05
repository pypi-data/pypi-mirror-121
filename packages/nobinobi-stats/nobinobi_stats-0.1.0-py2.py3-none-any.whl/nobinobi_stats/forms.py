from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.utils.translation import gettext as _
from django_select2.forms import ModelSelect2Widget
from nobinobi_child.models import Child


class ChoiceAttendancePeriodForm(forms.Form):
    from_date = forms.DateField(label=_("From date"),
                                widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}).start_of(
                                    'period days'))
    end_date = forms.DateField(label=_("End date"),
                               widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}).end_of(
                                   'period days'))

    class Meta:
        fields = ["from_date", "end_date"]

    def __init__(self, *args, **kwargs):
        super(ChoiceAttendancePeriodForm, self).__init__(*args, **kwargs)
        # fourni par la page d'avant dans le url

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"

        self.helper.add_input(Submit('submit', _("Submit")))


class ChoiceAttendanceCalendarForm(forms.Form):
    date = forms.DateField(label=_("Date"),
                           widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}))

    class Meta:
        fields = ["date", ]

    def __init__(self, *args, **kwargs):
        super(ChoiceAttendanceCalendarForm, self).__init__(*args, **kwargs)
        # fourni par la page d'avant dans le url

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"

        self.helper.add_input(Submit('submit', _("Submit")))


class ChoiceAttendanceChildForm(forms.Form):
    from_date = forms.DateField(label=_("From date"),
                                widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}).start_of(
                                    'period days'))
    end_date = forms.DateField(label=_("End date"),
                               widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}).end_of(
                                   'period days'))
    child = forms.ModelChoiceField(
        queryset=Child.objects.filter(status=Child.STATUS.in_progress).order_by("age_group",
                                                                                'first_name',
                                                                                'last_name'),
        label=_("Child"),
        widget=ModelSelect2Widget(
            model=Child,
            queryset=Child.objects.filter(status=Child.STATUS.in_progress).order_by("age_group",
                                                                                    'first_name',
                                                                                    'last_name'),
            search_fields=['first_name__icontains', 'last_name__icontains'],
        ),
        required=True
    )

    class Meta:
        fields = ["from_date", "end_date", "child"]

    def __init__(self, *args, **kwargs):
        super(ChoiceAttendanceChildForm, self).__init__(*args, **kwargs)
        # fourni par la page d'avant dans le url

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"

        self.helper.add_input(Submit('submit', _("Submit")))


class ChoiceOccupancyPeriodForm(forms.Form):
    from_date = forms.DateField(label=_("From date"),
                                widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}).start_of(
                                    'period days'))
    end_date = forms.DateField(label=_("End date"),
                               widget=DatePickerInput(options={"locale": "fr", "format": "DD/MM/YYYY"}).end_of(
                                   'period days'))

    class Meta:
        fields = ["from_date", "end_date"]

    def __init__(self, *args, **kwargs):
        super(ChoiceOccupancyPeriodForm, self).__init__(*args, **kwargs)
        # fourni par la page d'avant dans le url

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"

        self.helper.add_input(Submit('submit', _("Submit")))

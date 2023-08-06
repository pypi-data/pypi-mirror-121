#  Copyright (c) 2021 <Florian Alu - alu@prolibre.com - https://www.prolibre.com>
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from bootstrap_datepicker_plus import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit
from django import forms
from django.utils.translation import gettext as _
from model_utils import Choices


class KitchenSelectForm(forms.Form):
    KITCHEN_VIEW_CHOICES = Choices(
        (0, _("View 1")),
        (1, _("View 2"))
    )
    date = forms.DateField(
        label=_("Date"),
        widget=DatePickerInput(options={
            "locale": "fr",
            "format": "DD/MM/YYYY"
        }),
    )
    display_view = forms.ChoiceField(label=_("Choice view display"), choices=KITCHEN_VIEW_CHOICES,
                                     initial=KITCHEN_VIEW_CHOICES[0])

    class Meta:
        fields = ("date", "display_view")

    def __init__(self, *args, **kwargs):
        super(KitchenSelectForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_id = 'id-kitchen-select-form'
        self.helper.form_class = 'form-horizontal blueForms'
        self.helper.form_method = 'post'
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-10"
        self.helper.layout = Layout(
            Div(
                Field("date"),
                Field("display_view"),
                Submit('submit', _('Submit')),
                css_class="mx-auto col-md-12"
            )
        )

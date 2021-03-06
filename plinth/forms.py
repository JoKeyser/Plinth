#
# This file is part of FreedomBox.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Common forms for use by modules.
"""

import os

from django import forms
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import get_language_info

import plinth
from plinth import utils


class ServiceForm(forms.Form):
    """Generic configuration form for a service."""
    is_enabled = forms.BooleanField(label=_('Enable application'),
                                    required=False)


class DomainSelectionForm(forms.Form):
    """Form for selecting a domain name to be used for
    distributed federated applications
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['domain_name'].choices = utils.get_domain_names()

    domain_name = forms.ChoiceField(
        label=_('Select a domain name to be used with this application'),
        help_text=_(
            'Warning! The application may not work properly if domain name is '
            'changed later.'), choices=[])


class LanguageSelectionFormMixin:
    """Form mixin for selecting the user's preferred language."""

    language = forms.ChoiceField(
        label=_('Language'),
        help_text=_('Language to use for presenting this web interface'),
        required=False)

    def __init__(self, *args, **kwargs):
        """Initialize the form to fill language choice values."""
        super().__init__(*args, **kwargs)
        supported_languages = [
            (None, _('Use the language preference set in the browser'))
        ]
        for language_code, language_name in settings.LANGUAGES:
            locale_code = translation.to_locale(language_code)
            plinth_dir = os.path.dirname(plinth.__file__)
            if language_code == 'en' or os.path.exists(
                    os.path.join(plinth_dir, 'locale', locale_code)):
                supported_languages.append(
                    (language_code,
                     get_language_info(language_code)['name_local']))

        self.fields['language'].choices = supported_languages


class LanguageSelectionForm(LanguageSelectionFormMixin, forms.Form):
    """Language selection form."""

    language = LanguageSelectionFormMixin.language

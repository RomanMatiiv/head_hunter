from django.forms import ModelForm

from junior_hunter.models import Application


class ApplicationForm(ModelForm):

    class Meta:
        model = Application
        fields = (
            'written_username',
            'written_phone',
            'written_cover_letter',
        )

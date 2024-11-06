from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Q

import datetime as datetime
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet
from django.conf import settings


def validate_start_to_date(cleaned_data,startDate_fieldName,endDate_fieldName):
  start_date=cleaned_data.get(startDate_fieldName)
  end_date=cleaned_data.get(endDate_fieldName)
  if (start_date is not None) and (end_date is not None):
      if start_date >  end_date:
       # raise ValidationError(_(f' {startDate_fieldName} must be less than {endDate_fieldName}'))
       return  (f' {endDate_fieldName} must be more than {startDate_fieldName}')
  else:
      return None


class MyDateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class MyTimeInput(forms.TimeInput):
    input_type = "time"

class MyDateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    #input_type = "datetime"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)

class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields ='__all__'
        widgets = {
            'project_name': forms.TextInput(attrs={'size':100}),
            'project_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'project_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        error_project_date = validate_start_to_date(cleaned_data, "project_start", "project_end")
        if error_project_date is not None:
            self.add_error("project_start", ValidationError(error_project_date))
        
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'

        widgets = {
            'project': forms.HiddenInput(),
            'customer_warranty_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]),
            'customer_warranty_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"]),
            'remark': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'part_detail': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
        }

    def __init__(self, *args, brand_choices=None, model_choices=None, **kwargs):
        super().__init__(*args, **kwargs)

        if brand_choices:
            self.fields['brand'] = forms.ChoiceField(choices=brand_choices)

        if model_choices:
            self.fields['model'] = forms.ChoiceField(choices=model_choices)
import time
import datetime

from django.db import models
from django.db.models import Func
from django.conf import settings

from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.utils.encoding import force_str
from django.utils.formats import get_format
from django.utils import six

from django.core.validators import ValidationError
from django.forms import SelectDateWidget


YEARMONTH_INPUT_FORMATS = (
    '%Y-%m', '%m/%Y', '%m/%y', # '2006-10', '10/2006', '10/06'
)


class YearMonthField(models.CharField):
    default_error_messages = {
        'invalid': _('Enter a valid year and month.'),
    }

    def __init__(self, input_formats=None, *args, **kwargs):
        super(YearMonthField, self).__init__(*args, **kwargs)
        self.input_formats = YEARMONTH_INPUT_FORMATS

    def clean(self, value, model_instance):
        print("Year Month value: {}".format(value))
        if isinstance(value, datetime.datetime):
            return format(value, '%Y-%m')
        if isinstance(value, datetime.date):
            return format(value, '%Y-%m')
        for fmt in self.input_formats or YEARMONTH_INPUT_FORMATS:
            try:
                date = datetime.date(*time.strptime(value, fmt)[:3])
                return format(date, '%Y-%m')
            except ValueError:
                continue
        raise ValidationError(self.error_messages['invalid'])


class Month(Func):
    def __ror__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    function = 'EXTRACT'
    template = '%(function)s(MONTH from %(expressions)s)'
    output_field = models.IntegerField()


class Year(Month):
    template = '%(function)s(YEAR from %(expressions)s)'


class ToDate(Func):
    def __ror__(self, other):
        pass

    def __rand__(self, other):
        pass

    def __and__(self, other):
        pass

    def __or__(self, other):
        pass

    function = 'to_date'
    template = '%(function)s(CONCAT(%(expressions)s, \'-01\'), \'YYYY-MM-DD\')'
    output_field = models.DateField()

import re
from datetime import date
from datetime import datetime

from django.utils.timezone import now
from django.db.models import Count
from django.db.models.functions import Concat

from website.fields import Year, Month, ToDate


def map_months_counter(row):
    m = re.search('([0-9]{4})([0-9]{1,2})', str(row['year_month']))
    mdate = date(int(m.group(1)), int(m.group(2)), 1)
    row['year_month'] = mdate.strftime('%Y-%m')
    row['date'] = mdate.strftime('%B, %Y')
    return row


class WebsiteMixinTravelIndexPage(object):

    def get_context(self, request, *args, **kwargs):
        context = super(WebsiteMixinTravelIndexPage, self).get_context(request)
        year_month = request.GET.get('year_month')
        # avoid recursive dependencies
        from website.models import WebsiteTravelPage

        upcomming_travels = WebsiteTravelPage.objects.live().order_by('-first_published_at')

        upcomming_travel_months = upcomming_travels.filter(date__gt=str(now())).annotate(
            year_month=Concat(Year(ToDate('date')), Month(ToDate('date')))). \
            values('year_month'). \
            annotate(total=Count('id'))

        result = upcomming_travel_months
        months = map(map_months_counter, result)

        if year_month:
            filter_date = datetime.strptime(year_month, '%Y-%m')
            upcomming_travels = upcomming_travels.filter(date__month=filter_date.month, date__year=filter_date.year)
        else:
            upcomming_travels = upcomming_travels.filter(date__gt=now())


        context['travelpages'] = upcomming_travels
        context['months'] = months
        return context


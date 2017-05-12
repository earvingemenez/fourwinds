from __future__ import unicode_literals

from taggit.models import TaggedItemBase

from wagtail.wagtailcore.models import Page, Orderable
from django.db import models
from django import forms

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index


class WebsiteAboutIndexPage(Page):
    body = RichTextField(blank=False)

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body')
    ]


class WebsiteSafetyInsuranceIndexPage(Page):
    body_left = RichTextField(blank=False)
    body_right = RichTextField(blank=True)
    body_bottom = RichTextField(blank=True)
    pdf = models.ForeignKey('wagtaildocs.Document', null=True, on_delete=models.SET_NULL, related_name='+')

    search_fields = Page.search_fields + [
        index.SearchField('body_left'),
        index.SearchField('body_right'),
        index.SearchField('body_bottom'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('body_left'),
        FieldPanel('body_right'),
        FieldPanel('body_bottom'),
        FieldPanel('pdf')
    ]


class WebsiteTestimonalsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(WebsiteTestimonalsIndexPage, self).get_context(request)
        pages = self.get_children().live().order_by('-first_published_at')
        context['testimonialpages'] = pages
        return context


class WebsiteTestimonialPage(Page):
    text = RichTextField(blank=False)
    full_name = models.CharField(max_length=150, default='')
    organization = models.CharField(max_length=150)
    trip_event = models.CharField("Trip or/and Event", max_length=250, default='')
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    date = models.DateField("Date of the event/trip", null=True)

    search_fields = Page.search_fields + [
        index.SearchField('text'),
        index.SearchField('full_name'),
        index.SearchField('organization'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('full_name'),
            FieldPanel('trip_event'),
            FieldPanel('organization'),
            FieldPanel('date'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Trip information"),
        FieldPanel('text'),
    ]


@register_snippet
class WebsiteCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'

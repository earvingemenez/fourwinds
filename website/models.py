from __future__ import unicode_literals

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase, Tag

from wagtail.wagtailcore.models import Page, Orderable
from django import forms
from django.db import models
from django.forms import extras
from django.core.validators import ValidationError
from django.utils.text import slugify, _
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.wagtailcore.fields import RichTextField
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
    PageChooserPanel
)
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailforms.models import (
    AbstractForm,
    AbstractFormField,
    AbstractFormSubmission
)
from wagtail.wagtailsearch import index
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel

from website.fields import YearMonthField
from website.mixins import WebsiteMixinTravelIndexPage


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
        pages = WebsiteTestimonialPage.objects.descendant_of(self).live().order_by('-date')
        paginator = Paginator(pages, 10)
        page = request.GET.get('page')
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(num_pages)
        context['testimonialpages'] = pages
        return context

class WebsiteTestimonialPageTag(TaggedItemBase):
    content_object = ParentalKey('WebsiteTestimonialPage', related_name='tagged_items')


@register_snippet
class WebsiteTag(Tag):
    class Meta:
        proxy = True


class WebsiteTestimonialPage(Page):
    text = RichTextField(blank=False)
    full_name = models.CharField(max_length=150, default='')
    organization = models.CharField(max_length=150)
    trip_event = models.CharField("Trip or/and Event", max_length=250, default='')
    categories = ParentalManyToManyField('website.WebsiteCategory', blank=True)
    tags = ClusterTaggableManager(through=WebsiteTestimonialPageTag, blank=True)
    date = YearMonthField(max_length=10)

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
            FieldPanel('date', widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM'})),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags')
        ], heading="Trip information"),
        FieldPanel('text'),
    ]


class WebsiteTestimonialTagIndexPage(Page):

    def get_context(self, request):
        tag = request.GET.get('tag')
        testimonialpages = WebsiteTestimonialPage.objects.filter(tags__name=tag)

        context = super(WebsiteTestimonialTagIndexPage, self).get_context(request)
        context['testimonialpages'] = testimonialpages
        return context


@register_snippet
class WebsiteCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    slug = models.SlugField(unique=True, max_length=80)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name="children",
        help_text=_(
            'Categories, unlike tags, can have a hierarchy. You might have a '
            'Trip category, and under that have children categories for International'
            ' and Nacional. Totally optional.')
    )
    description = models.CharField(max_length=500, blank=True)
    page_link_to = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    class Meta:
        ordering = ['name']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    panels = [
        FieldPanel('name'),
        FieldPanel('parent'),
        FieldPanel('description'),
        ImageChooserPanel('icon'),
        PageChooserPanel('page_link_to')
    ]

    def __str__(self):
        parent_name = str(self.parent)
        if self.parent:
            return "{} - {}".format(parent_name, self.name)
        return self.name

    def clean(self):
        if self.parent:
            parent = self.parent
            if self.parent == self:
                raise ValidationError('Parent category cannot be self.')
            if parent.parent and parent.parent == self:
                raise ValidationError('Cannot have circular Parents.')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super(WebsiteCategory, self).save(*args, **kwargs)


class WebsiteTravelIndexPage(WebsiteMixinTravelIndexPage, Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]


class WebsiteTravelPage(Page):
    intro = RichTextField()
    text = RichTextField()
    destination = models.CharField(max_length=200)
    date = YearMonthField(max_length=10)
    start_location = models.CharField(max_length=255, default='')
    end_location = models.CharField(max_length=255, default='')
    categories = ParentalManyToManyField('website.WebsiteCategory')

    @property
    def main_image(self):
        gallery_item = self.gallery_images.first()
        print("gallery_image: ")
        print(gallery_item)
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('text'),
        index.SearchField('destination'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('destination'),
            FieldPanel('date', forms.SelectDateWidget),
            FieldPanel('start_location'),
            FieldPanel('end_location'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Trip/Event information"),
        FieldPanel('intro'),
        FieldPanel('text'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]


class WebsiteTravelGalleryImage(Orderable):
    page = ParentalKey(WebsiteTravelPage, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


class WebsiteTravelCategoryIndexPage(Page):

    def get_context(self, request):
        category = request.GET.get('category')
        travelpages = WebsiteTravelPage.objects.filter(categories__slug=category)

        context = super(WebsiteTravelCategoryIndexPage, self).get_context(request)
        context['travelpages'] = travelpages
        return context


class WebsiteInternalContentPage(Page):
    body = RichTextField(blank=True)
    docs = models.ForeignKey('wagtaildocs.Document', blank=True, null=True,
        on_delete=models.SET_NULL, related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
        FieldPanel('docs')
    ]


class FormField(AbstractFormField):
    page = ParentalKey('WebsiteGetQuotePage', related_name='form_fields')


class WebsiteGetQuotePage(AbstractForm):
    intro = RichTextField(blank=True)
    success_text = RichTextField(blank=True)

    content_panels = AbstractForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname='full'),
        FieldPanel('success_text', classname='full'),
        InlinePanel('form_fields', label='Form fields')
    ]

    def process_form_submission(self, form):
        email = EmailMessage(
            'Get a Quote Form Submission',
            render_to_string('email/get-a-quote-template.html', {
                'firstname': form.cleaned_data.get('first-name'),
                'lastname': form.cleaned_data.get('last-name'),
                'email': form.cleaned_data.get('email-address'),
                'phone_number': form.cleaned_data.get('phone-number'),
                'school_name': form.cleaned_data.get('school-name'),
                'school_zip_code': form.cleaned_data.get('school-zip-code'),
                'role': form.cleaned_data.get('role'),
                'type_of_trip': form.cleaned_data.get('type-of-trip'),
                'estimated_trip_year': form.cleaned_data.get('estimated-trip-year'),
                'desired_destination': form.cleaned_data.get('desired-destination'),
                'number_of_students': form.cleaned_data.get('number-of-students'),
                'approximate_budget': form.cleaned_data.get('approximate-budget'),
                'comments': form.cleaned_data.get('comments'),
            }),
            '{} {} <{}>'.format(form.cleaned_data.get('first-name'),
                form.cleaned_data.get('last-name'),
                form.cleaned_data.get('email-address')),
            [settings.DEFAULT_TO_EMAIL]
        )
        email.content_subtype = 'html'
        email.send()


class WebsiteTourCollectionIndexPage(Page):
    intro = RichTextField(blank=True)
    heading = models.CharField(max_length=250, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        FieldPanel('heading', classname='full'),
    ]

    def get_context(self, request):
        context = super(WebsiteTourCollectionIndexPage, self).get_context(request)
        tours = self.get_children().live().type(WebsiteTourCollectionItemPage)
        context['tours'] = tours
        return context


class WebsiteTourCollectionItemPage(Page):
    heading = models.CharField(max_length=250)
    description = RichTextField(blank=True)
    page_link_to = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
    )

    def header_image(self):
        header_image_item = self.header_images.first()
        if header_image_item:
            return header_image_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel('heading'),
        FieldPanel('description'),
        InlinePanel('header_images', label='Header images'),
        PageChooserPanel('page_link_to')
    ]


class TourCollectionHeaderImages(Orderable):
    page = ParentalKey(WebsiteTourCollectionItemPage, related_name='header_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image')
    ]


class ContactFormField(AbstractFormField):
    page = ParentalKey('WebsiteContactUsPage', related_name='form_fields')


class WebsiteContactUsPage(AbstractForm):
    intro = RichTextField(blank=True)
    success_text = models.CharField(max_length=250)

    content_panels = AbstractForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname='full'),
        FieldPanel('success_text', classname='full'),
        InlinePanel('form_fields', label='Contact form fields')
    ]

    def process_form_submission(self, form):
        email = EmailMessage(
            'Contact form submission',
            render_to_string('email/contact-form-template.html', {
                'firstname': form.cleaned_data.get('first-name'),
                'lastname': form.cleaned_data.get('last-name'),
                'email': form.cleaned_data.get('email-address'),
                'intended_recipient': form.cleaned_data.get('intended-recipient'),
                'your_message': form.cleaned_data.get('your-message'),
            }),
            '{} {} <{}>'.format(form.cleaned_data.get('first-name'),
                form.cleaned_data.get('last-name'),
                form.cleaned_data.get('email-address')),
            [settings.DEFAULT_TO_EMAIL]
        )
        email.content_subtype = 'html'
        email.send()
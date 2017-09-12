import datetime

from blog.models import BlogPage, BlogCategory
from home.models import HomePage
from django import template
from django.template.defaultfilters import stringfilter

from wagtail.wagtailcore.models import Page
from website.models import (
    WebsiteTestimonialPage,
    WebsiteTravelPage,
    WebsiteCategory,
    WebsiteTourCollectionIndexPage
)

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()

@register.inclusion_tag('home/tags/site_header.html', takes_context=True)
def get_site_header(context):
    return context


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('home/tags/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    queryset = parent.get_children()
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/footer_menu.html', takes_context=True)
def footer_menu(context, parent, calling_page=None):
    queryset = parent.get_children()
    menuitems = parent.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        # We don't directly check if calling_page is None since the template
        # engine can pass an empty string to calling_page
        # if the variable passed as calling_page does not exist.
        menuitem.active = (calling_page.url.startswith(menuitem.url)
                           if calling_page else False)
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('home/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent, calling_page=None):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()

    for menuitem in menuitems_children:
        # Check if menuitem has children
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
            if calling_page else False)

    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/submenu.html', takes_context=True)
def submenu(context, parent, calling_page=None):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()

    for menuitem in menuitems_children:
        # Check if menuitem has children
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (calling_page.url.startswith(menuitem.url)
            if calling_page else False)

    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/main_slider.html', takes_context=True)
def main_slider(context, calling_page):
    show_carousel = calling_page.gallery_images.count() > 0
    parent_page = Page.objects.type(HomePage).first()
    tours_page = Page.objects.type(WebsiteTourCollectionIndexPage).child_of(parent_page).first()
    return {
        "gallery_images": calling_page.gallery_images,
        "show_carousel" : show_carousel,
        "tours_page": tours_page
    }

@register.inclusion_tag('home/tags/quick_contact_form.html', takes_context=True)
def quick_contact_form(context):
    return {
        'request': context['request']
    }

@register.inclusion_tag('website/tags/get_a_quote_form.html', takes_context=True)
def get_a_quote_form(context):
    return {
        'request': context['request']
    }

@register.inclusion_tag('website/tags/testimonials.html', takes_context=True)
def testimonials_slider(context, calling_page):
    testimonials = WebsiteTestimonialPage.objects.live().order_by('-first_published_at')
    more_testimonials_link = testimonials[0].get_parent().url if len(testimonials) > 0 else "#"
    return {"testimonials": testimonials, "more_testimonials_link": more_testimonials_link}

@register.inclusion_tag('website/tags/side_testimonials.html', takes_context=True)
def testimonials_sidebar(context, calling_page):
    testimonials = WebsiteTestimonialPage.objects.live().order_by('-first_published_at')
    more_testimonials_link = testimonials[0].get_parent().url if len(testimonials) > 0 else "#"
    return {"testimonials": testimonials, "more_testimonials_link": more_testimonials_link}


@register.inclusion_tag('website/tags/travel_carousel.html', takes_context=True)
def travel_carousel(context, calling_page):
    travels = WebsiteTravelPage.objects.live().order_by('-first_published_at')[:10]
    return {"travelpages": travels}


@register.inclusion_tag('website/tags/travels.html', takes_context=True)
def travels_home(context, calling_page):
    travels = WebsiteTravelPage.objects.live().order_by('-first_published_at')[:2]
    return {
        'travelpages': travels
    }


@register.inclusion_tag('blog/tags/recents.html', takes_context=True)
def blog_recents(context):
    blogs = BlogPage.objects.live().order_by('-first_published_at')[:10]
    return {
        'blogs': blogs
    }

@register.inclusion_tag('blog/tags/categories.html', takes_context=True)
def blog_tags(context):
    cats = BlogCategory.objects.all()
    return {
        'cats': cats
    }

@register.inclusion_tag('website/tags/travel_categories.html', takes_context=True)
def travel_categories(context):
    categories = WebsiteCategory.objects.all()
    return {
        'categories': categories
    }

@stringfilter
def parse_date(date_string, format):
    """
    Return a datetime corresponding to date_string, parsed according to format.
    For example, to re-display a date string in another format:
        {{ "2017-10"|parse_date:"%Y-%m"|date:"F Y" }}
    """
    try:
        return datetime.datetime.strptime(date_string, format)
    except ValueError:
        return None
register.filter('parse_date', parse_date)

@stringfilter
def smart_truncate(text, limitTo):
    suffix = '...'
    if len(text) <= limitTo:
        return text
    else:
        return ' '.join(text[:int(limitTo)].split(' ')[:-1]) + suffix

register.filter('smart_truncate', smart_truncate)
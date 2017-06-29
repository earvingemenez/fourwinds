import datetime

from blog.models import BlogPage, BlogCategory
from django import template
from django.template.defaultfilters import stringfilter

from website.models import WebsiteTestimonialPage, WebsiteTravelPage

register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


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


# Retrieves the children of the top menu items for the drop downs
@register.inclusion_tag('home/tags/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('home/tags/main_slider.html', takes_context=True)
def main_slider(context, calling_page):
    show_carousel = calling_page.gallery_images.count() > 0
    return {
        "gallery_images": calling_page.gallery_images,
        "show_carousel" : show_carousel
    }


@register.inclusion_tag('website/tags/testimonials.html', takes_context=True)
def testimonials_slider(context, calling_page):
    testimonials = WebsiteTestimonialPage.objects.live().order_by('-first_published_at')
    more_testimonials_link = testimonials[0].get_parent().url if len(testimonials) > 0 else "#"
    return {"testimonials": testimonials, "more_testimonials_link": more_testimonials_link}


@register.inclusion_tag('website/tags/travel_carousel.html', takes_context=True)
def travel_carousel(context, calling_page):
    travels = WebsiteTravelPage.objects.live().order_by('-first_published_at')[:10]
    return {"travelpages": travels}


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
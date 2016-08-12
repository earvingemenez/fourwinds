from django import template

register = template.Library()


@register.inclusion_tag('top_header.html', takes_context=True)
def render_topheader(context):
    return {}


@register.inclusion_tag('top_navbar.html', takes_context=True)
def render_topnavbar(context):
    return {}


@register.inclusion_tag('widgets.html', takes_context=True)
def render_widgets(context):
    return {}


@register.inclusion_tag('get_started_form.html', takes_context=True)
def render_get_started_form(context):
    return {}


@register.inclusion_tag('welcome_signin_form.html', takes_context=True)
def render_welcome_signin_form(context):
    return {}


@register.inclusion_tag('testimonials.html', takes_context=True)
def render_testimonials(context):
    from website.models import Testimonial
    data = Testimonial.objects.all()[:5]
    return {'testimonials': data}


@register.inclusion_tag('footer.html', takes_context=True)
def render_footer(context):
    return {}

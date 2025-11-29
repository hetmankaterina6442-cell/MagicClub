from django import template
from ..forms import LoginBoxForm

register = template.Library()

@register.inclusion_tag("authbox/widget.html", takes_context=True)
def authbox_widget(context, next_url=None):
    request = context["request"]
    form = LoginBoxForm(request)
    return {"form": form, "next": next_url or request.get_full_path()}

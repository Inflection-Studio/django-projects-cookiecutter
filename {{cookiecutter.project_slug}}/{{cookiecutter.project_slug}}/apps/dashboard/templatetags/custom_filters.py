from django import template

register = template.Library()


@register.filter(name="get_badge_class")
def get_badge_class(badge_classes, status):
	return badge_classes.get(
		status, "badge-primary",
	)  # Default to 'badge-primary' if status not found

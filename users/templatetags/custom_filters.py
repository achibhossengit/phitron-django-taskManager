from django import template
from datetime import datetime
from django.utils import timezone

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        # USE_TZ = True সেট করা থাকলে, Django সর্বদা UTC টাইমজোনে ডেটা সংরক্ষণ করে যাতে বিভিন্ন টাইমজোনে ডেটা সহজে কনভার্ট করা যায়
        # Django শুধু HTML টেমপ্লেটের মধ্যে সরাসরি DateTimeField প্রদর্শন করলে লোকাল টাইমজোনে (TIME_ZONE='Asia/Dhaka') রূপান্তর করে।
        value = timezone.localtime(value)
        today = datetime.now().date()
        if value.date() == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value.date() == today.replace(day=today.day - 1):
            return f"Yeasterday at {value.strftime('%I:%M %p')}"
        else:
            return f"{value.date().strftime('%B %d')}, {value.strftime('%I:%M %p')}"
    return "No login record available!"
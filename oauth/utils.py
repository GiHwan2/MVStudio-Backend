from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from member.models import Member

User = get_user_model()

@transaction.atomic
def social_member_create(username, password=None, **extra_fields):
    member = Member(username=username, email=username)

    if password:
        member.set_password(password)
    else:
        member.set_unusable_password()
    try:
        member.profile_image = extra_fields['image']
    except:
        pass

    if extra_fields['nickname'] == '':
        member.nickname = username
    else:
        member.nickname = extra_fields['nickname']

    try:
        try:
            member.first_name = extra_fields['first_name']
            member.last_name = extra_fields['last_name']
        except:
            try:
                member.first_name = extra_fields['name']
            except:
                pass
    except:
        pass

    member.full_clean()
    member.save()
    return member


@transaction.atomic
def social_user_get_or_create(username, **extra_data):
    member = Member.objects.filter(email=username).first()

    if member:
        return member, False

    return social_member_create(username=username, **extra_data), True
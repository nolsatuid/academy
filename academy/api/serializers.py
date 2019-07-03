from django.conf import settings

from academy.apps.accounts.models import User


def user_profile(user: User) -> dict:
    profile = user.profile
    avatar = settings.MEDIA_HOST + profile.avatar.url \
        if profile.avatar else None
    cv = settings.MEDIA_HOST + profile.curriculum_vitae.url \
        if user.profile.curriculum_vitae else None

    return {
        'name': user.name,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'is_active': user.is_active,
        'gender': profile.get_gender_display(),
        'birthday': profile.birthday.strftime("%Y-%m-%d") if profile.birthday else None,
        'avatar': avatar,
        'linkedin': profile.linkedin,
        'git_repo': profile.git_repo,
        'blog': profile.blog,
        'facebook': profile.facebook,
        'youtube': profile.youtube,
        'twitter': profile.twitter,
        'instagram': profile.instagram,
        'telegram_id': profile.telegram_id,
        'curriculum_vitae': cv
    }


def logo(logo):
    """
    this serializer for LogoPerner and LogoSponsor
    """
    return {
        'name': logo.name,
        'image': settings.MEDIA_HOST + logo.image.url,
        'display_order': logo.display_order,
        'website': logo.website
    }

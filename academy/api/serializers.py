from django.conf import settings
from academy.apps.accounts.models import User
from academy.apps.students.templatetags.tags_students import get_status, status_to_display


def user_profile(user: User) -> dict:
    user_data = {
        'id': user.id,
        'name': user.name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'status': 1,
        'avatar': "",
        'linkedin': "",
        'git_repo': "",
        'blog': "",
        'facebook': "",
        'youtube': "",
        'twitter': "",
        'instagram': "",
        'telegram_id': "",
        'curriculum_vitae': "",
        'has_profile': False
    }

    if hasattr(user, 'profile'):
        profile = user.profile
        cv = settings.MEDIA_HOST + profile.curriculum_vitae.url \
            if user.profile.curriculum_vitae else None

        user_data['has_profile'] = True
        user_data['avatar'] = profile.get_avatar(with_host=True)
        user_data['linkedin'] = profile.linkedin
        user_data['git_repo'] = profile.git_repo
        user_data['blog'] = profile.blog
        user_data['facebook'] = profile.facebook
        user_data['facebook'] = profile.facebook
        user_data['youtube'] = profile.youtube
        user_data['youtube'] = profile.youtube
        user_data['twitter'] = profile.twitter
        user_data['instagram'] = profile.instagram
        user_data['telegram_id'] = profile.telegram_id
        user_data['telegram_id'] = profile.telegram_id
        user_data['curriculum_vitae'] = cv

    student = user.get_student()
    user_data['status'] = student.status if student else 1

    return user_data


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


def training_material(materi, user):
    status = get_status(materi, user)
    return {
        "code": materi.code,
        "title": materi.title,
        "status": status_to_display(status) if status else "Belum"
    }


def graduate_data(graduate):
    return {
        "certificate_url": settings.MEDIA_HOST + graduate.certificate_file.url,
        "certificate_number": graduate.certificate_number,
        "is_channeled": graduate.is_channeled,
        "channeled_at": graduate.channeled_at,
    }


def instructor(instructor):
    return {
        'name': instructor.user.name,
        'photo': settings.MEDIA_HOST + instructor.user.profile.avatar.url,
        'specialization': instructor.user.profile.specialization,
        'linkedin': instructor.user.profile.linkedin
    }


def news(source, post, identifier=""):
    return {
        "source_name": source["name"],
        "source_link": source["link"],
        "source_identifier": identifier,
        "post_title": post["title"],
        "post_link": post["link"],
    }

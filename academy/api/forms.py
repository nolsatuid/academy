from academy.apps.accounts.models import User
from academy.website.accounts.forms import SignupForm


class APIRegisterForm(SignupForm):
    def save(self, *args, **kwargs):
        user = super().save()
        user.registered_via = User.VIA.mobile
        user.save()

        return user

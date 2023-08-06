from django.conf import settings
from ..utils import import_class
from ..models import get_user_profile_model


def get_profile_serializer_class():
    return import_class(settings.SHA_ACCOUNTS.get('AUTH_USER_PROFILE_SERIALIZER'))


Profile = get_user_profile_model()

ProfileSerializer = get_profile_serializer_class()

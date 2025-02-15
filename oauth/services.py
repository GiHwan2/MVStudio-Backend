import requests

from django.conf import settings
from django.core.exceptions import ValidationError
from music_videos.models import MusicVideo

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def google_get_access_token(google_token_api, code, redirection_uri):
    client_id = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
    client_secret = settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
    code = code
    grant_type = 'authorization_code'
    state = "random_string"

    google_token_api += \
        f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirection_uri}&state={state}"

    token_response = requests.post(google_token_api)

    if not token_response.ok:
        raise ValidationError('google_token is invalid')

    access_token = token_response.json().get('access_token')

    return access_token

def google_get_user_info(access_token):
    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        params={
            'access_token': access_token
        }
    )

    if not user_info_response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    user_info = user_info_response.json()

    return user_info
from authlib.integrations.django_client import OAuth
from authlib.jose import jwt
from authlib.oidc.core import CodeIDToken
from django.http import JsonResponse

from GroupPlus.settings import JACCOUNT_CLIENT_ID, JACCOUNT_CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name='jaccount',
    client_id=JACCOUNT_CLIENT_ID,
    client_secret=JACCOUNT_CLIENT_SECRET,
    access_token_url='https://jaccount.sjtu.edu.cn/oauth2/token',
    authorize_url='https://jaccount.sjtu.edu.cn/oauth2/authorize',
    api_base_url='https://api.sjtu.edu.cn/',
    client_kwargs={
        "scope": "openid",
        "token_endpoint_auth_method": "client_secret_basic",
        "token_placement": "header"
    }
)
jaccount = oauth.jaccount


def login(request):
    if 'user' in request.session:
        return JsonResponse({"success": True, 'message': 'Do not log in repeatedly'})

    # build a full authorize callback uri
    redirect_uri = request.build_absolute_uri('/authorize')
    return jaccount.authorize_redirect(request, redirect_uri)


def authorize(request):
    token = oauth.jaccount.authorize_access_token(request)
    claims = jwt.decode(token.get('id_token'), jaccount.client_secret, claims_cls=CodeIDToken)
    request.session['user'] = claims
    request.session.set_expiry(claims['exp'] - claims['iat'])
    # resp = oauth.jaccount.get('user', token=token)
    return JsonResponse({"success": True})

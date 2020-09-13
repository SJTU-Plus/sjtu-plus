from authlib.jose import jwt
from authlib.oidc.core import CodeIDToken
from django.shortcuts import redirect, reverse

from SJTUPlus.oauth import jaccount


def login(request):
    if request.GET.get('app') == 'course_plus':
        redirect_uri = request.build_absolute_uri('/authorize?app=course_plus')
        return jaccount.authorize_redirect(request, redirect_uri, scope="openid lessons")

    redirect_uri = request.build_absolute_uri('/authorize')
    return jaccount.authorize_redirect(request, redirect_uri)


def authorize(request):
    token = jaccount.authorize_access_token(request)
    claims = jwt.decode(token.get('id_token'),
                        jaccount.client_secret, claims_cls=CodeIDToken)
    request.session['token'] = token
    request.session['user'] = claims
    request.session.set_expiry(claims['exp'] - claims['iat'])
    if request.GET.get('app') == 'course_plus':
        return redirect('/course-plus')
    return redirect(reverse('attest:index'))

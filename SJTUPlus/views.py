from urllib.parse import urlencode

import requests
from authlib.jose import jwt
from authlib.oidc.core import CodeIDToken
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, reverse

from SJTUPlus.oauth import jaccount
from SJTUPlus.settings import JACCOUNT_CLIENT_ID

from .utils import decode_state, encode_state, get_filtered_scope, get_filtered_redirecturi


def login(request):
    session_app = None
    redirect_uri = None
    scopes = {'openid'}

    app = request.GET.get('app')
    http_referer = request.META.get('HTTP_REFERER', '')

    if app:
        if app == 'course_plus':
            session_app = 'course_plus'
            redirect_uri = '/course-plus'
            scopes.add('lessons')
        elif app == 'group_verify':
            redirect_uri = reverse('attest:index')
        elif app == 'debug':
            redirect_uri = '/'
            scopes.add('basic')
            scopes.add('openid')
            scopes.add('essential')
            scopes.add('lessons')
            scopes.add('classes')
            scopes.add('exams')
            scopes.add('scores')
        else:
            redirect_uri = '/'
    else:
        redirect_uri = '/'

    if request.GET.get('scope'):  # 显式设定 scope 时，追加 scope
        scope_list = request.GET['scope'].split(',')
        scopes.update(scope_list)

    if request.GET.get('redirecturi'):  # 显式设定 redirecturi 时，按该 scope 执行
        redirect_uri = request.GET['redirecturi']

    scope_list = get_filtered_scope(scopes)
    redirect_uri = get_filtered_redirecturi(redirect_uri)

    redir_to = jaccount.authorize_redirect(
        request,
        redirect_uri=request.build_absolute_uri('/authorize'),
        scope=' '.join(scope_list),
        state=encode_state({  # 加密传递的参数
            'redir': redirect_uri,
            'scope': scope_list,
            'session_app': session_app,
            'referer': http_referer
        })
    ).url
    r = requests.get(redir_to)  # finish the first rediect
    return HttpResponseRedirect(r.url)


def authorize(request):
    token: dict = jaccount.authorize_access_token(request)
    claims = jwt.decode(token.pop('id_token'),
                        jaccount.client_secret, claims_cls=CodeIDToken)
    claims.validate()

    state = request.GET.get('state')

    if state:
        state = decode_state(state)

    request.session['token'] = token
    request.session['user'] = claims
    request.session['scope'] = state['scope']  # 事实上用户未必勾选了申请的所有权限
    request.session.set_expiry(claims['exp'] - claims['iat'])

    redir_uri = state['redir']

    return redirect(redir_uri)


def logout(request):
    # http_referer = request.META.get('HTTP_REFERER', '')

    app = request.GET.get('app')
    user_state = request.GET.get('state')
    redirect_uri = request.GET.get('redirecturi')

    if app:
        if app == 'course_plus':
            redirect_uri = '/course-plus'
        elif app == 'group_verify':
            redirect_uri = reverse('verify')
        else:
            redirect_uri = '/'
    else:
        if not redirect_uri:
            redirect_uri = '/'

    redirect_uri = get_filtered_redirecturi(redirect_uri)

    state = {
        'redirect_uri': redirect_uri
    }
    if user_state:
        state['state'] = user_state

    response = HttpResponseRedirect(
        'https://jaccount.sjtu.edu.cn/oauth2/logout?' +
        urlencode({
            'client_id': JACCOUNT_CLIENT_ID,
            'post_logout_redirect_uri': request.build_absolute_uri('/logged_out?'+urlencode({'state': encode_state(state)})),
            # 'state': '' # jAccount后台对该参数的处理疑似存在 bug，会在 state 前错误添加 ? 和 &，遂弃用
        })
    )
    response.delete_cookie('sessionid')  # 指示客户端清除 cookie 会话
    return response


def logged_out(request):
    state = decode_state(request.GET['state'])
    return HttpResponseRedirect(state['redirect_uri'])

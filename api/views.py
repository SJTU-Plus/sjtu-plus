import json
import re
from http import HTTPStatus
from time import time

import requests
from django.http import JsonResponse
from django.utils.encoding import escape_uri_path
from SJTUPlus.oauth import jaccount
from SJTUPlus.utils import jaccount_type_map


def canteen(request):
    result = requests.get('https://canteen.sjtu.edu.cn/CARD/Ajax/Place')
    # 当数据类型不是 dict 时，需要 safe=False
    return JsonResponse(
        result.json(), safe=False,
        content_type='application/json; charset=utf-8',
        json_dumps_params={'ensure_ascii': False}
    )


def canteen_detail(request, id: int):
    if not (0 < id < 100000):
        return JsonResponse({'error': 'invalid id'}, status=HTTPStatus.BAD_REQUEST)
    result = requests.get(
        f'https://canteen.sjtu.edu.cn/CARD/Ajax/PlaceDetails/{id}')
    # 当数据类型不是 dict 时，需要 safe=False
    return JsonResponse(
        result.json(), safe=False,
        content_type='application/json; charset=utf-8',
        json_dumps_params={'ensure_ascii': False}
    )


def canteen_all(request):
    result = requests.get(
        f'https://canteen.sjtu.edu.cn/card/ajax/placeall')
    # 当数据类型不是 dict 时，需要 safe=False
    return JsonResponse(
        result.json(), safe=False,
        content_type='application/json; charset=utf-8',
        json_dumps_params={'ensure_ascii': False}
    )


def library(request):
    result = requests.get(
        f'http://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson&_={time()}')
    strip = result.text[12:-2]
    return JsonResponse(
        json.loads(strip),
        content_type='application/json; charset=utf-8',
        json_dumps_params={'ensure_ascii': False}
    )


def cainiao(request):
    result = requests.get(
        f'https://map.sjtu.edu.cn/realtimePersion/kuaidi')
    return JsonResponse(
        json.loads(result.content.decode('gbk')),
        content_type='application/json; charset=utf-8',
        json_dumps_params={'ensure_ascii': False}
    )


def bathroom(request):
    result = requests.get(
        'http://wap.xt.beescrm.com/activity/WaterControl/getGroupInfo/version/1'
    )
    return JsonResponse(
        result.json(),
        content_type='application/json; charset=utf-8',
        json_dumps_params={'ensure_ascii': False}
    )


def washing_machine(request, machine_id: str):
    if not (4 < len(machine_id) < 10 and machine_id.isalnum()):
        return JsonResponse({'error': 'invalid machine_id'}, status=HTTPStatus.BAD_REQUEST)
    machine_id = machine_id.upper()

    try:
        result = requests.get(
            f'https://www.weimaqi.net/Index_1.aspx?device_name={machine_id}&extra=',
            allow_redirects=False,
            timeout=5
        )
    except requests.exceptions.Timeout:
        return JsonResponse({'error': 'timeout'}, status=HTTPStatus.BAD_GATEWAY)

    if result.status_code != 302:
        return JsonResponse({'error': f'bad response: code {result.status_code}'}, status=HTTPStatus.BAD_GATEWAY)

    server_redir_url = result.headers['Location']
    if server_redir_url == f'https://www.weimaqi.net/qr1/index/index?device_name={machine_id}&extra=':
        return JsonResponse(
            {
                'error': 'success',
                'machine_id': machine_id,
                'vacant': True
            }
        )
    elif server_redir_url.startswith('/shebei/device_disable.aspx?did='):
        return JsonResponse(
            {
                'error': 'success',
                'machine_id': machine_id,
                'vacant': False
            }
        )
    elif server_redir_url == '/device_disable.html':
        return JsonResponse({'error': 'invalid machine_id', 'machine_id': machine_id}, status=HTTPStatus.BAD_REQUEST)
    elif server_redir_url == f'https://www.weimaqi.net/debug/iot_transfer.ashx?device_name={machine_id}':
        return JsonResponse({'error': 'invalid machine_id', 'machine_id': machine_id}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse({'error': f'bad response: [{server_redir_url}]'}, status=HTTPStatus.BAD_GATEWAY)


def lesson(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({'error': 'not logged in'}, status=HTTPStatus.UNAUTHORIZED)
    term = request.GET.get('term', '')

    # validate the parameter
    parsed_term = re.fullmatch(
        r'(\d{4})-(\d{4})-(\d{1})', term, flags=re.ASCII)
    if not parsed_term:
        return JsonResponse({'error': 'invalid term'}, status=HTTPStatus.BAD_REQUEST)
    y_start, y_end, s = (int(i) for i in parsed_term.groups())
    if y_end-y_start != 1 or s not in [1, 2, 3] or y_start < 2000 or y_end > 2100:
        return JsonResponse({'error': 'invalid term'}, status=HTTPStatus.BAD_REQUEST)

    resp = jaccount.get(
        f'/v1/me/lessons/{escape_uri_path(term)}', token=token, params={'classes': False})

    if resp.status_code == HTTPStatus.OK:
        return JsonResponse(
            {'entities': resp.json()['entities'], 'error': 'success'},
            content_type='application/json; charset=utf-8',
            json_dumps_params={'ensure_ascii': False}
        )  # trim and rebuild response
    else:
        if resp.json()['error'] == 'AUTHENTICATION_SCOPE_FAILED':
            return JsonResponse({
                'error': 'lessons scope missed'
            }, status=HTTPStatus.UNAUTHORIZED)
        else:
            return JsonResponse({
                'error': 'bad response from JAccount server'
            }, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def user_profile(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({
            'error': 'not logged in'
        }, status=HTTPStatus.UNAUTHORIZED)
    resp = jaccount.get('/v1/me/profile', token=token)
    if resp.status_code == HTTPStatus.OK:
        raw_profile = resp.json()['entities'][0]
        if 'code' not in raw_profile:  # 说明未曾对本应用赋予 essential 权限
            return JsonResponse({
                'error': 'essential scope missed'
            }, status=HTTPStatus.UNAUTHORIZED)
        else:
            request.session['scope'].append('essential')
        profile = {
            'name': raw_profile['name'],
            'account': raw_profile['account'],
            'code': raw_profile['code'],
            'department': raw_profile['organize']['name'],  # 学院/部门名
            'type': raw_profile['userType'],
            'type_name': jaccount_type_map.get(raw_profile['userType'], '未知')
        }

        if 'identities' in raw_profile:  # 目前已知集体账号没有 identities 属性
            identitys = [
                identity
                for identity in raw_profile.get('identities')
                if identity['isDefault']
            ]
            default_identiy = identitys[0]
            profile.update({
                'expire_date': default_identiy['expireDate'],  # 身份过期日期
                'status': default_identiy['status'],  # 身份状态
            })
        if profile['type'] == 'student':
            profile.update({
                'class_code': raw_profile['classNo']  # 班号，仅学生身份有该字段
            })
        return JsonResponse({
            'error': 'success',
            'profile': profile
        }, content_type='application/json; charset=utf-8', json_dumps_params={'ensure_ascii': False})
    else:
        return JsonResponse({
            'error': 'bad response from JAccount server'
        }, status=HTTPStatus.INTERNAL_SERVER_ERROR)


def user_info(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({
            'error': 'not logged in'
        }, status=HTTPStatus.UNAUTHORIZED)
    user = request.session.get('user')

    return JsonResponse({
        'info': {
            'code': user['code'],    # 学工号
            'account': user['sub'],  # jAccount 账号
            'name': user['name'],    # 姓名
            'type': user['type'],    # 身份
            'type_name': jaccount_type_map.get(user['type'], '未知')  # 身份名
        },
        'error': 'success'
    }, content_type='application/json; charset=utf-8', json_dumps_params={'ensure_ascii': False})

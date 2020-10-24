import json
import re
from http import HTTPStatus

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from verify.utils import attestation

qq_pattern = re.compile(r'[1-9]\d{4,}')


def index(request):
    if 'user' not in request.session:
        return redirect(reverse('login'))
    return render(request, 'verify/index.j2')


def generate(request):
    if 'user' not in request.session:
        return JsonResponse({'success': True, 'message': '请先登录'}, status=HTTPStatus.UNAUTHORIZED)

    qq = request.POST.get('qq_number', '')
    if qq_pattern.fullmatch(qq):
        try:
            token = attestation.generate(qq)
            return JsonResponse({'success': True, 'token': token})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({'success': False, 'message': '填写错误，请输入正确的QQ号'}, status=HTTPStatus.BAD_REQUEST)


def verify(request):
    payload = json.loads(request.body)

    qq = payload.get('qq_number')
    token = payload.get('token')

    if qq is None or token is None:
        return JsonResponse({
            "success": False,
            "message": "Compulsory parameters lost"
        }, status=HTTPStatus.BAD_REQUEST)

    if not qq_pattern.fullmatch(qq):
        return JsonResponse({
            "success": False,
            "message": "Invalid QQ number"
        }, status=HTTPStatus.BAD_REQUEST)

    try:
        timestamp = attestation.verify(qq, token)
        if timestamp is None:
            return JsonResponse({
                "success": False,
                "message": "Verification Failed"
            })
        else:
            return JsonResponse({
                "success": True,
                "message": timestamp.isoformat()
            })
    except (UnicodeEncodeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Invalid token"
        }, status=HTTPStatus.BAD_REQUEST)

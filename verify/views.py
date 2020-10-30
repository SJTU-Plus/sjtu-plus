from datetime import datetime, timedelta
import json
import re
from http import HTTPStatus
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import ensure_csrf_cookie

from SJTUPlus.settings import TOKEN_EXPIRE_TIME
from verify.models import ApiKey
from verify.utils import attestation

qq_pattern = re.compile(r'^[1-9]\d{4,}')


@ensure_csrf_cookie
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


@csrf_exempt
def verify(request):
    api_key = request.headers.get('api-key', '')
    try:
        ApiKey.objects.get(key=api_key, is_enabled=True)
    except ApiKey.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Invalid Api-Key"
        }, status=HTTPStatus.BAD_REQUEST)
    try:
        payload = json.loads(request.body)
    except JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "Invalid Request Body"
        }, status=HTTPStatus.BAD_REQUEST)

    qq = payload.get('qq_number', '')
    token = payload.get('token', '')

    if not qq_pattern.fullmatch(qq):
        return JsonResponse({
            "success": False,
            "message": "Invalid QQ Number"
        }, status=HTTPStatus.BAD_REQUEST)

    try:
        timestamp = attestation.verify(qq, token)
        if timestamp is None:
            return JsonResponse({
                "success": False,
                "message": "Verification Failed"
            })
        else:
            now = datetime.now()
            return JsonResponse({
                "success": timestamp <= now <= timestamp + timedelta(days=TOKEN_EXPIRE_TIME),
                "message": timestamp.isoformat()
            })
    except (UnicodeEncodeError, ValueError):
        return JsonResponse({
            "success": False,
            "message": "Invalid token"
        }, status=HTTPStatus.BAD_REQUEST)

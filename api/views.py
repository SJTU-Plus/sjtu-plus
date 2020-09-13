from django.http import JsonResponse, HttpResponse
from time import time
import requests
from django.utils.encoding import escape_uri_path

from SJTUPlus.oauth import jaccount


def canteen(request):
    result = requests.get("https://canteen.sjtu.edu.cn/CARD/Ajax/Place")
    return JsonResponse(result.json(), safe=False)


def canteen_detail(request, id):
    result = requests.get(
        f"https://canteen.sjtu.edu.cn/CARD/Ajax/PlaceDetails/{id}")
    return JsonResponse(result.json(), safe=False)


def library(request):
    result = requests.get(
        f"http://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson&_={time()}")
    strip = result.text[12:-2]
    return HttpResponse(strip, content_type="application/json")


def lesson(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({"error": "not logged in"})
    term = request.GET.get("term", "")
    resp = jaccount.get(
        f'/v1/me/lessons/{escape_uri_path(term)}?classes=false', token=token)
    return HttpResponse(resp.text, content_type="application/json")

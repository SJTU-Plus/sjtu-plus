from django.http import JsonResponse, HttpResponse
from time import time
import requests

# Create your views here.


def canteen(request):
    result = requests.get("https://canteen.sjtu.edu.cn/CARD/Ajax/Place")
    return JsonResponse(result.json(), safe=False)


def library(request):
    result = requests.get(
        f"http://zgrstj.lib.sjtu.edu.cn/cp?callback=CountPerson&_={time()}")
    strip = result.text[12:-2]
    return HttpResponse(strip, content_type="application/json")

from http import HTTPStatus

from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import Lesson, Schedule


def lessons_info(request):
    token = request.session.get('token')
    if token is None:
        return JsonResponse({"error": "not logged in"}, status=HTTPStatus.UNAUTHORIZED)
    code_list = request.GET.get("code_list", "")

    lessons = {}
    for lesson_code in code_list.split(','):
        try:
            lesson = Lesson.objects.select_related(
                'course').get(code=lesson_code)
        except ObjectDoesNotExist:
            lessons[lesson_code] = None
            continue

        schedule_result = list(
            Schedule.objects.select_related(  # LEFT OUTER JOIN 合并两次查询
                'position'
            ).filter(
                lesson=lesson
            ))
        lessons[lesson_code] = {
            'schedule': [{
                'weeks_b': schedule.weeks,  # 二进制的周数
                'day': schedule.day,        # 星期几(1-7)
                'time_b': schedule.time,    # 二进制的课时位置
                'position': schedule.position.name if schedule.position else None,  # 上课教室
            } for schedule in schedule_result],
            'code': lesson_code,  # 课号
            'name': lesson.course.name,  # 课程名
            'teachers': lesson.teachers  # 授课教师(全部)
        }
    return JsonResponse({
        'lessons': lessons,
        'error': 'success'
    })

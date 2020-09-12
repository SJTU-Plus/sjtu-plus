import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from tqdm import tqdm

from courses.models import Course, Lesson, Position, Schedule


def create_course(data: dict) -> dict:
    return {
        'code': data.get('kch'),  # "kch": "MT495",
        'name': data.get('kcmc'),  # "kcmc": "材料科学基础",
        'type': data.get('kklx'),  # "kklx": "一专",
        'property': data.get('kcxzmc', ''),  # "kcxzmc": "必修",
        'department': data.get('kkxy'),  # "kkxy": "巴黎高科卓越工程师学院",
        'credit': float(data.get('xf')),  # "xf": "2.0",
        'workload': int(data.get('rwzxs', 0)),  # "rwzxs": 32,
        'structure': data.get('zhxs'),  # "zhxs": "理论(2.0)",
    }


def create_lesson(data: dict, course: Course) -> dict:
    return {
        'code': data.get('jxbmc'),  # "jxbmc": "(2020-2021-1)-MT495-1",
        'year': data.get('xn'),  # "xn": "2020-2021",
        'term': data.get('xq'),  # "xq": "3",
        'course': course,
        'main_teacher': data.get('zjs', data.get('jszc').split(',')[0]),  # "zjs": "钟圣怡",
        'teachers': data.get('jszc'),  # "jszc": "钟圣怡,陈哲,Andras.BORBELY",
        'grade': data.get('nj'),  # "nj": "2017",
        'audience': data.get('jxbzc'),  # "jxbzc": "2017机械工程(中法合作办学)",
        'comment': data.get('xkbz', ''),  # "xkbz": "仅限巴黎高科学院工科一专选课",
        'capacity': int(data.get('jxbrs')),  # "jxbrs": 8,
        'registered_count': int(data.get('xkrs')),  # "xkrs": 7,
    }


def create_position(data: dict) -> dict:
    obj = {
        'code': data.get('cdbh'),  # "cdbh": "ZY106",
        'name': data.get('cdmc'),  # "cdmc": "中院106",
        'capacity': data.get('zws'),  # "zws": 40,
    }

    if data.get('cdlbmc'):
        obj['type'] = data.get('cdlbmc')  # "cdlbmc": "智慧教室",

    return obj


def create_schedule(data: dict, lesson: Lesson, position: Position) -> dict:
    obj = {
        'lesson': lesson,
        'weeks': data.get('zcd'),  # "zcd": 4,
        'day': data.get('xqj'),  # "xqj": 1,
        'time': data.get('jc'),  # "jc": 3,
    }

    if position:
        obj['position'] = position

    return obj


class Command(BaseCommand):
    help = 'Load lesson arrangement data downloaded from i.sjtu.edu.cn'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(str(args)))
        self.stdout.write(self.style.SUCCESS(str(options)))

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        file_path = Path(options.get('json_file', ''))

        if not file_path.exists():
            raise CommandError(f"{file_path.absolute()} does not exist")

        if not file_path.is_file():
            raise CommandError(f"{file_path.absolute()} is not a file")

        data = None
        try:
            data = json.loads(file_path.read_text(encoding='utf-8'))
        except Exception:
            raise CommandError(f"Fail to load json from {file_path.absolute()}")

        with transaction.atomic():
            for item in tqdm(data, file=self.stderr):
                try:
                    course, _ = Course.objects.update_or_create(
                        code=item.get('kch'),
                        defaults=create_course(item)
                    )
                    lesson, _ = Lesson.objects.update_or_create(
                        code=item.get('jxbmc'),
                        defaults=create_lesson(item, course)
                    )

                    if item.get('cdbh') is not None:
                        position, _ = Position.objects.update_or_create(
                            code=item.get('cdbh'),
                            defaults=create_position(item)
                        )
                    else:
                        position = None

                    Schedule.objects.create(**create_schedule(item, lesson, position))
                except IntegrityError as e:
                    self.stdout.write(self.style.ERROR(str(e)))
                    self.stdout.write(str(item))
                    raise

        self.stdout.write(self.style.SUCCESS(f'{file_path.absolute()} has been loaded to database successfully'))

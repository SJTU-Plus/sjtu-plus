from django.db import models


class Course(models.Model):
    code = models.CharField(verbose_name='课程代码', max_length=32, null=False, blank=False, primary_key=True)
    name = models.CharField(verbose_name='课程名称', max_length=255, null=False, blank=False)
    type = models.CharField(verbose_name='课程类型', max_length=64, null=False, blank=True)
    property = models.CharField(verbose_name='课程性质', max_length=64, null=False, blank=True)
    department = models.CharField(verbose_name='开课院系', max_length=64, null=True, blank=True)

    credit = models.FloatField(verbose_name='学分', null=False, blank=False, default=0)
    workload = models.PositiveSmallIntegerField(verbose_name='学时', null=False, blank=False, default=0)
    structure = models.CharField(verbose_name='学分组成', max_length=255, null=True, blank=True)


class Lesson(models.Model):
    code = models.CharField(verbose_name='教学班名称', max_length=32, null=False, blank=False, primary_key=True)
    year = models.CharField(verbose_name='学年', max_length=16, null=False, blank=False)
    term = models.CharField(verbose_name='学期', max_length=8, null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)

    main_teacher = models.CharField(verbose_name='主讲教师', max_length=32, null=False, blank=False)
    teachers = models.CharField(verbose_name='教师组成', max_length=255, null=False, blank=False)
    grade = models.CharField(verbose_name='课程所属年级', max_length=32, null=True)
    audience = models.TextField(verbose_name='教学班组成', null=True, blank=True)
    comment = models.TextField(verbose_name='选课备注', null=False, blank=True)

    capacity = models.PositiveIntegerField(verbose_name='选课名额', null=False, blank=False, default=0)
    registered_count = models.PositiveIntegerField(verbose_name='选课人数', null=False, blank=False, default=0)


class Position(models.Model):
    code = models.CharField(verbose_name='场地编码', max_length=32, null=False, blank=False, primary_key=True)
    name = models.CharField(verbose_name='场地名称', max_length=32, null=False, blank=False)
    type = models.CharField(verbose_name='场地类别', max_length=32, null=False, blank=False)
    capacity = models.PositiveSmallIntegerField(verbose_name='场地容量', null=True)


class Schedule(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=False)
    weeks = models.PositiveIntegerField(null=False, blank=False)
    day = models.PositiveSmallIntegerField(null=False, blank=False)
    time = models.PositiveIntegerField(null=False, blank=False)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)

# SJTUPlus


## How to startup

1. Install dependencies
   ```
   $ pip3 install -r requirements.txt
   ```
2. Create database
   ```
   $ python3 manage.py makemigrations
   $ python3 manage.py migrate
   ```
3. Create Superuser
   ```
   $ python3 manage.py createsuperuser
   ```
4. Load database backup 
   ```
   $ python3 manage.py loaddata /path/to/backup.json
   ```
5. Run the server
   ```
   # To run a debug server
   $ python3 manage.py runserver
   # To run a production server
   # This will collect the static resources to /static-files
   # You need another web server to host the static resources
   $ python3 manage.py collectstatics 
   $ gunicorn -c gunicorn.conf.py SJTUPlus.wsgi:application
   ```
6. Run the db watcher
   ```
   python3 manage.py watch groups
   ```

## 文档

### /api/sjtu/canteen

返回各食堂的总座位数、总就餐人数、总剩余座位数

### /api/sjtu/canteen/[canteen_id]

根据食堂的 `canteen_id` 返回该食堂各子区域的座位数、就餐人数、剩余座位数

### /api/sjtu/library

返回各图书馆的在馆人数与限流人数

### /api/sjtu/bathroom

返回各浴室的机位使用情况

### /api/sjtu/washing_machine/[machine_id]

返回机器编号为 `machine_id` 的洗衣机使用情况，仅对部分商户的机型有效

### /api/course/lesson?term=[term]

查询用户 `term` 学期的课程表，学期格式形如 `2021-2022-1`。用户需通过 `/login?scope=lessons` 完成 jAccount 登录并提供 **课程表查询** 授权。

### /api/course/lesson_info?code_list=[code_list]

查询教学班编号列表 `code_list` 中的教学班的信息，教学班编号以逗号隔开形如 `(2020-2021-1)-AB202-1,(2020-2021-1)-AB203-1`。学期的课程表，学期格式形如 `2021-2022-1`。用户需通过 `/login?scope=lessons` 完成 jAccount 登录并提供 **课程表查询** 授权，该数据非实时数据。

### /api/user/profile

查询当前用户的身份，信息包括姓名、jAccount账号、学工号、所属部门/学院、账号类型、账号类型名、班号（若有）、身份状态（若有）、身份过期日期（若有）。

### /api/user/info

查询当前用户的身份，信息包括姓名、jAccount账号、学工号、账号类型、账号类型名。

### /login?app=[app]&scope=[scope]&redirecturi=[redirecturi]

跳转到 jAccount 登录页。可选的 `app` 参数提供了一些预设的 `scope` 和 `redirecturi` 参数组合，这些组合可通过额外指定 `scope` 和 `redirecturi` 参数进行覆盖。所有参数忽略时，登录后将跳转到首页。

### /authorize?code=[code]&state=[state]

用户完成 jAccount 登录后，将携带 `code` 和 `state` 返回此处完成 OAuth 认证。

### /logout?app=[app]&redirecturi=[redirecturi]&state=[state]

退出本网站和 jAccount 的登录。可选的 `app` 参数提供了一些预设的 `redirecturi` 参数，可通过额外指定 `redirecturi` 参数进行覆盖。所有参数忽略时，登录后将跳转到首页。



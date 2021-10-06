import gzip
from base64 import urlsafe_b64decode, urlsafe_b64encode
from json import dumps, loads

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from SJTUPlus.settings import SECRET_KEY

key = urlsafe_b64encode(
    PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'',
        iterations=100000,
        backend=default_backend()
    ).derive(SECRET_KEY.encode('utf-8'))
)
fernet = Fernet(key)


def get_filtered_scope(scopes):
    scopes = [i.lower() for i in scopes]
    allowed_scopes = ['basic', 'openid', 'essential',
                      'lessons', 'classes', 'exams', 'scores']
    filtered_scopes = []
    for scope in allowed_scopes:
        if scope in scopes:
            filtered_scopes.append(scope)
    return filtered_scopes


def encode_state(state_obj):
    # 对象<--->json字符串<--->gzip压缩<--->Fernet加密（base64字符串）
    # 与函数 decode_state 搭配使用
    state_str = dumps(state_obj, ensure_ascii=False)
    state_str_compressed = gzip.compress(
        state_str.encode('utf8'), compresslevel=9)
    state_str_encrypted = fernet.encrypt(state_str_compressed).decode('ascii')
    return state_str_encrypted


def decode_state(state_str_encoded: str):
    # 对象<--->json字符串<--->gzip压缩<--->Fernet加密（base64字符串）
    # 与函数 encode_state 搭配使用
    state_str_compressed = fernet.decrypt(state_str_encoded.encode('ascii'))
    state_str = gzip.decompress(state_str_compressed).decode('utf8')
    state_obj = loads(state_str)
    return state_obj


jaccount_type_map = {
    'faculty': '教职工',
    'student': '学生',
    'yxy': '医学院教职工',
    'fs': '附属单位职工',
    'vip': 'vip',
    'postphd': '博士后',
    'external_teacher': '外聘教师',
    'summer': '暑期生',
    'team': '集体账号',
    'alumni': '校友',
    'green': '绿色通道',
    'outside': '合作交流'
}  # 定义摘自 http://developer.sjtu.edu.cn/wiki/APIs#Profile

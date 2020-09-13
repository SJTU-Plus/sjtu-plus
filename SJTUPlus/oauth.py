from authlib.integrations.django_client import OAuth
from SJTUPlus.settings import JACCOUNT_CLIENT_ID, JACCOUNT_CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name='jaccount',
    client_id=JACCOUNT_CLIENT_ID,
    client_secret=JACCOUNT_CLIENT_SECRET,
    access_token_url='https://jaccount.sjtu.edu.cn/oauth2/token',
    authorize_url='https://jaccount.sjtu.edu.cn/oauth2/authorize',
    api_base_url='https://api.sjtu.edu.cn/',
    client_kwargs={
        "scope": "openid",
        "token_endpoint_auth_method": "client_secret_basic",
        "token_placement": "header"
    }
)
jaccount = oauth.jaccount

# 在 authentication.py 或 permissions.py 文件中

from ninja.security import HttpBearer
from jose import jwt
from back.models import newuser  # 确保正确引用您的用户模型
from .config import JWT_SECRET_KEY  # 确保正确引用您的密钥
class IsTeacher(HttpBearer):
    def authenticate(self, request, token):
        # 解码 JWT 令牌以获取用户信息
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user = newuser.objects.filter(pk=user_id).first()
        if user and user.is_teacher:
            return user
        return None

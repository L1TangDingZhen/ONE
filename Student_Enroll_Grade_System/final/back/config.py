# config.py
import os
import secrets
import string

alphabet = string.ascii_letters + string.digits
secret_key = ''.join(secrets.choice(alphabet) for i in range(32))

# 如果环境变量中有 JWT_SECRET_KEY,就使用环境变量的值
# 否则,使用上面生成的随机字符串
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', secret_key)
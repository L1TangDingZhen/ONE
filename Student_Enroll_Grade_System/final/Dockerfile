# 使用Python官方镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=final.settings
ENV STATIC_ROOT=/app/static
ENV MEDIA_ROOT=/app/media

# 安装系统依赖 - 添加 pkg-config
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# 复制项目文件
COPY . /app/

# 创建需要的目录
RUN mkdir -p /app/data /app/media /app/static

# 创建临时设置文件来设置 STATIC_ROOT
RUN echo "from final.settings import *; STATIC_ROOT = '/app/static'" > /app/temp_settings.py
ENV DJANGO_SETTINGS_MODULE=temp_settings

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 恢复原始设置模块
ENV DJANGO_SETTINGS_MODULE=final.settings

# 暴露端口
EXPOSE 8000

# 启动命令 - 使用gunicorn替代runserver
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "final.wsgi:application"]





# # 使用Python官方镜像作为基础镜像
# FROM python:3.10-slim

# # 设置工作目录
# WORKDIR /app

# # 设置环境变量
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV DJANGO_SETTINGS_MODULE=final.settings

# # 安装系统依赖 - 添加 pkg-config
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     default-libmysqlclient-dev \
#     pkg-config \
#     && apt-get clean \
#     && rm -rf /var/lib/apt/lists/*

# # 安装Python依赖
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir gunicorn

# # 复制项目文件
# COPY . /app/

# # 创建需要的目录
# RUN mkdir -p /app/data /app/media /app/static

# # 暴露端口
# EXPOSE 8000

# # 启动命令 - 使用gunicorn替代runserver
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "final.wsgi:application"]

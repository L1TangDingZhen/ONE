# P2P 应用云服务器部署指南

本文档说明如何在云服务器(EC2)上部署P2P应用。

## 准备工作

1. 确保服务器已安装 Docker 和 Docker Compose
2. 构建前端和后端镜像

### 前端构建

可以在本地构建前端，然后将静态文件上传到服务器:

```bash
# 在本地开发环境
cd p2p-client
npm install
npm run build
# 将build目录下的文件打包
tar -czvf p2p-frontend-static.tar.gz -C build .
```

### 后端构建

使用Dockerfile构建后端镜像:

```bash
# 在服务器上
cd P2P/P2P
docker build -t p2p-backend:latest .
```

## 部署步骤

1. 创建静态文件目录

```bash
mkdir -p /var/www/p2p
```

2. 解压前端静态文件

```bash
tar -xzvf p2p-frontend-static.tar.gz -C /var/www/p2p
```

3. 启动容器

```bash
docker-compose up -d
```

## 验证部署

部署完成后，可以通过以下URL访问应用:

- 前端: http://你的服务器IP/
- 或通过: http://你的服务器IP/p2p/
- API: http://你的服务器IP/api/p2p/...
- SignalR Hub: http://你的服务器IP/p2phub/

## 日志和调试

查看容器日志:

```bash
# 查看后端日志
docker logs p2p-backend

# 查看nginx日志
docker logs nginx-gateway
```

## 注意事项

1. 前端代码中已配置使用相对路径，无需额外配置API URL
2. WebSocket连接由nginx正确代理到后端
3. 所有API请求都通过/api/p2p/路径转发到后端

## 对前端静态文件的修改

如果需要修改前端对后端API的访问配置，可以编辑SignalRService.js和AuthService.js文件，更新API URL配置。

## 常见问题解决

1. **服务无法访问**: 检查Docker容器是否正常运行 `docker ps`
2. **API返回404**: 检查nginx配置是否正确转发请求
3. **WebSocket连接失败**: 确认nginx配置中正确设置了WebSocket代理头
4. **CORS错误**: 检查nginx添加的CORS头是否正确
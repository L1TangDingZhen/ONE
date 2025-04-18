#!/bin/bash
# 调试脚本 - 检查P2P后端可访问性

echo "====================================="
echo "P2P Backend Connectivity Test Script"
echo "====================================="

echo -e "\nChecking if p2p-backend container is running:"
docker ps | grep p2p-backend

echo -e "\nChecking p2p-backend container logs (last 20 lines):"
docker logs p2p-backend --tail 20

echo -e "\nTesting internal API connectivity from nginx container:"
docker exec -it nginx-gateway curl -v http://p2p-backend:5000/api/connectionstatus/health

echo -e "\nChecking if SignalR Hub is accessible from nginx container:"
docker exec -it nginx-gateway curl -v http://p2p-backend:5000/p2phub/negotiate

echo -e "\nTesting API route from external network:"
curl -v http://localhost/api/connectionstatus/health

echo -e "\nChecking nginx configuration:"
docker exec -it nginx-gateway nginx -T | grep -A 20 "location /api/"

echo -e "\nChecking container networking:"
docker network inspect $(docker network ls | grep all_default | awk '{print $1}')

echo -e "\nChecking nginx error logs:"
docker exec -it nginx-gateway tail -n 30 /var/log/nginx/error.log

echo -e "\n====================================="
echo "Debug information collected. If issues persist:"
echo "1. Check the ASPNETCORE_URLS setting in docker-compose.yml"
echo "2. Verify that Program.cs in the backend allows all origins"
echo "3. Ensure that the API endpoints are correctly exposed"
echo "====================================="
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# 直接复制当前目录的内容
COPY *.csproj ./
RUN dotnet restore

# 复制所有源代码
COPY . ./
RUN dotnet build "P2P.csproj" -c Release -o /app/build

# 发布
FROM build AS publish
RUN dotnet publish "P2P.csproj" -c Release -o /app/publish /p:UseAppHost=false

# 最终镜像
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000
ENTRYPOINT ["dotnet", "P2P.dll"]
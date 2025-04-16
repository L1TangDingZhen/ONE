FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src

# 复制csproj文件并恢复依赖
COPY ["P2P/*.csproj", "P2P/"]
RUN dotnet restore "P2P/P2P.csproj"

# 复制源代码并构建
COPY P2P/ P2P/
WORKDIR "/src/P2P"
RUN dotnet build "P2P.csproj" -c Release -o /app/build

# 发布
FROM build AS publish
RUN dotnet publish "P2P.csproj" -c Release -o /app/publish /p:UseAppHost=false

# 最终镜像
FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
EXPOSE 5000
ENV ASPNETCORE_URLS=http://+:5000
ENTRYPOINT ["dotnet", "P2P.dll"]
# 街舞信息共享平台

基于 `Django + SQLite + React + Vite` 的街舞信息共享平台原型，覆盖活动、视频、社交、商城和个人中心五个核心模块，适合课程设计或毕业设计演示。

## 技术栈

- 后端：Python 3.12、Django 6、SQLite
- 前端：React 19、Vite、React Router
- 依赖：Pillow

## 当前功能

- 用户：注册、登录、退出、个人信息维护、关注、收藏、个人中心汇总
- 活动：活动列表、发布活动、报名、签到、收藏、我的发布、我的报名
- 视频：视频列表、详情、发布、点赞、收藏、评论、我的视频
- 社交：默认聊天室初始化、房间列表、房间详情、发消息
- 商城：商品列表、创建商品、加入购物车、创建订单、模拟支付、订单记录
- 前端：首页、登录页、活动页、视频页、社交页、商城页、个人中心页

## 目录结构

```text
config/       Django 项目配置
users/        用户、关注、收藏、个人中心
activities/   活动与报名
videos/       视频与评论
social/       聊天室与消息
mall/         商品、购物车、订单
frontend/     React 前端
```

## 后端启动

1. 安装依赖

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

2. 执行迁移

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

3. 灌入演示数据

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo_data
```

4. 启动 Django

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

后端默认地址：`http://127.0.0.1:8000`

## 前端启动

1. 进入前端目录并安装依赖

```powershell
cd frontend
npm install
```

2. 启动开发服务器

```powershell
npm run dev
```

前端默认地址：`http://127.0.0.1:5173`

`vite.config.js` 已配置代理，开发模式下 `/users`、`/activities`、`/videos`、`/social`、`/mall` 会自动转发到 Django。

## 快速启动脚本

前后端一键启动：

```powershell
.\start_all.ps1
```

该脚本会分别打开两个 PowerShell 窗口：

- 后端窗口：执行 `migrate`、`seed_demo_data`、`runserver`
- 前端窗口：进入 `frontend` 并执行 `npm run dev`

后端一键启动：

```powershell
.\start_backend.ps1
```

前端一键启动：

```powershell
.\start_frontend.ps1
```

后端脚本会依次执行：

- `migrate`
- `seed_demo_data`
- `runserver`

## 接口文档

完整接口说明见：

- [API文档.md](/C:/Coding/260320_street-dance-system/API文档.md)

## 测试与构建

后端检查：

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

前端构建：

```powershell
cd frontend
npm run build
```

## 演示账号

运行 `seed_demo_data` 后可使用以下账号：

- 管理员：`admin_demo / Admin123456`
- 用户：`bboy_chen / Dance123456`
- 用户：`studio_muse / Dance123456`
- 用户：`jazz_luna / Dance123456`

## 演示建议流程

1. 使用 `bboy_chen` 或 `jazz_luna` 登录前端。
2. 在首页查看聊天室、视频和商品概览。
3. 在活动页查看活动、报名并收藏活动。
4. 在视频页查看作品、点赞、评论、收藏。
5. 在社交页进入房间发送消息。
6. 在商城页加入购物车、创建订单并模拟支付。
7. 在个人中心查看 dashboard、收藏、关注和最近记录。

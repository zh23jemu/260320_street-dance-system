# 基于 JavaScript 的街舞信息共享平台开发与 API 文档

## 1. 项目概述

### 1.1 项目背景
街舞文化近年来发展迅速，赛事、商演、培训、交流等活动日益增多，但相关信息长期分散在社交媒体、微信群、公众号及线下社群中，存在获取成本高、传播效率低、资源匹配困难等问题。为解决街舞领域信息碎片化和服务割裂的问题，本项目拟设计并实现一个街舞信息共享平台。

本平台定位为面向街舞爱好者、舞者、活动主办方及相关商家的垂直信息平台，提供活动发布与报名、视频分享、社区交流、商品购买及个人信息管理等功能，形成较完整的线上服务闭环。

### 1.2 项目目标
- 为舞者和爱好者提供统一的信息获取与交流入口。
- 为活动主办方提供活动发布、招募和报名管理能力。
- 为用户提供视频展示、互动和社交讨论空间。
- 为街舞周边商品提供展示与购买渠道。
- 构建一个功能完整、结构清晰、便于扩展的 Web 平台原型。

### 1.3 用户对象
- 普通用户：浏览活动、观看视频、参与聊天、购买商品。
- 舞者用户：发布视频、参与活动、分享经验。
- 活动主办方：发布比赛、商演、表演、伴舞等活动并管理报名。
- 商城管理方：维护商品信息与订单状态。

## 2. 技术栈说明

### 2.1 总体技术路线
- 前端：JavaScript、HTML5、CSS3、React、Vite
- 后端：Python、Django
- 数据库：SQLite

### 2.2 技术选型说明

#### 前端
- 使用 `JavaScript` 实现页面交互逻辑。
- 使用 `HTML5` 构建页面结构，实现响应式网页基础能力。
- 使用 `CSS3` 完成页面布局、美化与适配。
- 使用 `React + Vite` 组织前端页面模块，提高开发效率与可维护性。

#### 后端
- 使用 `Python` 处理业务逻辑。
- 使用 `Django` 作为后端开发框架，负责用户管理、接口处理、数据模型设计、后台管理和业务流程实现。

选择 Django 的原因：
- 框架成熟，适合快速搭建中小型 Web 系统。
- 自带 ORM，便于与数据库交互。
- 自带后台管理能力，适合毕设项目开发与演示。
- 结构规范，便于后期维护和扩展。

#### 数据库
- 使用 `SQLite` 作为系统数据库。

选择 SQLite 的原因：
- 轻量级，部署简单，无需单独安装数据库服务。
- 与 Django 默认兼容，开发成本低。
- 适用于毕业设计和课程设计阶段的原型开发与功能验证。
- 对本系统当前规模下的用户、活动、视频、订单等结构化数据存储需求能够满足。

### 2.3 不采用 Redis 的说明
本系统当前阶段不引入 `Redis`。

原因如下：
- `需求.txt` 中未对缓存系统、消息中间件或分布式组件提出明确要求。
- 当前项目以毕业设计原型实现为主，重点是完成业务功能闭环，而非高并发优化。
- 使用 `Django + SQLite` 已能够支撑活动管理、视频展示、商城订单、个人中心等核心业务。
- 引入 Redis 会增加部署和维护复杂度，不符合当前项目轻量实现的目标。

补充说明：若后续系统扩展到更高并发场景，或需要优化聊天室实时性、热门数据缓存、登录态管理等能力，可再考虑引入 Redis。

## 3. 系统功能需求

### 3.1 活动模块
- 用户发布活动信息
- 活动类型支持比赛、商演、表演、伴舞等
- 用户在线报名活动
- 支持活动定位与附近活动查看
- 支持活动签到与打卡
- 活动列表支持搜索与筛选

### 3.2 视频模块
- 用户上传跳舞视频
- 视频列表展示
- 个人主页展示个人视频内容
- 支持点赞、评论、收藏、关注

### 3.3 社交模块
聊天室分类包括：
- 舞房招聘
- 舞蹈心得交流
- 比赛经验
- Hiphop
- Swag
- Jazz
- Popping
- Locking
- Breaking
- 其他舞蹈分类

主要功能包括：
- 用户进入分类聊天室
- 用户在房间内发送消息
- 按话题进行交流互动

### 3.4 商城模块
- 商品展示
- 加入购物车
- 下单购买
- 支付功能
- 订单管理

说明：考虑到毕业设计项目实现难度，支付功能采用模拟支付流程完成演示。

### 3.5 我的模块
- 个人信息展示
- 我发布的活动
- 我报名的活动
- 我发布的视频
- 我的收藏与关注
- 我的订单记录

## 4. 非功能需求

### 4.1 易用性
- 界面布局清晰，操作流程简洁。
- 页面功能分类明确，降低用户学习成本。

### 4.2 响应式设计
- 页面兼容桌面端和移动端访问。
- 保证主要功能在不同分辨率下均可正常使用。

### 4.3 可维护性
- 前后端模块划分清晰。
- 后端代码按照 Django 应用进行组织，便于后续扩展。
- 数据模型与业务逻辑相对独立，降低维护成本。

### 4.4 安全性
- 用户登录信息需进行安全校验。
- 重要操作应具备权限控制。
- 上传内容应进行基础格式校验。

### 4.5 可扩展性
- 后续可扩展推荐系统、消息通知、第三方地图服务、对象存储等能力。
- 数据库模型设计为后期扩展预留空间。

## 5. 系统架构设计

### 5.1 架构模式
本系统采用前后端分离的 Web 架构：
- 前端负责页面展示、交互逻辑和请求发送。
- 后端负责业务逻辑处理、数据管理和接口返回。
- 数据库负责平台结构化数据的存储与查询。

### 5.2 架构组成

#### 表现层
- 用户登录注册页面
- 活动展示与报名页面
- 视频展示与互动页面
- 聊天室页面
- 商城页面
- 个人中心页面

#### 业务逻辑层
- 用户身份认证
- 活动发布与报名逻辑
- 视频信息管理
- 聊天内容管理
- 商品、购物车和订单处理
- 收藏、关注、评论等交互逻辑

#### 数据存储层
- 用户数据存储
- 活动与报名数据存储
- 视频与评论数据存储
- 聊天室与消息记录存储
- 商品、购物车和订单数据存储

## 6. 数据库设计

### 6.1 数据库选型
本系统数据库采用 `SQLite`。

### 6.2 核心实体
- 用户
- 活动
- 活动报名
- 视频
- 视频评论
- 聊天室
- 聊天消息
- 商品
- 购物车
- 订单
- 订单明细
- 收藏
- 关注

### 6.3 主要数据表设计

#### 用户表
- id
- username
- password
- nickname
- avatar
- gender
- phone
- email
- profile
- create_time

#### 活动表
- id
- title
- activity_type
- cover_image
- content
- organizer_id
- location
- latitude
- longitude
- start_time
- end_time
- signup_deadline
- status
- create_time

#### 活动报名表
- id
- user_id
- activity_id
- signup_time
- checkin_status

#### 视频表
- id
- user_id
- title
- video_url
- cover_image
- description
- like_count
- favorite_count
- comment_count
- create_time

#### 视频评论表
- id
- video_id
- user_id
- content
- create_time

#### 聊天室表
- id
- room_name
- category
- description
- create_time

#### 聊天消息表
- id
- room_id
- user_id
- content
- send_time

#### 商品表
- id
- name
- category
- cover_image
- price
- stock
- description
- status

#### 购物车表
- id
- user_id
- product_id
- quantity
- create_time

#### 订单表
- id
- user_id
- total_amount
- order_status
- payment_status
- create_time

#### 订单明细表
- id
- order_id
- product_id
- quantity
- unit_price

#### 收藏表
- id
- user_id
- target_id
- target_type
- create_time

#### 关注表
- id
- follower_id
- following_id
- create_time

## 7. 接口说明

### 7.1 接口通用说明

基地址（开发环境）：

- 后端：`http://127.0.0.1:8000`
- 前端开发代理：`http://127.0.0.1:5173`

说明：
- 当前接口主要返回 `JSON`
- 认证方式为 Django Session
- 需要登录的接口在未登录时返回 `401`
- 请求体默认使用 `application/json`

### 7.2 用户模块 `/users`

#### `POST /users/register/`
用途：注册并自动登录

请求示例：

```json
{
  "username": "dancer01",
  "password": "StrongPass123",
  "confirm_password": "StrongPass123",
  "nickname": "Bboy One"
}
```

#### `POST /users/login/`
用途：登录

请求示例：

```json
{
  "username": "bboy_chen",
  "password": "Dance123456"
}
```

#### `POST /users/logout/`
用途：退出登录

#### `GET /users/me/`
用途：获取当前登录用户信息

#### `PATCH /users/me/`
用途：修改个人资料

请求示例：

```json
{
  "nickname": "Locker",
  "phone": "13800138000",
  "profile": "擅长 locking"
}
```

#### `GET /users/dashboard/`
用途：获取个人中心统计和最近数据

返回包含：
- `counts.published_activities`
- `counts.registered_activities`
- `counts.videos`
- `counts.favorites`
- `counts.following`
- `counts.followers`
- `counts.orders`
- `latest.published_activities`
- `latest.registered_activities`
- `latest.videos`
- `latest.orders`

#### `GET /users/favorites/`
用途：获取当前用户收藏列表

#### `GET /users/followers/`
用途：获取粉丝列表

#### `GET /users/following/`
用途：获取关注列表

#### `POST /users/<user_id>/follow/`
用途：关注指定用户

### 7.3 活动模块 `/activities`

#### `GET /activities/list/`
用途：获取活动列表

支持查询参数：
- `keyword`
- `activity_type`
- `status`

#### `POST /activities/list/`
用途：发布活动

请求示例：

```json
{
  "title": "Freestyle Jam",
  "activity_type": "competition",
  "content": "开放报名",
  "location": "上海市黄浦区",
  "start_time": "2026-03-30T19:00:00+08:00",
  "end_time": "2026-03-30T21:00:00+08:00",
  "signup_deadline": "2026-03-28T18:00:00+08:00"
}
```

#### `GET /activities/<activity_id>/`
用途：获取活动详情

#### `POST /activities/<activity_id>/register/`
用途：报名活动

#### `POST /activities/<activity_id>/checkin/`
用途：活动签到

#### `POST /activities/<activity_id>/favorite/`
用途：收藏活动

#### `GET /activities/my/published/`
用途：获取我发布的活动

#### `GET /activities/my/registered/`
用途：获取我报名的活动

### 7.4 视频模块 `/videos`

#### `GET /videos/list/`
用途：获取视频列表

支持查询参数：
- `keyword`

#### `POST /videos/list/`
用途：发布视频

请求示例：

```json
{
  "title": "Battle Clip",
  "video_file": "videos/battle.mp4",
  "description": "比赛片段"
}
```

#### `GET /videos/<video_id>/`
用途：获取视频详情和评论

#### `POST /videos/<video_id>/like/`
用途：点赞视频

#### `POST /videos/<video_id>/favorite/`
用途：收藏视频

#### `POST /videos/<video_id>/comments/`
用途：发表评论

请求示例：

```json
{
  "content": "这段节奏处理很稳"
}
```

#### `GET /videos/my/`
用途：获取我的视频

### 7.5 社交模块 `/social`

#### `GET /social/rooms/`
用途：获取聊天室列表

说明：首次访问时会自动初始化默认聊天室分类

#### `GET /social/rooms/<room_id>/`
用途：获取房间详情和历史消息

#### `POST /social/rooms/<room_id>/messages/`
用途：发送消息

请求示例：

```json
{
  "content": "这周末有人一起约练吗？"
}
```

### 7.6 商城模块 `/mall`

#### `GET /mall/products/`
用途：获取商品列表

支持查询参数：
- `keyword`

#### `POST /mall/products/`
用途：创建商品

请求示例：

```json
{
  "name": "街舞卫衣",
  "category": "服装",
  "price": 199,
  "stock": 20,
  "description": "宽松版型"
}
```

#### `GET /mall/products/<product_id>/`
用途：获取商品详情

#### `GET /mall/cart/`
用途：获取当前用户购物车

#### `POST /mall/cart/`
用途：加入购物车

请求示例：

```json
{
  "product_id": 1,
  "quantity": 2
}
```

#### `POST /mall/orders/create/`
用途：根据购物车创建订单

#### `GET /mall/orders/`
用途：获取我的订单列表

#### `POST /mall/orders/<order_id>/pay/`
用途：模拟支付订单

### 7.7 基础检查接口

#### `GET /`
用途：健康检查

返回示例：

```json
{
  "status": "ok",
  "project": "street-dance-system"
}
```

## 8. 关键业务流程

### 8.1 用户注册登录流程
- 用户填写注册信息
- 系统校验信息合法性
- 注册成功后可登录系统
- 登录后访问个人中心及其他需要身份认证的功能

### 8.2 活动报名流程
- 主办方发布活动
- 用户浏览活动列表或搜索活动
- 用户查看活动详情后提交报名
- 系统保存报名记录
- 用户到场后可进行签到或打卡

### 8.3 视频发布与互动流程
- 用户上传视频及描述信息
- 系统保存视频记录并展示在视频列表中
- 其他用户可点赞、评论、收藏和关注发布者

### 8.4 商城下单流程
- 用户浏览商品
- 用户将商品加入购物车
- 用户创建订单
- 系统更新订单状态
- 用户在个人中心查看订单记录

### 8.5 聊天交流流程
- 用户进入指定分类聊天室
- 用户发送文字消息
- 系统保存消息记录并展示聊天内容

## 9. 开发进度计划

### 第一阶段：需求分析与资料整理
- 阅读任务书与相关文献
- 明确系统功能模块
- 确定开发环境与技术路线

### 第二阶段：系统设计
- 绘制系统功能结构图
- 完成页面原型设计
- 完成数据库设计与模块划分

### 第三阶段：系统实现
- 完成用户模块开发
- 完成活动模块开发
- 完成视频模块开发
- 完成社交模块开发
- 完成商城模块开发
- 完成个人中心模块开发

### 第四阶段：系统测试与优化
- 进行功能测试
- 修复主要问题
- 优化页面交互与流程体验

### 第五阶段：论文与答辩材料整理
- 整理系统设计文档
- 编写论文实现部分
- 准备演示与答辩材料

## 10. 测试方案

### 10.1 功能测试
- 测试用户注册、登录、退出是否正常
- 测试活动发布、报名、签到是否正常
- 测试视频上传、点赞、评论、收藏是否正常
- 测试聊天室发送消息是否正常
- 测试商品下单、订单查看是否正常
- 测试个人中心信息展示是否正常

### 10.2 界面测试
- 测试页面布局是否合理
- 测试移动端和桌面端页面显示是否正常
- 测试按钮、表单和导航交互是否正常

### 10.3 异常测试
- 未登录访问受限功能时应提示登录
- 表单信息不完整时应提示用户补充
- 上传非规定格式文件时应提示错误
- 库存不足或订单异常时应提示失败原因

## 11. 项目风险与应对措施

### 11.1 视频上传与展示复杂度较高
应对措施：
- 初期优先实现基础上传与展示功能
- 暂不实现复杂转码与推荐算法

### 11.2 聊天模块实时性实现难度较高
应对措施：
- 初期可先实现基础聊天记录存储与展示
- 后续再扩展更完整的实时通信方案

### 11.3 商城支付接入复杂
应对措施：
- 本项目采用模拟支付，重点完成订单流程演示

### 11.4 SQLite 并发能力有限
应对措施：
- 当前系统定位为毕业设计原型，采用 SQLite 满足开发和演示需要
- 若后续需要部署更大规模系统，可迁移至 MySQL 等关系型数据库

## 12. 总结
本项目围绕街舞文化场景，设计并实现一个集活动发布与报名、视频展示与互动、分类聊天室、商品购买和个人中心管理于一体的信息共享平台。系统在技术上采用前端 JavaScript 技术与后端 Django 框架结合的方式，并使用 SQLite 作为数据库，以满足毕业设计阶段对功能完整性、开发效率和部署简便性的要求。

在当前方案下，系统能够较好地体现街舞垂直平台的信息整合价值，也为后续功能扩展和性能优化预留了空间。

## 13. 演示账号说明

为便于系统测试与毕业设计答辩演示，项目提供以下默认演示账号：

- 管理员账号：`admin_demo / Admin123456`
- 普通用户账号：`bboy_chen / Dance123456`
- 普通用户账号：`studio_muse / Dance123456`
- 普通用户账号：`jazz_luna / Dance123456`

上述账号可通过执行项目演示数据初始化命令自动生成：

```powershell
.\.venv\Scripts\python.exe manage.py seed_demo_data
```

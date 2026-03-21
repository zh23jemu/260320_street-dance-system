# 街舞信息共享平台接口文档

基地址（开发环境）：

- 后端：`http://127.0.0.1:8000`
- 前端开发代理：`http://127.0.0.1:5173`

说明：

- 当前接口主要返回 `JSON`
- 认证方式为 Django Session
- 需要登录的接口在未登录时返回 `401`
- 请求体默认使用 `application/json`

## 1. 用户模块 `/users`

### `POST /users/register/`

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

### `POST /users/login/`

用途：登录

请求示例：

```json
{
  "username": "bboy_chen",
  "password": "Dance123456"
}
```

### `POST /users/logout/`

用途：退出登录

### `GET /users/me/`

用途：获取当前登录用户信息

### `PATCH /users/me/`

用途：修改个人资料

请求示例：

```json
{
  "nickname": "Locker",
  "phone": "13800138000",
  "profile": "擅长 locking"
}
```

### `GET /users/dashboard/`

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

### `GET /users/favorites/`

用途：获取当前用户收藏列表

### `GET /users/followers/`

用途：获取粉丝列表

### `GET /users/following/`

用途：获取关注列表

### `POST /users/<user_id>/follow/`

用途：关注指定用户

## 2. 活动模块 `/activities`

### `GET /activities/list/`

用途：获取活动列表

支持查询参数：

- `keyword`
- `activity_type`
- `status`

### `POST /activities/list/`

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

### `GET /activities/<activity_id>/`

用途：获取活动详情

### `POST /activities/<activity_id>/register/`

用途：报名活动

### `POST /activities/<activity_id>/checkin/`

用途：活动签到

### `POST /activities/<activity_id>/favorite/`

用途：收藏活动

### `GET /activities/my/published/`

用途：获取我发布的活动

### `GET /activities/my/registered/`

用途：获取我报名的活动

## 3. 视频模块 `/videos`

### `GET /videos/list/`

用途：获取视频列表

支持查询参数：

- `keyword`

### `POST /videos/list/`

用途：发布视频

请求示例：

```json
{
  "title": "Battle Clip",
  "video_file": "videos/battle.mp4",
  "description": "比赛片段"
}
```

### `GET /videos/<video_id>/`

用途：获取视频详情和评论

### `POST /videos/<video_id>/like/`

用途：点赞视频

### `POST /videos/<video_id>/favorite/`

用途：收藏视频

### `POST /videos/<video_id>/comments/`

用途：发表评论

请求示例：

```json
{
  "content": "这段节奏处理很稳"
}
```

### `GET /videos/my/`

用途：获取我的视频

## 4. 社交模块 `/social`

### `GET /social/rooms/`

用途：获取聊天室列表

说明：首次访问时会自动初始化默认聊天室分类

### `GET /social/rooms/<room_id>/`

用途：获取房间详情和历史消息

### `POST /social/rooms/<room_id>/messages/`

用途：发送消息

请求示例：

```json
{
  "content": "这周末有人一起约练吗？"
}
```

## 5. 商城模块 `/mall`

### `GET /mall/products/`

用途：获取商品列表

支持查询参数：

- `keyword`

### `POST /mall/products/`

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

### `GET /mall/products/<product_id>/`

用途：获取商品详情

### `GET /mall/cart/`

用途：获取当前用户购物车

### `POST /mall/cart/`

用途：加入购物车

请求示例：

```json
{
  "product_id": 1,
  "quantity": 2
}
```

### `POST /mall/orders/create/`

用途：根据购物车创建订单

### `GET /mall/orders/`

用途：获取我的订单列表

### `POST /mall/orders/<order_id>/pay/`

用途：模拟支付订单

## 6. 基础检查接口

### `GET /`

用途：健康检查

返回示例：

```json
{
  "status": "ok",
  "project": "street-dance-system"
}
```

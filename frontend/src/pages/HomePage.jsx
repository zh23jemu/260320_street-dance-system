import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

function HomePage({ currentUser }) {
  const [rooms, setRooms] = useState([])
  const [videos, setVideos] = useState([])
  const [products, setProducts] = useState([])

  useEffect(() => {
    async function loadHome() {
      const [roomData, videoData, productData] = await Promise.all([
        apiFetch('/social/rooms/'),
        apiFetch('/videos/list/'),
        apiFetch('/mall/products/'),
      ])
      setRooms(roomData.items.slice(0, 4))
      setVideos(videoData.items.slice(0, 3))
      setProducts(productData.items.slice(0, 3))
    }

    loadHome().catch(() => {})
  }, [])

  return (
    <div className="page-grid">
      <section className="hero-card">
        <p className="eyebrow">One Stop Street Dance Hub</p>
        <h2>活动、作品、社群和装备，在同一块地板上完成连接。</h2>
        <p>
          这是一个面向街舞用户的垂直平台原型。你可以发布活动、展示视频、进入聊天室交流，也可以在个人中心回看自己的报名、收藏和订单记录。
        </p>
        <div className="hero-tags">
          <span>活动报名</span>
          <span>视频分享</span>
          <span>聊天室</span>
          <span>个人中心</span>
        </div>
      </section>

      <section className="panel-row">
        <article className="panel-card accent-panel">
          <span className="panel-title">平台节奏</span>
          <strong>{currentUser ? '你已进入系统，可以直接发布活动或查看我的模块。' : '先登录，再开始发布作品和报名活动。'}</strong>
        </article>
        <article className="panel-card">
          <span className="panel-title">聊天室分类</span>
          {rooms.map((room) => (
            <div key={room.id} className="mini-row">
              <strong>{room.room_name}</strong>
              <span>{room.category}</span>
            </div>
          ))}
        </article>
      </section>

      <section className="triple-grid">
        <article className="panel-card">
          <span className="panel-title">最新视频</span>
          {videos.map((video) => (
            <div key={video.id} className="stack-item">
              <strong>{video.title}</strong>
              <span>{video.user.nickname || video.user.username}</span>
              <small>{video.description || '暂无描述'}</small>
            </div>
          ))}
        </article>

        <article className="panel-card">
          <span className="panel-title">商城商品</span>
          {products.map((product) => (
            <div key={product.id} className="stack-item">
              <strong>{product.name}</strong>
              <span>{product.category}</span>
              <small>¥ {product.price}</small>
            </div>
          ))}
        </article>

        <article className="panel-card spotlight-panel">
          <span className="panel-title">开发状态</span>
          <div className="stack-item"><strong>后端</strong><small>Django + SQLite 已打通</small></div>
          <div className="stack-item"><strong>前端</strong><small>React + Vite 正在接入</small></div>
          <div className="stack-item"><strong>当前重点</strong><small>登录、活动、个人中心</small></div>
        </article>
      </section>
    </div>
  )
}

export default HomePage

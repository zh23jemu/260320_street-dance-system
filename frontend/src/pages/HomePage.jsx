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
        <p className="eyebrow">首页概览</p>
        <h2>把活动信息、作品展示、社群交流和商城功能放到一个清晰的入口里。</h2>
        <p>
          这是一个面向街舞用户的课程设计原型。用户可以查看近期内容、进入不同功能模块，也可以在个人中心统一回看自己的发布、报名、收藏和订单记录。
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
          <span className="panel-title">当前入口</span>
          <strong>{currentUser ? '你已登录，可以直接进入活动、视频、社交、商城和个人中心。' : '当前可先浏览公开内容，登录后再进行发布、评论和下单。'}</strong>
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
          <span className="panel-title">当前进展</span>
          <div className="stack-item"><strong>后端接口</strong><small>活动、视频、社交、商城与用户中心已联通</small></div>
          <div className="stack-item"><strong>前端页面</strong><small>主要页面已经接入，当前重点是继续优化界面细节</small></div>
          <div className="stack-item"><strong>演示状态</strong><small>已具备课程设计与毕业设计展示基础</small></div>
        </article>
      </section>
    </div>
  )
}

export default HomePage

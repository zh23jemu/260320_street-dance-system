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
          欢迎来到街舞信息共享平台。这里可以先浏览比赛活动、视频作品、社交房间和商城商品；只有报名、购买、评论这类需要个人信息的操作时，才需要登录。登录后也可以在个人中心统一回看自己的发布、报名、收藏和订单记录。
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
          <span className="panel-title">平台服务</span>
          <div className="stack-item"><strong>找活动</strong><small>查看比赛、商演、公开课和其他街舞相关活动信息。</small></div>
          <div className="stack-item"><strong>看作品</strong><small>浏览街舞视频作品，了解不同舞种和风格内容。</small></div>
          <div className="stack-item"><strong>进社区</strong><small>进入聊天房间交流经验，也可以去商城挑选训练装备。</small></div>
        </article>
      </section>
    </div>
  )
}

export default HomePage

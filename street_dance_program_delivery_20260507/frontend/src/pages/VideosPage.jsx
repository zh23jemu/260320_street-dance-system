import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

const initialForm = {
  title: '',
  video_file: '',
  description: '',
}

function VideosPage({ currentUser, setNotice }) {
  const [videos, setVideos] = useState([])
  const [selectedVideo, setSelectedVideo] = useState(null)
  const [comment, setComment] = useState('')
  const [form, setForm] = useState(initialForm)

  async function loadVideos() {
    try {
      const data = await apiFetch('/videos/list/')
      setVideos(data.items)
      if (data.items.length > 0 && !selectedVideo) {
        await openDetail(data.items[0].id)
      }
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function openDetail(videoId) {
    try {
      const data = await apiFetch(`/videos/${videoId}/`)
      setSelectedVideo(data)
    } catch (error) {
      setNotice(error.message)
    }
  }

  useEffect(() => {
    loadVideos()
  }, [])

  async function submitVideo(event) {
    event.preventDefault()
    try {
      await apiFetch('/videos/list/', { method: 'POST', body: JSON.stringify(form) })
      setForm(initialForm)
      setNotice('视频发布成功')
      await loadVideos()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function likeVideo(videoId) {
    try {
      await apiFetch(`/videos/${videoId}/like/`, { method: 'POST', body: JSON.stringify({}) })
      setNotice('已点赞')
      await loadVideos()
      await openDetail(videoId)
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function favoriteVideo(videoId) {
    try {
      await apiFetch(`/videos/${videoId}/favorite/`, { method: 'POST', body: JSON.stringify({}) })
      setNotice('已收藏视频')
      await loadVideos()
      await openDetail(videoId)
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function submitComment(event) {
    event.preventDefault()
    if (!selectedVideo) {
      return
    }

    try {
      await apiFetch(`/videos/${selectedVideo.video.id}/comments/`, {
        method: 'POST',
        body: JSON.stringify({ content: comment }),
      })
      setComment('')
      setNotice('评论成功')
      await loadVideos()
      await openDetail(selectedVideo.video.id)
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="page-grid">
      <section className="panel-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">视频模块</p>
            <h2>视频作品墙</h2>
          </div>
          <span>{videos.length} 条作品</span>
        </div>

        <div className="dual-grid">
          <div className="scroll-list">
            {videos.map((video) => (
              <button key={video.id} className="list-card" onClick={() => openDetail(video.id)}>
                <strong>{video.title}</strong>
                <span>{video.user.nickname || video.user.username}</span>
                <small>{video.description || '暂无描述'}</small>
              </button>
            ))}
          </div>

          <div className="panel-card inner-card">
            {selectedVideo ? (
              <>
                <div className="stack-item">
                  <span className="panel-title">当前作品</span>
                  <strong>{selectedVideo.video.title}</strong>
                  <small>{selectedVideo.video.description || '暂无描述'}</small>
                  <small>文件：{selectedVideo.video.video_file}</small>
                </div>
                <div className="button-row">
                  <button onClick={() => likeVideo(selectedVideo.video.id)}>点赞 {selectedVideo.video.like_count}</button>
                  <button className="ghost-button" onClick={() => favoriteVideo(selectedVideo.video.id)}>
                    收藏 {selectedVideo.video.favorite_count}
                  </button>
                </div>
                <div className="comment-list">
                  {selectedVideo.comments.map((item) => (
                    <div key={item.id} className="stack-item comment-card">
                      <strong>{item.user.nickname || item.user.username}</strong>
                      <small>{item.content}</small>
                    </div>
                  ))}
                </div>
                <form className="form-grid" onSubmit={submitComment}>
                  <textarea placeholder="写下你的评论" value={comment} onChange={(event) => setComment(event.target.value)} />
                  <button type="submit">发表评论</button>
                </form>
              </>
            ) : (
              <p>选择左侧作品查看详情。</p>
            )}
          </div>
        </div>
      </section>

      <section className="panel-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">发布作品</p>
            <h2>发布视频</h2>
          </div>
          <span>{currentUser ? '已登录' : '需要登录'}</span>
        </div>
        <form className="form-grid" onSubmit={submitVideo}>
          <input placeholder="作品标题" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} />
          <input placeholder="视频地址或文件路径" value={form.video_file} onChange={(event) => setForm({ ...form, video_file: event.target.value })} />
          <textarea placeholder="作品描述" value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} />
          <button type="submit">发布作品</button>
        </form>
      </section>
    </div>
  )
}

export default VideosPage

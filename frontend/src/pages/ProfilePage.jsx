import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

function ProfilePage({ currentUser, refreshUser, setNotice }) {
  const [dashboard, setDashboard] = useState(null)
  const [favorites, setFavorites] = useState([])
  const [following, setFollowing] = useState([])
  const [form, setForm] = useState({ nickname: '', phone: '', profile: '' })

  useEffect(() => {
    if (!currentUser) {
      return
    }

    setForm({
      nickname: currentUser.nickname || '',
      phone: currentUser.phone || '',
      profile: currentUser.profile || '',
    })

    async function loadProfile() {
      try {
        const [dashboardData, favoritesData, followingData] = await Promise.all([
          apiFetch('/users/dashboard/'),
          apiFetch('/users/favorites/'),
          apiFetch('/users/following/'),
        ])
        setDashboard(dashboardData)
        setFavorites(favoritesData.items)
        setFollowing(followingData.items)
      } catch (error) {
        setNotice(error.message)
      }
    }

    loadProfile()
  }, [currentUser])

  async function submitProfile(event) {
    event.preventDefault()
    try {
      await apiFetch('/users/me/', { method: 'PATCH', body: JSON.stringify(form) })
      await refreshUser()
      setNotice('个人信息已更新')
    } catch (error) {
      setNotice(error.message)
    }
  }

  if (!currentUser) {
    return (
      <section className="hero-card">
        <p className="eyebrow">Profile Locked</p>
        <h2>登录后查看你的发布、报名、收藏和订单。</h2>
      </section>
    )
  }

  return (
    <div className="page-grid">
      <section className="panel-row">
        <article className="panel-card accent-panel">
          <span className="panel-title">个人概况</span>
          <strong>{currentUser.nickname || currentUser.username}</strong>
          <small>{currentUser.profile || '还没有填写个人简介'}</small>
        </article>
        {dashboard ? (
          <article className="panel-card metrics-grid">
            <div><strong>{dashboard.counts.published_activities}</strong><span>我发布的活动</span></div>
            <div><strong>{dashboard.counts.registered_activities}</strong><span>我报名的活动</span></div>
            <div><strong>{dashboard.counts.videos}</strong><span>我的视频</span></div>
            <div><strong>{dashboard.counts.orders}</strong><span>订单数</span></div>
          </article>
        ) : null}
      </section>

      <section className="panel-card">
        <div className="section-heading"><h2>编辑资料</h2></div>
        <form className="form-grid" onSubmit={submitProfile}>
          <input placeholder="昵称" value={form.nickname} onChange={(event) => setForm({ ...form, nickname: event.target.value })} />
          <input placeholder="手机号" value={form.phone} onChange={(event) => setForm({ ...form, phone: event.target.value })} />
          <textarea placeholder="个人简介" value={form.profile} onChange={(event) => setForm({ ...form, profile: event.target.value })} />
          <button type="submit">保存资料</button>
        </form>
      </section>

      <section className="triple-grid">
        <article className="panel-card">
          <span className="panel-title">我的收藏</span>
          {favorites.map((item) => (
            <div key={item.id} className="stack-item">
              <strong>{item.target.title}</strong>
              <small>{item.target_type}</small>
            </div>
          ))}
        </article>

        <article className="panel-card">
          <span className="panel-title">我的关注</span>
          {following.map((item) => (
            <div key={item.id} className="stack-item">
              <strong>{item.user.nickname || item.user.username}</strong>
              <small>{item.user.profile || '暂无简介'}</small>
            </div>
          ))}
        </article>

        <article className="panel-card">
          <span className="panel-title">最近动态</span>
          {dashboard?.latest.published_activities.map((item) => (
            <div key={item.id} className="stack-item">
              <strong>{item.title}</strong>
              <small>{item.location}</small>
            </div>
          ))}
        </article>
      </section>
    </div>
  )
}

export default ProfilePage

import { NavLink, Route, Routes, useNavigate } from 'react-router-dom'
import { useEffect, useState, startTransition } from 'react'

import { apiFetch } from './api'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import ActivitiesPage from './pages/ActivitiesPage'
import ProfilePage from './pages/ProfilePage'
import VideosPage from './pages/VideosPage'
import SocialPage from './pages/SocialPage'
import MallPage from './pages/MallPage'

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [notice, setNotice] = useState('')
  const navigate = useNavigate()

  async function refreshUser() {
    try {
      const data = await apiFetch('/users/me/', { method: 'GET' })
      startTransition(() => {
        setCurrentUser(data.user)
      })
    } catch {
      startTransition(() => {
        setCurrentUser(null)
      })
    }
  }

  useEffect(() => {
    refreshUser()
  }, [])

  useEffect(() => {
    // 全局提示只短暂展示一会，避免成功提示一直占着页面顶部。
    if (!notice) {
      return undefined
    }

    const timer = window.setTimeout(() => {
      setNotice('')
    }, 2500)

    return () => {
      window.clearTimeout(timer)
    }
  }, [notice])

  async function handleLogout() {
    try {
      await apiFetch('/users/logout/', { method: 'POST', body: JSON.stringify({}) })
      setNotice('已退出登录')
      setCurrentUser(null)
      navigate('/login')
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <p className="eyebrow">街舞平台</p>
          <h1>街舞信息共享平台</h1>
          <p className="sidebar-copy">围绕活动、作品、交流和装备交易整理一个更清晰的街舞社区入口。</p>
        </div>

        <nav className="nav-links">
          <NavLink to="/">首页</NavLink>
          <NavLink to="/activities">活动</NavLink>
          <NavLink to="/videos">视频</NavLink>
          <NavLink to="/social">社交</NavLink>
          <NavLink to="/mall">商城</NavLink>
          <NavLink to="/profile">我的</NavLink>
          <NavLink to="/login">登录</NavLink>
        </nav>

        <div className="sidebar-card">
          <span className="sidebar-label">当前状态</span>
          <strong>{currentUser ? `已登录：${currentUser.nickname || currentUser.username}` : '未登录'}</strong>
          <small>{currentUser ? '可以继续浏览、发布和互动。' : '登录后可发布活动、评论视频与下单。'}</small>
          {currentUser ? <button onClick={handleLogout}>退出</button> : null}
        </div>
      </aside>

      <main className="content">
        {notice ? <div className="notice">{notice}</div> : null}
        <Routes>
          <Route path="/" element={<HomePage currentUser={currentUser} refreshUser={refreshUser} setNotice={setNotice} />} />
          <Route path="/login" element={<LoginPage refreshUser={refreshUser} setNotice={setNotice} />} />
          <Route path="/activities" element={<ActivitiesPage currentUser={currentUser} setNotice={setNotice} />} />
          <Route path="/videos" element={<VideosPage currentUser={currentUser} setNotice={setNotice} />} />
          <Route path="/social" element={<SocialPage currentUser={currentUser} setNotice={setNotice} />} />
          <Route path="/mall" element={<MallPage currentUser={currentUser} setNotice={setNotice} />} />
          <Route path="/profile" element={<ProfilePage currentUser={currentUser} refreshUser={refreshUser} setNotice={setNotice} />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

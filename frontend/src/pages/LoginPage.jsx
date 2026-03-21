import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { apiFetch } from '../api'

const initialRegister = {
  username: '',
  password: '',
  confirm_password: '',
  nickname: '',
}

function LoginPage({ refreshUser, setNotice }) {
  const [mode, setMode] = useState('login')
  const [loginForm, setLoginForm] = useState({ username: '', password: '' })
  const [registerForm, setRegisterForm] = useState(initialRegister)
  const navigate = useNavigate()

  async function submitLogin(event) {
    event.preventDefault()
    try {
      await apiFetch('/users/login/', { method: 'POST', body: JSON.stringify(loginForm) })
      await refreshUser()
      setNotice('登录成功')
      navigate('/profile')
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function submitRegister(event) {
    event.preventDefault()
    try {
      await apiFetch('/users/register/', { method: 'POST', body: JSON.stringify(registerForm) })
      await refreshUser()
      setNotice('注册成功，已自动登录')
      navigate('/profile')
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="page-grid login-layout">
      <section className="hero-card login-copy">
        <p className="eyebrow">Join The Circle</p>
        <h2>先登录，再进入你的舞池。</h2>
        <p>当前前端已直接对接 Django 会话登录。登录后可以发布活动、查看 dashboard、收藏和关注。</p>
      </section>

      <section className="panel-card auth-card">
        <div className="tab-row">
          <button className={mode === 'login' ? 'active' : ''} onClick={() => setMode('login')}>登录</button>
          <button className={mode === 'register' ? 'active' : ''} onClick={() => setMode('register')}>注册</button>
        </div>

        {mode === 'login' ? (
          <form className="form-grid" onSubmit={submitLogin}>
            <input placeholder="用户名" value={loginForm.username} onChange={(event) => setLoginForm({ ...loginForm, username: event.target.value })} />
            <input type="password" placeholder="密码" value={loginForm.password} onChange={(event) => setLoginForm({ ...loginForm, password: event.target.value })} />
            <button type="submit">进入平台</button>
          </form>
        ) : (
          <form className="form-grid" onSubmit={submitRegister}>
            <input placeholder="用户名" value={registerForm.username} onChange={(event) => setRegisterForm({ ...registerForm, username: event.target.value })} />
            <input placeholder="昵称" value={registerForm.nickname} onChange={(event) => setRegisterForm({ ...registerForm, nickname: event.target.value })} />
            <input type="password" placeholder="密码" value={registerForm.password} onChange={(event) => setRegisterForm({ ...registerForm, password: event.target.value })} />
            <input type="password" placeholder="确认密码" value={registerForm.confirm_password} onChange={(event) => setRegisterForm({ ...registerForm, confirm_password: event.target.value })} />
            <button type="submit">创建账号</button>
          </form>
        )}
      </section>
    </div>
  )
}

export default LoginPage

import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

const initialForm = {
  title: '',
  activity_type: 'competition',
  content: '',
  location: '',
  start_time: '',
  end_time: '',
  signup_deadline: '',
}

function ActivitiesPage({ currentUser, setNotice }) {
  const [activities, setActivities] = useState([])
  const [form, setForm] = useState(initialForm)

  async function loadActivities() {
    try {
      const data = await apiFetch('/activities/list/')
      setActivities(data.items)
    } catch (error) {
      setNotice(error.message)
    }
  }

  useEffect(() => {
    loadActivities()
  }, [])

  async function submitActivity(event) {
    event.preventDefault()
    try {
      await apiFetch('/activities/list/', { method: 'POST', body: JSON.stringify(form) })
      setNotice('活动发布成功')
      setForm(initialForm)
      loadActivities()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function registerActivity(activityId) {
    try {
      await apiFetch(`/activities/${activityId}/register/`, { method: 'POST', body: JSON.stringify({}) })
      setNotice('报名成功')
      loadActivities()
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function favoriteActivity(activityId) {
    try {
      await apiFetch(`/activities/${activityId}/favorite/`, { method: 'POST', body: JSON.stringify({}) })
      setNotice('活动已收藏')
      loadActivities()
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="page-grid">
      <section className="panel-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Activity Flow</p>
            <h2>活动广场</h2>
          </div>
          <span>{activities.length} 场活动</span>
        </div>

        <div className="activity-grid">
          {activities.map((activity) => (
            <article key={activity.id} className="activity-card">
              <div className="activity-meta">
                <span>{activity.activity_type}</span>
                <span>{activity.status}</span>
              </div>
              <h3>{activity.title}</h3>
              <p>{activity.content}</p>
              <div className="stack-item compact">
                <strong>{activity.location}</strong>
                <small>{new Date(activity.start_time).toLocaleString()}</small>
              </div>
              <div className="button-row">
                <button onClick={() => registerActivity(activity.id)}>报名</button>
                <button className="ghost-button" onClick={() => favoriteActivity(activity.id)}>收藏</button>
              </div>
            </article>
          ))}
        </div>
      </section>

      <section className="panel-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">Publish</p>
            <h2>发布活动</h2>
          </div>
          <span>{currentUser ? '已登录' : '需要登录'}</span>
        </div>

        <form className="form-grid" onSubmit={submitActivity}>
          <input placeholder="活动标题" value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} />
          <select value={form.activity_type} onChange={(event) => setForm({ ...form, activity_type: event.target.value })}>
            <option value="competition">比赛</option>
            <option value="commercial">商演</option>
            <option value="performance">表演</option>
            <option value="backup_dancer">伴舞</option>
            <option value="other">其他</option>
          </select>
          <input placeholder="活动地点" value={form.location} onChange={(event) => setForm({ ...form, location: event.target.value })} />
          <textarea placeholder="活动描述" value={form.content} onChange={(event) => setForm({ ...form, content: event.target.value })} />
          <label>
            开始时间
            <input type="datetime-local" value={form.start_time} onChange={(event) => setForm({ ...form, start_time: event.target.value })} />
          </label>
          <label>
            结束时间
            <input type="datetime-local" value={form.end_time} onChange={(event) => setForm({ ...form, end_time: event.target.value })} />
          </label>
          <label>
            报名截止
            <input type="datetime-local" value={form.signup_deadline} onChange={(event) => setForm({ ...form, signup_deadline: event.target.value })} />
          </label>
          <button type="submit">发布活动</button>
        </form>
      </section>
    </div>
  )
}

export default ActivitiesPage

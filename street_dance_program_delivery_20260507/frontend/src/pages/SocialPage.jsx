import { useEffect, useState } from 'react'

import { apiFetch } from '../api'

function SocialPage({ currentUser, setNotice }) {
  const [rooms, setRooms] = useState([])
  const [activeRoom, setActiveRoom] = useState(null)
  const [message, setMessage] = useState('')

  async function loadRooms() {
    try {
      const data = await apiFetch('/social/rooms/')
      setRooms(data.items)
      if (data.items.length > 0 && !activeRoom) {
        await openRoom(data.items[0].id)
      }
    } catch (error) {
      setNotice(error.message)
    }
  }

  async function openRoom(roomId) {
    try {
      const data = await apiFetch(`/social/rooms/${roomId}/`)
      setActiveRoom(data)
    } catch (error) {
      setNotice(error.message)
    }
  }

  useEffect(() => {
    loadRooms()
  }, [])

  async function sendMessage(event) {
    event.preventDefault()
    if (!activeRoom) {
      return
    }

    try {
      await apiFetch(`/social/rooms/${activeRoom.room.id}/messages/`, {
        method: 'POST',
        body: JSON.stringify({ content: message }),
      })
      setMessage('')
      setNotice('消息已发送')
      await openRoom(activeRoom.room.id)
    } catch (error) {
      setNotice(error.message)
    }
  }

  return (
    <div className="page-grid">
      <section className="panel-card">
        <div className="section-heading">
          <div>
            <p className="eyebrow">社交模块</p>
            <h2>分类聊天室</h2>
          </div>
          <span>{currentUser ? '可以发言' : '未登录只能查看'}</span>
        </div>

        <div className="dual-grid">
          <div className="scroll-list">
            {rooms.map((room) => (
              <button key={room.id} className="list-card" onClick={() => openRoom(room.id)}>
                <strong>{room.room_name}</strong>
                <span>{room.category}</span>
                <small>{room.description || '进入房间开始交流'}</small>
              </button>
            ))}
          </div>

          <div className="panel-card inner-card">
            {activeRoom ? (
              <>
                <div className="stack-item">
                  <span className="panel-title">当前房间</span>
                  <strong>{activeRoom.room.room_name}</strong>
                  <small>{activeRoom.room.category}</small>
                </div>
                <div className="chat-stream">
                  {activeRoom.messages.map((item) => (
                    <div key={item.id} className="chat-bubble">
                      <strong>{item.user.nickname || item.user.username}</strong>
                      <small>{item.content}</small>
                    </div>
                  ))}
                </div>
                <form className="form-grid" onSubmit={sendMessage}>
                  <textarea placeholder="说点什么..." value={message} onChange={(event) => setMessage(event.target.value)} />
                  <button type="submit">发送消息</button>
                </form>
              </>
            ) : (
              <p>选择一个房间查看内容。</p>
            )}
          </div>
        </div>
      </section>
    </div>
  )
}

export default SocialPage

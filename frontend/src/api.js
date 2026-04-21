const defaultHeaders = {
  'Content-Type': 'application/json',
}

export async function apiFetch(path, options = {}) {
  // 所有前端接口统一走 /api 前缀。
  // 这样浏览器地址栏中的页面路由仍然保持 /videos、/mall 这类前端路径，
  // 只有真正的接口请求才会被 Vite 代理到 Django，避免刷新页面时误拿到后端 JSON。
  const requestPath = path.startsWith('/api/') ? path : `/api${path}`

  const response = await fetch(requestPath, {
    credentials: 'include',
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
    ...options,
  })

  const data = await response.json().catch(() => ({}))
  if (!response.ok) {
    throw new Error(data.detail || '请求失败')
  }

  return data
}

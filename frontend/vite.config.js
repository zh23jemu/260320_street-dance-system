import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // 统一把前端接口请求收口到 /api 前缀下，
      // 避免 React 路由路径（如 /videos、/social）和代理规则重名，
      // 导致浏览器刷新页面时被错误转发到 Django，最终只看到 JSON。
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/users': 'http://127.0.0.1:8000',
      '/activities': 'http://127.0.0.1:8000',
      '/videos': 'http://127.0.0.1:8000',
      '/social': 'http://127.0.0.1:8000',
      '/mall': 'http://127.0.0.1:8000',
    },
  },
})

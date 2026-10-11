import react from '@vitejs/plugin-react'
import { defineConfig, loadEnv } from 'vite'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const backendEnv = loadEnv(mode, path.resolve(__dirname, '../backend'), '')

  const supabaseUrl = env.VITE_SUPABASE_URL || env.SUPABASE_URL || backendEnv.VITE_SUPABASE_URL || backendEnv.SUPABASE_URL || process.env.VITE_SUPABASE_URL || process.env.SUPABASE_URL || ''
  const supabaseAnonKey = env.VITE_SUPABASE_ANON_KEY || env.SUPABASE_ANON_KEY || backendEnv.VITE_SUPABASE_ANON_KEY || backendEnv.SUPABASE_ANON_KEY || process.env.VITE_SUPABASE_ANON_KEY || process.env.SUPABASE_ANON_KEY || ''

  const define: Record<string, string> = {}
  if (supabaseUrl) {
    define['import.meta.env.VITE_SUPABASE_URL'] = JSON.stringify(supabaseUrl)
  }
  if (supabaseAnonKey) {
    define['import.meta.env.VITE_SUPABASE_ANON_KEY'] = JSON.stringify(supabaseAnonKey)
  }

  return {
    plugins: [react()],
    ...(Object.keys(define).length > 0 ? { define } : {})
  }
})

import { defineStore } from 'pinia'
import api from '../services/api'
export const useAuthStore = defineStore('auth', { state: () => ({ user: JSON.parse(localStorage.getItem('user') || 'null'), ready: false }), getters: { authenticated: s => !!s.user, hasRole: s => role => s.user?.roles?.includes(role) }, actions: {
  save(token, user) { localStorage.setItem('access_token', token); localStorage.setItem('user', JSON.stringify(user)); this.user = user },
  async login(payload) { const { data } = await api.post('/auth/login', payload); this.save(data.access_token, data.user) },
  async hydrate() { if (!localStorage.getItem('access_token')) { this.ready = true; return }; try { this.user = (await api.get('/auth/me')).data; localStorage.setItem('user', JSON.stringify(this.user)) } catch { this.clear() } finally { this.ready = true } },
  clear() { localStorage.removeItem('access_token'); localStorage.removeItem('user'); this.user = null },
  async logout() { try { await api.post('/auth/logout') } finally { this.clear() } }
} })

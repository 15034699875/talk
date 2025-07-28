import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    id: null as number | null,
    username: '',
    avatar_url: '',
    email: '',
    role: '',
    points: 0,
    exp: 0,
    token: localStorage.getItem('token') || ''
  }),
  actions: {
    setUser(user: any) {
      this.id = user.id
      this.username = user.username
      this.avatar_url = user.avatar_url
      this.email = user.email
      this.role = user.role
      this.points = user.points
      this.exp = user.exp
    },
    setToken(token: string) {
      this.token = token
      localStorage.setItem('token', token)
    },
    logout() {
      this.id = null
      this.username = ''
      this.avatar_url = ''
      this.email = ''
      this.role = ''
      this.points = 0
      this.exp = 0
      this.token = ''
      localStorage.removeItem('token')
    }
  }
}) 
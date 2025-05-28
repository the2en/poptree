import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    clearAuth() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
    setUser(user) {
      this.user = user
    },
    async logout() {
      if (!confirm('정말 로그아웃 하시겠습니까?')) return
      this.clearAuth()
      alert('로그아웃 되었습니다.')
      window.location.reload()
    },
    async withdraw() {
      if (!confirm('정말 회원탈퇴 하시겠습니까?')) return
      try {
        const res = await fetch('http://127.0.0.1:8000/api/accounts/delete/', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${this.token}`,
            'Content-Type': 'application/json',
          },
        })
        if (!res.ok) throw new Error('회원탈퇴 실패')
        alert('회원탈퇴가 완료되었습니다.')
        this.clearAuth()
        window.location.reload()
      } catch (err) {
        alert(err.message)
      }
    },
  },
}) 
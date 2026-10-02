import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import LoginView from '../views/LoginView.vue'; import RegisterView from '../views/RegisterView.vue'; import ForgotPasswordView from '../views/ForgotPasswordView.vue'; import ResetPasswordView from '../views/ResetPasswordView.vue'; import ProfileView from '../views/ProfileView.vue'; import UsersView from '../views/UsersView.vue'
const routes = [
  { path: '/', redirect: '/perfil' }, { path: '/ingresar', component: LoginView, meta: { guest: true } }, { path: '/registro', component: RegisterView, meta: { guest: true } }, { path: '/recuperar', component: ForgotPasswordView, meta: { guest: true } }, { path: '/restablecer', component: ResetPasswordView, meta: { guest: true } },
  { path: '/perfil', component: ProfileView, meta: { auth: true } }, { path: '/usuarios', component: UsersView, meta: { auth: true, roles: ['Administrador'] } }
]
const router = createRouter({ history: createWebHistory(), routes })
router.beforeEach(async to => { const auth = useAuthStore(); if (!auth.ready) await auth.hydrate(); if (to.meta.auth && !auth.authenticated) return { path: '/ingresar', query: { redirect: to.fullPath } }; if (to.meta.guest && auth.authenticated) return '/perfil'; if (to.meta.roles && !to.meta.roles.some(auth.hasRole)) return '/perfil' })
export default router

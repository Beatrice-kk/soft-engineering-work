import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/Manage.vue'
import store from "@/store";

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: () => import('../views/Manage.vue'),
    redirect: "/login",
    children: [
      { path: 'home', name: '系统主页', component: () => import('../views/Home.vue') },

      { path: 'arrange', name: '航班信息', component: () => import('../views/Arrange.vue') },
      { path: 'arrangetable', name: '增加航班', component: () => import('../views/Arrangetable.vue') },
      { path: 'train', name: '排班信息', component: () => import('../views/Train.vue') },
      { path: 'traintable', name: '增加排班', component: () => import('../views/Traintable.vue') },
      { path: 'Ticket', name: '航班信息', component: () => import('../views/Ticket.vue') },
      { path: 'passenger', name: '用户信息', component: () => import('../views/Passenger.vue') },
      { path: 'account', name: '用户账号', component: () => import('../views/Account.vue') },

      { path: 'profile', name: '个人资料', component: () => import('../views/Profile.vue') },
      { path: 'relation', name: '关联旅客', component: () => import('../views/Relation.vue') },
      { path: 'book', name: '航班预订', component: () => import('../views/Book.vue') },
      { path: 'order', name: '我的订单', component: () => import('../views/Order.vue') },
      { path: 'print', name: '打印航班', component: () => import('../views/Print.vue') },


    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../views/Register.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})
// 路由守卫
router.beforeEach((to, from, next) => {
  localStorage.setItem("currentPathName", to.name)  // 设置当前的路由名称，为了在Header组件中去使用
  store.commit("setPath")  // 触发store的数据更新
  next()  // 放行路由
})
export default router

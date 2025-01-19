import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import NewQuizPage from '../views/NewQuizPage.vue';
import QuestionsManager from '@/views/QuestionsManager.vue';
import ScorePage from '@/views/ScorePage.vue';
import About from '../views/AboutPage.vue';



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
    },
    {
      path: '/new-quiz',
      name: 'new-quiz',
      component: NewQuizPage,
    },
    {
      path: '/questions',
      name: 'QuestionsManager',
      component: QuestionsManager,
    },
    {
      path: '/score',
      name: 'ScorePage',
      component: ScorePage,
    },
    {
      path: '/about',
      name: 'about',
      component: About,
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
    },
  ],
})

export default router

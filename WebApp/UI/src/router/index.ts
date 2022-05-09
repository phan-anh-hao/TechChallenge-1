import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DatasetViewVue from '@/views/DatasetView.vue'
import NotFoundViewVue from '@/views/NotFoundView.vue'
import { useDatasetStore } from '@/stores/dataset'

const router = createRouter({
  history: createWebHistory(import.meta.env.VITE_BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/dataset/:dataset_name',
      name: 'dataset',
      component: DatasetViewVue,
      beforeEnter: () => {
        const store = useDatasetStore()
        if (!store.dataset) return '/dataset_not_found'
      },
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'notfound',
      component: NotFoundViewVue,
    },
  ],
})

export default router

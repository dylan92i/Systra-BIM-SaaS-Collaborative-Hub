import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '@/pages/LoginPage.vue'
import MainPage from '@/pages/MainPage.vue'
import CreateAccountPage from '@/pages/CreateAccountPage.vue'

import ProjectList from '@/components/ProjectList.vue'
import OSViewer from '@/pages/FileExplorer.vue'
import Test from '@/pages/Test.vue'
import ProjectDashboard from '@/pages/ProjectDashboard.vue'
import BIMViewer from '@/pages/BIMViewer.vue'
import Setting from '@/pages/Setting.vue'

const routes = [
  { path: '/', component: LoginPage },
  { path: '/create_account', component: CreateAccountPage },
  { path: '/test', component: Test },
  {
    path: '/main',
    component: MainPage,
    children: [
      { path: 'project', component: ProjectList },
      { path: 'setting', component: Setting },                    
      { path: 'viewer', component: BIMViewer },                  
      { path: 'project/:projectName', component: ProjectDashboard }, 
      { 
        path: 'files/:catchAll(.*)?',                                
        component: OSViewer 
      },
      { path: '', redirect: '/main/project' },                       
    ],
  },
  { 
    path: '/:pathMatch(.*)*',
    name: 'NotFound', 
    component: () => import('@/pages/NotFound.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router

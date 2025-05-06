<template>
  <div class="container">
    <h1 class="title">{{ $t('current_projects_title') }}</h1>
    <div v-if="loading" class="loading">{{ $t('loading') }}</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="projects.length > 0" class="grid">
      <!-- CREATE PROJECT CARD -->
      <CardProject
        customClass="create-card"
        :imgSrc="creationCardImg"
        :imgAlt="$t('create_card_img_alt')"
        :title="$t('create_project_card_title')"
        :desc="$t('create_project_card_desc')"
        :titleStyle="{ color: '#4ec265' }"
        :bodyStyle="{ background: 'rgba(20,40,20,0.93)' }"
        @click="showModal = true"
      />
      <!-- PROJECTS -->
      <CardProject
        v-for="project in projects"
        :key="project.id"
        :imgSrc="project.picture ? getPictureUrl(project.picture) : null"
        :imgAlt="$t('project_card_img_alt')"
        :title="project.name"
        :desc="project.description"
        :tag="$t('project_card_tag_active')"
        class="pointer"
        tabindex="0"
        @click="goToProject(project)"
        @keydown.enter="goToProject(project)"
      />
    </div>
    <div v-else-if="!loading" class="empty">
      {{ $t('empty_project_list') }}
    </div>
    <CreateProject :show="showModal" @close="showModal = false" @created="refreshProjects" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import CardProject from './CardProject.vue'
import CreateProject from './CreateProject.vue'
import { backend_config } from "@/config/system-config.js"

const router = useRouter()
const projects = ref([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)

const creationCardImg = backend_config.backend_uri + '/get_ressource/create_project.jpg'

function getPictureUrl(picture) {
  return picture
    ? `${backend_config.backend_uri}/get_project_picture?picture_name=${encodeURIComponent(picture)}`
    : 'https://via.placeholder.com/400x400/2c0a0a/ff6666?text=No+Image'
}

async function fetchProjects() {
  loading.value = true
  error.value = ''
  try {
    const response = await axios.get(backend_config.backend_uri + '/get_my_projects', {
      withCredentials: true,
    })
    projects.value = response.data
  } catch (e) {
    error.value = e.response?.data?.message || e.message || $t('generic_error')
  }
  loading.value = false
}

function refreshProjects() {
  fetchProjects()
}

function goToProject(project) {
  if (!project || !project.name) return
  router.push(`/main/project/${encodeURIComponent(project.name)}`)
}

onMounted(fetchProjects)
</script>

<style scoped>
.pointer {
  cursor: pointer;
}
.grid {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
}
.loading, .error, .empty {
  text-align: center;
  margin: 2rem 0;
}
</style>

<style scoped>
/* Rappelle tout le CSS de ta question, sauf la partie .card et enfants déjà dans le composant CardProject */
.container {
  min-height: 100vh;
  background: #0f0a0a;
  padding: 48px 10vw;
  box-sizing: border-box;
}
.title {
  text-align: center;
  font-size: 2.3rem;
  font-weight: 800;
  margin-bottom: 40px;
  letter-spacing: 1px;
  color: #ff6666;
  text-shadow: 0 2px 8px rgba(255, 59, 48, 0.3);
  position: relative;
  padding-bottom: 15px;
}
.title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 120px;
  height: 3px;
  background: linear-gradient(90deg, transparent, #ff3b30, transparent);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 30px;
  justify-content: center;
}
.loading, .empty {
  text-align: center;
  margin: 40px 0;
  font-size: 1.2rem;
  color: #ff6666;
}
.error {
  color: #ff3b30;
  text-align: center;
  margin: 40px 0;
  font-size: 1.2rem;
}
@media (max-width: 800px) {
  .container {
    padding: 32px 4vw;
  }
  .title {
    font-size: 1.8rem;
  }
  .grid {
    grid-template-columns: 1fr;
    max-width: 400px;
    margin: 0 auto;
  }
}
</style>

<template>
  <div class="dashboard-root" v-if="!loading && !error">
    <div class="main-grid">
      <!-- HEADER INFOS -->
      <section class="dashboard-header">
        <div class="icon-col">
          <svg class="project-icon" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="#C70039"/><rect x="10" y="7" width="4" height="10" fill="#fff" opacity="0.85"/><rect x="7" y="14" width="10" height="3" fill="#fff" opacity="0.15"/></svg>
        </div>
        <div class="header-text">
          <h2>{{ projet.name }}</h2>
          <div class="header-details">
            <div><strong>{{ $t('client') }} :</strong> {{ projet.client }}</div>
            <div><strong>{{ $t('project_manager') }} :</strong> {{ projet.chef }}</div>
            <div>
              <strong>{{ $t('status') }} :</strong>
              <span :class="['statut', projet.statut?.replace(' ','-').toLowerCase()]">
                {{ projet.statut }}
              </span>
            </div>
          </div>
          <div class="header-details">
            <div><strong>{{ $t('start_date') }} :</strong> {{ projet.debut }}</div>
            <div><strong>{{ $t('end_date') }} :</strong> {{ projet.fin }}</div>
            <div><strong>{{ $t('budget') }} :</strong> {{ projet.budget }} €</div>
          </div>
          <button @click="$router.push('/main/project')" class="back-button">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 12H5M12 19l-7-7 7-7"/>
            </svg>
            {{ $t('back') }}
          </button>
        </div>
      </section>

      <!-- MAIN CONTENT -->
      <section class="dashboard-content">
        <div class="progress-container">
          <span>{{ $t('global_progress') }}</span>
          <div class="progress-bar">
            <div
              class="progress-bar-inner"
              :style="{
                width: animationProgress + '%',
                background: progressGradient,
                boxShadow: rippleShadow,
              }"
            >
              <div class="progress-glow" :style="{ left: (animationProgress-2) + '%' }"></div>
            </div>
            <span class="progress-label">{{ projet.progression }}%</span>
          </div>
        </div>
        <div v-if="visas.length" class="visa-dropdown">
          <label for="visa-select">{{ $t('select_visa') }}</label>
          <select id="visa-select" v-model="selectedVisaIndex">
            <option v-for="(visa, idx) in visas" :key="idx" :value="idx">
              {{ visa.titre }} — {{ visa.objet }}
            </option>
          </select>
        </div>
        <div v-if="selectedVisa" class="visa-details">
          <h4>{{ $t('visa_details') }}</h4>
          <table>
            <tbody>
              <tr><th>{{ $t('visa_title') }}</th><td>{{ selectedVisa.titre }}</td></tr>
              <tr><th>{{ $t('visa_object') }}</th><td>{{ selectedVisa.objet }}</td></tr>
              <tr><th>{{ $t('visa_speciality') }}</th><td>{{ selectedVisa.specialite }}</td></tr>
              <tr><th>{{ $t('visa_doc_type') }}</th><td>{{ selectedVisa.type_doc }}</td></tr>
              <tr><th>{{ $t('visa_chrono') }}</th><td>{{ selectedVisa.chrono }}</td></tr>
              <tr><th>{{ $t('visa_ged_index') }}</th><td>{{ selectedVisa.indice_ged }}</td></tr>
              <tr><th>{{ $t('visa_discipline') }}</th><td>{{ selectedVisa.discipline }}</td></tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- STEP TIMELINE -->
      <section class="step-container">
        <StepBar :projectId="projet.id" />
      </section>
    </div>
  </div>
  <div v-if="loading" class="loading">{{ $t('loading') }}</div>
  <div v-if="error" class="error">{{ error }}</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute } from "vue-router";
import axios from "axios";
import { backend_config } from "@/config/system-config.js"
import StepBar from "@/components/StepBar.vue";

// --- Réactifs ---
const projet = ref({});
const visas = ref([]);
const loading = ref(true);
const error = ref("");
const selectedVisaIndex = ref(0);

const route = useRoute();

// --- Charge les infos projet/visa depuis le backend ---
async function fetchProject() {
  loading.value = true;
  error.value = "";
  const projectName = route.params.projectName;
  try {
    const res = await axios.get(
      `${backend_config.backend_uri}/main/project/${encodeURIComponent(projectName)}`,
      { withCredentials: true }
    );
    projet.value = res.data;
    visas.value = res.data.visas || [];
    selectedVisaIndex.value = 0;
    startProgressAnim();
  } catch (err) {
    error.value = err.response?.data?.message || err.message || "Erreur de chargement projet";
  }
  loading.value = false;
}

onMounted(fetchProject);

// --- VISA SELECT ---
const selectedVisa = computed(() => visas.value[selectedVisaIndex.value] || null);

// --- PROGRESS BAR ANIM ---
const animationProgress = ref(0);
function startProgressAnim() {
  animationProgress.value = 0;
  if(typeof projet.value.progression !== "number") return;
  const duree = 900;
  const fps = 44;
  const steps = Math.round((fps * duree) / 1000);
  let i = 0;
  const cible = projet.value.progression || 0;
  const timer = setInterval(() => {
    i++;
    animationProgress.value = Math.round(Math.min(cible, (cible * i) / steps));
    if (animationProgress.value >= cible) clearInterval(timer);
  }, duree / steps);
}

const progressGradient = computed(() => {
  let c1 = "#C70039", c2 = "#6503DC", c3 = "#2427FF";
  let p = animationProgress.value / 100;
  if (p < 0.5) {
    return `linear-gradient(90deg, ${c1} 0%, ${c2} ${p * 200}%)`;
  }
  return `linear-gradient(90deg, ${c1} 0%, ${c2} 55%, ${c3} ${50 + 50 * (p - 0.5) * 2}%)`;
});

const rippleShadow = computed(() => {
  let cl = animationProgress.value < 65 ? "#fa2b3d66" : "#2427ffaa";
  return `0 0 30px 8px ${cl}`;
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css?family=Inter:400,600,800&display=swap');

.dashboard-root {
  --txt-main: #f6f6fa;
  --txt-secondary: #cfcdd5;
  --txt-label: #b1a8cc;
  --bg-main: #18131d;
  --bg-header: #211d2a;
  --bg-content: #191723;
  --bg-sidebar: #201e31;
  --bg-card: #211f2c;
  --bg-hover: #28244a;
  color: var(--txt-main);
  font-family: "Inter", "Segoe UI", Arial, sans-serif;
  background: var(--bg-main);
  width: 100%;
  height: 100%;
  min-height: 0;
  min-width: 0;
  overflow: hidden;
  display: flex;
}

.main-grid {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(400px, 1fr);
  grid-template-rows: min-content 1fr;
  gap: 0;
}

.dashboard-header {
  grid-column: 1/3;
  display: flex;
  gap: 1.3rem;
  padding: 1.4rem 1.5rem 0.5rem 1.6rem;
  background: var(--bg-header);
  border-bottom: 1px solid #2e233c80;
}

.icon-col { display: flex; align-items: flex-start;}
.project-icon {
  width: 54px;
  height: 54px;
  filter: drop-shadow(0 1px 12px #c7003927);
  transition: transform .17s cubic-bezier(.29,1.18,.52,1.02);
}

.header-text { flex: 1 1 auto; min-width: 0;}
.dashboard-header h2 {
  margin: 0 0 0.17em;
  font-weight: 700;
  font-size: 1.32rem;
  letter-spacing: 0.4px;
}

.header-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1em 1.7em;
  font-size: 0.97rem;
  color: var(--txt-secondary);
}

.statut {
  padding: 0.09em 0.55em;
  border-radius: 1em;
  font-weight: 700;
  background: #272b34;
  border: 1px solid #af217737;
}

.statut.en-cours { background: #392c36; color: #ff8cb6;}
.statut.termine { background: #262941; color: #88beef;}

.dashboard-content {
  grid-column: 1/2;
  padding: 1.2rem 1.7rem 0.8rem 1.8rem;
  background: var(--bg-content);
  overflow-y: auto;
}

.progress-container {
  margin-bottom: 1.3rem;
  width: 100%;
  max-width: 600px;
}

.progress-bar {
  position: relative;
  background: #161122;
  height: 1.8em;
  border-radius: 1em;
  width: 100%;
}

.progress-bar-inner {
  height: 100%;
  border-radius: 1em 0 0 1em;
  transition: width 0.6s cubic-bezier(.2,1.1,.7,1);
}

.progress-label {
  position: absolute;
  top: 57%;
  right: 1em;
  font-weight: 900;
  color: #fff;
}

.progress-glow {
  position: absolute;
  top: 50%;
  width: 38px;
  height: 110%;
  background: radial-gradient(ellipse at center, #fff0 72%, #fff5 89%, #fff2 100%);
  filter: blur(1.5px) brightness(2);
  opacity: .26;
}

.visa-dropdown { margin-bottom: 1.4rem;}
.visa-dropdown select {
  background: #221830;
  color: #fff;
  border: 1.4px solid #b92658;
  padding: 0.35em 0.88em;
  border-radius: 7px;
}

.visa-details {
  background: var(--bg-card);
  border-radius: 10px;
  padding: 0.8rem 1.25rem;
  margin-top: 0.7rem;
}

.step-container {
  grid-column: 2/3;
  grid-row: 2/3;
  padding: 1rem;
  background: var(--bg-sidebar);
  overflow-y: auto;
}

.back-button {
  margin-top: 1em;
  background: #2c233d;
  color: #fff;
  border: none;
  padding: 0.5em 1em;
  border-radius: 0.5em;
  transition: background 0.2s;
}

@media (max-width: 1200px) {
  .main-grid { grid-template-columns: 1fr; }
  .step-container { grid-column: 1/3; }
}

@media (max-width: 900px) {
  .main-grid { display: flex; flex-direction: column; }
  .step-container { order: 3; }
}
</style>
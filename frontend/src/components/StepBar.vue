<template>
    <div class="timeline dark">
      <h2>Projet – Gestion des étapes</h2>
  
      <button class="edit-btn" @click="editMode = !editMode">
        {{ editMode ? "Quitter le mode modification" : "Modifier les étapes" }}
      </button>
  
      <div class="timeline-scroll-container">
        <div
          v-for="(step, stepIdx) in steps"
          :key="step.id"
          class="timeline-step"
          :class="{active: stepIdx === currentStep}"
        >
          <div class="timeline-point"></div>
          <div class="timeline-content">
            <template v-if="editMode">
              <input
                class="edit-title"
                v-model="step.title"
                placeholder="Titre de l’étape"
                @change="updateStep(step)"
              />
              <textarea
                class="edit-desc"
                v-model="step.description"
                placeholder="Description de l’étape"
                @change="updateStep(step)"
              ></textarea>
            </template>
            <template v-else>
              <h3>{{ step.title }}</h3>
              <p>{{ step.description }}</p>
            </template>
  
            <!-- SOUS-ÉTAPES -->
            <ul class="substeps">
              <li v-for="(sub, subIdx) in step.substeps" :key="sub.id">
                <span
                  class="icon pointer"
                  @click="!editMode && toggleSubStep(sub)"
                >
                  <svg v-if="sub.validated" width="18" height="18" viewBox="0 0 18 18" fill="#54C01E">
                    <path d="M6.7 12.3l-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4z" />
                  </svg>
                  <svg v-else width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="#8A92B0">
                    <circle cx="9" cy="9" r="8" stroke-width="2"/>
                  </svg>
                </span>
                <template v-if="editMode">
                  <input
                    class="edit-sub"
                    v-model="sub.label"
                    @change="updateSubStep(sub)"
                    :placeholder="'Sous-étape ' + (subIdx+1)"
                  />
                  <button @click="removeSubStep(sub.id)" class="del-btn" title="Supprimer la sous-étape">🗑️</button>
                </template>
                <template v-else>
                  {{ sub.label }}
                </template>
              </li>
            </ul>
  
            <button
              v-if="editMode"
              @click="addSubStep(step)"
              class="add-btn"
            >
              + Ajouter une sous-étape
            </button>
  
            <div class="step-actions" v-if="editMode">
              <button
                class="move-btn"
                :disabled="stepIdx === 0"
                @click="moveStep(stepIdx, stepIdx-1)"
              >▲</button>
              <button
                class="move-btn"
                :disabled="stepIdx === steps.length-1"
                @click="moveStep(stepIdx, stepIdx+1)"
              >▼</button>
              <button
                class="del-btn"
                @click="removeStep(step.id)"
                title="Supprimer l'étape"
              >🗑️</button>
            </div>
            <div class="validation" v-if="!editMode && step.substeps.length">
              <button
                class="validate-btn"
                v-if="!isStepValidated(step)"
                @click="validateFullStep(step)"
              >
                Valider toute l'étape
              </button>
              <span v-else class="validated-text">✅ Étape terminée</span>
            </div>
          </div>
        </div>
      </div>
      <button v-if="editMode" class="add-btn main" @click="addStep()">+ Ajouter une étape</button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue"
  import axios from "axios"
  import { backend_config } from "@/config/system-config.js"
  
  const steps = ref([])
  const editMode = ref(false)
  const currentStep = ref(0)
  const projectId = 10 // test
  
  async function loadSteps() {
    const url = `${backend_config.backend_uri}/project/${projectId}/steps`
    const resp = await axios.get(url, { withCredentials: true })
    steps.value = resp.data
  }
  onMounted(loadSteps)
  
  async function addStep() {
    await axios.post(
      `${backend_config.backend_uri}/project/${projectId}/steps`,
      { title: "Nouvelle étape", description: "" },
      { withCredentials: true }
    )
    await loadSteps()
  }
  async function removeStep(stepId) {
    await axios.delete(
      `${backend_config.backend_uri}/step/${stepId}`,
      { withCredentials: true }
    )
    await loadSteps()
  }
  async function updateStep(step) {
    await axios.put(
      `${backend_config.backend_uri}/step/${step.id}`,
      {
        title: step.title,
        description: step.description,
        order: step.order != null ? step.order : undefined,
        validated: step.validated
      },
      { withCredentials: true }
    )
  }
  async function moveStep(fromIdx, toIdx) {
    if (toIdx < 0 || toIdx >= steps.value.length) return
    const arr = steps.value
    arr.splice(toIdx, 0, arr.splice(fromIdx, 1)[0])
    // Met à jour l'ordre côté serveur
    for (let idx = 0; idx < arr.length; idx++) {
      await axios.put(
        `${backend_config.backend_uri}/step/${arr[idx].id}`,
        { order: idx + 1 },
        { withCredentials: true }
      )
    }
    await loadSteps()
  }
  
  // SOUS-ÉTAPES
  async function addSubStep(step) {
    await axios.post(
      `${backend_config.backend_uri}/step/${step.id}/substeps`,
      { label: 'Nouvelle sous-étape' },
      { withCredentials: true }
    )
    await loadSteps()
  }
  async function removeSubStep(subId) {
    await axios.delete(
      `${backend_config.backend_uri}/substep/${subId}`,
      { withCredentials: true }
    )
    await loadSteps()
  }
  async function updateSubStep(sub) {
    await axios.put(
      `${backend_config.backend_uri}/substep/${sub.id}`,
      { label: sub.label, validated: sub.validated, order: sub.order },
      { withCredentials: true }
    )
  }
  async function toggleSubStep(sub) {
    sub.validated = !sub.validated
    await updateSubStep(sub)
  }
  
  // VALIDATION
  function isStepValidated(step) {
    return step.substeps.length > 0 && step.substeps.every(s => s.validated)
  }
  async function validateFullStep(step) {
    for (const sub of step.substeps) {
      sub.validated = true
      await updateSubStep(sub)
    }
    await loadSteps()
  }
  </script>
  
  <style scoped>
  .timeline.dark {
    max-width: 600px;
    margin: 30px auto 0;
    padding: 23px 18px;
    background: #191c23;
    border-radius: 13px;
    box-shadow: 0 7px 24px -10px #000c28;
  }
  
  .timeline.dark h2 {
    text-align: center;
    color: #E6EDFF;
    margin-bottom: 24px;
    font-size: 1.8em;
    letter-spacing: -0.03em;
  }
  
  .timeline-scroll-container {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 8px;
  }
  
  .timeline-step {
    position: relative;
    padding-left: 30px;
    margin-bottom: 28px;
    transition: transform 0.2s ease;
  }
  
  .timeline-step:hover {
    transform: translateY(-2px);
  }
  
  .timeline-point {
    position: absolute;
    left: 1px; 
    top: 15px;
    width: 16px; 
    height: 16px;
    background: #2f3047;
    border: 3px solid #7B61FF;
    border-radius: 50%;
    z-index: 3;
    transition: all 0.2s ease;
  }
  
  .timeline-step.active .timeline-point {
    background: #7B61FF;
    box-shadow: 0 0 0 3px rgba(123, 97, 255, 0.2);
  }
  
  .timeline-content {
    background: linear-gradient(145deg, #232345 0%, #1E1F3A 100%);
    border-radius: 8px;
    padding: 15px 19px;
    box-shadow: 0 4px 32px -13px #1a113c7a;
    border: 1px solid #2D2F4A;
    transition: all 0.2s ease;
  }
  
  .timeline-step:hover .timeline-content {
    box-shadow: 0 6px 24px -8px #7B61FF33;
  }
  
  .timeline-content h3 {
    margin-top: 0;
    color: #DEE5FF;
    font-size: 1.15em;
    margin-bottom: 8px;
    font-weight: 600;
  }
  
  .timeline-content p {
    color: #8A92B0;
    font-size: 0.95em;
    line-height: 1.5;
    margin-bottom: 12px;
  }
  
  .timeline-content input.edit-title {
    border: 1px solid #3A3B5A;
    border-radius: 6px;
    background: #2A2B45;
    padding: 8px 12px; 
    color: #F0F4FF;
    font-size: 1.1em;
    width: 100%;
    margin-bottom: 10px;
    transition: all 0.2s ease;
  }
  
  .timeline-content input.edit-title:focus {
    border-color: #7B61FF;
    box-shadow: 0 0 0 2px #7B61FF33;
  }
  
  .timeline-content textarea.edit-desc {
    border: 1px solid #3A3B5A;
    border-radius: 6px;
    background: #2A2B45;
    color: #C5D0FF;
    width: 100%; 
    min-height: 80px; 
    padding: 8px 12px;
    font-size: 0.95em;
    line-height: 1.5;
    transition: all 0.2s ease;
  }
  
  .timeline-step:not(:last-child)::after {
    content: "";
    position: absolute;
    left: 8px;
    top: 28px;
    width: 2px;
    height: calc(100% - 20px);
    background: linear-gradient(to bottom, #3D3780 0%, #2A2766 100%);
  }
  
  .substeps {
    list-style-type: none;
    margin: 0 0 12px 0;
    padding: 0;
  }
  
  .substeps li {
    display: flex;
    color: #bcb9ff;
    align-items: center;
    margin: 8px 0;
    padding: 6px 8px;
    border-radius: 5px;
    background: #2A2B4522;
    transition: all 0.2s ease;
  }
  
  .substeps li:hover {
    background: #2A2B45;
  }
  
  .substeps li .icon {
    margin-right: 10px;
    transition: transform 0.2s ease;
  }
  
  .substeps li .icon:hover {
    transform: scale(1.1);
  }
  
  .substeps li input.edit-sub {
    border: 1px solid #3A3B5A;
    border-radius: 5px;
    background: #2A2B45;
    color: #F0F4FF;
    padding: 6px 10px;
    font-size: 0.95em;
    flex: 1;
    margin-right: 8px;
  }
  
  .edit-btn, .add-btn, .move-btn, .del-btn, .validate-btn { 
    transition: all 0.2s ease;
  }
  
  .edit-btn {
    border: none; 
    background: #7B61FF; 
    color: #fff;
    border-radius: 8px; 
    padding: 10px 24px;
    margin-bottom: 24px; 
    font-weight: 600;
    font-size: 1em;
    display: block;
    width: 100%;
    box-shadow: 0px 4px 12px #7B61FF33;
  }
  
  .edit-btn:hover { 
    transform: translateY(-1px);
    box-shadow: 0px 6px 16px #7B61FF4D;
  }
  
  .add-btn {
    background: #7B61FF;
    color: #fff;
    border: none;
    border-radius: 6px; 
    padding: 8px 16px;
    font-size: 0.95em;
    font-weight: 500;
    margin: 12px 0 0 0;
  }
  
  .add-btn:hover { 
    background: #927CFF;
    transform: scale(1.02);
  }
  
  .step-actions { 
    margin-top: 15px;
    display: flex;
    gap: 6px;
  }
  
  .move-btn {
    border: none; 
    background: #3A3B5A; 
    color: #DEE5FF;
    border-radius: 5px; 
    padding: 6px 12px;
    font-weight: 600;
  }
  
  .move-btn:hover:not(:disabled) {
    background: #7B61FF;
    transform: scale(1.05);
  }
  
  .del-btn {
    background: #3A3B5A;
    color: #FF5C7A;
    border-radius: 5px;
    padding: 6px 12px;
  }
  
  .del-btn:hover {
    background: #FF5C7A;
    color: white;
    transform: scale(1.05);
  }
  
  .validate-btn {
    background: #54C01E;
    padding: 8px 20px;
    border-radius: 6px;
    font-weight: 600;
  }
  
  .validate-btn:hover {
    background: #48A618;
    transform: translateY(-1px);
  }
  
  .validated-text {
    color: #54C01E;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .timeline.dark ::-webkit-scrollbar { 
    width: 8px; 
    background: #1A1C2A; 
  }
  
  .timeline.dark ::-webkit-scrollbar-thumb { 
    background: #3A3B5A; 
    border-radius: 8px; 
  }
  
  .timeline.dark ::-webkit-scrollbar-thumb:hover { 
    background: #7B61FF; 
  }
  </style>
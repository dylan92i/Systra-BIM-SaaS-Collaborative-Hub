<template>
    <div class="bg-dark-red fit-parent row-layout">
      <!-- Colonne gauche -->
      <div class="left-col">
        <div class="language-select-wrapper">
          <LanguageSelect />
        </div>
      </div>
  
      <!-- Colonne droite -->
      <div class="visual-col">
        <div class="visual-card">
          <div class="visual-title">Espace visuel</div>
          <label class="topbar-switch">
            <input type="checkbox" v-model="showTopBar" />
            <span>Afficher la TopBar</span>
          </label>
          <label class="color-label">
            Couleur de la TopBar&nbsp;:
            <input type="color" v-model="topBarColor" />
          </label>
        </div>
      </div>
      <slot />
    </div>
  </template>
  
  <script setup>
  import { inject, ref } from 'vue'
import LanguageSelect from "@/components/LanguageSelect.vue"
const showTopBar = inject('showTopBar')
const topBarColor = inject('topBarColor')
const fontFamily = inject('fontFamily')

// Quelques polices populaires :
const availableFonts = [
  { label: 'Inter', value: "Inter, Arial, sans-serif" },
  { label: 'Roboto', value: "Roboto, Arial, sans-serif" },
  { label: 'Montserrat', value: "Montserrat, Arial, sans-serif" },
  { label: 'Nunito', value: "Nunito, Arial, sans-serif" },
  { label: 'System', value: "system-ui, Arial, sans-serif" }
]
  </script>
  
  <style scoped>
  .bg-dark-red {
    background: #250a0a;
  }
  .fit-parent {
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    overflow: hidden;
    display: flex;
  }
  .row-layout {
    flex-direction: row;
    align-items: flex-start;
    justify-content: flex-start;
  }
  .left-col {
    flex: 0 0 260px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    padding-top: 32px;
  }
  .language-select-wrapper {
    margin-left: 22px;
    padding: 7px 12px;
    background: rgba(45, 18, 18, 0.87);
    border: 1.5px solid #4b2222;
    border-radius: 11px;
    box-shadow: 0 3px 14px rgba(30,0,0,0.13);
    width: fit-content;
  }
  /* Colonne droite (visual) */
  .visual-col {
    flex: 1;
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
    min-width: 0;
    padding: 40px 36px 0 14px;
  }
  .visual-card {
    background: linear-gradient(100deg, #291010 80%, #540f17 100%);
    border: 1.8px solid #7a2327;
    border-radius: 16px;
    box-shadow: 0 6px 24px rgba(70,10,30, 0.14);
    padding: 34px 38px 28px 38px;
    min-width: 260px;
    min-height: 130px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  .visual-title {
    color: #ffb4b4;
    font-size: 1.12em;
    letter-spacing: .5px;
    font-weight: 600;
    margin-bottom: 26px;
  }
  .topbar-switch {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    font-size: 1.07em;
    color: #ffe4e4;
    background: rgba(110,18,38,0.13);
    padding: 11px 16px;
    border-radius: 8px;
    transition: background .18s;
    font-weight: 500;
    cursor: pointer;
    margin-bottom: 20px;
  }
  .topbar-switch:hover {
    background: rgba(213,71,71,0.12);
  }
  .topbar-switch input[type="checkbox"] {
    accent-color: #be4d4d;
    width: 17px;
    height: 17px;
  }
  .color-label {
    display: flex;
    align-items: center;
    gap: 10px;
    color: #ffb4b4;
    font-size: 1.03em;
    margin-top: 2px;
  }
  .color-label input[type="color"] {
    border: none;
    background: none;
    width: 32px;
    height: 32px;
    cursor: pointer;
    padding: 0;
  }
  @media (max-width: 900px) {
    .fit-parent {
      flex-direction: column;
    }
    .visual-col {
      justify-content: center;
      padding: 20px 0 0 0;
    }
    .left-col {
      align-items: center;
      padding-top: 16px;
    }
  }
  </style>
  
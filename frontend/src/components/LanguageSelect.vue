<template>
  <div class="dropdown-container">
    <div class="dropdown-selected" @click="toggleDropdown">
      <img
        class="flag"
        :src="selectedLanguage.flag"
        :alt="selectedLanguage.label"
      />
      <span class="selected-label">{{ selectedLanguage.label }}</span>
      <span class="arrow">&#9662;</span>
    </div>
    <div v-if="showDropdown" class="dropdown-menu">
      <svg class="dropdown-tip" width="36" height="16">
        <polygon points="18,0 36,16 0,16" />
      </svg>
      <div
        v-for="lang in languages"
        :key="lang.code"
        :class="['dropdown-item', { active: lang.code === selectedLanguage.code }]"
        @click="selectLanguage(lang)"
      >
        <img class="flag" :src="lang.flag" :alt="lang.label" />
        <span>{{ lang.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import { useI18n } from "vue-i18n";

const { locale } = useI18n();
const showDropdown = ref(false);

const languages = [
  { code: "en", label: "English", flag: "https://flagcdn.com/gb.svg" },
  { code: "fr", label: "Français", flag: "https://flagcdn.com/fr.svg" },
  { code: "ar", label: "العربية", flag: "https://flagcdn.com/sa.svg" },
  { code: "pt", label: "Português", flag: "https://flagcdn.com/pt.svg" },
  { code: "ru", label: "Русский", flag: "https://flagcdn.com/ru.svg" },
  { code: "ja", label: "日本語", flag: "https://flagcdn.com/jp.svg" }
];

// Trouver la langue correspondante au code courant (locale.value)
const findLang = (code) => languages.find(l => l.code === code) || languages[0];

// Initialiser selectedLanguage à la langue du i18n
const selectedLanguage = ref(findLang(locale.value));

function toggleDropdown() {
  showDropdown.value = !showDropdown.value;
}
function selectLanguage(lang) {
  selectedLanguage.value = lang;
  locale.value = lang.code;
  showDropdown.value = false;
}

// Synchronisation si la locale change ailleurs dans l'app
watch(locale, (newLocale) => {
  selectedLanguage.value = findLang(newLocale);
});

// Mise à jour au montage du composant (utile en cas de SSR, etc)
onMounted(() => {
  selectedLanguage.value = findLang(locale.value);
});
</script>

<style scoped>
/* ... (exactement comme ton code d'origine) ... */
.dropdown-container {
  position: relative;
  width: 180px;
  margin: 0 auto 20px;
  font-family: "Inter", sans-serif;
}

.dropdown-selected {
  display: flex;
  align-items: center;
  background: #1f1f1f;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  color: #f3f3f3;
  gap: 8px;
  font-weight: 500;
  border: 1px solid #3a1e1e;
  transition: border-color 0.2s;
}

.dropdown-selected:hover {
  border-color: #d84b4b;
}

.arrow {
  margin-left: auto;
  font-size: 12px;
  color: #c75050;
}

.dropdown-menu {
  position: absolute;
  top: 44px;
  left: 0;
  width: 100%;
  background: #2b1f1f;
  border-radius: 10px;
  box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
  z-index: 20;
  padding: 10px 0;
  animation: fadein 120ms;
  border: 1px solid #3d2020;
}

@keyframes fadein {
  from { opacity: 0; }
  to { opacity: 1; }
}

.dropdown-tip {
  position: absolute;
  top: -16px;
  left: 30px;
}

.dropdown-tip polygon {
  fill: #2b1f1f;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 8px 14px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 6px;
  margin: 0 6px;
  transition: background 0.15s, transform 0.15s;
  color: #f1dddd;
  gap: 10px;
  font-weight: 500;
}

.dropdown-item.active {
  background: #3d2222;
  color: #ffffff;
}

.dropdown-item:hover {
  background: #472525;
  color: #ffffff;
  transform: scale(1.04) translateY(-2px);
  box-shadow: 0 2px 12px rgba(255, 80, 80, 0.05);
}

.flag {
  width: 22px;
  height: 16px;
  object-fit: contain;
  border-radius: 2px;
  border: 1px solid #4b2a2a;
  background: #2a1e1e;
}

.selected-label {
  text-shadow: none;
}
</style>

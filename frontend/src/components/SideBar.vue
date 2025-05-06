<template>
  <div
    class="sidebar"
    :style="{
      width: isCollapsed ? collapsedWidth : ui_config.side_bar_width,
      height: sidebarHeight
    }"
  >
    <!-- Bouton Toggle -->
    <button
      class="toggle-btn"
      @click="toggleSidebar"
      :title="isCollapsed ? $t('sidebar_toggle_open') : $t('sidebar_toggle_collapse')"
    >
      <svg
        :style="{ transform: isCollapsed ? 'rotate(180deg)' : 'rotate(0)' }"
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        fill="none"
        viewBox="0 0 24 24"
      >
        <path
          d="M9 6l6 6-6 6"
          stroke="#fff"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>

    <!-- Projects -->
    <router-link to="/main/project" custom v-slot="{ navigate }">
      <button class="menu-btn" @click="navigate">
        <span v-if="!isCollapsed">{{ $t('sidebar_projects') }}</span>
        <span v-else>
          <svg width="20" height="20" fill="#fff"><circle cx="10" cy="10" r="8"/></svg>
        </span>
      </button>
    </router-link>

    <!-- Files -->
    <router-link to="/main/files" custom v-slot="{ navigate }">
      <button class="menu-btn" @click="navigate">
        <span v-if="!isCollapsed">{{ $t('sidebar_files') }}</span>
        <span v-else>
          <svg width="20" height="20" fill="#fff"><rect width="16" height="12" x="2" y="4" rx="3"/></svg>
        </span>
      </button>
    </router-link>

    <!-- IFC Viewer -->
    <router-link to="/main/viewer" custom v-slot="{ navigate }">
      <button class="menu-btn" @click="navigate">
        <span v-if="!isCollapsed">{{ $t('ifc_viewer') }}</span>
        <span v-else>
          <svg width="20" height="20" fill="#fff">
            <ellipse cx="10" cy="10" rx="8" ry="5"/>
            <circle cx="10" cy="10" r="2.5" fill="#b91021"/>
          </svg>
        </span>
      </button>
    </router-link>

    <!-- Disabled: Messages -->
    <button class="menu-btn disabled-btn" disabled>
      <span v-if="!isCollapsed">{{ $t('sidebar_messages') }}</span>
      <span v-else>
        <svg width="20" height="20" fill="#888"><rect x="2" y="4" width="16" height="12" rx="3"/></svg>
      </span>
    </button>
    <div class="spacer"></div>
    <!-- Disabled: Settings -->
    <router-link to="/main/setting" custom v-slot="{ navigate }">
      <button class="menu-btn settings-btn" @click="navigate">
        <span v-if="!isCollapsed">{{ $t('sidebar_settings') }}</span>
        <span v-else>
          <svg width="20" height="20" fill="#fff"><circle cx="10" cy="10" r="8" /></svg>
        </span>
      </button>
    </router-link>
  </div>
</template>

<script setup>
import { ref, computed, inject } from 'vue'
import { ui_config } from '@/config/config'

// Largeur en mode réduit
const collapsedWidth = '62px'
const isCollapsed = ref(false)
function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

// Hauteur dynamique selon topbar
const showTopBar = inject('showTopBar', ref(true))
const topBarHeight = ui_config.top_bar_height || '60px'

// Hauteur calculée
const sidebarHeight = computed(() =>
  showTopBar.value ? `calc(100vh - ${topBarHeight})` : '100vh'
)
</script>

<style scoped>
.sidebar {
  background: #1a191c;
  margin-top: 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 26px 0 18px 0;
  overflow-y: auto;
  box-shadow: 2px 0 14px 0 rgba(115,0,0,0.05);
  border-right: 1px solid #24090f;
  transition:
    width 0.25s cubic-bezier(.68,-0.55,.27,1.55),
    height 0.3s cubic-bezier(.68,-0.55,.27,1.55);
  position: relative;
}

.toggle-btn {
  background: transparent;
  border: none;
  padding: 4px 0 10px 8px;
  cursor: pointer;
  align-self: flex-end;
  margin-right: 8px;
  margin-bottom: 8px;
  transition: background 0.2s;
  border-radius: 100px;
}
.toggle-btn:hover {
  background: #b9102111;
}
.toggle-btn svg {
  transition: transform 0.3s;
}

.menu-btn {
  background: #2d2d2f;
  border: none;
  color: #fff;
  margin: 13px 0 0 16px;
  width: 85%;
  padding: 15px 0;
  border-radius: 12px;
  font-size: 18px;
  font-family: inherit;
  text-align: center;
  cursor: pointer;
  transition:
    background 0.15s,
    color 0.18s,
    transform 0.17s,
    width 0.25s;
  box-shadow: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.menu-btn span {
  transition: opacity 0.18s;
  width: 100%;
}

.menu-btn svg {
  min-width: 18px;
  min-height: 18px;
  max-width: 20px;
  max-height: 20px;
}

.menu-btn:hover {
  background: #b91021;
  color: #fff;
  transform: translateY(-4px);
}

.spacer {
  flex: 1 1 auto;
}

.settings-btn {
  background:rgb(58, 58, 58);
  margin-bottom: 40px;
}
.settings-btn:hover {
  background: #d81e35;
}
</style>

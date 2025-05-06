<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import { fileIcon } from "@/config/os-icon-config";
import { backend_config } from "@/config/system-config.js"
import { useRoute, useRouter } from 'vue-router';
import { useI18n } from 'vue-i18n'

const route = useRoute();
const router = useRouter();

// Etats principaux
const currentFolder = ref("");
const files = ref([]);
const loading = ref(false);
const error = ref("");
const showContext = ref(false);
const contextPos = ref({ x: 0, y: 0 });
const contextType = ref("");
const contextFile = ref(null);

const newFolderName = ref("");
const newFileName = ref("");
const showFolderModal = ref(false);
const showFileModal = ref(false);

const fileInput = ref(null);

const api = axios.create({
  baseURL: backend_config.backend_uri,
  withCredentials: true
});

async function fetchFiles(path = "") {
  loading.value = true;
  error.value = "";
  try {
    let url = "/get_my_files";
    if (path) url += "?folder=" + encodeURIComponent(path);
    const resp = await api.get(url);
    files.value = resp.data.sort((a, b) => {
      if (a.is_dir && !b.is_dir) return -1;
      if (!a.is_dir && b.is_dir) return 1;
      return a.name.localeCompare(b.name);
    });
    currentFolder.value = path;
  } catch (e) {
    error.value = e.response?.data?.message || "Erreur de chargement des fichiers.";
  } finally {
    loading.value = false;
  }
}

// --- Synchroniser navigation avec l'URL --- //
// Charge les fichiers quand l'URL change (=> navigation réactive)
watch(
  () => route.params.catchAll,
  (newPath) => {
    const folderPath = newPath || "";
    fetchFiles(folderPath);
  },
  { immediate: true }
);

function goToFolder(folder) {
  const newPath = currentFolder.value ? currentFolder.value + "/" + folder : folder;
  // Navigue via le routeur (sans reload) :
  router.push('/main/files' + (newPath ? '/' + encodeURIComponent(newPath) : ''));
}

function goUp() {
  if (!currentFolder.value) return;
  const arr = currentFolder.value.split("/");
  arr.pop();
  const upPath = arr.join("/");
  router.push('/main/files' + (upPath ? '/' + encodeURIComponent(upPath) : ''));
}

function formatSize(size) {
  if (size == null) return "-";
  if (size < 1000) return size + " o";
  if (size < 1e6) return (size / 1024).toFixed(1) + " Ko";
  else return (size / 1024 / 1024).toFixed(1) + " Mo";
}

function showContextMenu(e, type = "bg", file = null) {
  e.preventDefault();
  showContext.value = true;
  contextPos.value = { x: e.clientX, y: e.clientY };
  contextType.value = type;
  contextFile.value = file;
  window.addEventListener("click", hideContextMenu);
}
function hideContextMenu() {
  showContext.value = false;
  contextType.value = "";
  contextFile.value = null;
  window.removeEventListener("click", hideContextMenu);
}

async function createFolder() {
  if (!newFolderName.value.trim()) return;
  loading.value = true;
  try {
    await api.post("/create_folder", {
      parent: currentFolder.value,
      name: newFolderName.value,
    });
    fetchFiles(currentFolder.value);
  } catch (e) {
    alert("Erreur création dossier: " + (e.response?.data?.message || ""));
  }
  showFolderModal.value = false;
  newFolderName.value = "";
  loading.value = false;
}

async function createFile() {
  if (!newFileName.value.trim()) return;
  const form = new FormData();
  const blob = new Blob([""], { type: "text/plain" });
  form.append("file", blob, newFileName.value);
  form.append("folder", currentFolder.value);
  loading.value = true;
  try {
    await api.post("/upload_file", form);
    fetchFiles(currentFolder.value);
  } catch (e) {
    alert("Erreur création fichier: " + (e.response?.data?.message || ""));
  }
  showFileModal.value = false;
  newFileName.value = "";
  loading.value = false;
}

async function deleteItem(file) {
  if (!confirm("Supprimer: " + file.name + " ?")) return;
  loading.value = true;
  try {
    await api.post("/delete", { path: currentFolder.value ? currentFolder.value + "/" + file.name : file.name });
    fetchFiles(currentFolder.value);
  } catch (e) {
    alert("Erreur suppression: " + (e.response?.data?.message || ""));
  }
  loading.value = false;
}

function openFileDialog() {
  if (fileInput.value) fileInput.value.value = "";
  fileInput.value?.click();
}
async function onFileInputChange(e) {
  const filesSelected = e.target.files;
  if (!filesSelected || !filesSelected.length) return;
  loading.value = true;
  try {
    for (const file of filesSelected) {
      const form = new FormData();
      form.append("file", file);
      form.append("folder", currentFolder.value);
      await api.post("/upload_file", form);
    }
    await fetchFiles(currentFolder.value);
  } catch (e) {
    alert("Erreur import: " + (e.response?.data?.message || ""));
  }
  loading.value = false;
}

function downloadFile(file) {
  let path = currentFolder.value ? currentFolder.value + "/" + file.name : file.name;
  const url = api.defaults.baseURL + `/download?path=${encodeURIComponent(path)}`;
  const a = document.createElement('a');
  a.href = url;
  a.target = "_blank";
  a.rel = "noopener";
  document.body.appendChild(a);
  a.click();
  setTimeout(() => a.remove(), 900);
}

function onProjectDblClick(file) {
  if (file.is_dir) {
    goToFolder(file.name);
  }
}
</script>

<template>
  <div class="explorer-root"
    @contextmenu="e => showContextMenu(e, 'bg')" tabindex="0">
    <!-- Header -->
    <h2 class="title-main">
      <span class="drop-shadow">🗂️</span>
      {{ $t('explorer_title_main') }}
    </h2>
    <div class="toolbar">
      <button class="btn-main" @click="goUp" :disabled="!currentFolder">
        {{ $t('explorer_btn_up') }}
      </button>
      <span v-if="currentFolder" class="cur-folder"><span>{{ currentFolder }}</span></span>
      <button class="btn-main red" @click="showFolderModal=true">
        {{ $t('explorer_btn_new_folder') }}
      </button>
      <button class="btn-main" @click="showFileModal=true">
        {{ $t('explorer_btn_new_file') }}
      </button>
      <button class="btn-main" @click="openFileDialog">
        {{ $t('explorer_btn_import') }}
      </button>
    </div>
    <transition name="fade">
      <div v-if="loading" class="loading-bar">
        <div class="lds-ellipsis"><div></div><div></div><div></div><div></div></div>
        <span>{{ $t('explorer_loading') }}</span>
      </div>
    </transition>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="files.length === 0 && !loading" class="vide">
      {{ $t('explorer_empty') }}
    </div>
    <!-- Fichier/dossier -->
    <div v-for="file in files" :key="file.name + file.is_dir"
      class="file-row"
      :class="{ folder: file.is_dir }"
      :style="{ cursor: file.is_dir ? 'pointer' : 'default' }"
      @dblclick="onProjectDblClick(file)"
      @contextmenu="e => showContextMenu(e, 'file', file)"
      :title="file.name"
      tabindex="0"
    >
      <span class="file-name" :class="{ folder: file.is_dir }">
        <span class="icon">{{ fileIcon(file) }}</span>
        {{ file.name }}
        <span v-if="file.is_dir" class="badge-folder">
          {{ $t('explorer_folder_badge') }}
        </span>
      </span>
      <span class="file-ext" v-if="!file.is_dir">
        {{ "." + file.name.split('.').pop().toLowerCase() }}
      </span>
      <span class="file-size">{{ formatSize(file.size) }}</span>
      <span class="file-actions">
        <button
          v-if="!file.is_dir"
          class="act-btn"
          :title="$t('explorer_btn_download', { name: file.name })"
          @click.stop="downloadFile(file)">
          ⬇️
        </button>
        <button
          class="act-btn delete"
          :title="$t('explorer_btn_delete', { name: file.name })"
          @click.stop="deleteItem(file)">
          🗑️
        </button>
      </span>
    </div>
    <!-- CONTEXT MENU -->
    <teleport to="body">
      <ul
        v-if="showContext"
        class="context-menu"
        :style="{ top: contextPos.y + 'px', left: contextPos.x + 'px' }"
      >
        <li v-if="contextType === 'bg'" @click="showFolderModal=true; hideContextMenu()">
          ➕ {{ $t('explorer_context_new_folder') }}
        </li>
        <li v-if="contextType === 'bg'" @click="showFileModal=true; hideContextMenu()">
          📄 {{ $t('explorer_context_new_file') }}
        </li>
        <li v-if="contextType === 'bg'" @click="openFileDialog(); hideContextMenu()">
          📤 {{ $t('explorer_context_import') }}
        </li>
        <li v-if="contextType === 'file'" @click="deleteItem(contextFile); hideContextMenu()">
          🗑️ {{ $t('explorer_context_delete') }}
        </li>
      </ul>
    </teleport>
    <input ref="fileInput" type="file" multiple style="display:none" @change="onFileInputChange" />
    <!-- MODALS -->
    <teleport to="body">
      <div class="modal-bg" v-if="showFolderModal">
        <div class="modal-win">
          <h3>{{ $t('explorer_modal_new_folder_title') }}</h3>
          <input v-model="newFolderName" @keyup.enter="createFolder"
            :placeholder="$t('explorer_modal_new_folder_placeholder')" />
          <div class="modal-actions">
            <button class="btn-main red" @click="createFolder">
              {{ $t('explorer_modal_create') }}
            </button>
            <button class="btn-main" @click="showFolderModal=false">
              {{ $t('explorer_modal_cancel') }}
            </button>
          </div>
        </div>
      </div>
      <div class="modal-bg" v-if="showFileModal">
        <div class="modal-win">
          <h3>{{ $t('explorer_modal_new_file_title') }}</h3>
          <input v-model="newFileName" @keyup.enter="createFile"
            :placeholder="$t('explorer_modal_new_file_placeholder')" />
          <div class="modal-actions">
            <button class="btn-main red" @click="createFile">
              {{ $t('explorer_modal_create') }}
            </button>
            <button class="btn-main" @click="showFileModal=false">
              {{ $t('explorer_modal_cancel') }}
            </button>
          </div>
        </div>
      </div>
    </teleport>
  </div>
</template>

<style lang="scss" scoped>
/* ----------------- VARIABLES THEME sombre/rouge ----------------- */
$bg-main: #151016;
$bg-sec: #1e1723;
$bg-ter: #231929;
$red-acc: #ff3355;
$red-hover: #ff1140;
$txt-main: #f7f5fa;
$txt-light: #efe7f2;
$txt-grey: #837e91;
$txt-danger: #ff657d;
$box-shadow: 0 4px 22px #0002, 0 2px 0 #570a1b0d;
$border: 1.4px solid #29151e;
$trans: cubic-bezier(.7,0,.23,1);

/* ================== RACINE =================== */
.explorer-root {
  font-family: 'Inter', 'Roboto', Arial, sans-serif;
  background: $bg-main;
  box-shadow: 0 10px 44px #1c050524, 0 0 2px #ff325606, 0 0 0 1px #ff335505;
  padding: 30px 28px 32px;
  width: 100%;
  min-height: 100vh; // 👈 assure que le fond couvre au moins toute la hauteur de l'écran
  position: relative;
  outline: none;
  box-sizing: border-box;
}

.title-main {
  color: $txt-main;
  margin-bottom: 34px;
  font-weight: 800;
  font-size: 2.15em;
  display: flex; align-items: center; gap:10px;
  letter-spacing: .03em;
  .red-acc { color: $red-acc; text-shadow: 0 0 5px #ff003820;}
  .drop-shadow { filter: drop-shadow(0 0 5px $red-acc);}
}

.toolbar {
  display: flex; flex-wrap: wrap; align-items: center; gap: 12px 18px;
  margin-bottom: 19px;
  .cur-folder {
    font-size:1.01em;
    font-weight:500;
    opacity:.93;
    color: $red-acc;
    margin-left:7px;
    background: $bg-ter;
    padding:4.5px 13px 4.5px 13px;
    border-radius: 7px;
    box-shadow: 0 1.5px 7px #ff335507;
    font-family: 'Menlo', 'Roboto Mono', Consolas, monospace;
    letter-spacing: .01em;
    user-select: all;
  }
}

.btn-main {
  background: linear-gradient(90deg, darken($bg-sec, 4%), lighten($red-acc, 7%) 140%);
  color: $txt-main;
  font-weight: 600;
  font-size: 1.07rem;
  border-radius: 8px;
  border: none;
  padding: 9px 23px;
  cursor: pointer;
  box-shadow: 0 3px 16px #ff335505, 0 1px 0 #fff1;
  outline: none;
  transition: box-shadow .19s $trans, background .14s $trans, color .18s, transform .21s $trans;
  margin-right:1px;
  letter-spacing: .01em;
  &:hover:not(:disabled), &:focus-visible {
    background: $red-hover;
    color: white;
    box-shadow: 0 6px 24px #ff003710, 0 1px 0 #fff1;
    transform: scale(1.08) translateY(-2px);
    z-index: 3;
  }
  &:disabled {
    opacity: 0.55;
    pointer-events: none;
    filter: grayscale(0.88) brightness(1.15);
  }
  &.red {
    background: linear-gradient(90deg, $red-acc 92%, $red-hover 130%);
    color: #fff9;
    &:hover:not(:disabled), &:focus-visible {
      background: $red-hover;
      color: #fff;
      filter: brightness(1.08);
    }
  }
}

.loading-bar {
  display: flex;
  align-items: center;
  gap: 21px;
  padding: 21px 0;
  color: $red-acc;
  font-weight: 600;
  font-size: 1.17em;
  .lds-ellipsis {
    display: inline-block; position:relative; width:54px; height:14px;
    div { position:absolute; top:6px; width:9px; height:9px; border-radius:50%; background:$red-acc; animation-timing-function: cubic-bezier(0,1,1,0);}
    div:nth-child(1) { left:6px;   animation:lds-ellipsis1 .6s infinite;}
    div:nth-child(2) { left:6px;   animation:lds-ellipsis2 .6s infinite;}
    div:nth-child(3) { left:26px;  animation:lds-ellipsis2 .6s infinite;}
    div:nth-child(4) { left:44px;  animation:lds-ellipsis3 .6s infinite;}
    @keyframes lds-ellipsis1 { 0%{transform:scale(0);} 100%{transform:scale(1);} }
    @keyframes lds-ellipsis2 { 0%{transform:translateX(0);} 100%{transform:translateX(20px);} }
    @keyframes lds-ellipsis3 { 0%{transform:scale(1);} 100%{transform:scale(0);} }
  }
}

.error {
  color: #fff;
  background: #a50936c6;
  border-left: 8px solid #ff3355;
  border-radius: 9px;
  padding: 14px 19px;
  margin: 18px 0 19px 0;
  font-weight: 550;
  letter-spacing:.025em;
  box-shadow: 0 3px 15px #44001811;
  animation: shake .19s cubic-bezier(.2,.51,0,1.49);
}
@keyframes shake { 0%{transform:translateX(-4px);} 50%{transform:translateX(3px);} 100%{transform:translateX(0);} }

.vide {
  color: $txt-grey;
  margin: 31px 0 21px 0;
  font-size: 1.11em;
  text-shadow: 0 0 4px #2b05238f;
}

.file-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: $bg-sec;
  padding: 14.5px 19px;
  margin-bottom: 7.5px;
  border-radius: 9px;
  border: $border;
  font-size:1.07em;
  user-select: none;
  transition: box-shadow .19s $trans, transform .23s $trans, background .17s $trans;
  box-shadow: 0 1.5px 10px #ff335504;
  outline: none;
  position: relative;
  z-index: 1;
  &:hover, &:focus-visible {
    box-shadow: 0 4px 24px #ff335511, 0 2px 14px #33001532;
    transform: scale(1.017) translateY(-2px);
    z-index: 4;
    background: $bg-ter;
    .file-name {
      color: $red-acc;
      text-shadow: 0 0 6px #ff345914;
      .icon { filter: drop-shadow(0 1px 3px #ff335530); color:$red-acc;}
    }
    .file-actions .act-btn {
      opacity: 1;
      pointer-events: all;
      filter: brightness(1.2);
    }
  }
  &:active {
    transform: scale(.989) translateY(1.5px);
    box-shadow: 0 2px 10px #82092836;
  }
  .file-name {
    display: flex;
    align-items: center;
    gap: 14px;
    font-weight: 500;
    color: $txt-main;
    font-size: 1.12em;
    letter-spacing:.01em;

    .icon {
      font-size: 1.34em;
      min-width: 1.35em;
      color: $red-acc;
      filter: drop-shadow(0 1px 2px #ff335517);
      transition: filter .16s, color .19s;
    }
    &.folder {
      font-weight: 700;
      color: $red-acc;
      letter-spacing: .03em;
      .badge-folder {
        font-size: .67em;
        font-weight: 700;
        background: #29111f;
        color: $red-acc;
        margin-left: 12px;
        padding: 2.5px 9px;
        border-radius: 5px;
        text-transform: uppercase;
        filter: drop-shadow(0 2px 6px #ff33551d);
        letter-spacing: .06em;
      }
    }
  }
  .file-ext {
    color: $red-acc;
    font-size: .98em;
    min-width: 76px;
    text-align: left;
    font-family: Consolas,'Roboto Mono',monospace;
    opacity:.88;
    margin-left:9px;
    font-weight: 550;
    text-shadow: 0 0 3px #ff335514;
  }
  .file-size {
    color: $txt-grey;
    text-align: right;
    min-width: 84px;
    font-size: 0.98em;
    font-family:'Roboto Mono', monospace;
    margin-right:12px;
  }
  .file-actions {
    display: flex;
    gap: 8px;
    align-items: center;
    margin-left: 16px;
    min-width:90px;
    .act-btn {
      background: none;
      border: none;
      font-size: 1.27em;
      cursor: pointer;
      padding: 2px 8px;
      color: $txt-grey;
      opacity: .82;
      border-radius: 8px;
      outline: none;
      transition: background .12s, color .15s, opacity .12s, box-shadow .13s;
      transform: translateY(0);
      pointer-events: all;
      &:hover, &:focus-visible {
        color: $red-acc;
        background: #2a0e18;
        opacity: 1;
        box-shadow: 0 3px 12px #ff33551b;
        transform: scale(1.23) translateY(-3px);
      }
      &.delete {
        color: $txt-danger;
        &:hover, &:focus-visible {
          background:#270207;
          color: #fff;
          box-shadow: 0 2px 17px #ff364299;
        }
      }
    }
  }
}

.context-menu {
  position: fixed;
  z-index: 9999;
  background: $bg-ter;
  border: 1.7px solid $red-acc;
  border-radius: 12px;
  box-shadow: 0 15px 60px #ff335537, 0 2px 10px #fff1, 0 0 15px #ff335535;
  min-width: 205px;
  padding: 10px 0;
  margin: 0;
  list-style: none;
  font-size: 1.12em;
  font-weight: 500;
  animation: popCubic .22s;
  li {
    padding: 14px 21px;
    color: $txt-light;
    cursor: pointer;
    transition: background .13s $trans, color .12s, transform .18s $trans;
    &:hover, &:focus-visible {
      background: $red-acc;
      color: white;
      transform: translateX(7px) scale(1.1);
      box-shadow: 0 2px 17px #ff335599;
      outline: none;
    }
    &:active { color:$red-acc; background: #fff2; }
  }
}
@keyframes popCubic { 0%{transform: scale(.65) translateY(-24px); opacity:.6;} 100%{transform: none; opacity:1;} }

/* MODALS & BACKDROPS */
.modal-bg {
  position: fixed; z-index: 10001; left:0; top:0; right:0; bottom:0;
  background: rgba(40,0,23,0.71);
  display: flex; align-items: center; justify-content: center;
  animation: darkIn .21s;
}
@keyframes darkIn {
  0% { background:rgba(40,0,23,0);}
  100% { background:rgba(40,0,23,0.71);}
}
.modal-win {
  background: $bg-ter;
  border-radius: 15px;
  padding: 39px 42px 26px 42px;
  min-width: 340px;
  box-shadow: 0 10px 38px #ff427c18, 0 4px 26px #22001952;
  h3 {
    margin-bottom:17px;
    color:$red-acc;
    font-size:1.19em;
    font-weight:700;
    text-shadow: 0 0 2px #fff5;
  }
  input {
    display:block;
    background: #190b15;
    color:$txt-main;
    font-size: 1.11em;
    margin-bottom:19px;
    padding:11px 15px 11px 14px;
    width:100%;
    border-radius:7px;
    border:1.7px solid #ff33551e;
    transition: border .14s, background .14s;
    box-shadow: 0 1px 8px #61001608;
    &:focus-visible {
      border:2.3px solid $red-acc;
      background: #220c18;
      outline: none;
    }
    &::placeholder { color: #ff7499a0; font-weight: 500; opacity:.79;}
  }
  .modal-actions {
    text-align:right;
  }
}

.fade-enter-active, .fade-leave-active { transition: opacity .2s;}
.fade-enter, .fade-leave-to { opacity: 0;}
</style>

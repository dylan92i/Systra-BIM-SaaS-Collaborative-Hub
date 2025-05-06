<template>
  <div v-if="show" class="modal-overlay" @click.self="close">
    <div class="modal-animate modal">
      <form @submit.prevent="handleCreateProject">
        <h2 class="modal-title" tabindex="0">
          {{ $t('create_project_modal_title') }}
        </h2>
        <div class="form-block">
          <input
            v-model="form.name"
            :placeholder="$t('create_project_name_placeholder')"
            required
            class="field"
          />
        </div>
        <div class="form-block">
          <textarea
            v-model="form.description"
            :placeholder="$t('create_project_desc_placeholder')"
            class="field"
          ></textarea>
        </div>
        <!-- Drag and Drop Zone -->
        <div
          class="drop-zone"
          @dragover.prevent="dragOver = true"
          @dragleave.prevent="dragOver = false"
          @drop.prevent="onDrop"
          :class="{ 'drag-over': dragOver }"
          @click="browseFile"
          tabindex="0"
        >
          <span v-if="!preview">{{ $t('create_project_dropzone_text') }}</span>
          <img
            v-if="preview"
            :src="preview"
            :alt="$t('create_project_preview_alt')"
            class="preview-img"
          />
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="onImageChange"
            style="display:none"
            tabindex="-1"
          />
        </div>
        <div class="modal-actions">
          <button :disabled="loading" type="submit">
            {{ $t('create_project_btn_create') }}
          </button>
          <button type="button" @click="close" class="cancel-btn">
            {{ $t('create_project_btn_cancel') }}
          </button>
        </div>
        <div v-if="error" class="error-mini">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import axios from 'axios'
import { backend_config } from '@/config/system-config.js'
import { useI18n } from 'vue-i18n'

const emit = defineEmits(['created', 'close'])
const props = defineProps({ show: Boolean })

const form = ref({ name: '', description: '' })
const imageFile = ref(null)
const preview = ref('')
const loading = ref(false)
const error = ref('')
const dragOver = ref(false)
const fileInput = ref(null)

watch(() => props.show, val => {
  if (!val) reset()
})

function reset() {
  form.value = { name: '', description: '' }
  imageFile.value = null
  preview.value = ''
  error.value = ''
  dragOver.value = false
}

function onImageChange(e) {
  const file = e.target.files[0]
  if (file) {
    imageFile.value = file
    preview.value = URL.createObjectURL(file)
  }
}

function onDrop(e) {
  dragOver.value = false
  const file = e.dataTransfer.files[0]
  if (file) {
    imageFile.value = file
    preview.value = URL.createObjectURL(file)
  }
}

function browseFile() {
  if (fileInput.value) fileInput.value.click()
}

function close() { emit('close') }

async function handleCreateProject() {
  loading.value = true
  error.value = ''
  let picture_name = ''
  if (imageFile.value) {
    try {
      const formData = new FormData()
      formData.append('image', imageFile.value)
      const res = await axios.post(
        backend_config.backend_uri + '/upload_project_image',
        formData,
        {
          withCredentials: true,
          headers: { 'Content-Type': 'multipart/form-data' }
        }
      )
      picture_name = res.data.image_url
    } catch (e) {
      error.value = $t('create_project_error_upload')
      loading.value = false
      return
    }
  }
  try {
    await axios.post(
      backend_config.backend_uri + '/add_project',
      {
        name: form.value.name,
        description: form.value.description,
        picture: picture_name
      },
      { withCredentials: true }
    )
    emit('created')
    close()
  } catch (e) {
    error.value =
      e.response?.data?.message ||
      e.message ||
      $t('create_project_error_generic')
  }
  loading.value = false
}
</script>

  
  <style scoped>
  /* Overlay qui centre vraiment tout */
  .modal-overlay {
    position: fixed;
    z-index: 1003;
    background: rgba(0,0,0,0.46);
    top:0;left:0;right:0;bottom:0;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .modal {
    background: #200a0a;
    border-radius: 13px;
    max-width: 350px;
    width: 100%;
    padding: 32px 26px 27px 26px;
    box-shadow: 0 2px 42px #ff574025;
    border: 1.3px solid #2e0a0a;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .modal-animate {
    animation: popup-in 0.38s cubic-bezier(.62,-0.08,.38,1.17);
    transition: transform 0.16s;
  }
  @keyframes popup-in {
    from { transform: scale(.85) translateY(25px); opacity: 0;}
    to   { transform: scale(1) translateY(0); opacity: 1;}
  }
  form {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center; /* centre tous les éléments enfants */
    gap: 0;
  }
  .modal-title {
    color: #ff6666;
    text-align: center;
    margin: 0 0 16px 0;
    font-size: 1.28rem;
    font-weight: 700;
    letter-spacing: 0.012em;
    text-shadow: 0 1px 12px #28000042, 0 7px 25px #52000122;
    transition: color .17s, transform .18s, text-shadow .18s;
    outline: none;
    cursor: pointer;
    will-change: transform, text-shadow;
    display: block;
  }
  
  .modal-title:hover, .modal-title:focus {
    color: #ff9e73;
    transform: scale(1.08) translateY(-2px);
    text-shadow: 0 5px 20px #ff5940cc, 0 2px 8px #fff2;
  }
  
  /* Champs d’écriture (hover + focus) */
  .field {
    width: 100%;
    margin-bottom: 17px;
    border-radius: 7px;
    border: 1.4px solid #311314;
    padding: 12px 13px;
    background: #120407;
    color: #ffc1bc;
    font-size: 1.05rem;
    resize: none;
    outline: none;
    box-shadow: 0 1px 8px #0001;
    transition: 
      border .16s, 
      box-shadow .20s,
      background .16s,
      transform .19s;
  }
  .field:hover {
    border-color: #cb7d7d;
    background: #190a0a;
    box-shadow: 0 3px 19px #ff574013;
    transform: scale(1.022);
  }
  .field:focus {
    border-color: #ff6666;
    background: #240d13;
    box-shadow: 0 3px 30px #ff574030;
    transform: scale(1.037);
  }
  
  
  .drop-zone {
    border: 2.3px dashed #964949;
    border-radius: 9px;
    padding: 20px 10px;
    background: #230e10;
    color: #b16d7b;
    text-align: center;
    cursor: pointer;
    margin-bottom: 18px;
    font-size: .99rem;
    user-select: none;
    mix-blend-mode: lighten;
    transition: border-color .21s, background .16s, color .18s, transform .17s;
    outline: none;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  .drop-zone:hover, .drop-zone:focus {
    border-color: #ff6666;
    background: #2e1414;
    color: #ffb3ad;
    transform: translateY(-2px) scale(1.025);
  }
  .drop-zone.drag-over {
    border-color: #74ffac;
    background: #29181a;
    color: #7fff94;
    transform: scale(1.045) translateY(-2px);
  }
  .preview-img {
    display: block;
    margin: 0 auto 12px auto;
  }
  .preview-img img, .drop-zone img {
    max-width: 92px;
    max-height: 82px;
    border-radius: 9px;
    margin-bottom: 0;
    box-shadow: 0 1px 9px #17000015;
    transition: transform .22s;
  }
  .preview-img img:hover, .drop-zone img:hover {
    transform: scale(1.15) rotate(-2deg);
    box-shadow: 0 8px 14px #ff574028;
  }
  .modal-actions {
    display: flex;
    gap: 14px;
    justify-content: center;
    margin-top: 13px;
  }
  button {
    background: #ff6666;
    border: none;
    color: #fff;
    border-radius: 8px;
    padding: 9px 25px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.13s, transform 0.15s, box-shadow .13s;
    box-shadow: 0 2px 12px #24000018;
    outline: none;
  }
  button:hover, button:focus {
    background: #ff9e73;
    transform: translateY(-2px) scale(1.08);
    box-shadow: 0 4px 18px #ff574028;
  }
  button:active { background: #fa5446; }
  button:disabled { background: #e9a3a3; }
  .cancel-btn { background: #311314; color: #ff7569; border: 1px solid #ff6666;}
  .cancel-btn:hover { background: #50231f; color: #ff9898;}
  .error-mini {
    color: #ff4545;
    font-size: 0.98em;
    margin-top: 8px;
    text-align: center;
  }
  .form-block {
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  @media (max-width: 520px) {
    .modal { padding: 9vw 2vw; }
  }
  </style>
  
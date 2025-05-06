<template>
  <div ref="container" class="viewer-container">
    <input
      ref="fileInput"
      type="file"
      accept=".ifc"
      style="display:none"
      @change="onFileChange"
    />
    <button class="load-btn" @click="triggerFileInput">
      {{ $t('load_ifc') }}
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as BUI from '@thatopen/ui';
import * as OBC from '@thatopen/components';
import * as THREE from 'three';
import Stats from 'stats.js';

// Init UI
BUI.Manager.init();

const container = ref(null);
const fileInput = ref(null);
const worldRef = ref(null);
const ifcLoaderRef = ref(null);
const lastIfcModel = ref(null);

onMounted(async () => {
  // Crée et ajoute le viewport
  const viewport = document.createElement('bim-viewport');
  viewport.style.width = "100%";
  viewport.style.height = "100%";
  container.value.appendChild(viewport);

  // Ajoute les stats (FPS) en haut à droite
  const stats = new Stats();
  stats.showPanel(0); // 0 = fps
  stats.dom.style.position = 'absolute';
  stats.dom.style.top = '0px';
  stats.dom.style.right = '0px'; // ICI → Haut droit
  stats.dom.style.left = '';
  stats.dom.style.zIndex = '20';
  container.value.appendChild(stats.dom);

  // --- Init components ---
  const components = new OBC.Components();

  const worlds = components.get(OBC.Worlds);
  const world = worlds.create(
    OBC.SimpleScene,
    OBC.SimpleCamera,
    OBC.SimpleRenderer
  );
  worldRef.value = world;

  world.scene = new OBC.SimpleScene(components);
  world.scene.setup();

  // Lumières
  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.2);
  directionalLight.position.set(10, 10, 10);
  world.scene.three.add(directionalLight);

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  world.scene.three.add(ambientLight);

  world.renderer = new OBC.SimpleRenderer(components, viewport);
  world.camera = new OBC.SimpleCamera(components);

  // Grille
  const viewerGrids = components.get(OBC.Grids);
  viewerGrids.create(world);

  components.init();
  world.camera.controls.setLookAt(12, 6, 8, 0, 2, -2);

  const ifcLoader = components.get(OBC.IfcLoader);
  await ifcLoader.setup();
  ifcLoaderRef.value = ifcLoader;

  // Ajoute stats à chaque rendu
  // Monkey-patch render loop
  const originalRender = world.renderer.three.render.bind(world.renderer.three);
  world.renderer.three.render = (...args) => {
    stats.begin();
    originalRender(...args);
    stats.end();
  };
});

const triggerFileInput = () => {
  fileInput.value.click();
};

const onFileChange = async (event) => {
  const file = event.target.files[0];
  if (file && ifcLoaderRef.value && worldRef.value) {
    if (lastIfcModel.value) {
      worldRef.value.scene.three.remove(lastIfcModel.value);
    }
    const arrayBuffer = await file.arrayBuffer();
    const buffer = new Uint8Array(arrayBuffer);
    const model = await ifcLoaderRef.value.load(buffer);
    worldRef.value.scene.three.add(model);
    lastIfcModel.value = model;
  }
};
</script>

<style scoped>
.viewer-container {
  position: relative;
  width: 100%;
  height: 100.1%;  /* Keep 100.1 */
  min-height: 400px;
  overflow: hidden;

}
.load-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
  background: #1976d2;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 0.8em 1.6em;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.08);
  transition: background 0.22s, transform 0.13s;
}
.load-btn:hover {
  background: #2060a0;
  transform: translateY(-2px) scale(1.03);
}

</style>

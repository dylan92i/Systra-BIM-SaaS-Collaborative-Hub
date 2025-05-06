<template>
    <div 
      class="card"
      :class="customClass"
      @click="handleClick"
    >
      <div class="card-header">
        <template v-if="tag">
          <span 
            class="card-tag"
            :style="tagStyle"
          >{{ tag }}</span>
        </template>
        <img
          v-if="imgSrc"
          :src="imgSrc"
          class="card-img"
          :alt="imgAlt"
          loading="lazy"
        />
        <slot name="header" />
      </div>
      <h2 class="card-title" :style="titleStyle">
        <slot name="title">{{ title }}</slot>
      </h2>
      <div class="card-body" :style="bodyStyle">
        <p class="card-desc">
          <slot name="desc">{{ desc }}</slot>
        </p>
        <slot />
        <div class="card-hover"></div>
      </div>
    </div>
  </template>
  
  <script setup>
  defineProps({
    imgSrc: String,      // url de l'image
    imgAlt: String,      // alt de l'image
    title: String,       // titre par défaut (sinon slot)
    desc: String,        // description (sinon slot)
    tag: String,         // texte du tag (optionnel)
    customClass: String, // ex: "create-card"
    tagStyle: Object,
    titleStyle: Object,
    bodyStyle: Object,
  })
  const emit = defineEmits(['click'])
  function handleClick(event) {
    emit('click', event)
  }
  </script>
  
  <style scoped>
  /* Même CSS que .card et enfants du parent ! */
  .card {
    background: #1a0808;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    border: 1px solid #330a0a;
    min-height: 230px;
  }
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(255, 59, 48, 0.2);
  }
  .card-header {
    position: relative;
    height: 180px;
    overflow: hidden;
  }
  .card-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: all 0.4s ease;
  }
  .card:hover .card-img {
    transform: scale(1.05);
  }
  .card-tag {
    position: absolute;
    top: 15px;
    right: -30px;
    background: #ff3b30;
    color: #fff;
    padding: 6px 35px;
    font-size: 0.85rem;
    transform: rotate(45deg);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    z-index: 1;
  }
  /* Ces classes personnalisées permettent d’égaler exactement l'ancien design */
  .create-card .card-tag {
    right: 15px;
    top: 15px;
    transform: none;
    background: #4ec265;
    font-size: 1.03rem;
    font-weight: 900;
    padding: 8px 19px;
    border-radius: 8px 0 7px 0;
    color: #fff;
    box-shadow: 0 2px 8px rgba(30,180,104,0.22);
  }
  .create-card .card-title {
    color: #4ec265;
  }
  .create-card .card-body {
    background: rgba(20,40,20,0.93);
  }
  .card-title {
    color: #ff9999;
    font-size: 1.3rem;
    font-weight: 600;
    padding: 18px 20px;
    margin: 0;
    background: linear-gradient(180deg, rgba(26, 8, 8, 0.9) 30%, rgba(26, 8, 8, 0.7));
    position: relative;
    z-index: 1;
  }
  .card-body {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    padding: 20px;
    background: rgba(26, 8, 8, 0.95);
    opacity: 0;
    transition: all 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }
  .card:hover .card-body {
    opacity: 1;
  }
  .card:active {
    transform: scale(0.98);
    box-shadow: 0 3px 18px rgba(255, 59, 48, 0.10);
    transition: transform 0.05s, box-shadow 0.07s;
  }
  .card-desc {
    color: #ffd8d6;
    font-size: 0.95rem;
    line-height: 1.4;
    margin: 0;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s ease 0.1s;
  }
  .card:hover .card-desc {
    opacity: 1;
    transform: translateY(0);
  }
  .card-hover {
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    border: 2px solid rgba(255, 59, 48, 0.4);
    border-radius: 12px;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  .card:hover .card-hover {
    opacity: 1;
  }
  /* Responsive */
  @media (max-width: 800px) {
    .card-title {
      font-size: 1.1rem;
      padding: 15px;
    }
    .card-desc {
      font-size: 0.85rem;
    }
  }
  </style>
  
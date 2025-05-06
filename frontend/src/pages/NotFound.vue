<template>
    <div class="page404">
      <!-- 404 not found en haut à gauche -->
      <div
        class="main-title"
        :class="{ hovered: hover, active: mainActive }"
        @mouseover="hover = true"
        @mouseleave="hover = false; mainActive = false"
        @mousedown="mainActive = true"
        @mouseup="mainActive = false"
      >
        404 <span class="sub">Not Found</span>
      </div>
  
      <!-- Logo Systra centré -->
      <div class="logo-center">
        <img src="/systra-logo.png" alt="Systra Logo" />
      </div>
  
      <!-- Message de contact en bas à droite -->
      <div
        class="contact"
        :class="{ hovered: contactHover, active: contactActive }"
        @mouseover="contactHover = true"
        @mouseleave="contactHover = false; contactActive = false"
        @mousedown="contactActive = true"
        @mouseup="contactActive = false"
      >
        Contact the administrator<br>
        <a :href="'mailto:' + config.administrator_email">
        {{ config.administrator_email }}
        </a>
        <br>
        if you found a problem.
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { config } from '@/config/config';

  const hover = ref(false)
  const mainActive = ref(false)
  const contactHover = ref(false)
  const contactActive = ref(false)
  </script>
  
  <style scoped>
  .page404 {
    width: 100vw;
    height: 100vh;
    background: linear-gradient(120deg, #370008 0%, #9d121e 100%);
    position: relative;
    overflow: hidden;
    font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
  }
  
  /* 404 not found en haut à gauche */
  .main-title {
    position: absolute;
    top: 50px;
    left: 65px;
    font-size: 2.7rem;
    font-weight: 800;
    color: #fff;
    background: rgba(224, 40, 40, 0.11);
    border-radius: 14px;
    padding: 12px 36px 10px 22px;
    box-shadow: 0 3px 12px rgba(224,40,40,0.08);
    transition: 
      transform 0.17s cubic-bezier(.48,.8,.44,1.5),
      background 0.14s, 
      text-shadow 0.13s, 
      box-shadow 0.16s;
    cursor: default;
    user-select: none;
    letter-spacing: 2px;
    display: flex;
    align-items: baseline;
    gap: 12px;
  }
  .main-title .sub {
    font-size: 2.7rem;
    font-family: inherit;
    color: #fa7388;
    font-weight: 800;
    margin-left: 12px;
    letter-spacing: 1.5px;
    transition: color 0.12s;
  }
  .main-title.hovered, .main-title:hover {
    transform: scale(1.025) translateY(-2px);
    background: rgba(224,40,40,0.15);
    box-shadow: 0 2px 13px 0 #a6293d27;
    text-shadow: 0 2px 10px #b71c1c2a;
  }
  .main-title.hovered .sub, .main-title:hover .sub {
    color: #ff94a8;
  }
  .main-title.active {
    background: rgba(224,40,40,0.15);
    transform: scale(0.985) translateY(1px);
    box-shadow: 0 0px 8px #b71c1c21;
    color: #ffeef0;
    text-shadow: 0 1px 4px #a6293d21;
  }
  
  /* Logo centré */
  .logo-center {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 1;
  }
  .logo-center img {
    width: 340px;
    max-width: 85vw;
    opacity: 0.96;
    filter: drop-shadow(0 0 24px #f63245a2);
    user-select: none;
  }
  
  /* Contact message en bas à droite */
  .contact {
    position: absolute;
    bottom: 48px;
    right: 68px;
    color: #ffd1d6;
    font-size: 1.01rem;
    background: rgba(60, 8, 24, 0.70);
    padding: 12px 22px 13px 18px;
    border-radius: 12px;
    box-shadow: 0 2px 7px #b71c1c1a;
    font-family: 'Segoe UI', sans-serif;
    z-index: 2;
    min-width: 220px;
    max-width: 93vw;
    line-height: 1.5;
    letter-spacing: 0.2px;
    transition:
      background 0.14s,
      box-shadow 0.15s,
      transform 0.13s;
    cursor: pointer;
    user-select: none;
  }
  .contact a {
    color: #ff8598;
    text-decoration: underline;
    font-weight: 500;
    word-break: break-all;
    transition: color 0.13s, text-decoration-thickness 0.15s;
  }
  .contact.hovered,
  .contact:hover {
    background: rgba(220, 35, 52, 0.11);
    box-shadow: 0 3px 12px #db002629;
    color: #ffe2e6;
    transform: scale(1.018) translateY(-1px);
  }
  .contact.hovered a,
  .contact:hover a {
    color:rgb(255, 255, 255);
    text-decoration-thickness: 1.5px;
  }
  .contact.active {
    background: rgba(255, 30, 80, 0.13);
    box-shadow: 0 1px 6px 2px #ff647716, 0 4px 11px #b71c1c0a;
    color: #fff3f5;
    transform: scale(0.985) translateY(1.5px);
    transition: background 0.11s, box-shadow 0.11s, transform 0.08s;
  }
  .contact.active a {
    color: #fff;
  }
  </style>
  
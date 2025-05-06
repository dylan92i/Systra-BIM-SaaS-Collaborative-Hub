<template>
    <div class="login-viewport">
      <div class="language-wrapper">
        <LanguageSelect />
      </div>
      <div class="login-container">
        <form class="login-form" @submit.prevent="onSubmit">
          <h1 class="title">{{ $t('create_account_title') }}</h1>
          <div v-if="successMessage" class="success-message">
            {{ successMessage }}
          </div>
          <div v-if="errorMessage" class="error-message">
            {{ errorMessage }}
          </div>
          <div class="input-group">
            <input 
              type="text"
              v-model="name"
              :placeholder="$t('create_account_name')"
              required
              class="input-field"
              autocomplete="username"
            />
            <span class="input-icon">{{ $t('create_account_emoticon_name') }}</span>
          </div>
          <div class="input-group">
            <input 
              type="email" 
              v-model="email"
              :placeholder="$t('create_account_email')"
              required
              class="input-field"
              autocomplete="email"
            />
            <span class="input-icon">{{ $t('create_account_emoticon_email') }}</span>
          </div>
          <div class="input-group">
            <input
              type="password"
              v-model="password"
              :placeholder="$t('create_account_password')"
              required
              class="input-field"
              autocomplete="new-password"
            />
            <span class="input-icon">{{ $t('create_account_emoticon_password') }}</span>
          </div>
          <button type="submit" class="submit-btn" :disabled="loading">
            {{ loading ? $t('create_account_signing') : $t('create_account_sign_up') }}
          </button>
          <div class="links">
            <a href="#" class="link" @click.prevent="gotoLogin">{{ $t('create_account_login_redirect') }}</a>
          </div>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import LanguageSelect from '@/components/LanguageSelect.vue';
  import { backend_config } from "@/config/system-config.js"

  const name = ref('');
  const email = ref('');
  const password = ref('');
  const loading = ref(false);
  const errorMessage = ref('');
  const successMessage = ref('');
  const router = useRouter();
  
  const onSubmit = async () => {
    errorMessage.value = '';
    successMessage.value = '';
    loading.value = true;
  
    // Validation basique côté frontend
    if (!name.value.trim() || !email.value.trim() || !password.value.trim()) {
      errorMessage.value = 'Tous les champs sont obligatoires.';
      loading.value = false;
      return;
    }
  
    try {
      const response = await fetch(backend_config.backend_uri + '/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.value,
          email: email.value,
          password: password.value,
        }),
      });
  
      let data;
      try {
        data = await response.json();
      } catch (e) {
        data = null;
      }
  
      if (response.ok) {
        // On attend au moins 1,2s pour UX cohérente
        setTimeout(() => {
          successMessage.value = (data && data.message) ? data.message : 'Compte créé !';
          errorMessage.value = '';
          // Tu peux router automatiquement après succès
          setTimeout(() => { router.push('/'); }, 1500);
          // Reset du formulaire
          name.value = '';
          email.value = '';
          password.value = '';
          loading.value = false;
        }, 700);
      } else {
        // Gestion robuste erreurs précises serveur
        switch (response.status) {
          case 400:
            errorMessage.value = (data && data.message) ? data.message : 'Données manquantes ou invalides.';
            break;
          case 409:
            errorMessage.value = (data && data.message) ? data.message : "L'email est déjà utilisé.";
            break;
          default:
            errorMessage.value = (data && data.message) ? data.message : 'Erreur inconnue.';
        }
        loading.value = false;
      }
    } catch (err) {
      errorMessage.value = "Le serveur est injoignable. Veuillez réessayer plus tard.";
      loading.value = false;
    }
  };
  
  const gotoLogin = () => {
    router.push('/');
  };
  </script>
  
  <style scoped>
  .success-message {
    color: #36e836;
    background: #132d13;
    font-weight: bold;
    border-radius: 5px;
    padding: 8px 12px;
    text-align: center;
    margin-bottom: 1em;
  }
  
  .error-message {
    color: #ff1a1a;
    background: #2d0f0f;
    font-weight: bold;
    border-radius: 5px;
    padding: 8px 12px;
    text-align: center;
    margin-bottom: 1em;
  }
  /* Toute ta feuille de style originale ici */
  .login-viewport {
    min-height: 100vh;
    background: #0a0a0a;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
    padding: 20px;
  }
  .language-wrapper {
    position: absolute;
    top: 24px;
    right: 28px;
    z-index: 10;
  }
  @media (max-width: 600px) {
    .language-wrapper {
      top: 14px;
      right: 10px;
    }
  }
  .login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  .login-form {
    background: rgba(20, 20, 20, 0.95);
    padding: 40px;
    border-radius: 20px;
    width: 100%;
    max-width: 450px;
    box-shadow: 0 15px 30px rgba(255, 0, 0, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
  }
  .title {
    color: #ff1a1a;
    text-align: center;
    margin-bottom: 2rem;
    font-size: 2.5em;
    text-shadow: 0 2px 4px rgba(255, 26, 26, 0.3);
  }
  .input-group {
    position: relative;
    margin-bottom: 1.5rem;
    width: 100%;
  }
  .input-field {
    width: 100%;
    padding: 15px 15px 15px 42px;
    border: 2px solid rgba(255, 26, 26, 0.3);
    border-radius: 10px;
    background: rgba(30, 30, 30, 0.8);
    color: #fff;
    font-size: 16px;
    transition: all 0.3s ease;
    box-sizing: border-box;
  }
  .input-field:focus {
    outline: none;
    border-color: #ff1a1a;
    box-shadow: 0 0 10px rgba(255, 26, 26, 0.3);
  }
  .input-icon {
    position: absolute;
    left: 14px;
    top: 50%;
    transform: translateY(-50%);
    color: rgba(255, 26, 26, 0.7);
    pointer-events: none;
    font-size: 1.15em;
  }
  .submit-btn {
    width: 100%;
    padding: 15px;
    background: linear-gradient(45deg, #ff1a1a, #b30000);
    border: none;
    border-radius: 10px;
    color: white;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .submit-btn:hover {
    background: linear-gradient(45deg, #ff3333, #cc0000);
    box-shadow: 0 5px 15px rgba(255, 26, 26, 0.3);
  }
  .submit-btn:disabled {
    background: linear-gradient(45deg, #5a0000, #3a0000);
    cursor: not-allowed;
  }
  .links {
    margin-top: 1.5rem;
    display: flex;
    justify-content: flex-end;
  }
  .link {
    color: rgba(255, 26, 26, 0.7);
    text-decoration: none;
    font-size: 0.9em;
    transition: color 0.3s ease;
  }
  .link:hover {
    color: #ff1a1a;
    text-decoration: underline;
  }
  @media (max-width: 480px) {
    .login-form {
      padding: 18px;
      max-width: 99vw;
    }
    .title {
      font-size: 2em;
    }
    .input-icon {
      left: 10px;
      font-size: 1em;
    }
  }
  </style>
  
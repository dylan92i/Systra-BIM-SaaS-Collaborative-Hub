<template>
  <!-- Aucun changement dans le template -->
  <div class="login-viewport">
    <div class="language-wrapper">
      <LanguageSelect />
    </div>
    <div class="login-container">
      <form class="login-form" @submit.prevent="onSubmit">
        <h1 class="title">{{ $t('login_company_title') }}</h1>
        
        <div class="input-group">
          <input 
            type="email" 
            v-model="email"
            :placeholder="$t('login_email')"
            required
            class="input-field"
          />
          <span class="input-icon">{{ $t('login_emoticon_email') }}</span>
        </div>
  
        <div class="input-group">
          <input
            type="password"
            v-model="password"
            :placeholder="$t('login_password')"
            required
            class="input-field"
          />
          <span class="input-icon">{{ $t('login_emoticon_password')}}</span>
        </div>
  
        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? $t('login_signing') : $t('login_sign_in') }}
        </button>

        <div v-if="errorMsg" class="error-message">
          {{ errorMsg }}
        </div>

        <div class="links">
          <a href="#" class="link">{{ $t('login_forgot_password') }}</a>
          <a href="#" class="link" @click.prevent="goToCreateAccount">{{ $t('login_create_account') }}</a>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios'; // 1. Importer Axios
import LanguageSelect from '@/components/LanguageSelect.vue';
import { backend_config } from "@/config/system-config.js"

const email = ref('');
const password = ref('');
const loading = ref(false);
const errorMsg = ref('');


const router = useRouter();

const onSubmit = async () => {
  loading.value = true;
  errorMsg.value = '';

  try {
    // 2. Remplacer fetch par Axios
    const { data } = await axios.post(
      backend_config.backend_uri + '/login',
      {
        email: email.value,
        password: password.value,
      },
      {
        withCredentials: true, // 3. Activer les cookies
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    // 4. Si requête réussie (status 2xx)
    router.push('/main');
    
  } catch (error) {
    // 5. Gestion améliorée des erreurs
    if (error.response) {
      switch (error.response.status) {
        case 401:
          errorMsg.value = error.response.data.message || 'Identifiants invalides';
          break;
        case 429:
          errorMsg.value = 'Trop de tentatives - Réessayez plus tard';
          break;
        default:
          errorMsg.value = 'Erreur de connexion - Code ' + error.response.status;
      }
    } else {
      errorMsg.value = 'Connexion impossible au serveur';
    }
  } finally {
    loading.value = false;
  }
};

function goToCreateAccount() {
  router.push('/create_account');
}
</script>

<style scoped>
/* Aucun changement dans les styles */
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
  justify-content: space-between;
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

.error-message {
  margin-top: 10px;
  color: #ff1a1a;
  text-align: center;
  font-size: 1em;
  font-weight: 500;
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

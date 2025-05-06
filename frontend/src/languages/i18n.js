import { createI18n } from 'vue-i18n'

import en from './en'
import fr from './fr'
import es from './es'
import ar from './ar'
import pt from './pt'
import ru from './ru'
import ja from './ja'

const messages = {
  en, fr, es, ar, pt, ru, ja
}

const i18n = createI18n({
  locale: 'en',       // langue par défaut
  fallbackLocale: 'en',
  messages,
})

export default i18n

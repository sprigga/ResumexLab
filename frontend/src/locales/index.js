import { createI18n } from 'vue-i18n'
import zhTW from './zh-TW'
import enUS from './en-US'

const messages = {
  'zh-TW': zhTW,
  'en-US': enUS,
}

const i18n = createI18n({
  legacy: false,
  locale: localStorage.getItem('locale') || 'zh-TW',
  fallbackLocale: 'en-US',
  messages,
})

export default i18n

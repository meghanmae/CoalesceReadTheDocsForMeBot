import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { mdi } from 'vuetify/iconsets/mdi'

import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Provide the useDisplay to other components so that it can be used in testing.

const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    sets: {
      mdi
    }
  },
  theme: {
    defaultTheme: 'dark',
    themes: {
      dark: {
        colors: {
          primary: '#2196F3',
          secondary: '#673AB7',
          error: '#F44336',
          botMessage: '#263238',
          userMessage: '#607D8B'
        }
      },
      light: {
        colors: {
          primary: '#2196F3',
          secondary: '#673AB7',
          error: '#F44336',
          botMessage: '#B0BEC5',
          userMessage: '#ECEFF1'
        }
      }
    }
  }
})

const app = createApp(App)

app.use(vuetify)

app.use(router)

app.mount('#app')

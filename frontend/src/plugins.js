import 'vuetify/styles'; import '@mdi/font/css/materialdesignicons.css'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: { mdi }
  },
  theme: {
    defaultTheme: 'taller',
    themes: {
      taller: {
        dark: false,
        colors: {
          primary: '#A2D2FF', secondary: '#CDB4DB', accent: '#FFAFCC',
          surface: '#FFFFFF', background: '#F8FBFF', error: '#BA1A1A', success: '#2E7D32'
        }
      }
    }
  }
})

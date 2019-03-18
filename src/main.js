import Vue from 'vue'
import App from './js/App.vue'
import router from './js/router'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlusSquare, faMinusSquare, faCoffee } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon, FontAwesomeLayers, FontAwesomeLayersText } from '@fortawesome/vue-fontawesome'

library.add(
  faPlusSquare, 
  faMinusSquare,
  faCoffee
)

Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

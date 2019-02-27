import Vue from 'vue'
import App from './js/App.vue'
import router from './js/router'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import HeaderComp from './components/HeaderComp'

Vue.config.productionTip = false
Vue.component('HeaderComp', HeaderComp)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
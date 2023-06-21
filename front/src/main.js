import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import HeaderComp from './components/HeaderComp'
import LoadButton from './components/LoadButton'

Vue.config.productionTip = false
Vue.component('HeaderComp', HeaderComp)
Vue.component('LoadButton', LoadButton)

new Vue({
  vuetify,
  render: h => h(App)
}).$mount('#app')
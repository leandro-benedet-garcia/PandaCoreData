import '../css_source/libraries.sass'

import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import "prismjs"
import VuePrismEditor from "vue-prism-editor"

Vue.use(BootstrapVue)
Vue.component("prism-editor", VuePrismEditor)

export default { Vue }

import '../css_source/style.sass'
import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'
import "prismjs";
import VuePrismEditor from "vue-prism-editor";


Vue.use(BootstrapVue)
Vue.component("prism-editor", VuePrismEditor);

default_app = new Vue
    el: "#app"
    data:
        code: "function test(){}"

import '../css_source/style.sass'

libraries.Vue.use(libraries.BootstrapVue)
libraries.Vue.component("prism-editor", libraries.VuePrismEditor)

default_app = new libraries.Vue
    el: "#app"
    data:
        code: "function test(){}"

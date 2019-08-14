(function () {
    'use strict';

    var default_app;

    libraries.Vue.use(libraries.BootstrapVue);

    libraries.Vue.component("prism-editor", libraries.VuePrismEditor);

    default_app = new libraries.Vue({
      el: "#app",
      data: {
        code: "function test(){}"
      }
    });

}());

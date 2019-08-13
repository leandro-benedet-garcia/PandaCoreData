import sass from 'rollup-plugin-sass';
import alias from 'rollup-plugin-alias';
import replace from 'rollup-plugin-replace';
import commonjs from 'rollup-plugin-commonjs';
import coffeescript from 'rollup-plugin-coffee-script';
import resolve from 'rollup-plugin-node-resolve';

import fse from 'fs-extra';
import path from 'path';

const available_extensions = ['.mjs', '.js', '.json', '.node', '.coffee'];

const prism_path = 'node_modules/prismjs/themes';
const prism_editor_path = 'node_modules/vue-prism-editor/dist/VuePrismEditor.css';

function copy_file(options) {
    return {
        generateBundle(){
            const targDir = path.dirname(options.dest);
            if (!fse.existsSync(targDir)){
                fse.mkdirSync(targDir);
            }
            fse.copy(options.src, options.dest);
        }
    };
}

export default {
    input: 'panda_core_data/ui/js_source/main.coffee',
    output: {
        file: 'panda_core_data/ui/bundle.js',
        format: 'iife'
    },
    plugins: [
        coffeescript(),
        alias({'vue': require.resolve('vue/dist/vue.esm.browser.js')}),
        sass({output: true, insert: false}),
        resolve({extensions: available_extensions}),
        commonjs({extensions: available_extensions}),
        replace({'process.env.NODE_ENV': JSON.stringify('development')}),
        copy_file({src: prism_path, dest: 'panda_core_data/ui/css_libs/prism_themes'}),
        copy_file({src: prism_editor_path, dest: 'panda_core_data/ui/css_libs/VuePrismEditor.css'})
      ]
};

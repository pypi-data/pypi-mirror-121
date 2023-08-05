"use strict";(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[7900],{35400:(n,r,e)=>{e.d(r,{Z:()=>s});var o=e(94015);var c=e.n(o);var t=e(23645);var a=e.n(t);var i=a()(c());i.push([n.id,'/**\n * "\n *  Using Zenburn color palette from the Emacs Zenburn Theme\n *  https://github.com/bbatsov/zenburn-emacs/blob/master/zenburn-theme.el\n *\n *  Also using parts of https://github.com/xavi/coderay-lighttable-theme\n * "\n * From: https://github.com/wisenomad/zenburn-lighttable-theme/blob/master/zenburn.css\n */\n\n.cm-s-zenburn .CodeMirror-gutters { background: #3f3f3f !important; }\n.cm-s-zenburn .CodeMirror-foldgutter-open, .CodeMirror-foldgutter-folded { color: #999; }\n.cm-s-zenburn .CodeMirror-cursor { border-left: 1px solid white; }\n.cm-s-zenburn.CodeMirror { background-color: #3f3f3f; color: #dcdccc; }\n.cm-s-zenburn span.cm-builtin { color: #dcdccc; font-weight: bold; }\n.cm-s-zenburn span.cm-comment { color: #7f9f7f; }\n.cm-s-zenburn span.cm-keyword { color: #f0dfaf; font-weight: bold; }\n.cm-s-zenburn span.cm-atom { color: #bfebbf; }\n.cm-s-zenburn span.cm-def { color: #dcdccc; }\n.cm-s-zenburn span.cm-variable { color: #dfaf8f; }\n.cm-s-zenburn span.cm-variable-2 { color: #dcdccc; }\n.cm-s-zenburn span.cm-string { color: #cc9393; }\n.cm-s-zenburn span.cm-string-2 { color: #cc9393; }\n.cm-s-zenburn span.cm-number { color: #dcdccc; }\n.cm-s-zenburn span.cm-tag { color: #93e0e3; }\n.cm-s-zenburn span.cm-property { color: #dfaf8f; }\n.cm-s-zenburn span.cm-attribute { color: #dfaf8f; }\n.cm-s-zenburn span.cm-qualifier { color: #7cb8bb; }\n.cm-s-zenburn span.cm-meta { color: #f0dfaf; }\n.cm-s-zenburn span.cm-header { color: #f0efd0; }\n.cm-s-zenburn span.cm-operator { color: #f0efd0; }\n.cm-s-zenburn span.CodeMirror-matchingbracket { box-sizing: border-box; background: transparent; border-bottom: 1px solid; }\n.cm-s-zenburn span.CodeMirror-nonmatchingbracket { border-bottom: 1px solid; background: none; }\n.cm-s-zenburn .CodeMirror-activeline { background: #000000; }\n.cm-s-zenburn .CodeMirror-activeline-background { background: #000000; }\n.cm-s-zenburn div.CodeMirror-selected { background: #545454; }\n.cm-s-zenburn .CodeMirror-focused div.CodeMirror-selected { background: #4f4f4f; }\n',"",{version:3,sources:["webpack://./node_modules/codemirror/theme/zenburn.css"],names:[],mappings:"AAAA;;;;;;;;EAQE;;AAEF,oCAAoC,8BAA8B,EAAE;AACpE,2EAA2E,WAAW,EAAE;AACxF,mCAAmC,4BAA4B,EAAE;AACjE,2BAA2B,yBAAyB,EAAE,cAAc,EAAE;AACtE,gCAAgC,cAAc,EAAE,iBAAiB,EAAE;AACnE,gCAAgC,cAAc,EAAE;AAChD,gCAAgC,cAAc,EAAE,iBAAiB,EAAE;AACnE,6BAA6B,cAAc,EAAE;AAC7C,4BAA4B,cAAc,EAAE;AAC5C,iCAAiC,cAAc,EAAE;AACjD,mCAAmC,cAAc,EAAE;AACnD,+BAA+B,cAAc,EAAE;AAC/C,iCAAiC,cAAc,EAAE;AACjD,+BAA+B,cAAc,EAAE;AAC/C,4BAA4B,cAAc,EAAE;AAC5C,iCAAiC,cAAc,EAAE;AACjD,kCAAkC,cAAc,EAAE;AAClD,kCAAkC,cAAc,EAAE;AAClD,6BAA6B,cAAc,EAAE;AAC7C,+BAA+B,cAAc,EAAE;AAC/C,iCAAiC,cAAc,EAAE;AACjD,gDAAgD,sBAAsB,EAAE,uBAAuB,EAAE,wBAAwB,EAAE;AAC3H,mDAAmD,wBAAwB,EAAE,gBAAgB,EAAE;AAC/F,uCAAuC,mBAAmB,EAAE;AAC5D,kDAAkD,mBAAmB,EAAE;AACvE,wCAAwC,mBAAmB,EAAE;AAC7D,4DAA4D,mBAAmB,EAAE",sourcesContent:['/**\n * "\n *  Using Zenburn color palette from the Emacs Zenburn Theme\n *  https://github.com/bbatsov/zenburn-emacs/blob/master/zenburn-theme.el\n *\n *  Also using parts of https://github.com/xavi/coderay-lighttable-theme\n * "\n * From: https://github.com/wisenomad/zenburn-lighttable-theme/blob/master/zenburn.css\n */\n\n.cm-s-zenburn .CodeMirror-gutters { background: #3f3f3f !important; }\n.cm-s-zenburn .CodeMirror-foldgutter-open, .CodeMirror-foldgutter-folded { color: #999; }\n.cm-s-zenburn .CodeMirror-cursor { border-left: 1px solid white; }\n.cm-s-zenburn.CodeMirror { background-color: #3f3f3f; color: #dcdccc; }\n.cm-s-zenburn span.cm-builtin { color: #dcdccc; font-weight: bold; }\n.cm-s-zenburn span.cm-comment { color: #7f9f7f; }\n.cm-s-zenburn span.cm-keyword { color: #f0dfaf; font-weight: bold; }\n.cm-s-zenburn span.cm-atom { color: #bfebbf; }\n.cm-s-zenburn span.cm-def { color: #dcdccc; }\n.cm-s-zenburn span.cm-variable { color: #dfaf8f; }\n.cm-s-zenburn span.cm-variable-2 { color: #dcdccc; }\n.cm-s-zenburn span.cm-string { color: #cc9393; }\n.cm-s-zenburn span.cm-string-2 { color: #cc9393; }\n.cm-s-zenburn span.cm-number { color: #dcdccc; }\n.cm-s-zenburn span.cm-tag { color: #93e0e3; }\n.cm-s-zenburn span.cm-property { color: #dfaf8f; }\n.cm-s-zenburn span.cm-attribute { color: #dfaf8f; }\n.cm-s-zenburn span.cm-qualifier { color: #7cb8bb; }\n.cm-s-zenburn span.cm-meta { color: #f0dfaf; }\n.cm-s-zenburn span.cm-header { color: #f0efd0; }\n.cm-s-zenburn span.cm-operator { color: #f0efd0; }\n.cm-s-zenburn span.CodeMirror-matchingbracket { box-sizing: border-box; background: transparent; border-bottom: 1px solid; }\n.cm-s-zenburn span.CodeMirror-nonmatchingbracket { border-bottom: 1px solid; background: none; }\n.cm-s-zenburn .CodeMirror-activeline { background: #000000; }\n.cm-s-zenburn .CodeMirror-activeline-background { background: #000000; }\n.cm-s-zenburn div.CodeMirror-selected { background: #545454; }\n.cm-s-zenburn .CodeMirror-focused div.CodeMirror-selected { background: #4f4f4f; }\n'],sourceRoot:""}]);const s=i},23645:n=>{n.exports=function(n){var r=[];r.toString=function r(){return this.map((function(r){var e=n(r);if(r[2]){return"@media ".concat(r[2]," {").concat(e,"}")}return e})).join("")};r.i=function(n,e,o){if(typeof n==="string"){n=[[null,n,""]]}var c={};if(o){for(var t=0;t<this.length;t++){var a=this[t][0];if(a!=null){c[a]=true}}}for(var i=0;i<n.length;i++){var s=[].concat(n[i]);if(o&&c[s[0]]){continue}if(e){if(!s[2]){s[2]=e}else{s[2]="".concat(e," and ").concat(s[2])}}r.push(s)}};return r}},94015:n=>{function r(n,r){return a(n)||t(n,r)||o(n,r)||e()}function e(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}function o(n,r){if(!n)return;if(typeof n==="string")return c(n,r);var e=Object.prototype.toString.call(n).slice(8,-1);if(e==="Object"&&n.constructor)e=n.constructor.name;if(e==="Map"||e==="Set")return Array.from(n);if(e==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(e))return c(n,r)}function c(n,r){if(r==null||r>n.length)r=n.length;for(var e=0,o=new Array(r);e<r;e++){o[e]=n[e]}return o}function t(n,r){var e=n&&(typeof Symbol!=="undefined"&&n[Symbol.iterator]||n["@@iterator"]);if(e==null)return;var o=[];var c=true;var t=false;var a,i;try{for(e=e.call(n);!(c=(a=e.next()).done);c=true){o.push(a.value);if(r&&o.length===r)break}}catch(s){t=true;i=s}finally{try{if(!c&&e["return"]!=null)e["return"]()}finally{if(t)throw i}}return o}function a(n){if(Array.isArray(n))return n}n.exports=function n(e){var o=r(e,4),c=o[1],t=o[3];if(!t){return c}if(typeof btoa==="function"){var a=btoa(unescape(encodeURIComponent(JSON.stringify(t))));var i="sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(a);var s="/*# ".concat(i," */");var A=t.sources.map((function(n){return"/*# sourceURL=".concat(t.sourceRoot||"").concat(n," */")}));return[c].concat(A).concat([s]).join("\n")}return[c].join("\n")}},7900:(n,r,e)=>{e.r(r);e.d(r,{default:()=>s});var o=e(93379);var c=e.n(o);var t=e(35400);var a={};a.insert="head";a.singleton=false;var i=c()(t.Z,a);const s=t.Z.locals||{}},93379:(n,r,e)=>{var o=function n(){var r;return function n(){if(typeof r==="undefined"){r=Boolean(window&&document&&document.all&&!window.atob)}return r}}();var c=function n(){var r={};return function n(e){if(typeof r[e]==="undefined"){var o=document.querySelector(e);if(window.HTMLIFrameElement&&o instanceof window.HTMLIFrameElement){try{o=o.contentDocument.head}catch(c){o=null}}r[e]=o}return r[e]}}();var t=[];function a(n){var r=-1;for(var e=0;e<t.length;e++){if(t[e].identifier===n){r=e;break}}return r}function i(n,r){var e={};var o=[];for(var c=0;c<n.length;c++){var i=n[c];var s=r.base?i[0]+r.base:i[0];var A=e[s]||0;var u="".concat(s," ").concat(A);e[s]=A+1;var f=a(u);var l={css:i[1],media:i[2],sourceMap:i[3]};if(f!==-1){t[f].references++;t[f].updater(l)}else{t.push({identifier:u,updater:b(l,r),references:1})}o.push(u)}return o}function s(n){var r=document.createElement("style");var o=n.attributes||{};if(typeof o.nonce==="undefined"){var t=true?e.nc:0;if(t){o.nonce=t}}Object.keys(o).forEach((function(n){r.setAttribute(n,o[n])}));if(typeof n.insert==="function"){n.insert(r)}else{var a=c(n.insert||"head");if(!a){throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.")}a.appendChild(r)}return r}function A(n){if(n.parentNode===null){return false}n.parentNode.removeChild(n)}var u=function n(){var r=[];return function n(e,o){r[e]=o;return r.filter(Boolean).join("\n")}}();function f(n,r,e,o){var c=e?"":o.media?"@media ".concat(o.media," {").concat(o.css,"}"):o.css;if(n.styleSheet){n.styleSheet.cssText=u(r,c)}else{var t=document.createTextNode(c);var a=n.childNodes;if(a[r]){n.removeChild(a[r])}if(a.length){n.insertBefore(t,a[r])}else{n.appendChild(t)}}}function l(n,r,e){var o=e.css;var c=e.media;var t=e.sourceMap;if(c){n.setAttribute("media",c)}else{n.removeAttribute("media")}if(t&&typeof btoa!=="undefined"){o+="\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(t))))," */")}if(n.styleSheet){n.styleSheet.cssText=o}else{while(n.firstChild){n.removeChild(n.firstChild)}n.appendChild(document.createTextNode(o))}}var d=null;var m=0;function b(n,r){var e;var o;var c;if(r.singleton){var t=m++;e=d||(d=s(r));o=f.bind(null,e,t,false);c=f.bind(null,e,t,true)}else{e=s(r);o=l.bind(null,e,r);c=function n(){A(e)}}o(n);return function r(e){if(e){if(e.css===n.css&&e.media===n.media&&e.sourceMap===n.sourceMap){return}o(n=e)}else{c()}}}n.exports=function(n,r){r=r||{};if(!r.singleton&&typeof r.singleton!=="boolean"){r.singleton=o()}n=n||[];var e=i(n,r);return function n(o){o=o||[];if(Object.prototype.toString.call(o)!=="[object Array]"){return}for(var c=0;c<e.length;c++){var s=e[c];var A=a(s);t[A].references--}var u=i(o,r);for(var f=0;f<e.length;f++){var l=e[f];var d=a(l);if(t[d].references===0){t[d].updater();t.splice(d,1)}}e=u}}}}]);
//# sourceMappingURL=7900.1f30e80c7ca8d5dd09dd.js.map?v=1f30e80c7ca8d5dd09dd
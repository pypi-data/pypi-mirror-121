/*! For license information please see 911.99f4bc262f5a565c61be.js.LICENSE.txt */
(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[911],{7836:e=>{e.exports=function e(t){var r={};var n=arguments[1];if(typeof n==="string"){n={};for(var i=1;i<arguments.length;i++){n[arguments[i]]=true}}for(var a in t){if(n[a])continue;r[a]=t[a]}return r}},36511:(e,t,r)=>{"use strict";var n=r(27418);var i={};if(false){}var a=function e(t){};if(false){}function o(e,t,r,n,i,o,s,c){a(t);if(!e){var p;if(t===undefined){p=new Error("Minified exception occurred; use the non-minified dev environment "+"for the full error message and additional helpful warnings.")}else{var l=[r,n,i,o,s,c];var f=0;p=new Error(t.replace(/%s/g,(function(){return l[f++]})));p.name="Invariant Violation"}p.framesToPop=1;throw p}}var s=function(){};if(false){var c}var p="mixins";function l(e){return e}var f;if(false){}else{f={}}function u(e,t,r){var a=[];var s={mixins:"DEFINE_MANY",statics:"DEFINE_MANY",propTypes:"DEFINE_MANY",contextTypes:"DEFINE_MANY",childContextTypes:"DEFINE_MANY",getDefaultProps:"DEFINE_MANY_MERGED",getInitialState:"DEFINE_MANY_MERGED",getChildContext:"DEFINE_MANY_MERGED",render:"DEFINE_ONCE",componentWillMount:"DEFINE_MANY",componentDidMount:"DEFINE_MANY",componentWillReceiveProps:"DEFINE_MANY",shouldComponentUpdate:"DEFINE_ONCE",componentWillUpdate:"DEFINE_MANY",componentDidUpdate:"DEFINE_MANY",componentWillUnmount:"DEFINE_MANY",UNSAFE_componentWillMount:"DEFINE_MANY",UNSAFE_componentWillReceiveProps:"DEFINE_MANY",UNSAFE_componentWillUpdate:"DEFINE_MANY",updateComponent:"OVERRIDE_BASE"};var c={getDerivedStateFromProps:"DEFINE_MANY_MERGED"};var f={displayName:function(e,t){e.displayName=t},mixins:function(e,t){if(t){for(var r=0;r<t.length;r++){d(e,t[r])}}},childContextTypes:function(e,t){if(false){}e.childContextTypes=n({},e.childContextTypes,t)},contextTypes:function(e,t){if(false){}e.contextTypes=n({},e.contextTypes,t)},getDefaultProps:function(e,t){if(e.getDefaultProps){e.getDefaultProps=v(e.getDefaultProps,t)}else{e.getDefaultProps=t}},propTypes:function(e,t){if(false){}e.propTypes=n({},e.propTypes,t)},statics:function(e,t){m(e,t)},autobind:function(){}};function u(e,t,r){for(var n in t){if(t.hasOwnProperty(n)){if(false){}}}}function h(e,t){var r=s.hasOwnProperty(t)?s[t]:null;if(b.hasOwnProperty(t)){o(r==="OVERRIDE_BASE","ReactClassInterface: You are attempting to override "+"`%s` from your class specification. Ensure that your method names "+"do not overlap with React methods.",t)}if(e){o(r==="DEFINE_MANY"||r==="DEFINE_MANY_MERGED","ReactClassInterface: You are attempting to define "+"`%s` on your component more than once. This conflict may be due "+"to a mixin.",t)}}function d(e,r){if(!r){if(false){var n,i}return}o(typeof r!=="function","ReactClass: You're attempting to "+"use a component class or function as a mixin. Instead, just use a "+"regular object.");o(!t(r),"ReactClass: You're attempting to "+"use a component as a mixin. Instead, just use a regular object.");var a=e.prototype;var c=a.__reactAutoBindPairs;if(r.hasOwnProperty(p)){f.mixins(e,r.mixins)}for(var l in r){if(!r.hasOwnProperty(l)){continue}if(l===p){continue}var u=r[l];var d=a.hasOwnProperty(l);h(d,l);if(f.hasOwnProperty(l)){f[l](e,u)}else{var m=s.hasOwnProperty(l);var y=typeof u==="function";var g=y&&!m&&!d&&r.autobind!==false;if(g){c.push(l,u);a[l]=u}else{if(d){var _=s[l];o(m&&(_==="DEFINE_MANY_MERGED"||_==="DEFINE_MANY"),"ReactClass: Unexpected spec policy %s for key %s "+"when mixing in component specs.",_,l);if(_==="DEFINE_MANY_MERGED"){a[l]=v(a[l],u)}else if(_==="DEFINE_MANY"){a[l]=E(a[l],u)}}else{a[l]=u;if(false){}}}}}}function m(e,t){if(!t){return}for(var r in t){var n=t[r];if(!t.hasOwnProperty(r)){continue}var i=r in f;o(!i,"ReactClass: You are attempting to define a reserved "+'property, `%s`, that shouldn\'t be on the "statics" key. Define it '+"as an instance property instead; it will still be accessible on the "+"constructor.",r);var a=r in e;if(a){var s=c.hasOwnProperty(r)?c[r]:null;o(s==="DEFINE_MANY_MERGED","ReactClass: You are attempting to define "+"`%s` on your component more than once. This conflict may be "+"due to a mixin.",r);e[r]=v(e[r],n);return}e[r]=n}}function y(e,t){o(e&&t&&typeof e==="object"&&typeof t==="object","mergeIntoWithNoDuplicateKeys(): Cannot merge non-objects.");for(var r in t){if(t.hasOwnProperty(r)){o(e[r]===undefined,"mergeIntoWithNoDuplicateKeys(): "+"Tried to merge two objects with the same key: `%s`. This conflict "+"may be due to a mixin; in particular, this may be caused by two "+"getInitialState() or getDefaultProps() methods returning objects "+"with clashing keys.",r);e[r]=t[r]}}return e}function v(e,t){return function r(){var n=e.apply(this,arguments);var i=t.apply(this,arguments);if(n==null){return i}else if(i==null){return n}var a={};y(a,n);y(a,i);return a}}function E(e,t){return function r(){e.apply(this,arguments);t.apply(this,arguments)}}function g(e,t){var r=t.bind(e);if(false){var n,i}return r}function _(e){var t=e.__reactAutoBindPairs;for(var r=0;r<t.length;r+=2){var n=t[r];var i=t[r+1];e[n]=g(e,i)}}var N={componentDidMount:function(){this.__isMounted=true}};var D={componentWillUnmount:function(){this.__isMounted=false}};var b={replaceState:function(e,t){this.updater.enqueueReplaceState(this,e,t)},isMounted:function(){if(false){}return!!this.__isMounted}};var I=function(){};n(I.prototype,e.prototype,b);function x(e){var t=l((function(e,n,a){if(false){}if(this.__reactAutoBindPairs.length){_(this)}this.props=e;this.context=n;this.refs=i;this.updater=a||r;this.state=null;var s=this.getInitialState?this.getInitialState():null;if(false){}o(typeof s==="object"&&!Array.isArray(s),"%s.getInitialState(): must return an object or null",t.displayName||"ReactCompositeComponent");this.state=s}));t.prototype=new I;t.prototype.constructor=t;t.prototype.__reactAutoBindPairs=[];a.forEach(d.bind(null,t));d(t,N);d(t,e);d(t,D);if(t.getDefaultProps){t.defaultProps=t.getDefaultProps()}if(false){}o(t.prototype.render,"createClass(...): Class specification must implement a `render` method.");if(false){}for(var n in s){if(!t.prototype[n]){t.prototype[n]=null}}return t}return x}e.exports=u},72555:(e,t,r)=>{"use strict";var n=r(77865);var i=r(36511);if(typeof n==="undefined"){throw Error("create-react-class could not find the React object. If you are using script tags, "+"make sure that React is being loaded before create-react-class.")}var a=(new n.Component).updater;e.exports=i(n.Component,n.isValidElement,a)},63150:e=>{"use strict";var t=/[|\\{}()[\]^$+*?.]/g;e.exports=function(e){if(typeof e!=="string"){throw new TypeError("Expected a string")}return e.replace(t,"\\$&")}},27418:e=>{"use strict";var t=Object.getOwnPropertySymbols;var r=Object.prototype.hasOwnProperty;var n=Object.prototype.propertyIsEnumerable;function i(e){if(e===null||e===undefined){throw new TypeError("Object.assign cannot be called with null or undefined")}return Object(e)}function a(){try{if(!Object.assign){return false}var e=new String("abc");e[5]="de";if(Object.getOwnPropertyNames(e)[0]==="5"){return false}var t={};for(var r=0;r<10;r++){t["_"+String.fromCharCode(r)]=r}var n=Object.getOwnPropertyNames(t).map((function(e){return t[e]}));if(n.join("")!=="0123456789"){return false}var i={};"abcdefghijklmnopqrst".split("").forEach((function(e){i[e]=e}));if(Object.keys(Object.assign({},i)).join("")!=="abcdefghijklmnopqrst"){return false}return true}catch(a){return false}}e.exports=a()?Object.assign:function(e,a){var o;var s=i(e);var c;for(var p=1;p<arguments.length;p++){o=Object(arguments[p]);for(var l in o){if(r.call(o,l)){s[l]=o[l]}}if(t){c=t(o);for(var f=0;f<c.length;f++){if(n.call(o,c[f])){s[c[f]]=o[c[f]]}}}}return s}},92703:(e,t,r)=>{"use strict";var n=r(50414);function i(){}function a(){}a.resetWarningCache=i;e.exports=function(){function e(e,t,r,i,a,o){if(o===n){return}var s=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. "+"Use PropTypes.checkPropTypes() to call them. "+"Read more at http://fb.me/use-check-prop-types");s.name="Invariant Violation";throw s}e.isRequired=e;function t(){return e}var r={array:e,bool:e,func:e,number:e,object:e,string:e,symbol:e,any:e,arrayOf:t,element:e,elementType:e,instanceOf:t,node:e,objectOf:t,oneOf:t,oneOfType:t,shape:t,exact:t,checkPropTypes:a,resetWarningCache:i};r.PropTypes=r;return r}},45697:(e,t,r)=>{if(false){var n,i}else{e.exports=r(92703)()}},50414:e=>{"use strict";var t="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED";e.exports=t},50911:(e,t,r)=>{var n=r(77865);var i=r(24901);var a=r(63150);var o=r(7836);var s=r(72555);var c=r(45697);function p(e,t){if(!String.prototype.normalize){return e}if(!t){return e.normalize("NFD").replace(/[\u0300-\u036f]/g,"")}else{var r=t.split("");return e.normalize("NFD").replace(/.[\u0300-\u036f]+/g,(function(e){return r.indexOf(e.normalize())>-1?e.normalize():e[0]}))}}var l=s({displayName:"Highlighter",count:0,propTypes:{search:c.oneOfType([c.string,c.number,c.bool,i]).isRequired,caseSensitive:c.bool,ignoreDiacritics:c.bool,diacriticsBlacklist:c.string,matchElement:c.oneOfType([c.string,c.func]),matchClass:c.string,matchStyle:c.object},render:function(){var e=o(this.props,"search","caseSensitive","ignoreDiacritics","diacriticsBlacklist","matchElement","matchClass","matchStyle");return n.createElement("span",e,this.renderElement(this.props.children))},renderElement:function(e){if(this.isScalar()&&this.hasSearch()){var t=this.getSearch();return this.highlightChildren(e,t)}return this.props.children},isScalar:function(){return/string|number|boolean/.test(typeof this.props.children)},hasSearch:function(){return typeof this.props.search!=="undefined"&&this.props.search},getSearch:function(){if(this.props.search instanceof RegExp){return this.props.search}var e="";if(!this.props.caseSensitive){e+="i"}var t=this.props.search;if(typeof this.props.search==="string"){t=a(t)}if(this.props.ignoreDiacritics){t=p(t,this.props.diacriticsBlacklist)}return new RegExp(t,e)},getMatchBoundaries:function(e,t){var r=t.exec(e);if(r){return{first:r.index,last:r.index+r[0].length}}},highlightChildren:function(e,t){var r=[];var n=e;while(n){var i=this.props.ignoreDiacritics?p(n,this.props.diacriticsBlacklist):n;if(!t.test(i)){r.push(this.renderPlain(n));return r}var a=this.getMatchBoundaries(i,t);if(a.first===0&&a.last===0){return r}var o=n.slice(0,a.first);if(o){r.push(this.renderPlain(o))}var s=n.slice(a.first,a.last);if(s){r.push(this.renderHighlight(s))}n=n.slice(a.last)}return r},renderPlain:function(e){this.count++;return n.createElement("span",{key:this.count,children:e})},renderHighlight:function(e){this.count++;return n.createElement(this.props.matchElement,{key:this.count,className:this.props.matchClass,style:this.props.matchStyle,children:e})}});l.defaultProps={caseSensitive:false,ignoreDiacritics:false,diacriticsBlacklist:"",matchElement:"mark",matchClass:"highlight",matchStyle:{}};e.exports=l},24901:e=>{var t=function(e,t,r,n){if(!(e[t]instanceof RegExp)){var i=typeof e[t];return new Error("Invalid "+n+" `"+t+"` of type `"+i+"` "+("supplied to `"+r+"`, expected `RegExp`."))}};e.exports=t}}]);
//# sourceMappingURL=911.99f4bc262f5a565c61be.js.map?v=99f4bc262f5a565c61be
(self["webpackChunk_jupyterlab_application_top"]=self["webpackChunk_jupyterlab_application_top"]||[]).push([[6509,4155],{15966:(t,s,n)=>{"use strict";n.d(s,{Vw:()=>e,Qn:()=>o,CY:()=>r,Ko:()=>c,cq:()=>u,rc:()=>h,x1:()=>a,kr:()=>$,$2:()=>M,jS:()=>O,x:()=>V,RP:()=>ft});const e=1;const o=2;const r=4;const c=8;const i=16;const u=32;const h=64;const a=128;const l=256;const f=512;const p=1024;const d=2048;const g=4096;const b=8192;const w=16384;const y=32768;const m=65536;const v=1<<17;const U=1<<18;const T=1<<19;const A=1<<20;const S=1<<21;const E=1<<22;const x=1<<23;const I=1<<24;const j=1<<25;const C=1<<26;const F=1<<27;const _=1<<28;const k=1<<29;const B=1<<30;const N=null&&1<<31;const L=0;const R=1;const P=3;const D=7;const G=15;const $=31;const M=63;const O=127;const V=255;const K=511;const X=1023;const Y=2047;const H=4095;const W=8191;const Z=16383;const z=32767;const J=65535;const q=v-1;const Q=U-1;const tt=T-1;const st=A-1;const nt=S-1;const et=E-1;const ot=x-1;const rt=I-1;const ct=j-1;const it=C-1;const ut=F-1;const ht=_-1;const at=k-1;const lt=B-1;const ft=2147483647;const pt=4294967295},65679:(t,s,n)=>{"use strict";n.d(s,{Te:()=>c,eh:()=>i,s3:()=>f,Gh:()=>p,f9:()=>d});var e=n(77504);var o=n(64310);const r=t=>new Uint8Array(t);const c=(t,s,n)=>new Uint8Array(t,s,n);const i=t=>new Uint8Array(t);const u=t=>{let s="";for(let n=0;n<t.byteLength;n++){s+=e.IK(t[n])}return btoa(s)};const h=t=>Buffer.from(t.buffer,t.byteOffset,t.byteLength).toString("base64");const a=t=>{const s=atob(t);const n=r(s.length);for(let e=0;e<s.length;e++){n[e]=s.charCodeAt(e)}return n};const l=t=>{const s=Buffer.from(t,"base64");return new Uint8Array(s.buffer,s.byteOffset,s.byteLength)};const f=o.jU?u:h;const p=o.jU?a:l;const d=t=>{const s=r(t.byteLength);s.set(t);return s};const g=t=>{const s=encoding.createEncoder();encoding.writeAny(s,t);return encoding.toUint8Array(s)};const b=t=>decoding.readAny(decoding.createDecoder(t))},64485:(t,s,n)=>{"use strict";n.d(s,{l1:()=>i,v3:()=>u,HN:()=>l,iU:()=>f,kj:()=>d,Jl:()=>b,yg:()=>U,F7:()=>T,kf:()=>E,v_:()=>B,XW:()=>N,UF:()=>P,dD:()=>G,sO:()=>$});var e=n(65679);var o=n(15966);var r=n(14247);class c{constructor(t){this.arr=t;this.pos=0}}const i=t=>new c(t);const u=t=>t.pos!==t.arr.length;const h=(t,s=t.pos)=>{const n=i(t.arr);n.pos=s;return n};const a=(t,s)=>{const n=e.Te(t.arr.buffer,t.pos+t.arr.byteOffset,s);t.pos+=s;return n};const l=t=>a(t,U(t));const f=t=>a(t,t.arr.length-t.pos);const p=t=>t.pos++;const d=t=>t.arr[t.pos++];const g=t=>{const s=t.arr[t.pos]+(t.arr[t.pos+1]<<8);t.pos+=2;return s};const b=t=>{const s=t.arr[t.pos]+(t.arr[t.pos+1]<<8)+(t.arr[t.pos+2]<<16)+(t.arr[t.pos+3]<<24)>>>0;t.pos+=4;return s};const w=t=>{const s=t.arr[t.pos+3]+(t.arr[t.pos+2]<<8)+(t.arr[t.pos+1]<<16)+(t.arr[t.pos]<<24)>>>0;t.pos+=4;return s};const y=t=>t.arr[t.pos];const m=t=>t.arr[t.pos]+(t.arr[t.pos+1]<<8);const v=t=>t.arr[t.pos]+(t.arr[t.pos+1]<<8)+(t.arr[t.pos+2]<<16)+(t.arr[t.pos+3]<<24)>>>0;const U=t=>{let s=0;let n=0;while(true){const e=t.arr[t.pos++];s=s|(e&o.jS)<<n;n+=7;if(e<o.x1){return s>>>0}if(n>35){throw new Error("Integer out of range!")}}};const T=t=>{let s=t.arr[t.pos++];let n=s&o.$2;let e=6;const r=(s&o.rc)>0?-1:1;if((s&o.x1)===0){return r*n}while(true){s=t.arr[t.pos++];n=n|(s&o.jS)<<e;e+=7;if(s<o.x1){return r*(n>>>0)}if(e>41){throw new Error("Integer out of range!")}}};const A=t=>{const s=t.pos;const n=U(t);t.pos=s;return n};const S=t=>{const s=t.pos;const n=T(t);t.pos=s;return n};const E=t=>{let s=U(t);if(s===0){return""}else{let n=String.fromCodePoint(d(t));if(--s<100){while(s--){n+=String.fromCodePoint(d(t))}}else{while(s>0){const e=s<1e4?s:1e4;const o=t.arr.subarray(t.pos,t.pos+e);t.pos+=e;n+=String.fromCodePoint.apply(null,o);s-=e}}return decodeURIComponent(escape(n))}};const x=t=>{const s=t.pos;const n=E(t);t.pos=s;return n};const I=(t,s)=>{const n=new DataView(t.arr.buffer,t.arr.byteOffset+t.pos,s);t.pos+=s;return n};const j=t=>I(t,4).getFloat32(0,false);const C=t=>I(t,8).getFloat64(0,false);const F=t=>I(t,8).getBigInt64(0,false);const _=t=>I(t,8).getBigUint64(0,false);const k=[t=>undefined,t=>null,T,j,C,F,t=>false,t=>true,E,t=>{const s=U(t);const n={};for(let e=0;e<s;e++){const s=E(t);n[s]=B(t)}return n},t=>{const s=U(t);const n=[];for(let e=0;e<s;e++){n.push(B(t))}return n},l];const B=t=>k[127-d(t)](t);class N extends c{constructor(t,s){super(t);this.reader=s;this.s=null;this.count=0}read(){if(this.count===0){this.s=this.reader(this);if(u(this)){this.count=U(this)+1}else{this.count=-1}}this.count--;return this.s}}class L extends(null&&c){constructor(t,s){super(t);this.s=s}read(){this.s+=T(this);return this.s}}class R extends(null&&c){constructor(t,s){super(t);this.s=s;this.count=0}read(){if(this.count===0){this.s+=T(this);if(u(this)){this.count=U(this)+1}else{this.count=-1}}this.count--;return this.s}}class P extends c{constructor(t){super(t);this.s=0;this.count=0}read(){if(this.count===0){this.s=T(this);const t=r.GR(this.s);this.count=1;if(t){this.s=-this.s;this.count=U(this)+2}}this.count--;return this.s}}class D extends(null&&c){constructor(t){super(t);this.s=0;this.count=0}read(){if(this.count===0){this.s=T(this);const t=math.isNegativeZero(this.s);this.count=1;if(t){this.s=-this.s;this.count=U(this)+2}}this.count--;return this.s++}}class G extends c{constructor(t){super(t);this.s=0;this.count=0;this.diff=0}read(){if(this.count===0){const t=T(this);const s=t&1;this.diff=t>>1;this.count=1;if(s){this.count=U(this)+2}}this.s+=this.diff;this.count--;return this.s}}class ${constructor(t){this.decoder=new P(t);this.str=E(this.decoder);this.spos=0}read(){const t=this.spos+this.decoder.read();const s=this.str.slice(this.spos,t);this.spos=t;return s}}},19038:(t,s,n)=>{"use strict";n.d(s,{sX:()=>H,GF:()=>$,TS:()=>W,HE:()=>K,Mf:()=>p,kE:()=>d,_f:()=>g,cW:()=>w,EM:()=>G,mK:()=>C,Ep:()=>A,$F:()=>m,HK:()=>F,pY:()=>I,uw:()=>j,uE:()=>x,mP:()=>_});var e=n(65679);var o=n(14247);var r=n(15966);const c=Number.MAX_SAFE_INTEGER;const i=Number.MIN_SAFE_INTEGER;const u=null&&1<<31;const h=r.RP;const a=Number.isInteger||(t=>typeof t==="number"&&isFinite(t)&&o.GW(t)===t);const l=Number.isNaN;class f{constructor(){this.cpos=0;this.cbuf=new Uint8Array(100);this.bufs=[]}}const p=()=>new f;const d=t=>{let s=t.cpos;for(let n=0;n<t.bufs.length;n++){s+=t.bufs[n].length}return s};const g=t=>{const s=new Uint8Array(d(t));let n=0;for(let e=0;e<t.bufs.length;e++){const o=t.bufs[e];s.set(o,n);n+=o.length}s.set(e.Te(t.cbuf.buffer,0,t.cpos),n);return s};const b=(t,s)=>{const n=t.cbuf.length;if(n-t.cpos<s){t.bufs.push(e.Te(t.cbuf.buffer,0,t.cpos));t.cbuf=new Uint8Array(o.Fp(n,s)*2);t.cpos=0}};const w=(t,s)=>{const n=t.cbuf.length;if(t.cpos===n){t.bufs.push(t.cbuf);t.cbuf=new Uint8Array(n*2);t.cpos=0}t.cbuf[t.cpos++]=s};const y=(t,s,n)=>{let e=null;for(let o=0;o<t.bufs.length&&e===null;o++){const n=t.bufs[o];if(s<n.length){e=n}else{s-=n.length}}if(e===null){e=t.cbuf}e[s]=n};const m=w;const v=null&&y;const U=(t,s)=>{w(t,s&binary.BITS8);w(t,s>>>8&binary.BITS8)};const T=(t,s,n)=>{y(t,s,n&binary.BITS8);y(t,s+1,n>>>8&binary.BITS8)};const A=(t,s)=>{for(let n=0;n<4;n++){w(t,s&r.x);s>>>=8}};const S=(t,s)=>{for(let n=3;n>=0;n--){w(t,s>>>8*n&binary.BITS8)}};const E=(t,s,n)=>{for(let e=0;e<4;e++){y(t,s+e,n&binary.BITS8);n>>>=8}};const x=(t,s)=>{while(s>r.jS){w(t,r.x1|r.jS&s);s>>>=7}w(t,r.jS&s)};const I=(t,s)=>{const n=o.GR(s);if(n){s=-s}w(t,(s>r.$2?r.x1:0)|(n?r.rc:0)|r.$2&s);s>>>=6;while(s>0){w(t,(s>r.jS?r.x1:0)|r.jS&s);s>>>=7}};const j=(t,s)=>{const n=unescape(encodeURIComponent(s));const e=n.length;x(t,e);for(let o=0;o<e;o++){w(t,n.codePointAt(o))}};const C=(t,s)=>F(t,g(s));const F=(t,s)=>{const n=t.cbuf.length;const e=t.cpos;const r=o.VV(n-e,s.length);const c=s.length-r;t.cbuf.set(s.subarray(0,r),e);t.cpos+=r;if(c>0){t.bufs.push(t.cbuf);t.cbuf=new Uint8Array(o.Fp(n*2,c));t.cbuf.set(s.subarray(r));t.cpos=c}};const _=(t,s)=>{x(t,s.byteLength);F(t,s)};const k=(t,s)=>{b(t,s);const n=new DataView(t.cbuf.buffer,t.cpos,s);t.cpos+=s;return n};const B=(t,s)=>k(t,4).setFloat32(0,s,false);const N=(t,s)=>k(t,8).setFloat64(0,s,false);const L=(t,s)=>k(t,8).setBigInt64(0,s,false);const R=(t,s)=>k(t,8).setBigUint64(0,s,false);const P=new DataView(new ArrayBuffer(4));const D=t=>{P.setFloat32(0,t);return P.getFloat32(0)===t};const G=(t,s)=>{switch(typeof s){case"string":w(t,119);j(t,s);break;case"number":if(a(s)&&s<=r.RP){w(t,125);I(t,s)}else if(D(s)){w(t,124);B(t,s)}else{w(t,123);N(t,s)}break;case"bigint":w(t,122);L(t,s);break;case"object":if(s===null){w(t,126)}else if(s instanceof Array){w(t,117);x(t,s.length);for(let n=0;n<s.length;n++){G(t,s[n])}}else if(s instanceof Uint8Array){w(t,116);_(t,s)}else{w(t,118);const n=Object.keys(s);x(t,n.length);for(let e=0;e<n.length;e++){const o=n[e];j(t,o);G(t,s[o])}}break;case"boolean":w(t,s?120:121);break;default:w(t,127)}};class $ extends f{constructor(t){super();this.w=t;this.s=null;this.count=0}write(t){if(this.s===t){this.count++}else{if(this.count>0){x(this,this.count-1)}this.count=1;this.w(this,t);this.s=t}}}class M extends(null&&f){constructor(t){super();this.s=t}write(t){I(this,t-this.s);this.s=t}}class O extends(null&&f){constructor(t){super();this.s=t;this.count=0}write(t){if(this.s===t&&this.count>0){this.count++}else{if(this.count>0){x(this,this.count-1)}this.count=1;I(this,t-this.s);this.s=t}}}const V=t=>{if(t.count>0){I(t.encoder,t.count===1?t.s:-t.s);if(t.count>1){x(t.encoder,t.count-2)}}};class K{constructor(){this.encoder=new f;this.s=0;this.count=0}write(t){if(this.s===t){this.count++}else{V(this);this.count=1;this.s=t}}toUint8Array(){V(this);return g(this.encoder)}}class X{constructor(){this.encoder=new f;this.s=0;this.count=0}write(t){if(this.s+this.count===t){this.count++}else{V(this);this.count=1;this.s=t}}toUint8Array(){V(this);return g(this.encoder)}}const Y=t=>{if(t.count>0){const s=t.diff<<1|(t.count===1?0:1);I(t.encoder,s);if(t.count>1){x(t.encoder,t.count-2)}}};class H{constructor(){this.encoder=new f;this.s=0;this.count=0;this.diff=0}write(t){if(this.diff===t-this.s){this.s=t;this.count++}else{Y(this);this.count=1;this.diff=t-this.s;this.s=t}}toUint8Array(){Y(this);return g(this.encoder)}}class W{constructor(){this.sarr=[];this.s="";this.lensE=new K}write(t){this.s+=t;if(this.s.length>19){this.sarr.push(this.s);this.s=""}this.lensE.write(t.length)}toUint8Array(){const t=new f;this.sarr.push(this.s);this.s="";j(t,this.sarr.join(""));F(t,this.lensE.toUint8Array());return g(t)}}},64310:(t,s,n)=>{"use strict";n.d(s,{jS:()=>g,jU:()=>h,UG:()=>u});var e=n(72382);var o=n(77504);const r=t=>t===undefined?null:t;var c=n(62794);var i=n(34155);const u=typeof i!=="undefined"&&i.release&&/node|io\.js/.test(i.release.name);const h=typeof window!=="undefined"&&!u;const a=typeof navigator!=="undefined"?/Mac/.test(navigator.platform):false;let l;const f=[];const p=()=>{if(l===undefined){if(u){l=e.Ue();const t=i.argv;let s=null;for(let n=0;n<t.length;n++){const e=t[n];if(e[0]==="-"){if(s!==null){l.set(s,"")}s=e}else{if(s!==null){l.set(s,e);s=null}else{f.push(e)}}}if(s!==null){l.set(s,"")}}else if(typeof location==="object"){l=e.Ue();(location.search||"?").slice(1).split("&").forEach((t=>{if(t.length!==0){const[s,n]=t.split("=");l.set(`--${o.NF(s,"-")}`,n);l.set(`-${o.NF(s,"-")}`,n)}}))}else{l=e.Ue()}}return l};const d=t=>p().has(t);const g=(t,s)=>p().get(t)||s;const b=t=>u?r(i.env[t.toUpperCase()]):r(c.X.getItem(t));const w=t=>p().get("--"+t)||b(t);const y=t=>d("--"+t)||b(t)!==null;const m=y("production")},72382:(t,s,n)=>{"use strict";n.d(s,{Ue:()=>e,JG:()=>o,Yu:()=>r,UI:()=>c,Yj:()=>i});const e=()=>new Map;const o=t=>{const s=e();t.forEach(((t,n)=>{s.set(n,t)}));return s};const r=(t,s,n)=>{let e=t.get(s);if(e===undefined){t.set(s,e=n())}return e};const c=(t,s)=>{const n=[];for(const[e,o]of t){n.push(s(o,e))}return n};const i=(t,s)=>{for(const[n,e]of t){if(s(e,n)){return true}}return false};const u=(t,s)=>{for(const[n,e]of t){if(!s(e,n)){return false}}return true}},58290:(t,s,n)=>{"use strict";n.d(s,{y:()=>c});var e=n(72382);var o=n(48307);var r=n(7049);class c{constructor(){this._observers=e.Ue()}on(t,s){e.Yu(this._observers,t,o.U).add(s)}once(t,s){const n=(...e)=>{this.off(t,n);s(...e)};this.on(t,n)}off(t,s){const n=this._observers.get(t);if(n!==undefined){n.delete(s);if(n.size===0){this._observers.delete(t)}}}emit(t,s){return r.Dp((this._observers.get(t)||e.Ue()).values()).forEach((t=>t(...s)))}destroy(){this._observers=e.Ue()}}},48307:(t,s,n)=>{"use strict";n.d(s,{U:()=>e});const e=()=>new Set;const o=t=>Array.from(t)},62794:(t,s,n)=>{"use strict";n.d(s,{X:()=>c,z:()=>i});class e{constructor(){this.map=new Map}setItem(t,s){this.map.set(t,s)}getItem(t){return this.map.get(t)}}let o=new e;let r=true;try{if(typeof localStorage!=="undefined"){o=localStorage;r=false}}catch(u){}const c=o;const i=t=>r||addEventListener("storage",t)},77504:(t,s,n)=>{"use strict";n.d(s,{IK:()=>e,NF:()=>h});const e=String.fromCharCode;const o=String.fromCodePoint;const r=t=>t.toLowerCase();const c=/^\s*/g;const i=t=>t.replace(c,"");const u=/([A-Z])/g;const h=(t,s)=>i(t.replace(u,(t=>`${s}${r(t)}`)));const a=t=>unescape(encodeURIComponent(t)).length;const l=t=>{const s=unescape(encodeURIComponent(t));const n=s.length;const e=new Uint8Array(n);for(let o=0;o<n;o++){e[o]=s.codePointAt(o)}return e};const f=typeof TextEncoder!=="undefined"?new TextEncoder:null;const p=t=>f.encode(t);const d=null&&(f?p:l);const g=t=>{let s=t.length;let n="";let e=0;while(s>0){const o=s<1e4?s:1e4;const r=t.subarray(e,e+o);e+=o;n+=String.fromCodePoint.apply(null,r);s-=o}return decodeURIComponent(escape(n))};let b=typeof TextDecoder==="undefined"?null:new TextDecoder("utf-8",{fatal:true,ignoreBOM:true});if(b&&b.decode(new Uint8Array).length===1){b=null}const w=t=>b.decode(t);const y=null&&(b?w:g)},20817:(t,s,n)=>{"use strict";n.d(s,{ZG:()=>o});const e=()=>new Date;const o=Date.now;const r=t=>{if(t<6e4){const s=metric.prefix(t,-1);return math.round(s.n*100)/100+s.prefix+"s"}t=math.floor(t/1e3);const s=t%60;const n=math.floor(t/60)%60;const e=math.floor(t/3600)%24;const o=math.floor(t/86400);if(o>0){return o+"d"+(e>0||n>30?" "+(n>30?e+1:e)+"h":"")}if(e>0){return e+"h"+(n>0||s>30?" "+(s>30?n+1:n)+"min":"")}return n+"min"+(s>0?" "+s+"s":"")}},34155:t=>{var s=t.exports={};var n;var e;function o(){throw new Error("setTimeout has not been defined")}function r(){throw new Error("clearTimeout has not been defined")}(function(){try{if(typeof setTimeout==="function"){n=setTimeout}else{n=o}}catch(t){n=o}try{if(typeof clearTimeout==="function"){e=clearTimeout}else{e=r}}catch(t){e=r}})();function c(t){if(n===setTimeout){return setTimeout(t,0)}if((n===o||!n)&&setTimeout){n=setTimeout;return setTimeout(t,0)}try{return n(t,0)}catch(s){try{return n.call(null,t,0)}catch(s){return n.call(this,t,0)}}}function i(t){if(e===clearTimeout){return clearTimeout(t)}if((e===r||!e)&&clearTimeout){e=clearTimeout;return clearTimeout(t)}try{return e(t)}catch(s){try{return e.call(null,t)}catch(s){return e.call(this,t)}}}var u=[];var h=false;var a;var l=-1;function f(){if(!h||!a){return}h=false;if(a.length){u=a.concat(u)}else{l=-1}if(u.length){p()}}function p(){if(h){return}var t=c(f);h=true;var s=u.length;while(s){a=u;u=[];while(++l<s){if(a){a[l].run()}}l=-1;s=u.length}a=null;h=false;i(t)}s.nextTick=function(t){var s=new Array(arguments.length-1);if(arguments.length>1){for(var n=1;n<arguments.length;n++){s[n-1]=arguments[n]}}u.push(new d(t,s));if(u.length===1&&!h){c(p)}};function d(t,s){this.fun=t;this.array=s}d.prototype.run=function(){this.fun.apply(null,this.array)};s.title="browser";s.browser=true;s.env={};s.argv=[];s.version="";s.versions={};function g(){}s.on=g;s.addListener=g;s.once=g;s.off=g;s.removeListener=g;s.removeAllListeners=g;s.emit=g;s.prependListener=g;s.prependOnceListener=g;s.listeners=function(t){return[]};s.binding=function(t){throw new Error("process.binding is not supported")};s.cwd=function(){return"/"};s.chdir=function(t){throw new Error("process.chdir is not supported")};s.umask=function(){return 0}}}]);
//# sourceMappingURL=6509.3acd40db9cd4cca62dc3.js.map?v=3acd40db9cd4cca62dc3
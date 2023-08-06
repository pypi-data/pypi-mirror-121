/*! For license information please see dd76bc85.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[41581],{35854:(e,t,r)=>{r.d(t,{G:()=>i,R:()=>n});r(65233);var a=r(21006),o=r(98235);const i={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},n=[a.V,o.x,i]},62132:(e,t,r)=>{r.d(t,{K:()=>c});r(65233);var a=r(35854),o=r(49075),i=r(84938);const n={_checkedChanged:function(){a.G._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){i.o._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},c=[o.B,a.R,n]},49075:(e,t,r)=>{r.d(t,{S:()=>n,B:()=>c});r(65233);var a=r(51644),o=r(26110),i=r(84938);const n={observers:["_focusedChanged(receivedFocusFromKeyboard)"],_focusedChanged:function(e){e&&this.ensureRipple(),this.hasRipple()&&(this._ripple.holdDown=e)},_createRipple:function(){var e=i.o._createRipple();return e.id="ink",e.setAttribute("center",""),e.classList.add("circle"),e}},c=[a.P,o.a,i.o,n]},84938:(e,t,r)=>{r.d(t,{o:()=>i});r(65233),r(60748);var a=r(51644),o=r(87156);const i={properties:{noink:{type:Boolean,observer:"_noinkChanged"},_rippleContainer:{type:Object}},_buttonStateChanged:function(){this.focused&&this.ensureRipple()},_downHandler:function(e){a.$._downHandler.call(this,e),this.pressed&&this.ensureRipple(e)},ensureRipple:function(e){if(!this.hasRipple()){this._ripple=this._createRipple(),this._ripple.noink=this.noink;var t=this._rippleContainer||this.root;if(t&&(0,o.vz)(t).appendChild(this._ripple),e){var r=(0,o.vz)(this._rippleContainer||this),a=(0,o.vz)(e).rootTarget;r.deepContains(a)&&this._ripple.uiDownAction(e)}}},getRipple:function(){return this.ensureRipple(),this._ripple},hasRipple:function(){return Boolean(this._ripple)},_createRipple:function(){return document.createElement("paper-ripple")},_noinkChanged:function(e){this.hasRipple()&&(this._ripple.noink=e)}}},32296:(e,t,r)=>{r(65233);var a=r(62132),o=r(49075),i=r(9672),n=r(50856),c=r(87529);const s=n.d`<style>
  :host {
    display: inline-block;
    white-space: nowrap;
    cursor: pointer;
    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);
    /* -1px is a sentinel for the default and is replaced in \`attached\`. */
    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);
    @apply --paper-font-common-base;
    line-height: 0;
    -webkit-tap-highlight-color: transparent;
  }

  :host([hidden]) {
    display: none !important;
  }

  :host(:focus) {
    outline: none;
  }

  .hidden {
    display: none;
  }

  #checkboxContainer {
    display: inline-block;
    position: relative;
    width: var(--calculated-paper-checkbox-size);
    height: var(--calculated-paper-checkbox-size);
    min-width: var(--calculated-paper-checkbox-size);
    margin: var(--paper-checkbox-margin, initial);
    vertical-align: var(--paper-checkbox-vertical-align, middle);
    background-color: var(--paper-checkbox-unchecked-background-color, transparent);
  }

  #ink {
    position: absolute;

    /* Center the ripple in the checkbox by negative offsetting it by
     * (inkWidth - rippleWidth) / 2 */
    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    width: var(--calculated-paper-checkbox-ink-size);
    height: var(--calculated-paper-checkbox-ink-size);
    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
  }

  #ink:dir(rtl) {
    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: auto;
  }

  #ink[checked] {
    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));
  }

  #checkbox {
    position: relative;
    box-sizing: border-box;
    height: 100%;
    border: solid 2px;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    border-radius: 2px;
    pointer-events: none;
    -webkit-transition: background-color 140ms, border-color 140ms;
    transition: background-color 140ms, border-color 140ms;

    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);
    transition-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  /* checkbox checked animations */
  #checkbox.checked #checkmark {
    -webkit-animation: checkmark-expand 140ms ease-out forwards;
    animation: checkmark-expand 140ms ease-out forwards;

    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);
    animation-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  @-webkit-keyframes checkmark-expand {
    0% {
      -webkit-transform: scale(0, 0) rotate(45deg);
    }
    100% {
      -webkit-transform: scale(1, 1) rotate(45deg);
    }
  }

  @keyframes checkmark-expand {
    0% {
      transform: scale(0, 0) rotate(45deg);
    }
    100% {
      transform: scale(1, 1) rotate(45deg);
    }
  }

  #checkbox.checked {
    background-color: var(--paper-checkbox-checked-color, var(--primary-color));
    border-color: var(--paper-checkbox-checked-color, var(--primary-color));
  }

  #checkmark {
    position: absolute;
    width: 36%;
    height: 70%;
    border-style: solid;
    border-top: none;
    border-left: none;
    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-color: var(--paper-checkbox-checkmark-color, white);
    -webkit-transform-origin: 97% 86%;
    transform-origin: 97% 86%;
    box-sizing: content-box; /* protect against page-level box-sizing */
  }

  #checkmark:dir(rtl) {
    -webkit-transform-origin: 50% 14%;
    transform-origin: 50% 14%;
  }

  /* label */
  #checkboxLabel {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    padding-left: var(--paper-checkbox-label-spacing, 8px);
    white-space: normal;
    line-height: normal;
    color: var(--paper-checkbox-label-color, var(--primary-text-color));
    @apply --paper-checkbox-label;
  }

  :host([checked]) #checkboxLabel {
    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));
    @apply --paper-checkbox-label-checked;
  }

  #checkboxLabel:dir(rtl) {
    padding-right: var(--paper-checkbox-label-spacing, 8px);
    padding-left: 0;
  }

  #checkboxLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #checkbox {
    opacity: 0.5;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
  }

  :host([disabled][checked]) #checkbox {
    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #checkboxLabel  {
    opacity: 0.65;
  }

  /* invalid state */
  #checkbox.invalid:not(.checked) {
    border-color: var(--paper-checkbox-error-color, var(--error-color));
  }
</style>

<div id="checkboxContainer">
  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">
    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>
  </div>
</div>

<div id="checkboxLabel"><slot></slot></div>`;s.setAttribute("strip-whitespace",""),(0,i.k)({_template:s,is:"paper-checkbox",behaviors:[a.K],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){(0,c.T8)(this,(function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",r=e.match(/[A-Za-z]+$/);null!==r&&(t=r[0]);var a=parseFloat(e),o=8/3*a;"px"===t&&(o=Math.floor(o))%2!=a%2&&o++,this.updateStyles({"--paper-checkbox-ink-size":o+t})}}))},_computeCheckboxClass:function(e,t){var r="";return e&&(r+="checked "),t&&(r+="invalid"),r},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,o.S._createRipple.call(this)}})},25782:(e,t,r)=>{r(65233),r(65660),r(70019),r(97968);var a=r(9672),o=r(50856),i=r(33760);(0,a.k)({_template:o.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[i.U]})},98626:(e,t,r)=>{r.d(t,{ZH:()=>p,MT:()=>i,U2:()=>s,RV:()=>o,t8:()=>l});var a=r(21354);function o(e){return new Promise(((t,r)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>r(e.error)}))}function i(e,t){const r=(0,a.Z)().then((()=>{const r=indexedDB.open(e);return r.onupgradeneeded=()=>r.result.createObjectStore(t),o(r)}));return(e,a)=>r.then((r=>a(r.transaction(t,e).objectStore(t))))}let n;function c(){return n||(n=i("keyval-store","keyval")),n}function s(e,t=c()){return t("readonly",(t=>o(t.get(e))))}function l(e,t,r=c()){return r("readwrite",(r=>(r.put(t,e),o(r.transaction))))}function p(e=c()){return e("readwrite",(e=>(e.clear(),o(e.transaction))))}},21354:(e,t,r)=>{r.d(t,{Z:()=>a});const a=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let e;return new Promise((t=>{const r=()=>indexedDB.databases().finally(t);e=setInterval(r,100),r()})).finally((()=>clearInterval(e)))}},93217:(e,t,r)=>{r.d(t,{Ud:()=>h});const a=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),i=Symbol("Comlink.releaseProxy"),n=Symbol("Comlink.thrown"),c=e=>"object"==typeof e&&null!==e||"function"==typeof e,s=new Map([["proxy",{canHandle:e=>c(e)&&e[a],serialize(e){const{port1:t,port2:r}=new MessageChannel;return l(e,t),[r,[r]]},deserialize:e=>(e.start(),h(e))}],["throw",{canHandle:e=>c(e)&&n in e,serialize({value:e}){let t;return t=e instanceof Error?{isError:!0,value:{message:e.message,name:e.name,stack:e.stack}}:{isError:!1,value:e},[t,[]]},deserialize(e){if(e.isError)throw Object.assign(new Error(e.value.message),e.value);throw e.value}}]]);function l(e,t=self){t.addEventListener("message",(function r(o){if(!o||!o.data)return;const{id:i,type:c,path:s}=Object.assign({path:[]},o.data),h=(o.data.argumentList||[]).map(m);let d;try{const t=s.slice(0,-1).reduce(((e,t)=>e[t]),e),r=s.reduce(((e,t)=>e[t]),e);switch(c){case"GET":d=r;break;case"SET":t[s.slice(-1)[0]]=m(o.data.value),d=!0;break;case"APPLY":d=r.apply(t,h);break;case"CONSTRUCT":d=function(e){return Object.assign(e,{[a]:!0})}(new r(...h));break;case"ENDPOINT":{const{port1:t,port2:r}=new MessageChannel;l(e,r),d=function(e,t){return b.set(e,t),e}(t,[t])}break;case"RELEASE":d=void 0;break;default:return}}catch(e){d={value:e,[n]:0}}Promise.resolve(d).catch((e=>({value:e,[n]:0}))).then((e=>{const[a,o]=v(e);t.postMessage(Object.assign(Object.assign({},a),{id:i}),o),"RELEASE"===c&&(t.removeEventListener("message",r),p(t))}))})),t.start&&t.start()}function p(e){(function(e){return"MessagePort"===e.constructor.name})(e)&&e.close()}function h(e,t){return u(e,[],t)}function d(e){if(e)throw new Error("Proxy has been released and is not useable")}function u(e,t=[],r=function(){}){let a=!1;const n=new Proxy(r,{get(r,o){if(d(a),o===i)return()=>g(e,{type:"RELEASE",path:t.map((e=>e.toString()))}).then((()=>{p(e),a=!0}));if("then"===o){if(0===t.length)return{then:()=>n};const r=g(e,{type:"GET",path:t.map((e=>e.toString()))}).then(m);return r.then.bind(r)}return u(e,[...t,o])},set(r,o,i){d(a);const[n,c]=v(i);return g(e,{type:"SET",path:[...t,o].map((e=>e.toString())),value:n},c).then(m)},apply(r,i,n){d(a);const c=t[t.length-1];if(c===o)return g(e,{type:"ENDPOINT"}).then(m);if("bind"===c)return u(e,t.slice(0,-1));const[s,l]=k(n);return g(e,{type:"APPLY",path:t.map((e=>e.toString())),argumentList:s},l).then(m)},construct(r,o){d(a);const[i,n]=k(o);return g(e,{type:"CONSTRUCT",path:t.map((e=>e.toString())),argumentList:i},n).then(m)}});return n}function k(e){const t=e.map(v);return[t.map((e=>e[0])),(r=t.map((e=>e[1])),Array.prototype.concat.apply([],r))];var r}const b=new WeakMap;function v(e){for(const[t,r]of s)if(r.canHandle(e)){const[a,o]=r.serialize(e);return[{type:"HANDLER",name:t,value:a},o]}return[{type:"RAW",value:e},b.get(e)||[]]}function m(e){switch(e.type){case"HANDLER":return s.get(e.name).deserialize(e.value);case"RAW":return e.value}}function g(e,t,r){return new Promise((a=>{const o=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");e.addEventListener("message",(function t(r){r.data&&r.data.id&&r.data.id===o&&(e.removeEventListener("message",t),a(r.data))})),e.start&&e.start(),e.postMessage(Object.assign({id:o},t),r)}))}},57835:(e,t,r)=>{r.d(t,{Xe:()=>a.Xe,pX:()=>a.pX,XM:()=>a.XM});var a=r(38941)}}]);
//# sourceMappingURL=dd76bc85.js.map
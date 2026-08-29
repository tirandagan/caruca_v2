import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-radio')){const s=document.createElement('style');s.id='krk-radio';s.textContent=`.krk-radio{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-sans);font-size:14px;color:var(--ink);cursor:pointer}
.krk-radio input{appearance:none;width:14px;height:14px;margin:0;border:2px solid var(--border-strong);border-radius:50%;position:relative;cursor:pointer;transition:border-color .12s ease-out}
.krk-radio input:checked{border-color:var(--blue)}
.krk-radio input:checked::after{content:'';position:absolute;inset:1px;border-radius:50%;background:var(--blue)}
.krk-radio input:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-radio input:disabled{opacity:.45}`;document.head.appendChild(s);}})();
export function Radio({label,...rest}){
  return <label className="krk-radio"><input type="radio" {...rest}/>{label}</label>;
}
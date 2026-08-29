import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-check')){const s=document.createElement('style');s.id='krk-check';s.textContent=`.krk-check{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-sans);font-size:14px;color:var(--ink);cursor:pointer}
.krk-check input{appearance:none;width:14px;height:14px;margin:0;border:2px solid var(--border-strong);border-radius:3px;position:relative;cursor:pointer;transition:background .12s ease-out,border-color .12s ease-out}
.krk-check input:checked{background:var(--blue);border-color:var(--blue)}
.krk-check input:checked::after{content:'\\2713';color:#fff;font-size:10px;position:absolute;top:-2px;left:1px}
.krk-check input:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-check input:disabled{opacity:.45}`;document.head.appendChild(s);}})();
export function Checkbox({label,...rest}){
  return <label className="krk-check"><input type="checkbox" {...rest}/>{label}</label>;
}
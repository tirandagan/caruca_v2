import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-switch')){const s=document.createElement('style');s.id='krk-switch';s.textContent=`.krk-switch{display:inline-flex;align-items:center;gap:8px;font-family:var(--font-sans);font-size:14px;color:var(--ink);cursor:pointer}
.krk-switch input{appearance:none;width:32px;height:18px;margin:0;border-radius:999px;background:var(--border-strong);position:relative;cursor:pointer;transition:background .14s ease-out}
.krk-switch input::after{content:'';position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:left .14s ease-out}
.krk-switch input:checked{background:var(--blue)}
.krk-switch input:checked::after{left:16px}
.krk-switch input:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-switch input:disabled{opacity:.45}`;document.head.appendChild(s);}})();
export function Switch({label,...rest}){
  return <label className="krk-switch"><input type="checkbox" role="switch" {...rest}/>{label}</label>;
}
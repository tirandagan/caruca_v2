import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-select')){const s=document.createElement('style');s.id='krk-select';s.textContent=`.krk-select{height:36px;padding:0 32px 0 12px;font-size:14px;font-family:var(--font-sans);color:var(--ink);background:#fff url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%23616B73' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E") no-repeat right 10px center;border:1px solid var(--border-strong);border-radius:var(--radius-md);appearance:none;cursor:pointer}
.krk-select:hover{border-color:var(--gray-400)}
.krk-select:focus{outline:2px solid var(--blue);outline-offset:1px}
.krk-select:disabled{opacity:.45}`;document.head.appendChild(s);}})();
export function Select({label,hint,options=[],style,...rest}){
  return <label className="krk-field" style={style}>
    {label && <span className="krk-field-label">{label}</span>}
    <select className="krk-select" {...rest}>{options.map(o=>{const v=typeof o==='string'?{value:o,label:o}:o;return <option key={v.value} value={v.value}>{v.label}</option>;})}</select>
    {hint && <span className="krk-field-hint">{hint}</span>}
  </label>;
}
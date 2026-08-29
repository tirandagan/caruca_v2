import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-tabs')){const s=document.createElement('style');s.id='krk-tabs';s.textContent=`.krk-tabs{display:flex;gap:4px;border-bottom:1px solid var(--border-default);font-family:var(--font-sans)}
.krk-tab{appearance:none;background:none;border:none;border-bottom:2px solid transparent;margin-bottom:-1px;padding:9px 14px;font-size:14px;font-weight:600;font-family:var(--font-sans);color:var(--gray-500);cursor:pointer;transition:color .14s ease-out}
.krk-tab:hover{color:var(--ink)}
.krk-tab[aria-selected="true"]{color:var(--blue);border-bottom-color:var(--blue)}
.krk-tab:focus-visible{outline:2px solid var(--blue);outline-offset:-2px}
.krk-tab-count{font-family:var(--font-mono);font-weight:400;font-size:12px;color:var(--gray-400);margin-left:6px}`;document.head.appendChild(s);}})();
export function Tabs({tabs=[],active,onChange}){
  return <div className="krk-tabs" role="tablist">{tabs.map(t=>{const v=typeof t==='string'?{id:t,label:t}:t;
    return <button key={v.id} role="tab" aria-selected={active===v.id} className="krk-tab" onClick={()=>onChange && onChange(v.id)}>{v.label}{v.count!=null && <span className="krk-tab-count">{v.count}</span>}</button>;})}</div>;
}
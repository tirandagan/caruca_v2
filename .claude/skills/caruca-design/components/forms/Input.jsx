import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-input')){const s=document.createElement('style');s.id='krk-input';s.textContent=`.krk-field{font-family:var(--font-sans);display:flex;flex-direction:column;gap:6px}
.krk-field-label{font-size:13px;font-weight:600;color:var(--ink)}
.krk-input{height:36px;padding:0 12px;font-size:14px;font-family:var(--font-sans);color:var(--ink);background:#fff;border:1px solid var(--border-strong);border-radius:var(--radius-md);transition:border-color .14s ease-out}
.krk-input::placeholder{color:var(--gray-400)}
.krk-input:hover{border-color:var(--gray-400)}
.krk-input:focus{outline:2px solid var(--blue);outline-offset:1px;border-color:var(--blue)}
.krk-input:disabled{opacity:.45;background:var(--surface-code)}
.krk-input-mono{font-family:var(--font-mono);font-size:13px}
.krk-input-error{border-color:var(--danger)}
.krk-field-hint{font-size:12px;color:var(--gray-500)}
.krk-field-hint-error{color:var(--danger-text)}`;document.head.appendChild(s);}})();
export function Input({label,hint,error,mono,style,...rest}){
  return <label className="krk-field" style={style}>
    {label && <span className="krk-field-label">{label}</span>}
    <input className={'krk-input'+(mono?' krk-input-mono':'')+(error?' krk-input-error':'')} {...rest}/>
    {(error||hint) && <span className={'krk-field-hint'+(error?' krk-field-hint-error':'')}>{error||hint}</span>}
  </label>;
}
import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-btn')){const s=document.createElement('style');s.id='krk-btn';s.textContent=`.krk-btn{font-family:var(--font-sans);font-weight:600;letter-spacing:.01em;border-radius:var(--radius-md);border:1px solid transparent;cursor:pointer;display:inline-flex;align-items:center;gap:8px;transition:background .14s ease-out,color .14s ease-out,border-color .14s ease-out;white-space:nowrap}
.krk-btn:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.krk-btn:disabled{opacity:.45;cursor:not-allowed}
.krk-btn-sm{height:28px;padding:0 10px;font-size:13px}.krk-btn-md{height:36px;padding:0 14px;font-size:14px}.krk-btn-lg{height:44px;padding:0 18px;font-size:15px}
.krk-btn-primary{background:var(--blue);color:#fff}.krk-btn-primary:hover:not(:disabled){background:var(--blue-hover)}
.krk-btn-secondary{background:#fff;color:var(--ink);border-color:var(--border-strong)}.krk-btn-secondary:hover:not(:disabled){background:var(--surface-code)}
.krk-btn-ghost{background:transparent;color:var(--blue)}.krk-btn-ghost:hover:not(:disabled){background:var(--surface-info)}
.krk-btn-danger{background:var(--danger-text);color:#fff}.krk-btn-danger:hover:not(:disabled){background:#B91C1C}`;document.head.appendChild(s);}})();
export function Button({variant='primary',size='md',icon,children,...rest}){
  return <button className={'krk-btn krk-btn-'+size+' krk-btn-'+variant} {...rest}>{icon}{children}</button>;
}
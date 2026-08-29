import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-card')){const s=document.createElement('style');s.id='krk-card';s.textContent=`.krk-card{font-family:var(--font-sans);background:#fff;border:1px solid var(--border-default);border-radius:var(--radius-md);color:var(--ink)}
.krk-card-head{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:14px 16px;border-bottom:1px solid var(--border-default)}
.krk-card-title{font-size:15px;font-weight:600;letter-spacing:-.01em}
.krk-card-body{padding:16px}`;document.head.appendChild(s);}})();
export function Card({title,actions,children,style}){
  return <div className="krk-card" style={style}>
    {(title||actions) && <div className="krk-card-head"><span className="krk-card-title">{title}</span>{actions}</div>}
    <div className="krk-card-body">{children}</div>
  </div>;
}
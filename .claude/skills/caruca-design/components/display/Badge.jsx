import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-badge')){const s=document.createElement('style');s.id='krk-badge';s.textContent=`.krk-badge{display:inline-flex;align-items:center;gap:5px;height:20px;padding:0 9px;border-radius:999px;font-family:var(--font-sans);font-size:12px;font-weight:600;letter-spacing:.01em}
.krk-badge-dot{width:6px;height:6px;border-radius:50%;background:currentColor}
.krk-badge-neutral{background:var(--surface-inline-code);color:var(--gray-600)}
.krk-badge-info{background:var(--surface-info);color:var(--blue)}
.krk-badge-success{background:var(--success-bg);color:var(--success-text)}
.krk-badge-warning{background:var(--warning-bg);color:var(--warning-text)}
.krk-badge-danger{background:var(--danger-bg);color:var(--danger-text)}
.krk-badge-mono{font-family:var(--font-mono);font-weight:400}`;document.head.appendChild(s);}})();
export function Badge({tone='neutral',dot,mono,children}){
  return <span className={'krk-badge krk-badge-'+tone+(mono?' krk-badge-mono':'')}>{dot && <span className="krk-badge-dot"></span>}{children}</span>;
}
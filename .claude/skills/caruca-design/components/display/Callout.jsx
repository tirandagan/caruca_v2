import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-callout')){const s=document.createElement('style');s.id='krk-callout';s.textContent=`.krk-callout{font-family:var(--font-sans);border-left:4px solid;border-radius:0 6px 6px 0;padding:16px 20px;font-size:14px;line-height:1.5;color:var(--ink)}
.krk-callout-title{font-weight:600;font-size:13px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:.5em}
.krk-callout-info{border-color:var(--blue);background:var(--surface-info)}.krk-callout-info .krk-callout-title{color:var(--blue)}
.krk-callout-warning{border-color:var(--warning);background:var(--warning-bg)}.krk-callout-warning .krk-callout-title{color:var(--warning-text)}
.krk-callout-tip{border-color:var(--success);background:var(--success-bg)}.krk-callout-tip .krk-callout-title{color:var(--success-text)}
.krk-callout-danger{border-color:var(--danger);background:var(--danger-bg)}.krk-callout-danger .krk-callout-title{color:var(--danger-text)}`;document.head.appendChild(s);}})();
export function Callout({kind='info',title,children,style}){
  return <div className={'krk-callout krk-callout-'+kind} style={style}>
    {title && <div className="krk-callout-title">{title}</div>}{children}
  </div>;
}
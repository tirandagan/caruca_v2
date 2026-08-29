import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-code')){const s=document.createElement('style');s.id='krk-code';s.textContent=`.krk-code{background:var(--surface-code);border:1px solid var(--border-strong);border-radius:var(--radius-md);padding:16px;margin:0;overflow-x:auto}
.krk-code-lang{display:block;text-align:right;font-family:var(--font-sans);font-size:11px;color:#656D76;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid var(--border-strong)}
.krk-code code{font-family:var(--font-mono);font-size:13px;line-height:1.4;color:var(--ink);white-space:pre-wrap;word-wrap:break-word}
.krk-code-inline{font-family:var(--font-mono);background:var(--surface-inline-code);padding:.15em .35em;border-radius:4px;font-size:.9em}`;document.head.appendChild(s);}})();
export function CodeBlock({language,children,style}){
  return <pre className="krk-code" style={style}>{language && <span className="krk-code-lang">{language}</span>}<code>{children}</code></pre>;
}
export function InlineCode({children}){return <code className="krk-code-inline">{children}</code>;}
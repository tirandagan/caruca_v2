import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-stat')){const s=document.createElement('style');s.id='krk-stat';s.textContent=`.krk-stat{font-family:var(--font-sans);display:flex;flex-direction:column;gap:4px;min-width:110px}
.krk-stat-label{font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--gray-500)}
.krk-stat-value{font-family:var(--font-mono);font-size:24px;line-height:1.1;color:var(--ink)}
.krk-stat-unit{font-size:13px;color:var(--gray-500);margin-left:2px}
.krk-stat-delta{font-family:var(--font-mono);font-size:12px;font-weight:400}
.krk-stat-delta-up{color:var(--success-text)}.krk-stat-delta-down{color:var(--danger-text)}.krk-stat-delta-flat{color:var(--gray-500)}`;document.head.appendChild(s);}})();
export function MetricStat({label,value,unit,delta,deltaTone='flat',style}){
  return <div className="krk-stat" style={style}>
    <span className="krk-stat-label">{label}</span>
    <span className="krk-stat-value">{value}{unit && <span className="krk-stat-unit">{unit}</span>}</span>
    {delta != null && <span className={'krk-stat-delta krk-stat-delta-'+deltaTone}>{delta}</span>}
  </div>;
}
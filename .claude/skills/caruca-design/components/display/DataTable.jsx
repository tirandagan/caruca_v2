import React from 'react';
(function(){if(typeof document!=='undefined'&&!document.getElementById('krk-table')){const s=document.createElement('style');s.id='krk-table';s.textContent=`.krk-table{width:100%;border-collapse:collapse;font-family:var(--font-sans);font-size:13px;color:var(--ink)}
.krk-table thead{background:var(--surface-thead)}
.krk-table th{font-weight:600;text-align:left;padding:10px 12px;border-bottom:2px solid #334155;font-size:12px;text-transform:uppercase;letter-spacing:.03em;color:var(--gray-600)}
.krk-table td{padding:8px 12px;border-bottom:1px solid var(--border-default);vertical-align:top}
.krk-table tbody tr:nth-child(even){background:var(--surface-zebra)}
.krk-table td.krk-td-mono{font-family:var(--font-mono);font-size:12.5px}
.krk-table td.krk-td-num{font-family:var(--font-mono);font-size:12.5px;text-align:right}
.krk-table th.krk-td-num{text-align:right}`;document.head.appendChild(s);}})();
export function DataTable({columns=[],rows=[],style}){
  return <table className="krk-table" style={style}>
    <thead><tr>{columns.map((c,i)=><th key={i} className={c.align==='right'?'krk-td-num':''}>{c.label}</th>)}</tr></thead>
    <tbody>{rows.map((r,ri)=><tr key={ri}>{columns.map((c,ci)=><td key={ci} className={c.mono?'krk-td-mono':(c.align==='right'?'krk-td-num':'')}>{r[c.key]}</td>)}</tr>)}</tbody>
  </table>;
}
const {Tabs, Badge, Button} = window.KarukaDesignSystem_69ceb9;
function Icon({name, size=16, color='currentColor', style}){
  const ref = React.useRef();
  React.useEffect(()=>{ if(ref.current && window.lucide && lucide.icons[name]){ ref.current.innerHTML=''; const el = lucide.createElement(lucide.icons[name]); el.setAttribute('width',size); el.setAttribute('height',size); el.setAttribute('stroke',color==='currentColor'?'currentColor':color); ref.current.appendChild(el);} },[name,size,color]);
  return <span ref={ref} style={{display:'inline-flex',alignItems:'center',...style}}></span>;
}
function ConsoleShell({active, onNav, children, right}){
  return <div style={{minHeight:'100vh',background:'#fff',fontFamily:'var(--font-sans)',color:'var(--ink)'}}>
    <header style={{display:'flex',alignItems:'center',gap:14,padding:'14px 28px 0',borderBottom:'1px solid var(--border-default)'}}>
      <img src="../../assets/logo.png" alt="Caruca" style={{height:34}}/>
      <div style={{marginRight:'auto'}}>
        <div style={{fontSize:17,fontWeight:700,lineHeight:1}}>Caruca v2 <span style={{fontWeight:400,color:'var(--gray-500)'}}>· eval console</span></div>
        <div style={{fontSize:11,fontStyle:'italic',color:'var(--gray-500)',marginTop:2}}>LLM-based specification mining for opaque shell commands.</div>
      </div>
      {right}
      <div style={{alignSelf:'flex-end'}}>
        <Tabs tabs={[{id:'runs',label:'Runs',count:12},{id:'live',label:'Live comparison'},{id:'report',label:'Report'}]} active={active} onChange={onNav}/>
      </div>
    </header>
    <main style={{padding:'22px 28px',maxWidth:1224,margin:'0 auto'}}>{children}</main>
  </div>;
}
function Term({title, host, lines, tone}){
  return <div style={{flex:1,minWidth:0,border:'1px solid var(--border-default)',borderRadius:6,overflow:'hidden',display:'flex',flexDirection:'column'}}>
    <div style={{display:'flex',alignItems:'center',gap:8,padding:'8px 12px',background:'var(--surface-thead)',borderBottom:'1px solid var(--border-default)'}}>
      <span style={{fontSize:11,fontWeight:600,textTransform:'uppercase',letterSpacing:'.05em',color:'var(--gray-600)'}}>{title}</span>
      <span style={{fontFamily:'var(--font-mono)',fontSize:11,color:'var(--gray-400)',marginLeft:'auto'}}>{host}</span>
      <span style={{width:7,height:7,borderRadius:'50%',background:tone==='live'?'var(--success)':'var(--gray-400)'}}></span>
    </div>
    <pre style={{margin:0,flex:1,background:'#0B1F33',color:'#D7E3F0',padding:'14px 16px',fontFamily:'var(--font-mono)',fontSize:12.5,lineHeight:1.55,whiteSpace:'pre-wrap',minHeight:290}}>{lines.map((l,i)=><div key={i} style={{color:l.c||'#D7E3F0'}}>{l.t}</div>)}</pre>
  </div>;
}
Object.assign(window, {Icon, ConsoleShell, Term});
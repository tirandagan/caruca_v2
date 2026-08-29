const {Badge, DataTable, MetricStat, Callout, Card, Button} = window.KarukaDesignSystem_69ceb9;
function ReportScreen(){
  return <div style={{display:'flex',flexDirection:'column',gap:20}}>
    <div style={{display:'flex',alignItems:'flex-end',gap:12}}>
      <div>
        <h2 style={{margin:0,fontSize:27,fontWeight:700,letterSpacing:'-.01em',color:'var(--blue)'}}>Three-way comparison</h2>
        <div style={{width:80,height:4,background:'linear-gradient(to right,var(--teal),var(--ink))',borderRadius:2,marginTop:8}}></div>
      </div>
      <div style={{marginLeft:'auto',display:'flex',gap:8}}>
        <Button variant="secondary" size="sm" icon={<Icon name="FileText" size={13}/>}>Export LaTeX tables</Button>
        <Button variant="ghost" size="sm" icon={<Icon name="Download" size={13}/>}>Figures (PDF)</Button>
      </div>
    </div>
    <div style={{display:'flex',gap:36}}>
      <MetricStat label="Q2 exact-match Δ" value="+4.2" unit="%" delta="v2 vs v1, N=12 cmds" deltaTone="up"/>
      <MetricStat label="Cost Δ" value="3.1x" delta="v2 vs v1" deltaTone="down"/>
      <MetricStat label="Coverage Δ" value="+38" unit="%" delta="v2-extended fixtures" deltaTone="up"/>
      <MetricStat label="Consistency" value="±2.3" unit="pp" delta="variance across N=5" deltaTone="flat"/>
      <MetricStat label="Hand-encoded LOC" value="−5,890" delta="of v1's 6,520" deltaTone="up"/>
    </div>
    <Card title="Per-command results — Q2 (cmp_specs.py methodology)" actions={<Badge tone="neutral" mono>eval/runs/2026-08-29T1942/</Badge>}>
      <DataTable
        columns={[{key:'cmd',label:'Command',mono:true},{key:'gt',label:'Ground truth',align:'right'},{key:'v1',label:'v1',align:'right'},{key:'naive',label:'naive-LLM (plain)',align:'right'},{key:'aug',label:'naive-LLM (augmented)',align:'right'},{key:'delta',label:'Δ v2 vs v1',align:'right'}]}
        rows={[
          {cmd:'rm',gt:'—',v1:'91.2%',naive:'94.1%',aug:'95.6%',delta:<span style={{color:'var(--success-text)'}}>+2.9pp</span>},
          {cmd:'mkdir',gt:'—',v1:'100%',naive:'100%',aug:'100%',delta:'0.0pp'},
          {cmd:'chmod',gt:'—',v1:'89.4%',naive:'88.7%',aug:'92.3%',delta:<span style={{color:'var(--danger-text)'}}>−0.7pp</span>},
          {cmd:'ln',gt:'—',v1:'84.0%',naive:'90.5%',aug:'91.1%',delta:<span style={{color:'var(--success-text)'}}>+6.5pp</span>},
          {cmd:'head',gt:'—',v1:'96.8%',naive:'97.2%',aug:'97.2%',delta:<span style={{color:'var(--success-text)'}}>+0.4pp</span>}
        ]}/>
      <div style={{fontSize:12,color:'var(--gray-500)',marginTop:10}}>Coverage subtotals are disaggregated (strong-normalization-only alongside blended %) by default. Conditions are reported separately, never blended.</div>
    </Card>
    <Callout kind="warning" title="Open dependency">v1's annotator was not built to interpret v2-extended trace shapes (symlinks, permission-denied, SIGPIPE). Where it mishandles one, that is itself a reportable coverage-gap finding — dimension 3 — not a defect to hide.</Callout>
  </div>;
}
Object.assign(window, {ReportScreen});
const {Button, Input, Select, Checkbox, Card, Badge, DataTable, MetricStat, Callout} = window.KarukaDesignSystem_69ceb9;
function RunsScreen({runs, onNewRun}){
  const [cmd,setCmd]=React.useState('rm');
  return <div style={{display:'flex',flexDirection:'column',gap:20}}>
    <div style={{display:'flex',gap:36,padding:'4px 2px'}}>
      <MetricStat label="Commands evaluated" value="12"/>
      <MetricStat label="Q2 exact-match" value="87.5" unit="%" delta="+4.2% vs v1" deltaTone="up"/>
      <MetricStat label="Cost / command" value="$0.041" delta="3.1x v1" deltaTone="down"/>
      <MetricStat label="Wall-clock / cmd" value="12.4" unit="s" delta="−18% vs v1" deltaTone="up"/>
      <MetricStat label="Variance (N=5)" value="±2.3" unit="pp"/>
    </div>
    <div style={{display:'grid',gridTemplateColumns:'1fr 330px',gap:20,alignItems:'start'}}>
      <Card title="Telemetry runs" actions={<Button variant="ghost" size="sm" icon={<Icon name="Download" size={14}/>}>Export JSON</Button>}>
        <DataTable
          columns={[{key:'run',label:'Run',mono:true},{key:'cmd',label:'Command',mono:true},{key:'cond',label:'Condition',mono:true},{key:'status',label:'Status'},{key:'q2',label:'Q2 match',align:'right'},{key:'cost',label:'Cost',align:'right'},{key:'wall',label:'Wall-clock',align:'right'}]}
          rows={runs}/>
        <div style={{fontSize:12,color:'var(--gray-500)',marginTop:10}}>Runs write to <code style={{fontFamily:'var(--font-mono)',background:'var(--surface-inline-code)',padding:'1px 4px',borderRadius:4}}>eval/runs/&lt;timestamp&gt;/</code> — conditions are never blended.</div>
      </Card>
      <div style={{display:'flex',flexDirection:'column',gap:16}}>
        <Card title="New run">
          <div style={{display:'flex',flexDirection:'column',gap:12}}>
            <Input label="Command" mono value={cmd} onChange={e=>setCmd(e.target.value)} hint="Binary name as invoked"/>
            <div style={{display:'flex',gap:10}}>
              <Select label="Profile" options={['v1-faithful','v2-extended','both']} style={{flex:1}}/>
              <Input label="Seed" mono defaultValue="7" style={{width:80}}/>
            </div>
            <Select label="Isolation backend" options={[{value:'',label:'No default — undecided'},{value:'docker',label:'docker'},{value:'firecracker',label:'firecracker'},{value:'gvisor',label:'gvisor'}]} hint="Open question: backend choice is unresolved"/>
            <Checkbox label="Variance sampling (N=5)" defaultChecked/>
            <Checkbox label="Augmented docs — separate condition"/>
            <Button icon={<Icon name="Play" size={15}/>} onClick={()=>onNewRun(cmd)}>Run comparison</Button>
          </div>
        </Card>
        <Callout kind="info" title="Telemetry">Every run records tokens, cost, wall-clock, model-ID and seed automatically — no measurement is reconstructed after the fact.</Callout>
      </div>
    </div>
  </div>;
}
Object.assign(window, {RunsScreen});
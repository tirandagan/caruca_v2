const {Button, Badge, MetricStat, Card} = window.KarukaDesignSystem_69ceb9;
const V1_LINES=[{t:'$ caruca syntax-spec rm',c:'#7FB2F0'},{t:'[dspy] loading few-shot module … ok'},{t:'[dspy] model=claude-sonnet-4-5 seed=7'},{t:'[spec] parsing man/rm.1 (4.1 KB)'},{t:'[spec] inferring flag grammar … 17 flags'},{t:'[spec] emitting Python DSL → specs/rm_v1.py',c:'#8BE0A4'},{t:''},{t:'tokens: 8,412 in / 1,206 out'},{t:'wall-clock: 14.9s  cost: $0.0130',c:'#9CA3AF'}];
const V2_LINES=[{t:'$ caruca-v2 naive-llm rm --docs man/rm.1 --seed 7',c:'#7FB2F0'},{t:'[naive] single-prompt, few-shot primed'},{t:'[naive] no tool use, no retry loop (by design)'},{t:'[naive] model=claude-sonnet-4-5 seed=7'},{t:'[spec] emitting Python DSL → specs/rm_naive.py',c:'#8BE0A4'},{t:'[sandbox] profile=v2-extended backend=firecracker'},{t:'[sandbox] 312 permutations · strace visible · teardown ok',c:'#8BE0A4'},{t:''},{t:'tokens: 6,077 in / 988 out'},{t:'wall-clock: 12.4s  cost: $0.0410',c:'#9CA3AF'}];
function LiveScreen({command}){
  return <div style={{display:'flex',flexDirection:'column',gap:20}}>
    <div style={{display:'flex',alignItems:'center',gap:12}}>
      <h2 style={{margin:0,fontSize:20,fontWeight:600,letterSpacing:'-.01em'}}>Live comparison — <span style={{fontFamily:'var(--font-mono)',fontWeight:400}}>{command}</span></h2>
      <Badge tone="success" dot>Streaming</Badge>
      <Badge tone="info" mono>seed 7</Badge>
      <div style={{marginLeft:'auto',display:'flex',gap:8}}>
        <Button variant="secondary" size="sm" icon={<Icon name="Square" size={13}/>}>Stop</Button>
        <Button variant="ghost" size="sm" icon={<Icon name="RotateCcw" size={13}/>}>Re-run</Button>
      </div>
    </div>
    <div style={{display:'flex',gap:16}}>
      <Term title="v1 · caruca" host="pty:0 · cloudlab-04" lines={V1_LINES} tone="live"/>
      <Term title="v2 · caruca-v2" host="pty:1 · cloudlab-04" lines={V2_LINES} tone="live"/>
    </div>
    <Card title="Telemetry — this run">
      <div style={{display:'flex',gap:40,flexWrap:'wrap'}}>
        <MetricStat label="v1 tokens" value="9,618"/>
        <MetricStat label="v2 tokens" value="7,065" delta="−26.5%" deltaTone="up"/>
        <MetricStat label="v1 cost" value="$0.013"/>
        <MetricStat label="v2 cost" value="$0.041" delta="3.1x v1" deltaTone="down"/>
        <MetricStat label="v1 wall-clock" value="14.9" unit="s"/>
        <MetricStat label="v2 wall-clock" value="12.4" unit="s" delta="−18%" deltaTone="up"/>
        <MetricStat label="Model" value="sonnet-4-5"/>
      </div>
    </Card>
  </div>;
}
Object.assign(window, {LiveScreen});
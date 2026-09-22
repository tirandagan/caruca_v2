
const CORPUS=['rm','mkdir','chmod','cp','mv','ls','cat','grep','sed','awk','find','tar','curl','wget','ln','touch','head','tail','sort','uniq','cut','tr','wc','diff','patch','xargs','chown','chgrp','du','df','stat','file','basename','dirname','realpath','readlink','mktemp','install','split','join','paste','comm','tee','date','sleep','env','printf','echo','test','expr','seq','yes'];
const RUN=new Set(['rm','mkdir','chmod','cp','ls','grep','find','tar','chown','du','sort','cut']);
const V1=[
 {t:'$ caruca syntax-spec {C} --docs man/{C}.1 --seed {S}',c:'#7FB2F0',stage:'boot'},
 {t:'[dspy] loading few-shot module … ok',stage:'load module'},
 {t:'[dspy] model=claude-sonnet-4-5 seed={S}',stage:'load module'},
 {t:'[spec] parsing man/{C}.1 (4.1 KB)',stage:'parse docs'},
 {t:'[spec] inferring flag grammar … 17 flags',stage:'infer grammar'},
 {t:'[spec] emitting Python DSL → specs/{C}_v1.py',c:'#8BE0A4',stage:'emit DSL'},
 {t:'[pipe] config-gen → 128 invocations',stage:'config-gen'},
 {t:'[pipe] trace (docker) … 128/128 ok',stage:'trace'},
 {t:'[pipe] annotate → benchmarks/annotations/{C}.json',c:'#8BE0A4',stage:'annotate'},
 {t:'',stage:'annotate'},
 {t:'tokens: 9,618 in+out   cost: $0.0130',c:'#9CA3AF',stage:'done'},
 {t:'wall-clock: 14.9s   exit 0',c:'#9CA3AF',stage:'done'}];
const V2=[
 {t:'$ caruca-v2 naive-llm {C} --docs {D} --profile {P} --seed {S}',c:'#7FB2F0',stage:'boot'},
 {t:'[naive] single-prompt, few-shot primed',stage:'prompt'},
 {t:'[naive] no tool use, no retry loop (by design)',stage:'prompt'},
 {t:'[naive] model=claude-sonnet-4-5 seed={S}',stage:'prompt'},
 {t:'[spec] emitting Python DSL → specs/{C}_naive.py',c:'#8BE0A4',stage:'emit DSL'},
 {t:'[sandbox] profile={P} backend={B}',stage:'sandbox up'},
 {t:'[sandbox] 312 permutations · strace visible',stage:'permutations'},
 {t:'[sandbox] teardown ok',c:'#8BE0A4',stage:'teardown'},
 {t:'[pipe] annotate (shared v1 stage) … ok',stage:'annotate'},
 {t:'',stage:'annotate'},
 {t:'tokens: 7,065 in+out   cost: $0.0410',c:'#9CA3AF',stage:'done'},
 {t:'wall-clock: 12.4s   exit 0',c:'#9CA3AF',stage:'done'}];
const DIFF_L=[['def spec(cmd):','ctx'],['  flag("-f","--force", bool)','ctx'],['  flag("-r","--recursive", bool)','ctx'],['  flag("-i","--interactive", enum("never","once","always"))','del'],['  flag("--one-file-system", bool)','del'],['  flag("-d","--dir", bool)','ctx'],['  operand("FILE", nargs="+")','ctx'],['  # 17 flags total','ctx']];
const DIFF_R=[['def spec(cmd):','ctx'],['  flag("-f","--force", bool)','ctx'],['  flag("-r","--recursive", bool)','ctx'],['  flag("-i","--interactive", str)','add'],['','gap'],['  flag("-d","--dir", bool)','ctx'],['  operand("FILE", nargs="+")','ctx'],['  # 16 flags total','add']];
const DS={ctx:'#fff',add:'#ECFDF5',del:'#FEF2F2',gap:'#F8FAFC'};
const DC={ctx:'#0B1F33',add:'#15803D',del:'#DC2626',gap:'#9CA3AF'};

class Component extends DCLogic {
  state={mode:this.props.defaultMode||'simultaneous',cmd:'rm',query:'',profile:'v2-extended',docs:'plain',backend:'docker',seed:'7',view:'run',running:false,i1:0,i2:0,t:0,done1:false,done2:false};
  componentWillUnmount(){clearInterval(this.iv);}
  fill(s){return s.replace(/\{C\}/g,this.state.cmd).replace(/\{S\}/g,this.state.seed).replace(/\{P\}/g,this.state.profile).replace(/\{B\}/g,this.state.backend).replace(/\{D\}/g,this.state.docs);}
  reset(){clearInterval(this.iv);this.setState({running:false,i1:0,i2:0,t:0,done1:false,done2:false,view:'run'});}
  toggleRun=()=>{
    if(this.state.running){clearInterval(this.iv);this.setState({running:false});return;}
    if(this.state.done1&&this.state.done2){this.reset();setTimeout(this.toggleRun,60);return;}
    this.setState({running:true,view:'run'});
    const speed=this.props.streamSpeed||300;
    this.iv=setInterval(()=>{
      this.setState(s=>{
        const seq=s.mode==='sequential';
        let i1=s.i1,i2=s.i2;
        if(seq){ if(i1<V1.length) i1++; else if(i2<V2.length) i2++; }
        else { if(i1<V1.length) i1++; if(i2<V2.length) i2++; }
        const d1=i1>=V1.length,d2=i2>=V2.length;
        if(d1&&d2){clearInterval(this.iv);setTimeout(()=>this.setState({view:'report'}),700);}
        return {i1,i2,t:s.t+speed/1000,done1:d1,done2:d2,running:!(d1&&d2)};
      });
    },speed);
  };
  pick=(c)=>()=>{this.reset();this.setState({cmd:c});};
  renderVals(){
    const s=this.state, seq=s.mode==='sequential';
    const q=s.query.trim().toLowerCase();
    const btn=(on)=>`appearance:none;border:none;padding:7px 14px;font:600 12.5px var(--font-sans);cursor:pointer;background:${on?'var(--blue)':'#fff'};color:${on?'#fff':'var(--gray-600)'}`;
    const chip=(t)=>({run:{tone:'success',label:'Streaming'},idle:{tone:'neutral',label:'Idle'},queue:{tone:'warning',label:'Queued'},ok:{tone:'info',label:'Complete'}}[t]);
    const st1=s.done1?'ok':(s.running?'run':'idle');
    const st2=s.done2?'ok':(seq&&!s.done1?(s.running?'queue':'idle'):(s.running&&(!seq||s.done1)?'run':'idle'));
    const l1=V1.slice(0,s.i1).map((l,i)=>({t:this.fill(l.t)||' ',c:l.c||'#D7E3F0',key:i}));
    const l2=V2.slice(0,s.i2).map((l,i)=>({t:this.fill(l.t)||' ',c:l.c||'#D7E3F0',key:i}));
    const stage1=s.i1?V1[Math.min(s.i1,V1.length)-1].stage:'not started';
    const stage2=s.i2?V2[Math.min(s.i2,V2.length)-1].stage:(seq?'waiting on v1':'not started');
    const money=(n)=>'$'+n.toFixed(4);
    return {
      cmd:s.cmd, seed:s.seed, profile:s.profile, docs:s.docs, backend:s.backend, query:s.query,
      commands:CORPUS.filter(c=>!q||c.includes(q)).map(c=>({name:c,flags:RUN.has(c)?'run':'',dot:RUN.has(c)?'var(--success)':'transparent',pick:this.pick(c),
        style:`width:100%;display:flex;align-items:center;gap:8px;text-align:left;appearance:none;border:none;border-radius:5px;padding:6px 9px;cursor:pointer;background:${c===s.cmd?'var(--surface-info)':'transparent'};color:${c===s.cmd?'var(--blue)':'var(--ink)'};font-weight:${c===s.cmd?600:400}`})),
      onQuery:e=>this.setState({query:e.target.value}),
      onProfile:e=>this.setState({profile:e.target.value}), onDocs:e=>this.setState({docs:e.target.value}),
      onBackend:e=>this.setState({backend:e.target.value}), onSeed:e=>this.setState({seed:e.target.value}),
      setSim:()=>{this.reset();this.setState({mode:'simultaneous'});}, setSeq:()=>{this.reset();this.setState({mode:'sequential'});},
      simBtn:btn(!seq), seqBtn:btn(seq),
      toggleRun:this.toggleRun,
      runLabel:s.running?'Stop':(s.done1&&s.done2?'Re-run':(seq?'Run v1, then v2':'Run comparison')),
      runVariant:s.running?'secondary':'primary',
      profileOpts:['v1-faithful','v2-extended','both'], docsOpts:['plain','augmented'], backendOpts:['docker','firecracker'],
      navTabs:[{id:'runs',label:'Runs',count:12},{id:'run',label:seq?'Sequential run':'Live comparison'},{id:'report',label:'Report'}],
      view:s.view, onNav:(id)=>this.setState({view:id}), isRunsView:s.view==='runs',
      dimCols:[{key:'d',label:'Dimension'},{key:'v1',label:'v1',mono:true},{key:'v2',label:'v2',mono:true},{key:'delta',label:'Delta',mono:true,align:'right'}],
      dimRows:[{d:'Correctness / fidelity',v1:'83.3%',v2:'87.5%',delta:'+4.2pp'},{d:'Cost / performance',v1:'$0.013',v2:'$0.041',delta:'3.1x'},{d:'Coverage (v2-extended fixtures)',v1:'n/a',v2:'312 perms',delta:'new'},{d:'Consistency (N=5, variance)',v1:'±0.0pp',v2:'±2.3pp',delta:'less stable'},{d:'Hand-encoded logic',v1:'1,240 LOC',v2:'71 LOC',delta:'−94%'}],
      runsCols:[{key:'cmd',label:'Command',mono:true},{key:'mode',label:'Mode'},{key:'prof',label:'Profile',mono:true},{key:'docs',label:'Docs',mono:true},{key:'q2',label:'Q2 match',align:'right'},{key:'cost',label:'Cost',align:'right'},{key:'when',label:'When',align:'right'}],
      runsRows:[{cmd:'rm',mode:'Simultaneous',prof:'v2-extended',docs:'plain',q2:'87.5%',cost:'$0.041',when:'2 min ago'},{cmd:'chmod',mode:'Sequential',prof:'v2-extended',docs:'augmented',q2:'88.7%',cost:'$0.067',when:'18 min ago'},{cmd:'mkdir',mode:'Simultaneous',prof:'v1-faithful',docs:'plain',q2:'100%',cost:'$0.022',when:'42 min ago'},{cmd:'cp',mode:'Simultaneous',prof:'both',docs:'plain',q2:'91.2%',cost:'$0.049',when:'1 hr ago'},{cmd:'find',mode:'Sequential',prof:'v2-extended',docs:'augmented',q2:'76.4%',cost:'$0.118',when:'3 hr ago'},{cmd:'tar',mode:'Simultaneous',prof:'v2-extended',docs:'plain',q2:'81.0%',cost:'$0.093',when:'yesterday'}],
      invocation:this.fill(`caruca-v2 compare {C} --profile {P} --docs {D} --backend {B} --seed {S}`)+(seq?' --serial':''),
      modeNote:seq?'Sequential — v1 runs to completion, then v2 on the same pty pool. Removes contention from the wall-clock figure.':'Simultaneous — both CLIs spawn at once in separate ptys. Fastest, but wall-clock is contended.',
      isRunView:s.view==='run', isReportView:s.view==='report',
      backToRun:()=>this.setState({view:'run'}),
      v1Lines:l1, v2Lines:l2,
      v1Caret:(s.running&&!s.done1)?'▊':'', v2Caret:(s.running&&s.i2>0&&!s.done2)?'▊':'',
      v2Waiting:(seq&&!s.done1&&s.i2===0)?'— queued. starts when v1 exits.':'',
      v1Stage:stage1, v2Stage:stage2,
      v1Step:`${Math.min(s.i1,V1.length)}/${V1.length}`, v2Step:`${Math.min(s.i2,V2.length)}/${V2.length}`,
      v1Pct:`${Math.round(s.i1/V1.length*100)}%`, v2Pct:`${Math.round(s.i2/V2.length*100)}%`,
      v1Tone:chip(st1).tone, v1Status:chip(st1).label, v2Tone:chip(st2).tone, v2Status:chip(st2).label,
      v1Tokens:(s.i1/V1.length*9618|0).toLocaleString(), v2Tokens:(s.i2/V2.length*7065|0).toLocaleString(),
      v1Cost:money(s.i1/V1.length*0.013), v2Cost:money(s.i2/V2.length*0.041),
      v1Time:(s.i1/V1.length*14.9).toFixed(1)+'s', v2Time:(s.i2/V2.length*12.4).toFixed(1)+'s',
      totalElapsed:s.t.toFixed(1)+'s', totalTokens:((s.i1/V1.length*9618|0)+(s.i2/V2.length*7065|0)).toLocaleString(),
      totalCost:money(s.i1/V1.length*0.013+s.i2/V2.length*0.041),
      finishNote:(s.done1&&s.done2)?'Both exited 0 — opening comparison report.':(s.running?'Telemetry written to runs/'+s.cmd+'-seed'+s.seed+'.jsonl':'Pick a command and run.'),
      diffLeft:DIFF_L.map(([t,k])=>({t:t||' ',style:`font-family:var(--font-mono);font-size:12.5px;line-height:1.7;padding:0 14px;background:${DS[k]};color:${DC[k]}`})),
      diffRight:DIFF_R.map(([t,k])=>({t:t||' ',style:`font-family:var(--font-mono);font-size:12.5px;line-height:1.7;padding:0 14px;background:${DS[k]};color:${DC[k]}`}))
    };
  }
}

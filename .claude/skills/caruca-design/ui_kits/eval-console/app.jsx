function App(){
  const [screen,setScreen]=React.useState('runs');
  const [command,setCommand]=React.useState('rm');
  const [runs,setRuns]=React.useState([
    {run:'1942-07',cmd:'rm',cond:'naive-LLM (plain)',status:<window.KarukaDesignSystem_69ceb9.Badge tone="success" dot>Completed</window.KarukaDesignSystem_69ceb9.Badge>,q2:'94.1%',cost:'$0.038',wall:'12.4s'},
    {run:'1942-06',cmd:'rm',cond:'v1 baseline',status:<window.KarukaDesignSystem_69ceb9.Badge tone="success" dot>Completed</window.KarukaDesignSystem_69ceb9.Badge>,q2:'91.2%',cost:'$0.013',wall:'14.9s'},
    {run:'1938-02',cmd:'chmod',cond:'naive-LLM (augmented)',status:<window.KarukaDesignSystem_69ceb9.Badge tone="success" dot>Completed</window.KarukaDesignSystem_69ceb9.Badge>,q2:'92.3%',cost:'$0.067',wall:'21.0s'},
    {run:'1938-01',cmd:'chmod',cond:'naive-LLM (plain)',status:<window.KarukaDesignSystem_69ceb9.Badge tone="warning" dot>Queued</window.KarukaDesignSystem_69ceb9.Badge>,q2:'—',cost:'—',wall:'—'},
    {run:'1921-04',cmd:'ln',cond:'naive-LLM (plain)',status:<window.KarukaDesignSystem_69ceb9.Badge tone="danger" dot>Failed</window.KarukaDesignSystem_69ceb9.Badge>,q2:'—',cost:'$0.004',wall:'2.1s'}
  ]);
  const onNewRun=(cmd)=>{ setCommand(cmd);
    setRuns(r=>[{run:'now',cmd,cond:'naive-LLM (plain)',status:<window.KarukaDesignSystem_69ceb9.Badge tone="info" dot>Streaming</window.KarukaDesignSystem_69ceb9.Badge>,q2:'—',cost:'—',wall:'—'},...r]);
    setScreen('live'); };
  return <ConsoleShell active={screen} onNav={setScreen}>
    {screen==='runs' && <RunsScreen runs={runs} onNewRun={onNewRun}/>}
    {screen==='live' && <LiveScreen command={command}/>}
    {screen==='report' && <ReportScreen/>}
  </ConsoleShell>;
}
ReactDOM.createRoot(document.getElementById('root')).render(<App/>);
"""Modern self-contained ResearchGuard research and AI-usage workstation."""
CONSOLE_HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#080c17"><title>ResearchGuard · Multi-agent AI Research Studio</title>
<style>
:root{font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;color:#eaf0fd;color-scheme:dark;background:#080c17;--panel:#101827;--stroke:#26344b;--muted:#93a4bd;--accent:#8b80ff;--mint:#4be3bd;--pink:#fe96d3}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(ellipse at 65% -8%,#29236e88,transparent 42%),radial-gradient(ellipse at 5% 65%,#0d3f6066,transparent 45%),#080c17;min-height:100vh}
a{color:#bab6ff;text-decoration:none}a:hover{text-decoration:underline}
button,input{font:inherit}button{cursor:pointer}
.frame{display:grid;grid-template-columns:246px 1fr;max-width:1720px;min-height:100vh;margin:0 auto}
.side{background:#0c1220dd;border-right:1px solid #ffffff12;padding:29px 18px;position:sticky;top:0;max-height:100vh}
.brand{display:flex;gap:12px;align-items:center;margin-bottom:55px;padding:0 11px}
.brandmark{width:41px;height:41px;background:linear-gradient(145deg,#a88eff,#519ae2);border-radius:13px;display:grid;place-items:center;font-size:22px;font-weight:900;color:#101426;box-shadow:0 8px 32px #645fea55}
.brand strong{display:block;font-size:14px;letter-spacing:.11em}.brand small{font-size:10px;color:#889cb8;letter-spacing:.18em}
.sideLabel{font-size:10px;font-weight:850;color:#647a9c;padding:0 16px;letter-spacing:.18em}
.sideLink{display:flex;align-items:center;gap:12px;padding:14px 15px;color:#aab9d2;border-radius:11px;margin:5px 0;font-size:13px;font-weight:700}
.sideLink.active{background:#7273c026;color:#dedbff;border:1px solid #9395e23a}.sideLink:hover{background:#ffffff0e;text-decoration:none}
.sideFoot{position:absolute;bottom:25px;left:22px;right:22px;color:#6c839e;font-size:11px;line-height:1.8}
.main{padding:28px clamp(22px,4vw,70px) 80px;min-width:0}
.top{display:flex;align-items:center;justify-content:space-between;gap:18px;padding-bottom:26px;border-bottom:1px solid #ffffff18}
.crumb{font-size:12px;color:#849ab4}.crumb b{color:#e7edfb}
.pill{border-radius:30px;border:1px solid #65dbbb55;background:#50d8ab14;color:#82e7cf;padding:8px 13px;font-size:10px;font-weight:850;letter-spacing:.06em;display:inline-flex;align-items:center;gap:8px}
.pulse{width:7px;height:7px;border-radius:50%;background:currentColor;box-shadow:0 0 16px currentColor}
.intro{display:flex;justify-content:space-between;gap:25px;align-items:end;padding:45px 0 28px}
.eyebrow{letter-spacing:.2em;color:#b2adff;font-size:11px;font-weight:850}
h1{font-size:clamp(34px,4.6vw,65px);letter-spacing:-.055em;margin:9px 0 13px;line-height:1.1}
h1 em{font-style:normal;background:linear-gradient(110deg,#d2b4ff,#ffaddd);-webkit-background-clip:text;background-clip:text;color:transparent}
.lead{max-width:760px;color:#9aacbf;line-height:1.7;font-size:14px}
.smallLink{font-size:12px;white-space:nowrap;color:#a0b9d8}
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:15px;margin:12px 0 26px}
.stat,.panel{border:1px solid #ffffff20;border-radius:17px;background:linear-gradient(160deg,#142035da,#0e1625d9);box-shadow:0 14px 45px #03071136}
.stat{padding:19px}.stat span{display:block;color:#8fa4bf;letter-spacing:.06em;font-size:11px;margin-bottom:13px}.stat strong{font-size:27px;letter-spacing:-.03em}.stat small{display:block;color:#7e93ad;font-size:10px;margin-top:7px}
.content{display:grid;grid-template-columns:minmax(0,1.46fr) minmax(285px,1fr);gap:18px}
.panel{padding:22px;min-width:0}.panel h2{font-size:16px;margin:0 0 8px;letter-spacing:-.02em}.panelSub{font-size:12px;color:#879ab5;line-height:1.65;margin:0 0 19px}
.topline{display:flex;align-items:start;justify-content:space-between;gap:15px}.tinyTag{font-size:10px;color:#b7aeff;background:#7d71f721;border:1px solid #8b81e750;border-radius:20px;padding:6px 9px;white-space:nowrap}
.modes{display:flex;gap:7px;background:#070c18;border-radius:11px;padding:5px;border:1px solid #ffffff1a;margin-bottom:20px}
.mode{flex:1;border:0;border-radius:8px;padding:11px 8px;background:transparent;color:#9fb0c6;font-size:12px;font-weight:800}
.mode[aria-pressed=true]{background:#6f65c445;color:#e0ddff;box-shadow:0 4px 18px #4e43b42d}
label{display:block;color:#bfcde0;font-size:11px;letter-spacing:.06em;font-weight:850;margin:16px 0 8px}
input{background:#090f1d;border:1px solid #ffffff28;border-radius:10px;color:#f0f5ff;padding:15px 16px;width:100%;outline:none}
input:focus{border-color:#998bff;box-shadow:0 0 0 3px #8377ff25}input::placeholder{color:#657a93}
#secretRow{display:none}.secretNote{font-size:11px;color:#8197b1;line-height:1.5;margin:8px 0 0}
.runButton{width:100%;display:flex;justify-content:center;align-items:center;gap:10px;border:0;border-radius:10px;padding:16px;background:linear-gradient(100deg,#a49aff,#dc9aea);color:#161328;font-weight:900;margin-top:20px;box-shadow:0 12px 35px #8c70f32e}
.runButton:disabled{opacity:.65;cursor:wait}.runButton:hover:not(:disabled){filter:brightness(1.07)}
.notice{border-radius:10px;padding:12px 14px;background:#8a7ce21a;border:1px solid #8a7ce24d;color:#c0baff;font-size:12px;line-height:1.6;margin-top:15px}
.notice.error{color:#ffb4b8;border-color:#f08c9f4f;background:#a72c491b}
.track{display:flex;flex-direction:column;gap:10px}
.step{border-radius:11px;border:1px solid #ffffff16;padding:13px 14px;background:#ffffff07;display:flex;align-items:center;gap:12px}
.stepIcon{width:32px;height:32px;display:grid;place-items:center;border-radius:10px;color:#b0a9ff;background:#8179e123;font-size:15px}
.step strong{display:block;font-size:12px}.step small{display:block;color:#778ca7;font-size:11px;margin-top:4px}
.step:nth-child(1) .stepIcon{color:#70edcf;background:#65dccb23}
.stretch{grid-column:1/-1}.report{min-height:90px;white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px;line-height:1.8;color:#d0dcef;margin:0}
.sources{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin-top:16px}
.source{border:1px solid #ffffff1d;background:#090e1c7e;border-radius:11px;padding:14px}
.source b{display:block;font-size:12px;line-height:1.5;margin:0 0 10px}.source small{color:#7f94ad;font-size:11px}
.source a{display:inline-block;margin-top:11px;font-size:11px}
.ledger{margin-top:22px}
.ledgerRow{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:10px;padding:12px 0;border-top:1px solid #ffffff19;font-size:11px;color:#b1c0d8}
.ledgerRow.header{color:#7e93b1;font-weight:850}
.meter{height:9px;background:#0a1020;border-radius:10px;overflow:hidden;margin-top:11px;border:1px solid #ffffff18}
.meter>i{display:block;width:0;height:100%;border-radius:10px;background:linear-gradient(90deg,#7f92ff,#e6a2dc);transition:width .5s}
.notes{color:#8197b1;font-size:11px;line-height:1.7;margin-top:13px}
.billLink{display:inline-flex;gap:6px;align-items:center;color:#b9aaff;font-size:12px;font-weight:750;margin-top:12px}
code{font-size:11px;color:#d9b3ff}
@media(max-width:1100px){.content{grid-template-columns:1fr}.stats{grid-template-columns:repeat(2,1fr)}.side{width:215px}.frame{grid-template-columns:215px 1fr}}
@media(max-width:760px){.frame{display:block}.side{position:relative;max-height:none;width:auto;border-bottom:1px solid #ffffff1c;border-right:0;padding:14px 20px;display:flex;align-items:center;gap:10px}.brand{margin:0}.sideLabel,.sideLink,.sideFoot{display:none}.main{padding:22px 17px 65px}.intro{align-items:start;flex-direction:column;padding:27px 0 14px}.stats{gap:9px}.stat{padding:15px}.stat strong{font-size:22px}.sources{grid-template-columns:1fr}.panel{padding:17px}}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{transition:none!important;animation:none!important;scroll-behavior:auto!important}}
</style></head><body>
<div class="frame"><aside class="side">
<div class="brand"><div class="brandmark">RG</div><div><strong>RESEARCHGUARD</strong><small>MUHRIS AI LAB</small></div></div>
<div class="sideLabel">WORKSPACE</div>
<a class="sideLink active" href="/">◈ &nbsp; Agent Command Center</a>
<a class="sideLink" href="/docs">▣ &nbsp; API Documentation</a>
<a class="sideLink" href="/health">◎ &nbsp; System Health</a>
<a class="sideLink" href="https://github.com/MUHRIS-AJ/ResearchGuard" target="_blank" rel="noopener noreferrer">⌘ &nbsp; Source Code</a>
<div class="sideFoot">Source-backed research.<br>No fabricated citations.<br>Human-reviewed decisions.</div>
</aside>
<main class="main">
<div class="top"><div class="crumb">WORKSPACES / <b>ResearchGuard</b> / Agent Operations</div><div class="pill"><i class="pulse"></i><span id="system">Checking gateway…</span></div></div>
<div class="intro"><div><div class="eyebrow">INTELLIGENT RESEARCH / CONTROL ROOM V2</div>
<h1>Research with <em>receipts.</em></h1><p class="lead">Discover real Crossref publications, then let three independent AI agents analyze, audit and report on source-linked evidence. See every token and estimated cost before calling it a bill.</p></div>
<a class="smallLink" href="https://muhris-ai-lab.vercel.app/#agents" target="_blank" rel="noopener noreferrer">↗ Return to portfolio</a></div>
<div class="stats">
<div class="stat"><span>SOURCES DISCOVERED</span><strong id="sourceMetric">—</strong><small>Actual DOI-linked metadata</small></div>
<div class="stat"><span>AI AGENT CALLS</span><strong id="callsMetric">0</strong><small>Current browser session</small></div>
<div class="stat"><span>TOKENS CONSUMED</span><strong id="tokensMetric">0</strong><small>Provider-reported when available</small></div>
<div class="stat"><span>ESTIMATED SESSION COST</span><strong id="costMetric">$0.000000</strong><small>USD · not an invoice</small></div>
</div>
<div class="content">
<section class="panel" aria-labelledby="runTitle"><div class="topline"><div><h2 id="runTitle">New research run</h2><p class="panelSub">Start with live sources; switch to authenticated multi-agent mode for independent LLM analysis and verification.</p></div><span class="tinyTag">READ ONLY</span></div>
<div class="modes" role="group" aria-label="Research workflow mode">
<button type="button" class="mode" data-mode="sources" aria-pressed="true">↗ Evidence discovery</button>
<button type="button" class="mode" data-mode="agents" aria-pressed="false">✦ Multi-agent AI</button></div>
<form id="form">
<label for="query">RESEARCH TOPIC OR DOI</label>
<input id="query" minlength="3" maxlength="120" value="AI in higher education" required placeholder="Example: AI in higher education" autocomplete="off">
<div id="secretRow"><label for="secret">OPERATOR ACCESS TOKEN</label><input id="secret" type="password" autocomplete="off" placeholder="Configured on Vercel (not saved in your browser)">
<p class="secretNote">Only authorized operators may spend AI credits. The token stays in memory for this page and is not sent to third-party services by your browser.</p></div>
<button class="runButton" id="run" type="submit">RUN SOURCE WORKFLOW ↗</button>
</form>
<div class="notice" id="status" role="status">Read-only Crossref discovery is available without an AI Gateway account or paid token.</div></section>
<section class="panel" aria-labelledby="pipelineTitle"><h2 id="pipelineTitle">Agent execution pipeline</h2><p class="panelSub">Each LLM stage is a separate model call, not a decorative label. Sources are retrieved through a real tool.</p>
<div class="track">
<div class="step"><div class="stepIcon">01</div><div><strong>Crossref Source Agent</strong><small>Real DOI metadata · no LLM charge</small></div></div>
<div class="step"><div class="stepIcon">02</div><div><strong>Analysis LLM Agent</strong><small>Interpret paper metadata carefully</small></div></div>
<div class="step"><div class="stepIcon">03</div><div><strong>Independent Audit LLM Agent</strong><small>Critique unsupported conclusions</small></div></div>
<div class="step"><div class="stepIcon">04</div><div><strong>Report LLM Agent</strong><small>Compose sourced memo and limitations</small></div></div>
</div></section>
<section class="panel stretch" aria-labelledby="reportTitle"><div class="topline"><div><h2 id="reportTitle">Evidence & agent outputs</h2><p class="panelSub">Every cited DOI links to its original metadata record.</p></div><span class="tinyTag" id="reportTag">AWAITING RUN</span></div>
<p class="report" id="report">Choose a research topic to retrieve real papers and evidence-linked findings.</p>
<div class="sources" id="sources"></div>
<div id="agentTrace"></div>
</section>
<section class="panel stretch" aria-labelledby="costTitle"><div class="topline"><div><h2 id="costTitle">Usage, API cost & billing</h2><p class="panelSub">Real token counts from Gateway responses; standard model-list prices determine the estimate. Provider invoice amounts may differ.</p></div><span class="tinyTag">USD / CURRENT SESSION</span></div>
<div class="stats">
<div class="stat"><span>MODEL</span><strong style="font-size:15px">Gemini 2.5 Flash Lite</strong><small>Vercel AI Gateway</small></div>
<div class="stat"><span>INPUT PRICE</span><strong style="font-size:17px">$0.10 / 1M</strong><small>Standard tier · 2026-11-24</small></div>
<div class="stat"><span>OUTPUT PRICE</span><strong style="font-size:17px">$0.40 / 1M</strong><small>Standard tier · 2026-11-24</small></div>
<div class="stat"><span>PER-RUN ESTIMATE LIMIT</span><strong style="font-size:19px">$0.01</strong><small>Software guardrail; not a billing cap</small></div>
</div>
<div class="ledger" id="ledger"><div class="ledgerRow header"><span>AGENT</span><span>TOKENS IN / OUT</span><span>ESTIMATED USD</span></div><p class="notes">No AI model requests yet in this browser session.</p></div>
<div class="meter" aria-label="Estimate vs per-run limit"><i id="meterFill"></i></div>
<p class="notes">An operator token and configured AI Gateway access are required for model calls. Session totals reset when this page is reloaded. A $0 estimate is never presented as actual Vercel billing. The official Vercel AI Gateway account is the source of truth for invoices and credit balances.</p>
<div class="topline"><a class="billLink" href="https://vercel.com/muhris-ajs-projects/~/ai-gateway" target="_blank" rel="noopener noreferrer">↗ Official Vercel AI Gateway usage & billing</a><button type="button" class="mode" style="flex:0 0 auto;border:1px solid #ffffff24" id="balanceButton">Check official credits</button></div>
<p id="balance" class="notes"></p>
</section>
</div></main></div>
<script>
"use strict";
let mode="sources",sessionCalls=0,sessionTokens=0,sessionEstimated=0;
const $=id=>document.getElementById(id), status=$("status");
function setStatus(msg,bad=false){status.textContent=msg;status.classList.toggle("error",bad)}
const formatUsd=n=>"$"+Number(n).toFixed(6);
function textNode(tag,value,klass){const el=document.createElement(tag);el.textContent=value;if(klass)el.className=klass;return el}
function reset(el){el.replaceChildren()}
function addSource(p){const card=textNode("div","","source");card.append(textNode("b",p.title||"Untitled publication"));card.append(textNode("small",[p.year,p.publisher].filter(Boolean).join(" · ")));
if(typeof p.doi_url==="string"&&p.doi_url.startsWith("https://doi.org/")){const a=document.createElement("a");a.href=p.doi_url;a.target="_blank";a.rel="noopener noreferrer";a.textContent=p.doi||"View DOI";card.append(document.createElement("br"),a)}
$("sources").append(card)}
function showData(data,agentRun){
const papers=data.sources||data.papers||[];$("sourceMetric").textContent=papers.length;
reset($("sources"));papers.forEach(addSource);reset($("agentTrace"));
const report=typeof data.report==="string"?data.report:("Found "+papers.length+" source-backed publication records. This mode does not make claims about full-text scientific findings.");
$("report").textContent=report;$("reportTag").textContent=agentRun?"AI AGENTS COMPLETED":"CROSSREF SOURCES";
if(agentRun){(data.stages||[]).forEach(s=>{const card=textNode("div","","step");card.style.marginTop="12px";const info=textNode("div");info.append(textNode("strong",s.agent+" · "+s.duration_ms+" ms"),textNode("small",s.output));card.append(info);$("agentTrace").append(card)});
const b=data.billing||{};sessionCalls+=Number(b.requests)||0;sessionTokens+=(Number(b.input_tokens)||0)+(Number(b.output_tokens)||0);sessionEstimated+=Number(b.estimated_usd)||0;
$("callsMetric").textContent=String(sessionCalls);$("tokensMetric").textContent=sessionTokens.toLocaleString();$("costMetric").textContent=formatUsd(sessionEstimated);
const list=$("ledger");reset(list);list.append(textNode("div","AGENT                          TOKENS IN / OUT          ESTIMATED USD","ledgerRow header"));
(data.stages||[]).forEach(s=>{const row=textNode("div","","ledgerRow");row.append(textNode("span",s.agent),textNode("span",s.input_tokens+" / "+s.output_tokens),textNode("span",s.estimated_usd==null?"Unavailable":formatUsd(s.estimated_usd)));list.append(row)});
$("meterFill").style.width=Math.min(100,Math.round(((Number(b.estimated_usd)||0)/0.01)*100))+"%";
}}
document.querySelectorAll("[data-mode]").forEach(btn=>btn.addEventListener("click",()=>{mode=btn.dataset.mode;document.querySelectorAll("[data-mode]").forEach(x=>x.setAttribute("aria-pressed",String(x.dataset.mode===mode)));$("secretRow").style.display=mode==="agents"?"block":"none";$("run").textContent=mode==="agents"?"RUN 3 AI AGENTS ↗":"RUN SOURCE WORKFLOW ↗";setStatus(mode==="agents"?"AI calls require your operator access token, configured Gateway credits, and server-side enablement.":"Read-only discovery is free; no model is contacted.")}));
$("form").addEventListener("submit",async event=>{event.preventDefault();const topic=$("query").value.trim();if(topic.length<3)return;const button=$("run");button.disabled=true;setStatus("Executing "+(mode==="agents"?"agent workflow":"Crossref source discovery")+"…");
try{let response;
if(mode==="sources"){const qs=new URLSearchParams({query:topic,service:"ResearchGuard"});response=await fetch("/api?"+qs)}
else{const key=$("secret").value;if(!key){setStatus("Enter your operator token, configured in Vercel project settings.",true);return}response=await fetch("/api/agents",{method:"POST",headers:{"Content-Type":"application/json","Authorization":"Bearer "+key},body:JSON.stringify({topic})})}
const data=await response.json();if(!response.ok)throw Error(data.detail||data.error||"Request failed: "+response.status);
showData(data,mode==="agents");setStatus("Completed · Original citations and limitations included.")}
catch(e){setStatus(String(e.message||e),true)}
finally{button.disabled=false}});
async function checkConfig(){try{const r=await fetch("/api/agent-config");const data=await r.json();$("system").textContent=data.ai_enabled?"AI OPERATOR ONLINE":"SOURCE MODE ONLINE"}catch{$("system").textContent="CHECK SYSTEM STATUS"}}
$("balanceButton").addEventListener("click",async()=>{const key=$("secret").value;if(!key){$("balance").textContent="Enter your operator token in Multi-agent AI mode first.";return}
try{const res=await fetch("/api/credits",{headers:{"Authorization":"Bearer "+key}});const json=await res.json();if(!res.ok)throw Error(json.detail||"Credit request failed");$("balance").textContent="Gateway credit summary: "+JSON.stringify(json)+". Consult Vercel for official billed charges."}catch(err){$("balance").textContent="Official credit data unavailable: "+String(err.message||err)}});
checkConfig();
</script></body></html>''';

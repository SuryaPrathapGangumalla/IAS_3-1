const state={tls:0,ssh:0};
async function post(url,data){let r=await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});let j=await r.json();if(!r.ok)throw Error(j.error||"Request failed");return j}
function display(id,j){document.getElementById(id).innerHTML=`<h3>Step ${j.step} of ${j.total}: ${j.title}</h3><p>${j.explanation}</p>${j.complete?'<strong>Sequence complete.</strong>':''}`}
async function showStep(kind){try{display(kind,await post("/api/handshake",{kind,step:state[kind]}))}catch(e){alert(e.message)}}
function start(kind){state[kind]=0;showStep(kind)}
function next(kind){state[kind]=Math.min(4,state[kind]+1);showStep(kind)}
function previous(kind){state[kind]=Math.max(0,state[kind]-1);showStep(kind)}
async function demoKey(){try{document.getElementById("keyresult").textContent=JSON.stringify(await post("/api/demo-key",{}),null,2)}catch(e){alert(e.message)}}
async function ipsec(){try{let mode=document.querySelector('input[name="mode"]:checked').value,j=await post("/api/ipsec",{mode});document.getElementById("packet").innerHTML='<p>'+j.explanation+'</p>'+j.layers.map(x=>'<span class="layer">'+x+'</span>').join('')}catch(e){alert(e.message)}}

let lastCipher="", lastSignature="";
async function api(path,data={}){let r=await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(data)});let j=await r.json();if(!r.ok)throw Error(j.error||"Request failed");return j}
function show(id,v){document.getElementById(id).textContent=typeof v==="string"?v:JSON.stringify(v,null,2)}
async function safe(fn){try{await fn()}catch(e){alert(e.message)}}
function register(){safe(async()=>{let j=await api("/api/register",{username:document.getElementById("username").value});show("identity",j)})}
function encrypt(){safe(async()=>{let j=await api("/api/rsa/encrypt",{message:document.getElementById("message").value});lastCipher=j.ciphertext;show("cipher",lastCipher)})}
function decrypt(){safe(async()=>{let j=await api("/api/rsa/decrypt",{ciphertext:lastCipher});show("plain",j.plaintext)})}
function sign(){safe(async()=>{let message=document.getElementById("signmsg").value;let j=await api("/api/rsa/sign",{message});lastSignature=j.signature;show("signature",j.signature)})}
function verify(){safe(async()=>{show("verifyresult",await api("/api/rsa/verify",{message:document.getElementById("signmsg").value,signature:lastSignature}))})}
function dh(){safe(async()=>show("dhresult",await api("/api/dh",{})))}
function hash(){safe(async()=>show("hashresult",(await api("/api/hash",{message:document.getElementById("hashmsg").value})).sha512))}
function certificate(){safe(async()=>show("cert",await api("/api/certificate",{})))}

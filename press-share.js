(()=>{const a=document.querySelector('[data-share-root]');if(!a)return;
const ORG='जीवन केशरी मराठी विद्यार्थी समूह, नाशिक';
function mk(){const d=a.dataset,h=document.getElementById('shareHost');if(!h)return;
const u=encodeURIComponent(d.url),t=encodeURIComponent(d.title);
h.innerHTML=`<div class="acts"><button class="btn" data-share="press">📱 पत्रकारांसाठी WhatsApp</button><button class="btn" data-share="social">🔗 सोशल मीडियावर शेअर करा</button><button class="btn alt" data-share="copy-press">पत्रकारांसाठी मजकूर कॉपी करा</button><button class="btn alt" onclick="print()">प्रिंट करा</button></div><div class="acts" id="socialBox" hidden><a class="btn alt" target="_blank" rel="noopener" href="https://wa.me/?text=${t}%0A${u}">WhatsApp</a><a class="btn alt" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u=${u}">Facebook</a><a class="btn alt" target="_blank" rel="noopener" href="https://twitter.com/intent/tweet?url=${u}&text=${t}">X</a><button class="btn alt" data-share="copy">लिंक कॉपी करा (Instagram साठी)</button></div>`}
function pt(){const d=a.dataset;let x=d.text||'';if(x.length>1200)x=x.slice(0,1200).replace(/\s\S*$/,'')+'…';
return `📰 *प्रसिद्धीपत्रक*\n*${d.title}*\n\n${x}\n\n📅 ${d.date}${d.loc?' | 📍 '+d.loc:''}${d.ref?'\nसंदर्भ क्र.: '+d.ref:''}\n🔗 संपूर्ण प्रसिद्धीपत्रक: ${d.url}\n\n— ${ORG}\n✉️ jivankeshrimarathi@gmail.com`}
function fl(b){const o=b.textContent;b.textContent='कॉपी झाले ✓';setTimeout(()=>b.textContent=o,1800)}
document.addEventListener('click',e=>{const b=e.target.closest('[data-share]');if(!b)return;const k=b.dataset.share,d=a.dataset;
if(k==='press')window.open('https://wa.me/?text='+encodeURIComponent(pt()),'_blank','noopener');
else if(k==='copy-press')navigator.clipboard.writeText(pt()).then(()=>fl(b));
else if(k==='copy')navigator.clipboard.writeText(d.url).then(()=>fl(b));
else if(k==='social'){if(navigator.share)navigator.share({title:d.title,text:d.excerpt||d.title,url:d.url}).catch(()=>{});else document.getElementById('socialBox').hidden=false}});
window.PLShare=mk;if(a.dataset.url)mk()})();

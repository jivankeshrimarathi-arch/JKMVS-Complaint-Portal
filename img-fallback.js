/* imgbb (i.ibb.co) चित्रे थेट लोड न झाल्यास (नेटवर्क/ISP ब्लॉक, hotlink) आपोआप पर्यायी मार्गाने लोड करते. */
(function(){
  var H=/^https?:\/\/i\.ibb\.co\//;
  function px(u){return 'https://wsrv.nl/?url='+encodeURIComponent(u.replace(/^https?:\/\//,''))}
  function bad(i){
    if(!i||i.tagName!=='IMG')return;
    var s=i.currentSrc||i.src||'';
    if(i.dataset.fb==='1'||i.dataset.fb==='2'){i.dataset.fb='2';return}
    if(H.test(s)){i.dataset.fb='1';i.referrerPolicy='no-referrer';i.src=px(s)}
  }
  document.addEventListener('error',function(e){bad(e.target)},true);
  function sweep(){var a=document.images;for(var k=0;k<a.length;k++){if(a[k].complete&&a[k].naturalWidth===0&&!a[k].dataset.fb)bad(a[k])}}
  window.addEventListener('load',function(){sweep();setTimeout(sweep,2500)});
})();

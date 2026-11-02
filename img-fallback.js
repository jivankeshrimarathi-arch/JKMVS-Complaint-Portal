/* JKMVS: i.ibb.co चित्रे लोड न झाल्यास पर्यायी मार्ग. फक्त error आल्यावरच चालते. */
(function () {
  'use strict';
  var IBB = /^https?:\/\/i\.ibb\.co\//i;
  function strip(u) { return u.replace(/^https?:\/\//i, ''); }
  function routes(o) {
    return [
      o + (o.indexOf('?') > -1 ? '&' : '?') + 'r=1',
      'https://wsrv.nl/?url=' + encodeURIComponent(strip(o)),
      'https://images.weserv.nl/?url=' + encodeURIComponent(strip(o))
    ];
  }
  document.addEventListener('error', function (e) {
    var img = e.target;
    if (!img || img.tagName !== 'IMG') return;
    var orig = img.getAttribute('data-orig');
    if (!orig) {
      orig = img.getAttribute('src') || '';
      if (!IBB.test(orig)) return;
      img.setAttribute('data-orig', orig);
    }
    var i = parseInt(img.getAttribute('data-step') || '0', 10);
    var list = routes(orig);
    if (i < list.length) {
      img.setAttribute('data-step', i + 1);
      img.referrerPolicy = 'no-referrer';
      img.src = list[i];
    } else {
      img.style.visibility = 'hidden';
    }
  }, true);
})();

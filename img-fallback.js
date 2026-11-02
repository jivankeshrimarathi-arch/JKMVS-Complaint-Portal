/* JKMVS: i.ibb.co चित्रे लोड न झाल्यास आपोआप पर्यायी मार्गांनी प्रयत्न */
(function () {
  'use strict';
  var IBB = /^https?:\/\/i\.ibb\.co\//i;

  function strip(u) { return u.replace(/^https?:\/\//i, ''); }

  // क्रमवार पर्याय: 1) मूळ लिंक (no-referrer) 2) wsrv.nl 3) weserv 4) placeholder
  function routes(orig) {
    return [
      orig,
      'https://wsrv.nl/?url=' + encodeURIComponent(strip(orig)),
      'https://images.weserv.nl/?url=' + encodeURIComponent(strip(orig))
    ];
  }

  function onFail(img) {
    var orig = img.getAttribute('data-orig') || img.getAttribute('src') || '';
    if (!IBB.test(orig) && !img.getAttribute('data-orig')) return;
    if (!img.getAttribute('data-orig')) img.setAttribute('data-orig', orig);
    var step = parseInt(img.getAttribute('data-step') || '0', 10) + 1;
    var list = routes(img.getAttribute('data-orig'));
    img.setAttribute('data-step', step);
    if (step < list.length) {
      img.referrerPolicy = 'no-referrer';
      // cache-bust फक्त पहिल्या पुन:प्रयत्नासाठी
      img.src = step === 0 ? list[0] : list[step];
    } else {
      img.style.visibility = 'hidden';
      img.removeAttribute('data-step');
    }
  }

  // error इव्हेंट bubble होत नाही, म्हणून capture वापरतो
  document.addEventListener('error', function (e) {
    var t = e.target;
    if (t && t.tagName === 'IMG') onFail(t);
  }, true);

  // सर्व img ना no-referrer (hotlink संरक्षण टाळण्यासाठी)
  function fix(root) {
    var imgs = (root || document).querySelectorAll('img');
    for (var i = 0; i < imgs.length; i++) {
      var im = imgs[i];
      if (!im.referrerPolicy) im.referrerPolicy = 'no-referrer';
      // आधीच अयशस्वी झालेली चित्रे
      if (im.complete && im.naturalWidth === 0 && im.getAttribute('src') && !im.getAttribute('data-step')) onFail(im);
    }
  }
  document.addEventListener('DOMContentLoaded', function () { fix(); });
  window.addEventListener('load', function () { fix(); });
})();

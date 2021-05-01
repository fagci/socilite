Array.prototype.forEach.call(document.querySelectorAll('time[datetime]'), function(el){
  el.innerHTML = new Date(el.getAttribute('datetime'))
    .toLocaleString();
});

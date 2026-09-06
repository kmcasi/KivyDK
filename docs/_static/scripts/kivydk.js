document.querySelectorAll('a[href^="http"]').forEach(a=>{
    a.target="_blank";
    a.rel="noopener noreferrer";
});

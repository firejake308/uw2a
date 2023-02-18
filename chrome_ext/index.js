function addButton() {
    const qid_display = document.querySelector('.question-id');
    const qid = /Question Id: (\d+)/.exec(qid_display.textContent)[1];
    const btn = document.createElement('button');
    btn.onclick = () => fetch(`http://localhost:8088/${qid}`, {mode: 'no-cors'}).catch(
        () => alert('Failed to open card. Check if Anki is running. and q2uw extension is installed')
    );
    btn.innerHTML = `Open in Anki: ${qid}`;
    qid_display.textContent = '';
    qid_display.prepend(btn);
}

document.addEventListener("DOMContentLoaded", addButton);

var observer = new MutationObserver(function(mutations){
    if(document.querySelector('.question-id')) {
        addButton();
        observer.disconnect(); // to stop observing the dom
    }
})

observer.observe(document.body, { 
    childList: true,
    subtree: true // needed if the node you're targeting is not the direct parent
});

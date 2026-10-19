"use strict";
document.addEventListener("click",event=>{
  const filter=event.target.closest("[data-filter]");
  if(filter){
    const current=filter.dataset.filter;
    document.querySelectorAll("[data-filter]").forEach(button=>button.setAttribute("aria-pressed",String(button===filter)));
    document.querySelectorAll(".wine-card").forEach(card=>{card.hidden=current!=="all"&&!card.dataset.cats.split(" ").includes(current)});
    return;
  }
  const open=event.target.closest("[data-open-wine]");
  if(open){const dialog=document.getElementById("wine-"+open.dataset.openWine);if(dialog&&typeof dialog.showModal==="function")dialog.showModal();return;}
  const close=event.target.closest("[data-close-dialog]");
  if(close){const dialog=close.closest("dialog");if(dialog)dialog.close();}
});
document.querySelectorAll(".wine-dialog").forEach(dialog=>{
  dialog.addEventListener("click",event=>{if(event.target===dialog)dialog.close()});
});

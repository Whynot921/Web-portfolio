var modal1 = document.getElementById("myModal1");
var modal = document.getElementById("myModal");
var btnOpen = document.getElementById("openModal");
var btnOpen1 = document.getElementById("openModal1");
var btnClose1 = document.getElementById("closeModal1");
var btnClose = document.getElementById("closeModal");

btnOpen1.onclick = function () {
  modal1.style.display = "block";
};
btnOpen.onclick = function () {
  modal.style.display = "block";
};
btnClose1.onclick = function () {
  modal1.style.display = "none";
};
btnClose.onclick = function () {
  modal.style.display = "none";
};
window.onclick = function (event) {
  if (event.target == modal1) {
    modal1.style.display = "none";
  } else if (event.target == modal) {
    modal.style.display = "none";
  }
};

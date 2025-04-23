document.addEventListener("DOMContentLoaded", function () {
  const gallery = document.querySelector(".gallery");
  const images = document.querySelectorAll(".gallery_img");

  if (images.length > 0) {
    gallery.classList.add("show"); // Добавляет класс show, если есть изображения
  }
});

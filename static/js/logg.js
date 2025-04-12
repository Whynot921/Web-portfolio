document.querySelectorAll("img").forEach((img) => {
  img.addEventListener("click", function () {
    const imageId = this.dataset.imageId;
    const confirmation = confirm("Удалить этот документ?");
    if (confirmation) {
      // Удаляем элемент из DOM
      this.remove();
      // Здесь можно также отправить запрос на сервер для удаления изображения с базы данных, если необходимо
    }
  });
});

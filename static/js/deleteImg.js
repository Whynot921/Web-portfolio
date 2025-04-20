const CurrUrl = window.location.href;
console.log(CurrUrl);

document.querySelectorAll(".gallery_img").forEach((image) => {
  image.addEventListener("click", function () {
    const imageId = this.dataset.imageId;
    const data = { ToDelete: imageId };
    const confirmation = confirm(
      "Вы уверены, что хотите удалить это изображение?"
    );
    if (confirmation) {
      this.remove();
      fetch(CurrUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((responseData) => {
          console.log("Success:", responseData);
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  });
});

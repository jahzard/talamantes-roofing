"use strict";

const photoDialog = document.querySelector("#photo-dialog");
const galleryPhotos = [...document.querySelectorAll("[data-gallery-photo]")];
const enlargedPhoto = document.querySelector("#enlarged-photo");
const photoCaption = document.querySelector("#photo-caption");
const photoPosition = document.querySelector("#photo-position");
let activePhoto = 0;

function showPhoto(index) {
  activePhoto = (index + galleryPhotos.length) % galleryPhotos.length;
  const photo = galleryPhotos[activePhoto];
  enlargedPhoto.src = photo.dataset.full;
  enlargedPhoto.alt = translate(photo.dataset.alt);
  photoCaption.textContent = translate(photo.dataset.caption);
  photoPosition.textContent = `${activePhoto + 1} / ${galleryPhotos.length}`;
}

galleryPhotos.forEach((button, index) => {
  button.addEventListener("click", () => {
    showPhoto(index);
    photoDialog.showModal();
    document.body.classList.add("modal-open");
  });
});

document.querySelector(".photo-dialog-close").addEventListener("click", () => photoDialog.close());
document.querySelector("[data-photo-previous]").addEventListener("click", () => showPhoto(activePhoto - 1));
document.querySelector("[data-photo-next]").addEventListener("click", () => showPhoto(activePhoto + 1));
photoDialog.addEventListener("keydown", event => {
  if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
    event.preventDefault();
    showPhoto(activePhoto + (event.key === "ArrowRight" ? 1 : -1));
  }
});
photoDialog.addEventListener("click", event => {
  const bounds = photoDialog.getBoundingClientRect();
  if (event.target === photoDialog &&
    (event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom)) photoDialog.close();
});
photoDialog.addEventListener("close", () => document.body.classList.remove("modal-open"));
// Keep the page quiet and avoid multiple clips playing at once.
document.querySelectorAll("video").forEach(video => {
  video.addEventListener("play", () => {
    document.querySelectorAll("video").forEach(other => {
      if (other !== video) other.pause();
    });
  });
});

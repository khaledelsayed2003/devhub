const projectImageInput = document.getElementById("id_featured_image");
const projectUploadName = document.getElementById("projectUploadName");
const projectPreviewArt = document.getElementById("projectPreviewArt");

function setProjectPreview(file) {
  if (!projectPreviewArt) {
    return;
  }

  if (!file) {
    projectPreviewArt.innerHTML = "<span>Featured image preview will appear here</span>";
    return;
  }

  const objectUrl = URL.createObjectURL(file);
  projectPreviewArt.innerHTML = `<img src="${objectUrl}" alt="Selected project preview">`;

  const previewImage = projectPreviewArt.querySelector("img");
  if (previewImage) {
    previewImage.addEventListener(
      "load",
      () => {
        URL.revokeObjectURL(objectUrl);
      },
      { once: true }
    );
  }
}

if (projectImageInput) {
  projectImageInput.addEventListener("change", () => {
    const file = projectImageInput.files && projectImageInput.files[0];

    if (projectUploadName) {
      projectUploadName.textContent = file ? file.name : "No file selected";
    }

    setProjectPreview(file);
  });
}

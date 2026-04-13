const projectImageInput = document.getElementById("id_featured_image");
const projectUploadName = document.getElementById("projectUploadName");
const projectPreviewArt = document.getElementById("projectPreviewArt");
const projectUploadClear = document.getElementById("projectUploadClear");
const projectUploadDefault = document.getElementById("projectUploadDefault");
const projectRemoveFlag = document.querySelector('input[name="remove_featured_image"]');
const existingProjectImageSrc =
  projectPreviewArt && projectPreviewArt.dataset ? projectPreviewArt.dataset.existingSrc || "" : "";
const existingProjectImageName =
  projectPreviewArt && projectPreviewArt.dataset ? projectPreviewArt.dataset.existingName || "" : "";
const defaultProjectImageSrc = "/images/default.png";
let currentObjectUrl = null;

function revokeCurrentObjectUrl() {
  if (currentObjectUrl) {
    URL.revokeObjectURL(currentObjectUrl);
    currentObjectUrl = null;
  }
}

function setProjectPreview(file) {
  if (!projectPreviewArt) {
    return;
  }

  revokeCurrentObjectUrl();

  if (!file) {
    if (existingProjectImageSrc) {
      projectPreviewArt.innerHTML = `<img src="${existingProjectImageSrc}" alt="Current project image">`;
      if (projectUploadName) {
        projectUploadName.textContent = existingProjectImageName || "Current image";
      }
      return;
    }

    projectPreviewArt.innerHTML = "<span>Featured image preview will appear here</span>";
    if (projectUploadName) {
      projectUploadName.textContent = "No file selected";
    }
    return;
  }

  currentObjectUrl = URL.createObjectURL(file);
  projectPreviewArt.innerHTML = `<img src="${currentObjectUrl}" alt="Selected project preview">`;

  const previewImage = projectPreviewArt.querySelector("img");
  if (previewImage) {
    previewImage.addEventListener(
      "load",
      () => {},
      { once: true }
    );
  }
}

function setProjectPreviewFromSrc(src, altText) {
  if (!projectPreviewArt) {
    return;
  }

  revokeCurrentObjectUrl();
  projectPreviewArt.innerHTML = `<img src="${src}" alt="${altText}">`;
}

if (projectImageInput) {
  projectImageInput.addEventListener("change", () => {
    const file = projectImageInput.files && projectImageInput.files[0];

    if (projectRemoveFlag) {
      projectRemoveFlag.value = "";
    }

    if (projectUploadName) {
      projectUploadName.textContent = file ? file.name : "No file selected";
    }

    setProjectPreview(file);
  });
}

if (projectUploadClear && projectImageInput) {
  projectUploadClear.addEventListener("click", () => {
    projectImageInput.value = "";
    if (projectRemoveFlag) {
      projectRemoveFlag.value = "";
    }
    setProjectPreview(null);
  });
}

if (projectUploadDefault && projectImageInput) {
  projectUploadDefault.addEventListener("click", () => {
    projectImageInput.value = "";
    if (projectRemoveFlag) {
      projectRemoveFlag.value = "on";
    }
    setProjectPreviewFromSrc(defaultProjectImageSrc, "Default project image");
    if (projectUploadName) {
      projectUploadName.textContent = "Default image";
    }
  });
}

setProjectPreview(null);

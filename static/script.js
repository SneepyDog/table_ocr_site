let uploadedFile = null;
let rotation = 0;
let cropBox = null;
let isDrawing = false;
let startX = 0, startY = 0;

function uploadFile() {
  const file = document.getElementById("fileInput").files[0];
  const formData = new FormData();
  formData.append("file", file);

  $.ajax({
    url: "/upload",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (res) {
      uploadedFile = res.filename;
      $("#status").text("Файл загружен: " + uploadedFile);
      drawOriginal();
    },
    error: function (xhr) {
      console.error("Ошибка загрузки:", xhr.responseText);
    }
  });
}

function drawOriginal() {
  const img = new Image();
  img.onload = function () {
    const canvas = document.getElementById("imageCanvas");
    const ctx = canvas.getContext("2d");
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(img, 0, 0);
  };
  img.src = `${window.location.origin}/uploads/${uploadedFile}`;
}

function rotate(deg) {
  rotation += deg;
  drawOriginal();
}

function recognize() {
  if (!uploadedFile || !cropBox) {
    alert("Выделите область перед распознаванием.");
    return;
  }
  $("#status").text("⏳ Распознавание...");

  $.ajax({
    url: "/process",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({
      filename: uploadedFile,
      crop: cropBox,
      rotate: rotation
    }),
    success: function (res) {
      $("#status").text("✅ Готово!");
      $("#download").html(`<a href="/download/${res.result_file}" download>Скачать результат</a>`);
    }
  });
}

// Crop interaction
const canvas = document.getElementById("imageCanvas");
const ctx = canvas.getContext("2d");

function getMousePos(e) {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / rect.width;
  const scaleY = canvas.height / rect.height;
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY
  };
}

canvas.addEventListener("mousedown", (e) => {
  isDrawing = true;
  const pos = getMousePos(e);
  startX = pos.x;
  startY = pos.y;
});

canvas.addEventListener("mousemove", (e) => {
  if (!isDrawing) return;
  drawOriginal();
  const pos = getMousePos(e);
  const width = pos.x - startX;
  const height = pos.y - startY;
  ctx.strokeStyle = "red";
  ctx.lineWidth = 2;
  ctx.strokeRect(startX, startY, width, height);
});

canvas.addEventListener("mouseup", (e) => {
  isDrawing = false;
  const pos = getMousePos(e);
  cropBox = {
    x: Math.min(startX, pos.x),
    y: Math.min(startY, pos.y),
    width: Math.abs(pos.x - startX),
    height: Math.abs(pos.y - startY)
  };
  console.log("Область обрезки:", cropBox);
  drawCroppedPreview();
});

function drawCroppedPreview() {
  const img = new Image();
  img.onload = function () {
    const preview = document.getElementById("previewImage");
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = cropBox.width;
    tempCanvas.height = cropBox.height;
    const tempCtx = tempCanvas.getContext("2d");
    tempCtx.drawImage(img, cropBox.x, cropBox.y, cropBox.width, cropBox.height, 0, 0, cropBox.width, cropBox.height);
    preview.src = tempCanvas.toDataURL();
  };
  img.src = `${window.location.origin}/uploads/${uploadedFile}`;
}
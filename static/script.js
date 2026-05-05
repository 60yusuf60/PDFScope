document.addEventListener("dragover", (event) => event.preventDefault());
document.addEventListener("drop", (event) => event.preventDefault());

const pdfDropZone = document.getElementById("drop-zone");
const resultZone = document.getElementById("results");

async function handleDrop(event) {
  event.preventDefault();
  const file = event.dataTransfer.files[0];
  const formData = new FormData();
  formData.append("pdf", file);

  pdfDropZone.innerHTML = file.name;
  resultZone.innerHTML = "Analyzing...";

  const result = await fetch("/analyze", {
    method: "POST",
    body: formData,
  });

  const data = await result.json();

  let html = "";
  for (const [key, value] of Object.entries(data)) {
    html += `<p><strong>${key}:</strong> ${value}</p>`;
  }
  resultZone.innerHTML = html;
}

pdfDropZone.addEventListener("drop", handleDrop);

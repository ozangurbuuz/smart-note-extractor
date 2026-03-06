const API_BASE_URL = "http://localhost:8000";

export async function summarizeFile({ file, summaryType, summaryLength }) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("summary_type", summaryType);
  formData.append("summary_length", summaryLength);

  const response = await fetch(`${API_BASE_URL}/summarize`, {
    method: "POST",
    body: formData,
  });

  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.detail || "Failed to summarize file");
  }

  return payload;
}

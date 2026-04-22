import type { CompareFilesResponse } from "../types/plagiarism";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");

export async function compareFiles(files: File[]): Promise<CompareFilesResponse> {
  const fd = new FormData();
  for (const file of files) {
    fd.append("files", file, file.name);
  }

  const res = await fetch(`${API_BASE}/compare-files`, {
    method: "POST",
    body: fd,
  });
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data?.error || "Request failed");
  }
  return data;
}

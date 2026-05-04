"use client";
import { useState } from "react";
import { uploadResume } from "@/lib/api";

const MAX_SIZE = 10 * 1024 * 1024;

export function useResumeUpload() {
  const [file, setFile] = useState<File | null>(null);
  const [resumeId, setResumeId] = useState<number | null>(null);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const selectFile = (f: File) => {
    if (!f.name.toLowerCase().endsWith(".pdf")) {
      setError("仅支持 PDF 格式");
      return;
    }
    if (f.size > MAX_SIZE) {
      setError("文件大小不能超过 10 MB");
      return;
    }
    setError("");
    setFile(f);
    setResumeId(null);
  };

  const upload = async (): Promise<number> => {
    if (!file) throw new Error("请先选择简历文件");
    if (resumeId) return resumeId;
    setUploading(true);
    try {
      const { resume_id } = await uploadResume(file);
      setResumeId(resume_id);
      return resume_id;
    } finally {
      setUploading(false);
    }
  };

  return { file, selectFile, upload, uploading, error, resumeId };
}

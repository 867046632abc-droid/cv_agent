"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import { ResumeDropzone } from "@/components/upload/resume-dropzone";
import { uploadResume, startAnalysis } from "@/lib/api";

export default function HomePage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [jdText, setJdText] = useState("");
  const [loading, setLoading] = useState(false);
  const [fileError, setFileError] = useState("");

  const handleFileChange = (f: File) => {
    if (!f.name.toLowerCase().endsWith(".pdf")) {
      setFileError("仅支持 PDF 格式");
      return;
    }
    if (f.size > 10 * 1024 * 1024) {
      setFileError("文件大小不能超过 10 MB");
      return;
    }
    setFileError("");
    setFile(f);
  };

  const handleSubmit = async () => {
    if (!file || !jdText.trim()) return;
    setLoading(true);
    try {
      const { resume_id } = await uploadResume(file);
      const { analysis_id } = await startAnalysis(resume_id, jdText);
      router.push(`/analysis/${analysis_id}`);
    } catch (e: unknown) {
      toast.error((e as Error).message ?? "启动失败，请重试");
      setLoading(false);
    }
  };

  const canSubmit = !!file && jdText.trim().length > 20 && !loading;

  return (
    <div className="max-w-5xl mx-auto px-4 py-10 space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-zinc-100">JD 智能匹配分析</h1>
        <p className="text-zinc-500">上传简历 + 粘贴 JD，AI 自动分析匹配度、预测面试题、生成定制自我介绍</p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* JD Input */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">
            职位描述（JD）
            <span className="ml-2 text-zinc-400 font-normal">{jdText.length} 字</span>
          </label>
          <textarea
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
            placeholder="将职位描述粘贴到这里..."
            rows={14}
            className="w-full rounded-xl border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-900 p-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-zinc-400"
          />
        </div>

        {/* Resume Upload */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-zinc-700 dark:text-zinc-300">简历（PDF）</label>
          <ResumeDropzone file={file} onChange={handleFileChange} error={fileError} />
          <p className="text-xs text-zinc-400">上传后简历将仅用于本次分析，不会长期存储</p>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleSubmit}
          disabled={!canSubmit}
          className="px-8 py-3 rounded-xl bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 font-medium text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:bg-zinc-700 dark:hover:bg-zinc-300 transition-colors"
        >
          {loading ? "正在启动分析..." : "开始 AI 分析"}
        </button>
      </div>
    </div>
  );
}

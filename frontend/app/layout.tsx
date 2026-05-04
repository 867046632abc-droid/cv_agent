import type { Metadata } from "next";
import "./globals.css";
import { Navbar } from "@/components/layout/navbar";
import { Toaster } from "sonner";

export const metadata: Metadata = {
  title: "JD Analyzer — AI 职位匹配分析",
  description: "上传简历，粘贴 JD，AI 自动分析匹配度、预测面试题、生成自我介绍",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh">
      <body>
        <Navbar />
        <main className="min-h-screen bg-zinc-50 dark:bg-zinc-950">{children}</main>
        <footer className="border-t border-zinc-200 dark:border-zinc-800 py-4 text-center text-xs text-zinc-400">
          JD Analyzer · Powered by GPT-4o + LangGraph
        </footer>
        <Toaster position="top-right" richColors />
      </body>
    </html>
  );
}

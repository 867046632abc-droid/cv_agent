import Link from "next/link";

export function Navbar() {
  return (
    <nav className="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-950">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="font-semibold text-zinc-900 dark:text-zinc-100 text-lg">
          JD Analyzer
        </Link>
        <Link
          href="/history"
          className="text-sm text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
        >
          历史记录
        </Link>
      </div>
    </nav>
  );
}

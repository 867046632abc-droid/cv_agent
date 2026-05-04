import Link from "next/link";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4 text-center px-4">
      <h1 className="text-6xl font-bold text-zinc-200 dark:text-zinc-800">404</h1>
      <p className="text-zinc-500">找不到这个页面</p>
      <Link
        href="/"
        className="px-4 py-2 text-sm bg-zinc-900 dark:bg-zinc-100 text-white dark:text-zinc-900 rounded-lg hover:opacity-80 transition-opacity"
      >
        回到首页
      </Link>
    </div>
  );
}

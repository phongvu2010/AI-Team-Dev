export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 text-center">
      <div className="max-w-2xl rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <div className="inline-flex items-center gap-2 rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700 mb-4">
          <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          Antigravity 2.0 Multi-Agent Template
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
          AI Team Dev Starter
        </h1>
        <p className="mt-4 text-sm text-slate-600 leading-relaxed">
          Full-stack template ready for Matrix Architecture (DB / Backend / Frontend) with automated Planning, Dev Squads, Testing &amp; Review.
        </p>
        <div className="mt-6 flex flex-wrap justify-center gap-2 text-xs text-slate-600">
          <span className="rounded-md bg-slate-100 px-2.5 py-1 font-mono">Next.js 15</span>
          <span className="rounded-md bg-slate-100 px-2.5 py-1 font-mono">React 19</span>
          <span className="rounded-md bg-slate-100 px-2.5 py-1 font-mono">FastAPI</span>
          <span className="rounded-md bg-slate-100 px-2.5 py-1 font-mono">SQLAlchemy 2.0</span>
          <span className="rounded-md bg-slate-100 px-2.5 py-1 font-mono">PostgreSQL</span>
        </div>
      </div>
    </main>
  );
}

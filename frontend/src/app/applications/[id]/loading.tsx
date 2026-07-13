function ContentCardSkeleton({
  lines,
}: {
  lines: number;
}) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="h-6 w-36 animate-pulse rounded bg-slate-200" />

      <div className="mt-5 space-y-3">
        {Array.from({ length: lines }).map((_, index) => (
          <div
            key={index}
            className={`h-4 animate-pulse rounded bg-slate-200 ${
              index === lines - 1 ? "w-2/3" : "w-full"
            }`}
          />
        ))}
      </div>
    </section>
  );
}

export default function ApplicationLoading() {
  return (
    <main
      className="min-h-screen bg-slate-50 px-6 py-10"
      aria-busy="true"
      aria-label="Loading application"
    >
      <div className="mx-auto max-w-4xl">
        <div className="flex items-center justify-between gap-4">
          <div className="h-4 w-36 animate-pulse rounded bg-slate-200" />
          <div className="h-10 w-36 animate-pulse rounded-lg bg-slate-200" />
        </div>

        <header className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
            <div className="w-full">
              <div className="h-4 w-32 animate-pulse rounded bg-slate-200" />
              <div className="mt-4 h-9 w-96 max-w-full animate-pulse rounded bg-slate-200" />
              <div className="mt-3 h-5 w-44 animate-pulse rounded bg-slate-200" />
            </div>

            <div className="h-8 w-24 animate-pulse rounded-full bg-slate-200" />
          </div>

          <div className="mt-6 flex gap-6 border-t border-slate-200 pt-5">
            <div className="h-4 w-36 animate-pulse rounded bg-slate-200" />
            <div className="h-4 w-36 animate-pulse rounded bg-slate-200" />
          </div>
        </header>

        <div className="mt-6 grid gap-6">
          <ContentCardSkeleton lines={1} />
          <ContentCardSkeleton lines={7} />
          <ContentCardSkeleton lines={3} />
        </div>
      </div>
    </main>
  );
}
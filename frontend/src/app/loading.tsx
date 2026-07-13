function SummaryCardSkeleton() {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div className="h-4 w-28 animate-pulse rounded bg-slate-200" />
      <div className="mt-3 h-9 w-12 animate-pulse rounded bg-slate-200" />
    </div>
  );
}

function TableRowSkeleton() {
  return (
    <tr className="border-t border-slate-100">
      <td className="px-6 py-4">
        <div className="h-4 w-28 animate-pulse rounded bg-slate-200" />
      </td>

      <td className="px-6 py-4">
        <div className="h-4 w-40 animate-pulse rounded bg-slate-200" />
      </td>

      <td className="px-6 py-4">
        <div className="h-6 w-20 animate-pulse rounded-full bg-slate-200" />
      </td>

      <td className="px-6 py-4">
        <div className="h-4 w-24 animate-pulse rounded bg-slate-200" />
      </td>

      <td className="px-6 py-4">
        <div className="h-4 w-24 animate-pulse rounded bg-slate-200" />
      </td>

      <td className="px-6 py-4">
        <div className="ml-auto h-4 w-10 animate-pulse rounded bg-slate-200" />
      </td>
    </tr>
  );
}

export default function DashboardLoading() {
  return (
    <main
      className="min-h-screen bg-slate-50 px-6 py-10"
      aria-busy="true"
      aria-label="Loading applications"
    >
      <div className="mx-auto max-w-7xl">
        <header className="flex flex-col justify-between gap-5 sm:flex-row sm:items-start">
          <div>
            <div className="h-4 w-36 animate-pulse rounded bg-slate-200" />
            <div className="mt-4 h-9 w-72 max-w-full animate-pulse rounded bg-slate-200" />
            <div className="mt-3 h-5 w-96 max-w-full animate-pulse rounded bg-slate-200" />
          </div>

          <div className="h-10 w-36 animate-pulse rounded-lg bg-slate-200" />
        </header>

        <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <SummaryCardSkeleton key={index} />
          ))}
        </section>

        <section className="mt-8 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-5">
            <div className="h-6 w-32 animate-pulse rounded bg-slate-200" />
            <div className="mt-3 h-4 w-72 max-w-full animate-pulse rounded bg-slate-200" />

            <div className="mt-5 grid gap-3 md:grid-cols-[minmax(0,1fr)_220px_auto]">
              <div className="h-10 animate-pulse rounded-lg bg-slate-200" />
              <div className="h-10 animate-pulse rounded-lg bg-slate-200" />
              <div className="h-10 w-28 animate-pulse rounded-lg bg-slate-200" />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead className="bg-slate-50">
                <tr>
                  {[
                    "Company",
                    "Position",
                    "Status",
                    "Location",
                    "Updated",
                    "Action",
                  ].map((label) => (
                    <th
                      key={label}
                      className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-400"
                    >
                      {label}
                    </th>
                  ))}
                </tr>
              </thead>

              <tbody>
                {Array.from({ length: 5 }).map((_, index) => (
                  <TableRowSkeleton key={index} />
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </main>
  );
}
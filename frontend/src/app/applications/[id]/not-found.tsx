import Link from "next/link";

export default function ApplicationNotFound() {
  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <section className="rounded-xl border border-slate-200 bg-white p-8 text-center shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            404
          </p>

          <h1 className="mt-3 text-2xl font-bold text-slate-950">
            Application not found
          </h1>

          <p className="mt-3 text-slate-600">
            This application may have been deleted or the link may be
            incorrect.
          </p>

          <Link
            href="/"
            className="mt-6 inline-flex rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
          >
            Return to dashboard
          </Link>
        </section>
      </div>
    </main>
  );
}
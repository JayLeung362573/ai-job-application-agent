"use client";

import { useEffect } from "react";

interface DashboardErrorProps {
  error: Error & {
    digest?: string;
  };
  unstable_retry: () => void;
}

export default function DashboardError({
  error,
  unstable_retry,
}: DashboardErrorProps) {
  useEffect(() => {
    console.error("Dashboard route error:", error);
  }, [error]);

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-3xl">
        <section className="rounded-xl border border-red-200 bg-white p-8 text-center shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-wide text-red-600">
            Connection error
          </p>

          <h1 className="mt-3 text-2xl font-bold text-slate-950">
            Could not load applications
          </h1>

          <p className="mt-3 leading-7 text-slate-600">
            The application dashboard could not reach the backend service.
            Confirm that the API and database are running, then try again.
          </p>

          {error.digest ? (
            <p className="mt-3 text-xs text-slate-400">
              Error reference: {error.digest}
            </p>
          ) : null}

          <button
            type="button"
            onClick={() => unstable_retry()}
            className="mt-6 inline-flex rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
          >
            Try again
          </button>
        </section>
      </div>
    </main>
  );
}
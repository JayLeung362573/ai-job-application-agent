"use client";

import Link from "next/link";
import { useEffect } from "react";

interface ApplicationErrorProps {
  error: Error & {
    digest?: string;
  };
  unstable_retry: () => void;
}

export default function ApplicationError({
  error,
  unstable_retry,
}: ApplicationErrorProps) {
  useEffect(() => {
    console.error("Application route error:", error);
  }, [error]);

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-3xl">
        <section className="rounded-xl border border-red-200 bg-white p-8 text-center shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-wide text-red-600">
            Connection error
          </p>

          <h1 className="mt-3 text-2xl font-bold text-slate-950">
            Could not load application
          </h1>

          <p className="mt-3 leading-7 text-slate-600">
            The application data could not be loaded. Confirm that the
            backend service is available, then try again.
          </p>

          {error.digest ? (
            <p className="mt-3 text-xs text-slate-400">
              Error reference: {error.digest}
            </p>
          ) : null}

          <div className="mt-6 flex flex-col justify-center gap-3 sm:flex-row">
            <Link
              href="/"
              className="inline-flex justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Return to dashboard
            </Link>

            <button
              type="button"
              onClick={() => unstable_retry()}
              className="inline-flex justify-center rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
            >
              Try again
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}
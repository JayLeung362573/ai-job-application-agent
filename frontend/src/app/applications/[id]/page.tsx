import Link from "next/link";
import { notFound } from "next/navigation";

import { getApplication } from "@/lib/api";
import type { ApplicationStatus } from "@/types/application";

export const dynamic = "force-dynamic";

interface ApplicationDetailPageProps {
  params: Promise<{
    id: string;
  }>;
}

const statusStyles: Record<ApplicationStatus, string> = {
  SAVED: "bg-slate-100 text-slate-700",
  APPLIED: "bg-blue-100 text-blue-700",
  INTERVIEW: "bg-amber-100 text-amber-800",
  OFFER: "bg-emerald-100 text-emerald-700",
  REJECTED: "bg-red-100 text-red-700",
};

function formatDateTime(value: string): string {
  return new Intl.DateTimeFormat("en-CA", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function getSafeJobUrl(value: string | null): string | null {
  if (!value) {
    return null;
  }

  try {
    const parsedUrl = new URL(value);

    if (
      parsedUrl.protocol !== "http:" &&
      parsedUrl.protocol !== "https:"
    ) {
      return null;
    }

    return parsedUrl.toString();
  } catch {
    return null;
  }
}

export default async function ApplicationDetailPage({
  params,
}: ApplicationDetailPageProps) {
  const { id } = await params;

  let application;

  try {
    application = await getApplication(id);
  } catch {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-10">
        <div className="mx-auto max-w-4xl">
          <Link
            href="/"
            className="text-sm font-medium text-blue-700 hover:text-blue-900"
          >
            ← Back to applications
          </Link>

          <section className="mt-8 rounded-xl border border-red-200 bg-white p-8 shadow-sm">
            <h1 className="text-xl font-semibold text-red-700">
              Could not load application
            </h1>

            <p className="mt-2 text-sm text-slate-600">
              Confirm that the FastAPI backend and PostgreSQL services are
              running, then refresh this page.
            </p>
          </section>
        </div>
      </main>
    );
  }

  if (application === null) {
    notFound();
  }

  const safeJobUrl = getSafeJobUrl(application.job_url);

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/"
          className="text-sm font-medium text-blue-700 hover:text-blue-900"
        >
          ← Back to applications
        </Link>

        <header className="mt-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
            <div>
              <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
                {application.company}
              </p>

              <h1 className="mt-2 text-3xl font-bold text-slate-950">
                {application.title}
              </h1>

              <p className="mt-2 text-slate-600">
                {application.location ?? "Location not specified"}
              </p>
            </div>

            <span
              className={`inline-flex w-fit rounded-full px-3 py-1.5 text-sm font-semibold ${
                statusStyles[application.status]
              }`}
            >
              {application.status}
            </span>
          </div>

          <div className="mt-6 flex flex-wrap gap-x-6 gap-y-2 border-t border-slate-200 pt-5 text-sm text-slate-500">
            <p>Created {formatDateTime(application.created_at)}</p>
            <p>Updated {formatDateTime(application.updated_at)}</p>
          </div>
        </header>

        <div className="mt-6 grid gap-6">
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-950">
              Job posting
            </h2>

            <div className="mt-4">
              {safeJobUrl ? (
                <a
                  href={safeJobUrl}
                  target="_blank"
                  rel="noreferrer"
                  className="font-medium text-blue-700 hover:text-blue-900"
                >
                  Open original job posting ↗
                </a>
              ) : (
                <p className="text-sm text-slate-500">
                  No valid job posting URL provided.
                </p>
              )}
            </div>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-950">
              Job description
            </h2>

            <p className="mt-4 whitespace-pre-wrap leading-7 text-slate-700">
              {application.job_description}
            </p>
          </section>

          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-950">
              Notes
            </h2>

            {application.notes ? (
              <p className="mt-4 whitespace-pre-wrap leading-7 text-slate-700">
                {application.notes}
              </p>
            ) : (
              <p className="mt-4 text-sm text-slate-500">
                No notes have been added.
              </p>
            )}
          </section>
        </div>
      </div>
    </main>
  );
}
import Link from "next/link";
import { notFound } from "next/navigation";

import { getApplication } from "@/lib/api";

import EditApplicationForm from "./edit-application-form";

export const dynamic = "force-dynamic";

interface EditApplicationPageProps {
  params: Promise<{
    id: string;
  }>;
}

export default async function EditApplicationPage({
  params,
}: EditApplicationPageProps) {
  const { id } = await params;

  let application;

  try {
    application = await getApplication(id);
  } catch {
    return (
      <main className="min-h-screen bg-slate-50 px-6 py-10">
        <div className="mx-auto max-w-3xl">
          <Link
            href={`/applications/${id}`}
            className="text-sm font-medium text-blue-700 hover:text-blue-900"
          >
            ← Back to application
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

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-3xl">
        <Link
          href={`/applications/${application.id}`}
          className="text-sm font-medium text-blue-700 hover:text-blue-900"
        >
          ← Back to application
        </Link>

        <header className="mt-6">
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            Edit application
          </p>

          <h1 className="mt-2 text-3xl font-bold text-slate-950">
            {application.company}
          </h1>

          <p className="mt-2 text-slate-600">
            Update the role information, status, job description, or notes.
          </p>
        </header>

        <EditApplicationForm application={application} />
      </div>
    </main>
  );
}
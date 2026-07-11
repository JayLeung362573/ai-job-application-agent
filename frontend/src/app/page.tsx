import Link from "next/link";

import { getApplications } from "@/lib/api";
import type {
  Application,
  ApplicationStatus,
} from "@/types/application";

export const dynamic = "force-dynamic";

const statusStyles: Record<ApplicationStatus, string> = {
  SAVED: "bg-slate-100 text-slate-700",
  APPLIED: "bg-blue-100 text-blue-700",
  INTERVIEW: "bg-amber-100 text-amber-800",
  OFFER: "bg-emerald-100 text-emerald-700",
  REJECTED: "bg-red-100 text-red-700",
};

function countByStatus(
  applications: Application[],
  status: ApplicationStatus,
): number {
  return applications.filter(
    (application) => application.status === status,
  ).length;
}

function formatDate(value: string): string {
  return new Intl.DateTimeFormat("en-CA", {
    dateStyle: "medium",
  }).format(new Date(value));
}

export default async function Home() {
  let applications: Application[] = [];
  let errorMessage: string | null = null;

  try {
    applications = await getApplications();
  } catch (error) {
    errorMessage =
      error instanceof Error
        ? error.message
        : "Unable to load applications.";
  }

  const summaryCards = [
    {
      label: "Total Applications",
      value: applications.length,
    },
    {
      label: "Applied",
      value: countByStatus(applications, "APPLIED"),
    },
    {
      label: "Interviews",
      value: countByStatus(applications, "INTERVIEW"),
    },
    {
      label: "Offers",
      value: countByStatus(applications, "OFFER"),
    },
  ];

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-7xl">
        <header>
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            Internship Search
          </p>

          <h1 className="mt-2 text-3xl font-bold text-slate-950">
            Job Application Tracker
          </h1>

          <p className="mt-2 text-slate-600">
            Track applications and prepare role-specific resume analysis.
          </p>
        </header>

        <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {summaryCards.map((card) => (
            <article
              key={card.label}
              className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
            >
              <p className="text-sm font-medium text-slate-500">
                {card.label}
              </p>

              <p className="mt-2 text-3xl font-semibold text-slate-950">
                {card.value}
              </p>
            </article>
          ))}
        </section>

        <section className="mt-8 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
          <div className="border-b border-slate-200 px-6 py-5">
            <h2 className="text-lg font-semibold text-slate-950">
              Applications
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Most recently updated applications appear first.
            </p>
          </div>

          {errorMessage ? (
            <div className="px-6 py-12 text-center">
              <p className="font-medium text-red-700">
                Could not load applications
              </p>

              <p className="mt-2 text-sm text-slate-500">
                Confirm that the FastAPI backend and PostgreSQL services
                are running.
              </p>
            </div>
          ) : applications.length === 0 ? (
            <div className="px-6 py-12 text-center">
              <p className="font-medium text-slate-800">
                No applications yet
              </p>

              <p className="mt-2 text-sm text-slate-500">
                Applications created through the API will appear here.
              </p>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-slate-200">
                <thead className="bg-slate-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Company
                    </th>

                    <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Position
                    </th>

                    <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Status
                    </th>

                    <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Location
                    </th>

                    <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Updated
                    </th>

                    <th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wide text-slate-500">
                      Action
                    </th>
                  </tr>
                </thead>

                <tbody className="divide-y divide-slate-100">
                  {applications.map((application) => (
                    <tr
                      key={application.id}
                      className="hover:bg-slate-50"
                    >
                      <td className="whitespace-nowrap px-6 py-4 font-medium text-slate-900">
                        {application.company}
                      </td>

                      <td className="px-6 py-4 text-slate-700">
                        {application.title}
                      </td>

                      <td className="whitespace-nowrap px-6 py-4">
                        <span
                          className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${
                            statusStyles[application.status]
                          }`}
                        >
                          {application.status}
                        </span>
                      </td>

                      <td className="px-6 py-4 text-slate-600">
                        {application.location ?? "Not specified"}
                      </td>

                      <td className="whitespace-nowrap px-6 py-4 text-sm text-slate-500">
                        {formatDate(application.updated_at)}
                      </td>

                      <td className="whitespace-nowrap px-6 py-4 text-right">
                      <Link
                        href={`/applications/${application.id}`}
                        className="text-sm font-semibold text-blue-700 hover:text-blue-900"
                      >
                        View
                      </Link>
                    </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
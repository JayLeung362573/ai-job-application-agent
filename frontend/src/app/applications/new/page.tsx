"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { createApplication } from "@/lib/client-api";
import type {
  ApplicationCreatePayload,
  ApplicationStatus,
} from "@/types/application";

const statusOptions: Array<{
  value: ApplicationStatus;
  label: string;
}> = [
  { value: "SAVED", label: "Saved" },
  { value: "APPLIED", label: "Applied" },
  { value: "INTERVIEW", label: "Interview" },
  { value: "OFFER", label: "Offer" },
  { value: "REJECTED", label: "Rejected" },
];

const initialFormData = {
  company: "",
  title: "",
  location: "",
  jobUrl: "",
  status: "SAVED" as ApplicationStatus,
  jobDescription: "",
  notes: "",
};

export default function NewApplicationPage() {
  const router = useRouter();

  const [formData, setFormData] = useState(initialFormData);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  function updateField(
    field: keyof typeof initialFormData,
    value: string,
  ): void {
    setFormData((current) => ({
      ...current,
      [field]: value,
    }));
  }

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>,
  ): Promise<void> {
    event.preventDefault();

    const company = formData.company.trim();
    const title = formData.title.trim();
    const jobDescription = formData.jobDescription.trim();

    if (!company || !title || !jobDescription) {
      setErrorMessage(
        "Company, position title, and job description are required.",
      );
      return;
    }

    const payload: ApplicationCreatePayload = {
      company,
      title,
      location: formData.location.trim() || null,
      job_url: formData.jobUrl.trim() || null,
      status: formData.status,
      job_description: jobDescription,
      notes: formData.notes.trim() || null,
    };

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const application = await createApplication(payload);

      router.push(`/applications/${application.id}`);
      router.refresh();
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to create application.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-10">
      <div className="mx-auto max-w-3xl">
        <Link
          href="/"
          className="text-sm font-medium text-blue-700 hover:text-blue-900"
        >
          ← Back to applications
        </Link>

        <header className="mt-6">
          <p className="text-sm font-semibold uppercase tracking-wide text-slate-500">
            New application
          </p>

          <h1 className="mt-2 text-3xl font-bold text-slate-950">
            Add a job application
          </h1>

          <p className="mt-2 text-slate-600">
            Store the role information and job description before running
            resume analysis.
          </p>
        </header>

        <form
          onSubmit={handleSubmit}
          className="mt-8 space-y-6 rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
        >
          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <label
                htmlFor="company"
                className="block text-sm font-medium text-slate-700"
              >
                Company
              </label>

              <input
                id="company"
                type="text"
                required
                maxLength={255}
                value={formData.company}
                onChange={(event) =>
                  updateField("company", event.target.value)
                }
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Example Robotics"
              />
            </div>

            <div>
              <label
                htmlFor="title"
                className="block text-sm font-medium text-slate-700"
              >
                Position title
              </label>

              <input
                id="title"
                type="text"
                required
                maxLength={255}
                value={formData.title}
                onChange={(event) =>
                  updateField("title", event.target.value)
                }
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Software Engineering Intern"
              />
            </div>

            <div>
              <label
                htmlFor="location"
                className="block text-sm font-medium text-slate-700"
              >
                Location
              </label>

              <input
                id="location"
                type="text"
                maxLength={255}
                value={formData.location}
                onChange={(event) =>
                  updateField("location", event.target.value)
                }
                className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
                placeholder="Vancouver, BC"
              />
            </div>

            <div>
              <label
                htmlFor="status"
                className="block text-sm font-medium text-slate-700"
              >
                Status
              </label>

              <select
                id="status"
                value={formData.status}
                onChange={(event) =>
                  updateField("status", event.target.value)
                }
                className="mt-2 w-full rounded-lg border border-slate-300 bg-white px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              >
                {statusOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div>
            <label
              htmlFor="job-url"
              className="block text-sm font-medium text-slate-700"
            >
              Job posting URL
            </label>

            <input
              id="job-url"
              type="url"
              value={formData.jobUrl}
              onChange={(event) =>
                updateField("jobUrl", event.target.value)
              }
              className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              placeholder="https://example.com/jobs/software-intern"
            />
          </div>

          <div>
            <label
              htmlFor="job-description"
              className="block text-sm font-medium text-slate-700"
            >
              Job description
            </label>

            <textarea
              id="job-description"
              required
              rows={12}
              value={formData.jobDescription}
              onChange={(event) =>
                updateField("jobDescription", event.target.value)
              }
              className="mt-2 w-full resize-y rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              placeholder="Paste the complete job description here."
            />
          </div>

          <div>
            <label
              htmlFor="notes"
              className="block text-sm font-medium text-slate-700"
            >
              Notes
            </label>

            <textarea
              id="notes"
              rows={4}
              value={formData.notes}
              onChange={(event) =>
                updateField("notes", event.target.value)
              }
              className="mt-2 w-full resize-y rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              placeholder="Referral, deadline, interview notes, or resume changes."
            />
          </div>

          {errorMessage ? (
            <div
              role="alert"
              className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700"
            >
              {errorMessage}
            </div>
          ) : null}

          <div className="flex flex-col-reverse gap-3 border-t border-slate-200 pt-6 sm:flex-row sm:justify-end">
            <Link
              href="/"
              className="inline-flex justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
            >
              Cancel
            </Link>

            <button
              type="submit"
              disabled={isSubmitting}
              className="inline-flex justify-center rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {isSubmitting ? "Creating..." : "Create application"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}
"use client";

import Link from "next/link";
import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { updateApplication } from "@/lib/client-api";
import type {
  Application,
  ApplicationStatus,
  ApplicationUpdatePayload,
} from "@/types/application";

interface EditApplicationFormProps {
  application: Application;
}

interface EditFormData {
  company: string;
  title: string;
  location: string;
  jobUrl: string;
  status: ApplicationStatus;
  jobDescription: string;
  notes: string;
}

type TextFieldName =
  | "company"
  | "title"
  | "location"
  | "jobUrl"
  | "jobDescription"
  | "notes";

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

export default function EditApplicationForm({
  application,
}: EditApplicationFormProps) {
  const router = useRouter();

  const [formData, setFormData] = useState<EditFormData>({
    company: application.company,
    title: application.title,
    location: application.location ?? "",
    jobUrl: application.job_url ?? "",
    status: application.status,
    jobDescription: application.job_description,
    notes: application.notes ?? "",
  });

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  function updateTextField(
    field: TextFieldName,
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

    const payload: ApplicationUpdatePayload = {
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
      const updatedApplication = await updateApplication(
        application.id,
        payload,
      );

      router.replace(`/applications/${updatedApplication.id}`);
      router.refresh();
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to update application.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
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
              updateTextField("company", event.target.value)
            }
            className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
              updateTextField("title", event.target.value)
            }
            className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
              updateTextField("location", event.target.value)
            }
            className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
              setFormData((current) => ({
                ...current,
                status: event.target.value as ApplicationStatus,
              }))
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
            updateTextField("jobUrl", event.target.value)
          }
          className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
            updateTextField("jobDescription", event.target.value)
          }
          className="mt-2 w-full resize-y rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
            updateTextField("notes", event.target.value)
          }
          className="mt-2 w-full resize-y rounded-lg border border-slate-300 px-3 py-2.5 text-slate-950 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
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
          href={`/applications/${application.id}`}
          className="inline-flex justify-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50"
        >
          Cancel
        </Link>

        <button
          type="submit"
          disabled={isSubmitting}
          className="inline-flex justify-center rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isSubmitting ? "Saving..." : "Save changes"}
        </button>
      </div>
    </form>
  );
}
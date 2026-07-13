"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

import { deleteApplication } from "@/lib/client-api";

interface DeleteApplicationButtonProps {
  applicationId: string;
  applicationLabel: string;
}

export default function DeleteApplicationButton({
  applicationId,
  applicationLabel,
}: DeleteApplicationButtonProps) {
  const router = useRouter();

  const [isConfirming, setIsConfirming] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  function beginConfirmation(): void {
    setErrorMessage(null);
    setIsConfirming(true);
  }

  function cancelConfirmation(): void {
    if (isDeleting) {
      return;
    }

    setErrorMessage(null);
    setIsConfirming(false);
  }

  async function handleDelete(): Promise<void> {
    setIsDeleting(true);
    setErrorMessage(null);

    try {
      await deleteApplication(applicationId);

      router.replace("/");
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to delete application.",
      );
      setIsDeleting(false);
    }
  }

  if (!isConfirming) {
    return (
      <button
        type="button"
        onClick={beginConfirmation}
        className="inline-flex rounded-lg border border-red-300 bg-white px-4 py-2.5 text-sm font-semibold text-red-700 hover:bg-red-50"
      >
        Delete application
      </button>
    );
  }

  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4">
      <p className="font-semibold text-red-800">
        Delete this application?
      </p>

      <p className="mt-2 text-sm leading-6 text-red-700">
        You are about to permanently delete{" "}
        <span className="font-semibold">{applicationLabel}</span>. This
        action cannot be undone.
      </p>

      {errorMessage ? (
        <p
          role="alert"
          className="mt-3 rounded-md border border-red-300 bg-white px-3 py-2 text-sm text-red-700"
        >
          {errorMessage}
        </p>
      ) : null}

      <div className="mt-4 flex flex-col-reverse gap-3 sm:flex-row">
        <button
          type="button"
          onClick={cancelConfirmation}
          disabled={isDeleting}
          className="inline-flex justify-center rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-60"
        >
          Cancel
        </button>

        <button
          type="button"
          onClick={handleDelete}
          disabled={isDeleting}
          className="inline-flex justify-center rounded-lg bg-red-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-red-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {isDeleting ? "Deleting..." : "Delete permanently"}
        </button>
      </div>
    </div>
  );
}
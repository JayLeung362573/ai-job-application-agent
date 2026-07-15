"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { runApplicationAnalysis } from "@/lib/client-api";

interface RunAnalysisButtonProps {
  applicationId: string;
  hasExistingAnalysis: boolean;
}

export default function RunAnalysisButton({
  applicationId,
  hasExistingAnalysis,
}: RunAnalysisButtonProps) {
  const router = useRouter();

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(
    null,
  );

  async function handleRunAnalysis() {
    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await runApplicationAnalysis(applicationId);
      router.refresh();
    } catch (error) {
      setErrorMessage(
        error instanceof Error
          ? error.message
          : "Unable to analyze application.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="flex flex-col items-start gap-2 sm:items-end">
      <button
        type="button"
        onClick={handleRunAnalysis}
        disabled={isSubmitting}
        className="inline-flex min-w-32 justify-center rounded-lg bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-300"
      >
        {isSubmitting
          ? "Analyzing..."
          : hasExistingAnalysis
            ? "Run again"
            : "Run analysis"}
      </button>

      {errorMessage ? (
        <p
          role="alert"
          className="max-w-sm text-sm text-red-700 sm:text-right"
        >
          {errorMessage}
        </p>
      ) : null}
    </div>
  );
}
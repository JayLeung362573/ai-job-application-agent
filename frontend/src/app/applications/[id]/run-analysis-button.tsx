"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { runApplicationAnalysis } from "@/lib/client-api";

const ACCESS_TOKEN_STORAGE_KEY = "analysis-access-token";

interface RunAnalysisButtonProps {
  applicationId: string;
  hasExistingAnalysis: boolean;
}

export default function RunAnalysisButton({
  applicationId,
  hasExistingAnalysis,
}: RunAnalysisButtonProps) {
  const router = useRouter();

  const [accessToken, setAccessToken] = useState("");
  const [isTokenRequired, setIsTokenRequired] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(
    null,
  );

  async function handleRunAnalysis() {
    const storedToken = window.sessionStorage.getItem(
      ACCESS_TOKEN_STORAGE_KEY,
    );

    const token = (
      isTokenRequired ? accessToken : storedToken
    )?.trim();

    if (!token) {
      setIsTokenRequired(true);
      setErrorMessage(null);
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await runApplicationAnalysis(applicationId, token);

      window.sessionStorage.setItem(
        ACCESS_TOKEN_STORAGE_KEY,
        token,
      );

      setAccessToken("");
      setIsTokenRequired(false);
      router.refresh();
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unable to analyze application.";

      if (message === "Invalid analysis access password.") {
        window.sessionStorage.removeItem(
          ACCESS_TOKEN_STORAGE_KEY,
        );
        setAccessToken("");
        setIsTokenRequired(true);
      }

      setErrorMessage(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form
      className="flex flex-col items-start gap-2 sm:items-end"
      onSubmit={(event) => {
        event.preventDefault();
        void handleRunAnalysis();
      }}
    >
      {isTokenRequired ? (
        <label className="flex flex-col gap-1 text-sm text-slate-700">
          Analysis access password
          <input
            type="password"
            value={accessToken}
            onChange={(event) => {
              setAccessToken(event.target.value);
            }}
            autoComplete="current-password"
            autoFocus
            required
            className="w-64 rounded-lg border border-slate-300 px-3 py-2 text-slate-950 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />
        </label>
      ) : null}

      <button
        type="submit"
        disabled={isSubmitting}
        className="inline-flex min-w-32 justify-center rounded-lg bg-blue-700 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:bg-blue-300"
      >
        {isSubmitting
          ? "Analyzing..."
          : isTokenRequired
            ? "Unlock and analyze"
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
    </form>
  );
}
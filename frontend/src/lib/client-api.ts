import type {
  Application,
  ApplicationCreatePayload,
  ApplicationUpdatePayload,
} from "@/types/application";

import type { Analysis } from "@/types/analysis";
import { resolveApiUrl } from "@/lib/api-url";

const PUBLIC_API_URL = resolveApiUrl(
  process.env.NEXT_PUBLIC_API_URL,
  "NEXT_PUBLIC_API_URL",
);

interface ApiValidationError {
  loc?: Array<string | number>;
  msg?: string;
  type?: string;
}

interface ApiErrorBody {
  detail?: string | ApiValidationError[];
}

async function getApiErrorMessage(
  response: Response,
  fallbackMessage: string,
): Promise<string> {
  try {
    const body = (await response.json()) as ApiErrorBody;

    if (typeof body.detail === "string") {
      return body.detail;
    }

    if (Array.isArray(body.detail)) {
      const firstError = body.detail[0];

      if (firstError?.msg) {
        return firstError.msg;
      }
    }
  } catch {
    // Use the fallback when the response body is not valid JSON.
  }

  return fallbackMessage;
}

export async function createApplication(
  payload: ApplicationCreatePayload,
): Promise<Application> {
  const response = await fetch(`${PUBLIC_API_URL}/applications`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const message = await getApiErrorMessage(
      response,
      "Unable to create application.",
    );

    throw new Error(message);
  }

  return (await response.json()) as Application;
}

export async function updateApplication(
  applicationId: string,
  payload: ApplicationUpdatePayload,
): Promise<Application> {
  const response = await fetch(
    `${PUBLIC_API_URL}/applications/${encodeURIComponent(applicationId)}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(payload),
    },
  );

  if (!response.ok) {
    const message = await getApiErrorMessage(
      response,
      "Unable to update application.",
    );

    throw new Error(message);
  }

  return (await response.json()) as Application;
}

export async function deleteApplication(
  applicationId: string,
): Promise<void> {
  const response = await fetch(
    `${PUBLIC_API_URL}/applications/${encodeURIComponent(applicationId)}`,
    {
      method: "DELETE",
      headers: {
        Accept: "application/json",
      },
    },
  );

  if (!response.ok) {
    const message = await getApiErrorMessage(
      response,
      "Unable to delete application.",
    );

    throw new Error(message);
  }
}

export async function runApplicationAnalysis(
  applicationId: string,
  accessToken: string,
): Promise<Analysis> {
  const response = await fetch(
    `${PUBLIC_API_URL}/applications/${encodeURIComponent(applicationId)}/analyze`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
        "X-Analysis-Access-Token": accessToken,
      },
    },
  );

  if (response.status === 401) {
    throw new Error("Invalid analysis access password.");
  }

  if (!response.ok) {
    const message = await getApiErrorMessage(
      response,
      "Unable to analyze application.",
    );

    throw new Error(message);
  }

  return (await response.json()) as Analysis;
}
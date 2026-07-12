import type {
  Application,
  ApplicationCreatePayload,
} from "@/types/application";

const PUBLIC_API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface ApiErrorBody {
  detail?: string | Array<{
    loc?: Array<string | number>;
    msg?: string;
    type?: string;
  }>;
}

function getErrorMessage(body: ApiErrorBody): string {
  if (typeof body.detail === "string") {
    return body.detail;
  }

  if (Array.isArray(body.detail)) {
    const firstError = body.detail[0];

    if (firstError?.msg) {
      return firstError.msg;
    }
  }

  return "Unable to create application.";
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
    let message = "Unable to create application.";

    try {
      const errorBody = (await response.json()) as ApiErrorBody;
      message = getErrorMessage(errorBody);
    } catch {
      // Keep the fallback message when the response is not JSON.
    }

    throw new Error(message);
  }

  return (await response.json()) as Application;
}
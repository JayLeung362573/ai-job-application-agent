const LOCAL_API_URL = "http://localhost:8000";

export function resolveApiUrl(
  value: string | undefined,
  variableName: string,
): string {
  const normalizedValue = value?.trim().replace(/\/+$/, "");

  if (normalizedValue) {
    return normalizedValue;
  }

  if (process.env.NODE_ENV === "production") {
    throw new Error(
      `${variableName} must be configured in production.`,
    );
  }

  return LOCAL_API_URL;
}
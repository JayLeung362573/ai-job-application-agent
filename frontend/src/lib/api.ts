import type { Application } from "@/types/application";

const API_URL = process.env.API_URL ?? "http://localhost:8000";

export async function getApplications(): Promise<Application[]> {
  const response = await fetch(`${API_URL}/applications`, {
    cache: "no-store",
    headers: {
      Accept: "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(
      `Failed to load applications: backend returned ${response.status}`,
    );
  }

  return (await response.json()) as Application[];
}
import type {
  Application,
  ApplicationStatus,
} from "@/types/application";

import type { Analysis } from "@/types/analysis";

const API_URL = process.env.API_URL ?? "http://localhost:8000";

export interface ApplicationFilters {
  q?: string;
  status?: ApplicationStatus;
}

export async function getApplications(
  filters: ApplicationFilters = {},
): Promise<Application[]> {
  const searchParams = new URLSearchParams();

  const searchTerm = filters.q?.trim();

  if (searchTerm) {
    searchParams.set("q", searchTerm);
  }

  if (filters.status) {
    searchParams.set("status", filters.status);
  }

  const queryString = searchParams.toString();
  const endpoint = `${API_URL}/applications${
    queryString ? `?${queryString}` : ""
  }`;

  const response = await fetch(endpoint, {
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

export async function getApplication(
  applicationId: string,
): Promise<Application | null> {
  const response = await fetch(
    `${API_URL}/applications/${encodeURIComponent(applicationId)}`,
    {
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    },
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      `Failed to load application: backend returned ${response.status}`,
    );
  }

  return (await response.json()) as Application;
}

export async function getLatestApplicationAnalysis(
  applicationId: string,
): Promise<Analysis | null> {
  const response = await fetch(
    `${API_URL}/applications/${encodeURIComponent(applicationId)}/analysis`,
    {
      cache: "no-store",
      headers: {
        Accept: "application/json",
      },
    },
  );

  if (response.status === 404) {
    return null;
  }

  if (!response.ok) {
    throw new Error(
      `Failed to load analysis: backend returned ${response.status}`,
    );
  }

  return (await response.json()) as Analysis;
}
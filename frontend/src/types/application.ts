export type ApplicationStatus =
  | "SAVED"
  | "APPLIED"
  | "INTERVIEW"
  | "OFFER"
  | "REJECTED";

export interface Application {
  id: string;
  company: string;
  title: string;
  location: string | null;
  job_url: string | null;
  status: ApplicationStatus;
  job_description: string;
  notes: string | null;
  created_at: string;
  updated_at: string;
}
export interface MatchedProject {
  project_name: string;
  matched_skills: string[];
  reason: string;
}

export interface SuggestedBullet {
  project_name: string;
  bullet: string;
  target_skill: string;
}

export interface Analysis {
  id: string;
  application_id: string;
  required_skills: string[];
  preferred_skills: string[];
  responsibilities: string[];
  matched_projects: MatchedProject[];
  missing_skills: string[];
  suggested_bullets: SuggestedBullet[];
  interview_questions: string[];
  match_score: number;
  created_at: string;
}
import type { Analysis } from "@/types/analysis";

import RunAnalysisButton from "./run-analysis-button";

interface AnalysisSectionProps {
  applicationId: string;
  analysis: Analysis | null;
}

function formatDateTime(value: string): string {
  return new Intl.DateTimeFormat("en-CA", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function SkillList({
  skills,
  emptyMessage,
  variant = "default",
}: {
  skills: string[];
  emptyMessage: string;
  variant?: "default" | "missing";
}) {
  if (skills.length === 0) {
    return (
      <p className="mt-3 text-sm text-slate-500">
        {emptyMessage}
      </p>
    );
  }

  const skillClasses =
    variant === "missing"
      ? "bg-red-50 text-red-700 ring-red-200"
      : "bg-blue-50 text-blue-700 ring-blue-200";

  return (
    <div className="mt-3 flex flex-wrap gap-2">
      {skills.map((skill, index) => (
        <span
          key={`${skill}-${index}`}
          className={`rounded-full px-2.5 py-1 text-xs font-semibold ring-1 ring-inset ${skillClasses}`}
        >
          {skill}
        </span>
      ))}
    </div>
  );
}

export default function AnalysisSection({
  applicationId,
  analysis,
}: AnalysisSectionProps) {
  return (
    <section className="mt-6 rounded-xl border border-blue-200 bg-white p-6 shadow-sm">
      <header className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
        <div>
          <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
            Resume match agent
          </p>

          <h2 className="mt-2 text-xl font-semibold text-slate-950">
            Role analysis
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">
            Compare this job description against the stored resume
            projects and generate role-specific preparation material.
          </p>
        </div>

        <RunAnalysisButton
          applicationId={applicationId}
          hasExistingAnalysis={analysis !== null}
        />
      </header>

      {analysis === null ? (
        <div className="mt-6 rounded-lg border border-dashed border-slate-300 bg-slate-50 px-5 py-8 text-center">
          <p className="font-medium text-slate-800">
            No analysis has been generated
          </p>

          <p className="mt-2 text-sm text-slate-500">
            Run the analysis to identify matching projects, missing
            skills, resume suggestions, and interview questions.
          </p>
        </div>
      ) : (
        <>
          <div className="mt-6 grid gap-4 md:grid-cols-[180px_minmax(0,1fr)]">
            <div className="rounded-xl bg-slate-950 p-5 text-white">
              <p className="text-sm font-medium text-slate-300">
                Match score
              </p>

              <p className="mt-2 text-4xl font-bold">
                {analysis.match_score}%
              </p>

              <p className="mt-4 text-xs leading-5 text-slate-400">
                Generated {formatDateTime(analysis.created_at)}
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <div className="rounded-xl border border-slate-200 p-5">
                <h3 className="font-semibold text-slate-900">
                  Required skills
                </h3>

                <SkillList
                  skills={analysis.required_skills}
                  emptyMessage="No required skills were identified."
                />
              </div>

              <div className="rounded-xl border border-slate-200 p-5">
                <h3 className="font-semibold text-slate-900">
                  Missing skills
                </h3>

                <SkillList
                  skills={analysis.missing_skills}
                  emptyMessage="No missing skills were identified."
                  variant="missing"
                />
              </div>

              <div className="rounded-xl border border-slate-200 p-5 sm:col-span-2">
                <h3 className="font-semibold text-slate-900">
                  Preferred skills
                </h3>

                <SkillList
                  skills={analysis.preferred_skills}
                  emptyMessage="No preferred skills were identified."
                />
              </div>
            </div>
          </div>

          <div className="mt-8">
            <h3 className="text-lg font-semibold text-slate-950">
              Matched projects
            </h3>

            {analysis.matched_projects.length > 0 ? (
              <div className="mt-4 grid gap-4">
                {analysis.matched_projects.map(
                  (project, index) => (
                    <article
                      key={`${project.project_name}-${index}`}
                      className="rounded-xl border border-slate-200 bg-slate-50 p-5"
                    >
                      <h4 className="font-semibold text-slate-950">
                        {project.project_name}
                      </h4>

                      <div className="mt-3 flex flex-wrap gap-2">
                        {project.matched_skills.map(
                          (skill, skillIndex) => (
                            <span
                              key={`${skill}-${skillIndex}`}
                              className="rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 ring-1 ring-inset ring-emerald-200"
                            >
                              {skill}
                            </span>
                          ),
                        )}
                      </div>

                      <p className="mt-4 text-sm leading-6 text-slate-600">
                        {project.reason}
                      </p>
                    </article>
                  ),
                )}
              </div>
            ) : (
              <p className="mt-3 text-sm text-slate-500">
                No stored projects matched the identified skills.
              </p>
            )}
          </div>

          <div className="mt-8">
            <h3 className="text-lg font-semibold text-slate-950">
              Suggested resume bullets
            </h3>

            {analysis.suggested_bullets.length > 0 ? (
              <ul className="mt-4 space-y-3">
                {analysis.suggested_bullets.map(
                  (suggestion, index) => (
                    <li
                      key={`${suggestion.project_name}-${index}`}
                      className="rounded-xl border border-slate-200 p-5"
                    >
                      <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                        {suggestion.project_name}
                      </p>

                      <p className="mt-2 leading-7 text-slate-800">
                        {suggestion.bullet}
                      </p>

                      <p className="mt-3 text-sm text-blue-700">
                        Target skill: {suggestion.target_skill}
                      </p>
                    </li>
                  ),
                )}
              </ul>
            ) : (
              <p className="mt-3 text-sm text-slate-500">
                No resume bullet suggestions were generated.
              </p>
            )}
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-2">
            <div>
              <h3 className="text-lg font-semibold text-slate-950">
                Responsibilities
              </h3>

              {analysis.responsibilities.length > 0 ? (
                <ul className="mt-4 list-disc space-y-2 pl-5 text-slate-700">
                  {analysis.responsibilities.map(
                    (responsibility, index) => (
                      <li key={`${responsibility}-${index}`}>
                        {responsibility}
                      </li>
                    ),
                  )}
                </ul>
              ) : (
                <p className="mt-3 text-sm text-slate-500">
                  No responsibilities were identified.
                </p>
              )}
            </div>

            <div>
              <h3 className="text-lg font-semibold text-slate-950">
                Interview questions
              </h3>

              {analysis.interview_questions.length > 0 ? (
                <ol className="mt-4 list-decimal space-y-2 pl-5 text-slate-700">
                  {analysis.interview_questions.map(
                    (question, index) => (
                      <li key={`${question}-${index}`}>
                        {question}
                      </li>
                    ),
                  )}
                </ol>
              ) : (
                <p className="mt-3 text-sm text-slate-500">
                  No interview questions were generated.
                </p>
              )}
            </div>
          </div>
        </>
      )}
    </section>
  );
}
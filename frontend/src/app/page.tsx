import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 px-8 py-10">
      <section className="mx-auto max-w-5xl">
        <h1 className="text-3xl font-bold text-slate-900">
          AI Job Application Tracker
        </h1>
        <p className="mt-3 text-slate-600">
          Track internship applications, store job descriptions, and analyze role fit.
        </p>
      </section>
    </main>
  );
}

import Link from "next/link";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";
import { Button } from "@/components/ui/Button";

export default async function HomePage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  const isAuthenticated = !!session;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="py-20 text-center">
        <h1 className="text-5xl font-bold text-[var(--foreground)] mb-6">
          Organize Your Tasks
          <span className="text-[var(--primary)]"> Effortlessly</span>
        </h1>
        <p className="text-xl text-[var(--muted-foreground)] mb-8 max-w-2xl mx-auto">
          A simple, powerful todo app to help you stay organized and productive.
          Create, manage, and complete your tasks with ease.
        </p>
        <div className="flex gap-4 justify-center">
          {isAuthenticated ? (
            <Link href="/dashboard">
              <Button size="lg">Go to Dashboard</Button>
            </Link>
          ) : (
            <Link href="/register">
              <Button size="lg">Get Started</Button>
            </Link>
          )}
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 grid md:grid-cols-3 gap-8">
        <div className="bg-[var(--card)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
          <div className="w-12 h-12 bg-[var(--accent)] rounded-lg flex items-center justify-center mb-4">
            <svg
              className="w-6 h-6 text-[var(--primary)]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6v6m0 0v6m0-6h6m-6 0H6"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold mb-2 text-[var(--foreground)]">Easy Task Creation</h3>
          <p className="text-[var(--muted-foreground)]">
            Quickly add tasks with titles and descriptions. Stay organized with minimal effort.
          </p>
        </div>

        <div className="bg-[var(--card)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
          <div className="w-12 h-12 bg-[var(--accent)] rounded-lg flex items-center justify-center mb-4">
            <svg
              className="w-6 h-6 text-[var(--primary)]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold mb-2 text-[var(--foreground)]">Track Progress</h3>
          <p className="text-[var(--muted-foreground)]">
            Mark tasks as complete and filter by status. See your progress at a glance.
          </p>
        </div>

        <div className="bg-[var(--card)] p-6 rounded-xl shadow-sm border border-[var(--border)]">
          <div className="w-12 h-12 bg-[var(--accent)] rounded-lg flex items-center justify-center mb-4">
            <svg
              className="w-6 h-6 text-[var(--primary)]"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"
              />
            </svg>
          </div>
          <h3 className="text-lg font-semibold mb-2 text-[var(--foreground)]">Secure & Private</h3>
          <p className="text-[var(--muted-foreground)]">
            Your tasks are private and secure. Only you can see and manage your data.
          </p>
        </div>
      </div>
    </div>
  );
}

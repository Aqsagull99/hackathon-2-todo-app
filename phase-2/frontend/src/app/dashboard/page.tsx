import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";
import { TaskList } from "@/components/tasks/TaskList";
import { SignJWT } from "jose";

export const metadata = {
  title: "Dashboard - Todo App",
  description: "Manage your tasks",
};

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login");
  }

  // Create a JWT signed specifically for our Python backend
  // using the same secret and algorithm (HS256)
  const secret = new TextEncoder().encode(
    process.env.BETTER_AUTH_SECRET || "Gidun9j+gA9F5uj7HIh2m2jalXqCJH357iqRZUJfAqg="
  );

  const accessToken = await new SignJWT({
    sub: session.user.id,
    email: session.user.email,
    userId: session.user.id,
  })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("2h")
    .sign(secret);

  return (
    <div className="min-h-screen">
      {/* Header */}
      <div className="border-b border-[var(--border)] bg-white">
        <div className="max-w-4xl mx-auto px-4 py-8">
          <h1 className="text-3xl font-bold text-[var(--foreground)]">
            Welcome, {session.user.name || "User"}!
          </h1>
          <p className="text-[var(--muted-foreground)] mt-1">
            Manage your tasks and stay productive.
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <TaskList userId={session.user.id} accessToken={accessToken} />
      </div>
    </div>
  );
}

import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";
import { DashboardClient } from "@/components/dashboard/DashboardClient";
import { SignJWT } from "jose";

// Force this page to be dynamic to prevent static generation
export const dynamic = 'force-dynamic';

export const metadata = {
  title: "Dashboard - Todo App",
  description: "Manage your tasks",
};

export default async function DashboardPage({ searchParams }: { searchParams: Promise<Record<string, string | string[] | undefined>> }) {
  const resolvedSearchParams = await searchParams;

  // Ensure we're getting the headers properly for session validation
  const requestHeaders = await headers();
  const session = await auth.api.getSession({
    headers: requestHeaders,
  });

  if (!session) {
    console.log("No session found, redirecting to login"); // Debug log
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
    <DashboardClient
      userId={session.user.id}
      accessToken={accessToken}
      userName={session.user.name}
      initialShowAddTask={resolvedSearchParams.addTask === "true"}
    />
  );
}
import { redirect } from "next/navigation";
import { headers } from "next/headers";
import { auth } from "@/lib/auth";
import { DashboardClient } from "@/components/dashboard/DashboardClient";
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
    <DashboardClient
      userId={session.user.id}
      accessToken={accessToken}
      userName={session.user.name}
    />
  );
}

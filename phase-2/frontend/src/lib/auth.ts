/**
 * Better Auth server configuration
 */
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { Pool } from "pg";

// Create a singleton pool to prevent multiple connections during dev
const globalForPool = globalThis as unknown as { pool: Pool | undefined };

export const pool = globalForPool.pool ?? new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: process.env.NODE_ENV === "production" ? {
    rejectUnauthorized: false
  } : undefined // No SSL in development unless required
});

if (process.env.NODE_ENV !== "production") globalForPool.pool = pool;

// Ensure the secret is properly set - fail loudly if missing
const authSecret = process.env.BETTER_AUTH_SECRET || process.env.AUTH_SECRET;
if (!authSecret) {
  console.error("BETTER_AUTH_SECRET is not set! This will cause authentication to fail.");
  // Use a placeholder in dev, but in production this should be set
  if (process.env.NODE_ENV === "production") {
    throw new Error("BETTER_AUTH_SECRET environment variable is required in production");
  }
}

export const auth = betterAuth({
  secret: authSecret || "dev-secret-for-development-only-change-in-production",
  baseURL: process.env.BETTER_AUTH_URL ||
           (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` :
           process.env.VERCEL_BRANCH_URL ? `https://${process.env.VERCEL_BRANCH_URL}` :
           "http://localhost:3000"),
  database: pool,
  trustedOrigins: [
    "https://hackathon-2-todo-app-theta.vercel.app",  // Production Vercel URL
    `https://hackathon-2-todo-app-theta-git-*vercel.app`, // Vercel preview URLs
    "http://localhost:3000",                          // Local development
    "http://127.0.0.1:3000",                         // Alternative local address
  ],
  emailAndPassword: {
    enabled: true,
    autoSignIn: true,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    },
    facebook: {
      clientId: process.env.FACEBOOK_CLIENT_ID as string,
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET as string,
    },
  },
  advanced: {
    useSecureCookies: process.env.NODE_ENV === "production", // Force secure cookies in production
    session: {
      expiresIn: 7 * 24 * 60 * 60, // 7 days in seconds
      updateAge: 24 * 60 * 60,      // Update session every 24 hours
    },
    defaultCookieAttributes: {
      // Set default attributes for all cookies
      sameSite: process.env.NODE_ENV === "production" ? "none" : "lax", // "none" for cross-site in production with secure
      secure: process.env.NODE_ENV === "production", // Secure in production
    }
  },
  plugins: [
    nextCookies()
  ],
});

export type Session = typeof auth.$Infer.Session;

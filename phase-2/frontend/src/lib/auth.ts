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

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: process.env.BETTER_AUTH_URL || (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000"),
  database: pool,
  trustedOrigins: [
    "https://hackathon-2-todo-app-theta.vercel.app",  // Production Vercel URL
    `https://${process.env.VERCEL_URL}`,               // Dynamic Vercel URL during build
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

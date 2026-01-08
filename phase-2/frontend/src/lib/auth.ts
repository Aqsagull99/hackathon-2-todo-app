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
  ssl: {
      rejectUnauthorized: false
  }
});

if (process.env.NODE_ENV !== "production") globalForPool.pool = pool;

export const auth = betterAuth({
  database: pool,
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
  plugins: [
    nextCookies()
  ],
});

export type Session = typeof auth.$Infer.Session;

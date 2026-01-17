/**
 * Better Auth client for React components
 */
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

// Determine the correct base URL based on environment
const getBaseURL = () => {
  if (typeof window !== "undefined") {
    // Browser environment
    return process.env.NEXT_PUBLIC_BETTER_AUTH_URL ||
           (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000");
  } else {
    // Server environment
    return process.env.BETTER_AUTH_URL ||
           (process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "http://localhost:3000");
  }
};

export const authClient = createAuthClient({
  baseURL: getBaseURL(),
  plugins: [
    jwtClient()
  ]
});

export const { signIn, signUp, signOut, useSession } = authClient;

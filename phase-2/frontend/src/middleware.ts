/**
 * Next.js Middleware for Authentication Protection
 *
 * Protects routes based on auth state from Better Auth.
 * Public routes are accessible without authentication.
 * Protected routes require valid session.
 */
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { getSessionCookie } from "better-auth/cookies";

// Public routes that don't require authentication
const publicRoutes = ["/", "/login", "/register"];

export function middleware(req: NextRequest) {
  try {
    // Use Better Auth's utility to properly parse the session cookie
    // This handles the different prefixes automatically (__Secure- in production)
    const sessionToken = getSessionCookie(req);

    const isLoggedIn = !!sessionToken;
    const isOnPublicRoute = publicRoutes.includes(req.nextUrl.pathname);

    // If on a protected route without being logged in, redirect to login
    if (!isOnPublicRoute && !isLoggedIn) {
      return NextResponse.redirect(new URL("/login", req.url));
    }

    // If logged in and trying to access login/register, redirect to dashboard
    if ((req.nextUrl.pathname === "/login" || req.nextUrl.pathname === "/register") && isLoggedIn) {
      return NextResponse.redirect(new URL("/dashboard", req.url));
    }
  } catch (error) {
    // If there's an error parsing the session, treat as not logged in
    console.error("Session parsing error:", error);
    const isOnPublicRoute = publicRoutes.includes(req.nextUrl.pathname);

    if (!isOnPublicRoute) {
      return NextResponse.redirect(new URL("/login", req.url));
    }
  }

  return NextResponse.next();
}

// Configure which paths the middleware runs on
export const config = {
  matcher: [
    /*
     * Match all request paths except for:
     * - api routes (handled by Better Auth API)
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!api|_next/static|_next/image|favicon.ico|public).*)",
  ],
};

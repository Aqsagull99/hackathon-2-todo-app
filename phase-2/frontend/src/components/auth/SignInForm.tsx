"use client";

import React, { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { signIn } from "@/lib/auth-client";
import {
  FormField,
  SocialButton,
  AppLogo,
  PrimaryButton,
  RememberMeCheckbox,
} from "./AuthComponents";
import { cn } from "@/lib/utils";

type SocialProvider = "facebook" | "instagram" | "pinterest";

interface SignInFormProps {
  onSocialSignIn?: (provider: SocialProvider) => void;
}

export function SignInForm({ onSocialSignIn }: SignInFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const [rememberMe, setRememberMe] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [socialLoading, setSocialLoading] = useState<SocialProvider | null>(null);
  const [generalError, setGeneralError] = useState<string | null>(null);

  const validateField = (name: string, value: string): string => {
    switch (name) {
      case "email":
        if (!value.trim()) return "Email is required";
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) return "Please enter a valid email address";
        return "";
      case "password":
        if (!value) return "Password is required";
        return "";
      default:
        return "";
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setGeneralError(null);

    if (touched[name]) {
      setErrors((prev) => ({ ...prev, [name]: validateField(name, value) }));
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setTouched((prev) => ({ ...prev, [name]: true }));
    setErrors((prev) => ({ ...prev, [name]: validateField(name, value) }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const newErrors: Record<string, string> = {};
    let hasErrors = false;

    Object.keys(formData).forEach((key) => {
      const error = validateField(key, formData[key as keyof typeof formData]);
      if (error) {
        newErrors[key] = error;
        hasErrors = true;
      }
    });

    setErrors(newErrors);
    setTouched(
      Object.keys(formData).reduce((acc, key) => ({ ...acc, [key]: true }), {})
    );

    if (hasErrors) return;

    setIsLoading(true);
    setGeneralError(null);

    try {
      const result = await signIn.email({
        email: formData.email,
        password: formData.password,
        rememberMe,
      });

      if (result.error) {
        setGeneralError(result.error.message || "Sign in failed. Please try again.");
        return;
      }

      router.push("/dashboard");
      router.refresh();
    } catch (err) {
      setGeneralError(
        err instanceof Error ? err.message : "An unexpected error occurred"
      );
    } finally {
      setIsLoading(false);
    }
  };

  const handleSocialSignIn = async (provider: SocialProvider) => {
    setSocialLoading(provider);
    try {
      await signIn.social({ provider });
    } catch (err) {
      setGeneralError(
        err instanceof Error ? err.message : `${provider} sign in failed. Please try again.`
      );
      setSocialLoading(null);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center p-4 md:p-8">
      {/* Ambient Background Glow */}
      <div
        className="fixed inset-0 pointer-events-none ambient-glow"
        aria-hidden="true"
      />

      {/* Animated Background Shapes - Softer for SignIn */}
      <div
        className="fixed top-1/3 left-1/3 w-80 h-80 bg-[rgba(255,110,199,0.06)] rounded-full blur-3xl pointer-events-none animate-pulse"
        style={{ animationDuration: "5s" }}
        aria-hidden="true"
      />
      <div
        className="fixed bottom-1/3 right-1/3 w-64 h-64 bg-[rgba(219,39,119,0.04)] rounded-full blur-3xl pointer-events-none animate-pulse"
        style={{ animationDuration: "6s", animationDelay: "1s" }}
        aria-hidden="true"
      />

      <div className="w-full max-w-6xl flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
        {/* Left Panel - Context & Trust (35-40%) */}
        <div className="flex-1 w-full max-w-lg lg:max-w-none text-center lg:text-left order-2 lg:order-1 lg:pr-8">
          <div className="flex justify-center lg:justify-start mb-6">
            <AppLogo />
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-4xl font-bold text-white leading-tight mb-4">
            Welcome back
          </h1>

          <p className="text-base md:text-lg text-[rgba(255,255,255,0.7)] leading-relaxed max-w-sm mx-auto lg:mx-0">
            Pick up right where you left off. Your tasks are waiting.
          </p>
        </div>

        {/* Right Panel - Quick Action (60-65%) */}
        <div className="flex-1 w-full max-w-lg lg:max-w-none order-1 lg:order-2">
          <div className="glass rounded-2xl p-6 md:p-8 pink-glow">
            {/* Card Header */}
            <div className="text-center mb-8">
              <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
                Sign In
              </h2>
              <p className="text-[rgba(255,255,255,0.6)] text-sm">
                Enter your credentials to access your account
              </p>
            </div>

            {/* General Error Alert */}
            {generalError && (
              <div
                className="mb-6 p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-sm text-red-400"
                role="alert"
                aria-live="assertive"
              >
                <div className="flex items-start gap-3">
                  <svg
                    className="w-5 h-5 flex-shrink-0 mt-0.5"
                    fill="currentColor"
                    viewBox="0 0 20 20"
                    aria-hidden="true"
                  >
                    <path
                      fillRule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clipRule="evenodd"
                    />
                  </svg>
                  <p>{generalError}</p>
                </div>
              </div>
            )}

            {/* Form */}
            <form onSubmit={handleSubmit} noValidate>
              <div className="space-y-5">
                <FormField
                  id="email"
                  label="Email Address"
                  type="email"
                  placeholder="Enter your email"
                  value={formData.email}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  error={touched.email ? errors.email : undefined}
                  required
                  autoComplete="email"
                />

                <FormField
                  id="password"
                  label="Password"
                  type="password"
                  placeholder="Enter your password"
                  value={formData.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  error={touched.password ? errors.password : undefined}
                  required
                  autoComplete="current-password"
                />

                {/* Remember Me & Forgot Password Row */}
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <RememberMeCheckbox
                    checked={rememberMe}
                    onChange={(e) => setRememberMe(e.target.checked)}
                    label="Remember me"
                  />

                  <Link
                    href="/forgot-password"
                    className={cn(
                      "text-sm font-medium transition-colors duration-200",
                      "text-[rgba(255,110,199,0.8)] hover:text-[rgba(255,110,199,1)]",
                      "focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]",
                      "rounded"
                    )}
                  >
                    Forgot password?
                  </Link>
                </div>

                {/* Submit Button */}
                <PrimaryButton type="submit" isLoading={isLoading} className="text-white">
                  Sign In
                </PrimaryButton>
              </div>

              {/* Social Sign In Divider */}
              <div className="relative my-8">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-[rgba(255,110,199,0.2)]" />
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-4 bg-[rgba(255,110,199,0.08)] text-[rgba(255,255,255,0.5)]">
                    or continue with
                  </span>
                </div>
              </div>

              {/* Social Buttons */}
              <div className="flex justify-center gap-4">
                <SocialButton
                  provider="facebook"
                  onClick={() => handleSocialSignIn("facebook")}
                  label="Sign in with Facebook"
                  isLoading={socialLoading === "facebook"}
                />
                <SocialButton
                  provider="instagram"
                  onClick={() => handleSocialSignIn("instagram")}
                  label="Sign in with Instagram"
                  isLoading={socialLoading === "instagram"}
                />
                <SocialButton
                  provider="pinterest"
                  onClick={() => handleSocialSignIn("pinterest")}
                  label="Sign in with Pinterest"
                  isLoading={socialLoading === "pinterest"}
                />
              </div>

              {/* Sign Up Link */}
              <p className="mt-8 text-center text-sm text-[rgba(255,255,255,0.6)]">
                Do not have an account?{" "}
                <Link
                  href="/register"
                  className={cn(
                    "font-medium transition-colors duration-200",
                    "text-[rgba(255,110,199,0.8)] hover:text-[rgba(255,110,199,1)]",
                    "focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]",
                    "rounded"
                  )}
                >
                  Sign up
                </Link>
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignInForm;

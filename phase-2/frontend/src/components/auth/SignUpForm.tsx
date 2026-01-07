"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { signUp } from "@/lib/auth-client";
import {
  FormField,
  SocialButton,
  AppLogo,
  PrimaryButton,
  FacebookIcon,
  InstagramIcon,
  PinterestIcon,
} from "./AuthComponents";
import { cn } from "@/lib/utils";

type SocialProvider = "facebook" | "google";

interface SignUpFormProps {
  onSocialSignUp?: (provider: SocialProvider) => void;
}

export function SignUpForm({ onSocialSignUp }: SignUpFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [touched, setTouched] = useState<Record<string, boolean>>({});
  const [isLoading, setIsLoading] = useState(false);
  const [socialLoading, setSocialLoading] = useState<SocialProvider | null>(null);
  const [generalError, setGeneralError] = useState<string | null>(null);

  const validateField = (name: string, value: string): string => {
    switch (name) {
      case "fullName":
        if (!value.trim()) return "Full name is required";
        if (value.trim().length < 2) return "Name must be at least 2 characters";
        return "";
      case "email":
        if (!value.trim()) return "Email is required";
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) return "Please enter a valid email address";
        return "";
      case "password":
        if (!value) return "Password is required";
        if (value.length < 8) return "Password must be at least 8 characters";
        if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value)) {
          return "Password must contain uppercase, lowercase, and number";
        }
        return "";
      case "confirmPassword":
        if (!value) return "Please confirm your password";
        if (value !== formData.password) return "Passwords do not match";
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
      const result = await signUp.email({
        email: formData.email,
        password: formData.password,
        name: formData.fullName.trim(),
      });

      if (result.error) {
        setGeneralError(result.error.message || "Registration failed. Please try again.");
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

  const handleSocialSignUp = async (provider: SocialProvider) => {
    setSocialLoading(provider);
    try {
      // For social sign-up, we need to redirect to the provider's OAuth page
      if (provider === 'google') {
        window.location.href = '/api/auth/google';
      } else if (provider === 'facebook') {
        window.location.href = '/api/auth/facebook';
      }
    } catch (err) {
      setGeneralError(
        err instanceof Error ? err.message : `${provider} sign up failed. Please try again.`
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

      {/* Animated Background Shapes */}
      <div
        className="fixed top-1/4 left-1/4 w-96 h-96 bg-[rgba(255,110,199,0.08)] rounded-full blur-3xl pointer-events-none animate-pulse"
        style={{ animationDuration: "4s" }}
        aria-hidden="true"
      />
      <div
        className="fixed bottom-1/4 right-1/4 w-80 h-80 bg-[rgba(219,39,119,0.06)] rounded-full blur-3xl pointer-events-none animate-pulse"
        style={{ animationDuration: "5s", animationDelay: "1s" }}
        aria-hidden="true"
      />

      <div className="w-full max-w-6xl flex flex-col lg:flex-row items-center gap-8 lg:gap-12">
        {/* Left Panel - Brand & Motivation (45%) */}
        <div className="flex-1 w-full max-w-xl lg:max-w-none text-center lg:text-left order-2 lg:order-1">
          <div className="flex justify-center lg:justify-start mb-8">
            <AppLogo />
          </div>

          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-white leading-tight mb-4">
            Organize your life.{" "}
            <span className="block mt-2 text-[rgba(255,110,199,0.9)]">
              One task at a time.
            </span>
          </h1>

          <p className="text-base md:text-lg text-[rgba(255,255,255,0.7)] leading-relaxed max-w-md mx-auto lg:mx-0">
            A clean, focused todo app designed to help you stay consistent and
            stress-free.
          </p>

          {/* Decorative Pink Glow Elements */}
          <div
            className="hidden lg:block absolute top-1/3 left-[15%] w-32 h-32 bg-[rgba(255,110,199,0.1)] rounded-full blur-2xl pointer-events-none"
            aria-hidden="true"
          />
        </div>

        {/* Right Panel - Action Card (55%) */}
        <div className="flex-1 w-full max-w-lg lg:max-w-none order-1 lg:order-2">
          <div className="glass rounded-2xl p-6 md:p-8 pink-glow">
            {/* Card Header */}
            <div className="text-center mb-8">
              <h2 className="text-2xl md:text-3xl font-bold text-white mb-2">
                Sign Up
              </h2>
              <p className="text-[rgba(255,255,255,0.6)] text-sm">
                Create your account to get started
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
                  id="fullName"
                  label="Full Name"
                  type="text"
                  placeholder="Enter your full name"
                  value={formData.fullName}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  error={touched.fullName ? errors.fullName : undefined}
                  required
                  autoComplete="name"
                />

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
                  placeholder="Create a password"
                  value={formData.password}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  error={touched.password ? errors.password : undefined}
                  required
                  autoComplete="new-password"
                />

                <FormField
                  id="confirmPassword"
                  label="Confirm Password"
                  type="password"
                  placeholder="Confirm your password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  onBlur={handleBlur}
                  error={touched.confirmPassword ? errors.confirmPassword : undefined}
                  required
                  autoComplete="new-password"
                />

                {/* Submit Button */}
                <PrimaryButton type="submit" isLoading={isLoading}>
                  Create Account
                </PrimaryButton>
              </div>

              {/* Social Sign Up Divider */}
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
                  onClick={() => handleSocialSignUp("facebook")}
                  label="Sign up with Facebook"
                  isLoading={socialLoading === "facebook"}
                />
                <SocialButton
                  provider="google"
                  onClick={() => handleSocialSignUp("google")}
                  label="Sign up with Google"
                  isLoading={socialLoading === "google"}
                />
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignUpForm;

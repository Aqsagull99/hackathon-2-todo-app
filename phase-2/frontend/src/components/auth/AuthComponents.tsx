"use client";

import React from "react";
import { cn } from "@/lib/utils";

// ============================================================================
// SOCIAL ICONS - Used in both SignUp and SignIn
// ============================================================================

export const FacebookIcon = ({ className }: { className?: string }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
  </svg>
);

export const InstagramIcon = ({ className }: { className?: string }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z" />
  </svg>
);

export const PinterestIcon = ({ className }: { className?: string }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="currentColor"
    aria-hidden="true"
  >
    <path d="M12 0C5.373 0 0 5.372 0 12c0 5.084 3.163 9.426 7.627 11.174-.105-.949-.2-2.405.042-3.441.218-.937 1.407-5.965 1.407-5.965s-.359-.719-.359-1.782c0-1.668.967-2.914 2.171-2.914 1.023 0 1.518.769 1.518 1.69 0 1.029-.655 2.568-.994 3.995-.283 1.194.599 2.169 1.777 2.169 2.133 0 3.772-2.249 3.772-5.495 0-2.873-2.064-4.882-5.012-4.882-3.414 0-5.418 2.561-5.418 5.207 0 1.031.397 2.138.893 2.738.098.119.112.224.083.345l-.333 1.36c-.053.22-.174.267-.402.161-1.499-.698-2.436-2.889-2.436-4.649 0-3.785 2.75-7.262 7.929-7.262 4.163 0 7.398 2.967 7.398 6.931 0 4.136-2.607 7.464-6.227 7.464-1.216 0-2.359-.631-2.75-1.378l-.748 2.853c-.271 1.043-1.002 2.35-1.492 3.146C9.57 23.812 10.763 24 12 24c6.627 0 12-5.373 12-12 0-6.628-5.373-12-12-12z" />
  </svg>
);

// ============================================================================
// FORM FIELD COMPONENT - Reusable across both screens
// ============================================================================

interface FormFieldProps {
  id: string;
  label: string;
  type?: string;
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  autoComplete?: string;
  showPasswordToggle?: boolean;
}

export function FormField({
  id,
  label,
  type = "text",
  placeholder,
  value,
  onChange,
  onBlur,
  error,
  required = false,
  autoComplete,
}: FormFieldProps) {
  const fieldId = id || `field-${label.toLowerCase().replace(/\s+/g, "-")}`;

  return (
    <div className="w-full">
      <label
        htmlFor={fieldId}
        className="block text-sm font-medium text-[rgba(255,110,199,0.9)] mb-2"
      >
        {label}
        {required && (
          <span className="text-[rgba(255,110,199,0.6)] ml-0.5" aria-hidden="true">
            *
          </span>
        )}
      </label>
      <input
        id={fieldId}
        name={fieldId}
        type={type}
        autoComplete={autoComplete}
        required={required}
        value={value}
        onChange={onChange}
        onBlur={onBlur}
        placeholder={placeholder}
        aria-invalid={error ? "true" : "false"}
        aria-describedby={error ? `${fieldId}-error` : undefined}
        className={cn(
          "w-full px-4 py-3.5 rounded-lg text-white placeholder-[rgba(255,255,255,0.4)]",
          "bg-[rgba(255,255,255,0.08)] border transition-all duration-200",
          "backdrop-blur-sm focus:outline-none",
          error
            ? "border-red-500/50 focus:border-red-500/50 focus:ring-2 focus:ring-red-500/20"
            : "border-[rgba(255,110,199,0.25)] focus:border-[rgba(255,110,199,0.5)] focus:ring-2 focus:ring-[rgba(255,110,199,0.2)]"
        )}
      />
      {error && (
        <p
          id={`${fieldId}-error`}
          className="mt-1.5 text-sm text-red-400"
          role="alert"
        >
          {error}
        </p>
      )}
    </div>
  );
}

// ============================================================================
// SOCIAL BUTTON COMPONENT - Reusable across both screens
// ============================================================================

type SocialProvider = "facebook" | "instagram" | "pinterest";

interface SocialButtonProps {
  provider: SocialProvider;
  onClick: () => void;
  label: string;
  isLoading?: boolean;
}

export function SocialButton({
  provider,
  onClick,
  label,
  isLoading = false,
}: SocialButtonProps) {
  const icons: Record<SocialProvider, React.ComponentType<{ className?: string }>> = {
    facebook: FacebookIcon,
    instagram: InstagramIcon,
    pinterest: PinterestIcon,
  };

  const Icon = icons[provider];

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={isLoading}
      aria-label={label}
      className={cn(
        "group w-12 h-12 rounded-xl bg-[rgba(255,255,255,0.08)] border border-[rgba(255,110,199,0.25)]",
        "hover:bg-[rgba(255,110,199,0.15)] hover:border-[rgba(255,110,199,0.45)]",
        "focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]",
        "transition-all duration-200 flex items-center justify-center",
        "disabled:opacity-50 disabled:cursor-not-allowed"
      )}
    >
      {isLoading ? (
        <svg
          className="animate-spin h-5 w-5 text-[rgba(255,110,199,0.8)]"
          fill="none"
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
      ) : (
        <Icon className="w-5 h-5 text-[rgba(255,255,255,0.9)] group-hover:text-white transition-colors" />
      )}
    </button>
  );
}

// ============================================================================
// APP LOGO COMPONENT - Used in both screens
// ============================================================================

export function AppLogo({ className }: { className?: string }) {
  return (
    <div className={cn("flex items-center gap-3", className)} aria-hidden="true">
      <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[rgba(255,110,199,0.9)] to-[rgba(219,39,119,0.9)] flex items-center justify-center shadow-lg shadow-[rgba(255,110,199,0.3)]">
        <svg
          className="w-6 h-6 text-white"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          strokeWidth={2}
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"
          />
        </svg>
      </div>
      <span className="text-xl font-semibold text-white tracking-tight">TaskFlow</span>
    </div>
  );
}

// ============================================================================
// PRIMARY BUTTON COMPONENT
// ============================================================================

interface PrimaryButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  isLoading?: boolean;
  children: React.ReactNode;
}

export function PrimaryButton({
  isLoading = false,
  children,
  className,
  disabled,
  ...props
}: PrimaryButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      className={cn(
        "w-full py-3.5 px-6 rounded-xl font-semibold text-white",
        "bg-gradient-to-r from-[rgba(255,110,199,0.9)] to-[rgba(219,39,119,0.9)]",
        "hover:from-[rgba(255,110,199,1)] hover:to-[rgba(219,39,119,1)]",
        "focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]",
        "active:scale-[0.98] transition-all duration-200",
        "disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100",
        "shadow-lg shadow-[rgba(255,110,199,0.3)]",
        className
      )}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center justify-center gap-2">
          <svg
            className="animate-spin h-5 w-5"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          {children}
        </span>
      ) : (
        children
      )}
    </button>
  );
}

// ============================================================================
// REMEMBER ME CHECKBOX COMPONENT - SignIn only
// ============================================================================

interface RememberMeCheckboxProps {
  checked: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  label?: string;
}

export function RememberMeCheckbox({
  checked,
  onChange,
  label = "Remember me",
}: RememberMeCheckboxProps) {
  return (
    <label className="flex items-center gap-3 cursor-pointer group">
      <div className="relative flex items-center">
        <input
          type="checkbox"
          checked={checked}
          onChange={onChange}
          className={cn(
            "peer appearance-none w-5 h-5 rounded border-2 border-[rgba(255,110,199,0.35)]",
            "bg-[rgba(255,255,255,0.08)] checked:bg-[rgba(255,110,199,0.8)]",
            "checked:border-[rgba(255,110,199,0.8)]",
            "focus:outline-none focus:ring-2 focus:ring-[rgba(255,110,199,0.4)] focus:ring-offset-2 focus:ring-offset-[#0a0a0f]",
            "transition-all duration-200 cursor-pointer"
          )}
        />
        <svg
          className="absolute left-0.5 top-0.5 w-3.5 h-3.5 text-white opacity-0 peer-checked:opacity-100 pointer-events-none transition-opacity"
          viewBox="0 0 14 14"
          fill="none"
          aria-hidden="true"
        >
          <path
            d="M3 8L6 11L11 5.5"
            stroke="currentColor"
            strokeWidth={2}
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        </svg>
      </div>
      <span className="text-sm text-[rgba(255,255,255,0.7)] group-hover:text-white transition-colors">
        {label}
      </span>
    </label>
  );
}

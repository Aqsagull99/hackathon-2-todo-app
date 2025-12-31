import { HTMLAttributes, ReactNode } from "react";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  children: ReactNode;
}

export function Card({ children, className = "", ...props }: CardProps) {
  return (
    <div
      className={`bg-[var(--card)] text-[var(--card-foreground)] rounded-xl shadow-sm border border-[var(--border)] ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ children, className = "", ...props }: CardProps) {
  return (
    <div className={`px-6 py-4 border-b border-[var(--border)] ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardContent({ children, className = "", ...props }: CardProps) {
  return (
    <div className={`px-6 py-4 ${className}`} {...props}>
      {children}
    </div>
  );
}

export function CardFooter({ children, className = "", ...props }: CardProps) {
  return (
    <div
      className={`px-6 py-4 border-t border-[var(--border)] bg-[var(--muted)] rounded-b-xl ${className}`}
      {...props}
    >
      {children}
    </div>
  );
}

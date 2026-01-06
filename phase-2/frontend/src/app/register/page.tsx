import { SignUpForm } from "@/components/auth/SignUpForm";

export const metadata = {
  title: "Create Account - TaskFlow",
  description: "Sign up for TaskFlow and start organizing your life today.",
};

export default function RegisterPage() {
  return <SignUpForm />;
}

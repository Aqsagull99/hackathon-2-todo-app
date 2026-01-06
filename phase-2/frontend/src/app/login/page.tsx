import { SignInForm } from "@/components/auth/SignInForm";

export const metadata = {
  title: "Sign In - TaskFlow",
  description: "Sign in to your TaskFlow account",
};

export default function LoginPage() {
  return <SignInForm />;
}

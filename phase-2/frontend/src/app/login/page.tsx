import { LoginForm } from "@/components/auth/LoginForm";

export const metadata = {
  title: "Sign In - Todo App",
  description: "Sign in to your Todo App account",
};

export default function LoginPage() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center py-12 px-4">
      <LoginForm />
    </div>
  );
}

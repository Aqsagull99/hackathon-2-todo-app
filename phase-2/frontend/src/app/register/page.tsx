import { RegisterForm } from "@/components/auth/RegisterForm";

export const metadata = {
  title: "Create Account - Todo App",
  description: "Create your Todo App account",
};

export default function RegisterPage() {
  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center py-12 px-4 bg-[var(--secondary)]">
      <RegisterForm />
    </div>
  );
}

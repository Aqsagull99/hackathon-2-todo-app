'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import AuthLayout from '@/components/layout/AuthLayout';
import SignUpForm from '@/components/features/auth/SignUpForm';

const SignUpPage: React.FC = () => {
  const router = useRouter();

  const handleSignUpSuccess = () => {
    // Redirect to dashboard after successful signup
    router.push('/dashboard');
  };

  return (
    <AuthLayout title="Create Account">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Create your account</h2>
        <p className="mt-2 text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/signin" className="font-medium text-pink-600 hover:text-pink-500">
            Sign in
          </Link>
        </p>
      </div>

      <SignUpForm onSuccess={handleSignUpSuccess} />

      <div className="mt-6 text-center text-sm text-gray-500">
        By signing up, you agree to our{' '}
        <Link href="/terms" className="font-medium text-pink-600 hover:text-pink-500">
          Terms
        </Link>{' '}
        and{' '}
        <Link href="/privacy" className="font-medium text-pink-600 hover:text-pink-500">
          Privacy Policy
        </Link>
        .
      </div>
    </AuthLayout>
  );
};

export default SignUpPage;
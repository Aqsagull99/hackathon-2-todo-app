'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button, Input } from '@/components/ui';
import { Mail, Lock } from 'lucide-react';
import AuthLayout from '@/components/layout/AuthLayout';

const SignInPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    setLoading(true);

    try {
      // In a real app, this would call the backend API
      console.log('Signing in with:', { email, password });

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // On success, redirect to dashboard
      router.push('/dashboard');
    } catch (err) {
      setError('Invalid email or password. Please try again.');
      console.error('Sign in error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Sign In">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Sign in to your account</h2>
        <p className="mt-2 text-sm text-gray-600">
          Don't have an account?{' '}
          <Link href="/signup" className="font-medium text-pink-600 hover:text-pink-500">
            Sign up
          </Link>
        </p>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md text-sm">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700">
            Email Address
          </label>
          <div className="mt-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Mail className="h-5 w-5 text-gray-400" />
            </div>
            <Input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="pl-10 w-full"
              placeholder="email@example.com"
            />
          </div>
        </div>

        <div>
          <div className="flex items-center justify-between">
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <div className="text-sm">
              <Link href="/forgot-password" className="font-medium text-pink-600 hover:text-pink-500">
                Forgot password?
              </Link>
            </div>
          </div>
          <div className="mt-1 relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Lock className="h-5 w-5 text-gray-400" />
            </div>
            <Input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="pl-10 w-full"
              placeholder="••••••••"
            />
          </div>
        </div>

        <div>
          <Button
            type="submit"
            className="w-full bg-pink-600 hover:bg-pink-700"
            disabled={loading}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </Button>
        </div>
      </form>

      <div className="mt-6 text-center text-sm text-gray-500">
        By signing in, you agree to our{' '}
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

export default SignInPage;
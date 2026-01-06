import React from 'react';
import Link from 'next/link';

interface AuthLayoutProps {
  children: React.ReactNode;
  title?: string;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title = 'Todo App' }) => {
  return (
    <div className="min-h-screen bg-pink-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <div className="flex justify-center">
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            {title}
          </h2>
        </div>
        <p className="mt-2 text-center text-sm text-gray-600">
          Securely manage your tasks
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          {children}
          <div className="mt-6 text-center text-sm text-gray-500">
            <Link href="/" className="font-medium text-pink-600 hover:text-pink-500">
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout;
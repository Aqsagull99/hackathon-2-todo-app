import React from 'react';

interface LayoutProps {
  children: React.ReactNode;
}

export const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-pink-600">Todo App</h1>
          </div>
          <nav className="flex space-x-4">
            <a href="/" className="text-gray-700 hover:text-pink-600 px-3 py-2 rounded-md text-sm font-medium">
              Home
            </a>
            <a href="/dashboard" className="text-gray-700 hover:text-pink-600 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </a>
          </nav>
        </div>
      </div>
    </header>
  );
};

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="md:flex md:items-center md:justify-between">
          <div className="text-center md:text-left">
            <p className="text-sm text-gray-500">&copy; 2026 Todo App. All rights reserved.</p>
          </div>
        </div>
      </div>
    </footer>
  );
};

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-grow">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
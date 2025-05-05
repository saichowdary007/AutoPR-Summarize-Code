import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'PR Summary & Code Review Assistant',
  description: 'Generate comprehensive PR summaries and conduct automated code reviews',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="light">
      <head>
        {/* Force stylesheet reload on client */}
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body className={`${inter.className} antialiased bg-gray-50 min-h-screen`}>
        <div className="flex flex-col min-h-screen">
          <header className="sticky top-0 z-10 bg-white shadow-sm">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
              <a href="/" className="flex items-center space-x-2">
                <span className="font-bold text-xl text-primary-600">PR Assistant</span>
              </a>
              <nav className="hidden md:flex space-x-8">
                <a href="/" className="text-gray-600 hover:text-primary-600 transition-colors">
                  Home
                </a>
                <a href="/pr-summary" className="text-gray-600 hover:text-primary-600 transition-colors">
                  PR Summary
                </a>
                <a href="/code-review" className="text-gray-600 hover:text-primary-600 transition-colors">
                  Code Review
                </a>
              </nav>
            </div>
          </header>
          
          <main className="flex-grow container mx-auto px-4 py-8">
            {children}
          </main>
          
          <footer className="bg-gray-800 text-white py-8">
            <div className="container mx-auto px-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div>
                  <h3 className="text-lg font-semibold mb-4">PR Assistant</h3>
                  <p className="text-gray-300">
                    A powerful tool for generating comprehensive PR summaries and conducting code reviews automatically.
                  </p>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-4">Links</h3>
                  <ul className="space-y-2">
                    <li>
                      <a href="/" className="text-gray-300 hover:text-white transition-colors">
                        Home
                      </a>
                    </li>
                    <li>
                      <a href="/pr-summary" className="text-gray-300 hover:text-white transition-colors">
                        PR Summary
                      </a>
                    </li>
                    <li>
                      <a href="/code-review" className="text-gray-300 hover:text-white transition-colors">
                        Code Review
                      </a>
                    </li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-4">About</h3>
                  <p className="text-gray-300">
                    Built to help developers and reviewers improve code quality and streamline PR processes.
                  </p>
                </div>
              </div>
              <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-400">
                <p>&copy; {new Date().getFullYear()} PR Summary & Code Review Assistant. All rights reserved.</p>
              </div>
            </div>
          </footer>
        </div>
      </body>
    </html>
  );
} 
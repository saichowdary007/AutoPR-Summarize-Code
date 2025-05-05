import Link from 'next/link';
import { FaGithub, FaCode, FaFileAlt } from 'react-icons/fa';

export default function Home() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="py-16 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-3xl text-white">
        <div className="container mx-auto px-6 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-6">
            PR Summary & Code Review Assistant
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
            Automatically generate comprehensive PR summaries and conduct thorough code reviews to improve code quality.
          </p>
          <div className="flex flex-col md:flex-row justify-center gap-4">
            <Link 
              href="/pr-summary" 
              className="btn bg-white text-primary-600 hover:bg-gray-100 transition-colors px-8 py-3 rounded-lg font-medium text-lg"
            >
              Generate PR Summary
            </Link>
            <Link 
              href="/code-review"
              className="btn bg-secondary-700 text-white hover:bg-secondary-800 transition-colors px-8 py-3 rounded-lg font-medium text-lg"
            >
              Perform Code Review
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-12">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Key Features</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card p-6 hover:shadow-lg transition-shadow">
              <div className="text-primary-500 mb-4">
                <FaFileAlt className="w-12 h-12" />
              </div>
              <h3 className="text-xl font-bold mb-3">Comprehensive PR Summaries</h3>
              <p className="text-gray-600">
                Generate structured summaries with title, overview, key changes, affected components, testing info, and more.
              </p>
            </div>
            
            {/* Feature 2 */}
            <div className="card p-6 hover:shadow-lg transition-shadow">
              <div className="text-primary-500 mb-4">
                <FaCode className="w-12 h-12" />
              </div>
              <h3 className="text-xl font-bold mb-3">Thorough Code Reviews</h3>
              <p className="text-gray-600">
                Automatically analyze code for security issues, performance bottlenecks, code quality problems, and test coverage gaps.
              </p>
            </div>
            
            {/* Feature 3 */}
            <div className="card p-6 hover:shadow-lg transition-shadow">
              <div className="text-primary-500 mb-4">
                <FaGithub className="w-12 h-12" />
              </div>
              <h3 className="text-xl font-bold mb-3">GitHub Integration</h3>
              <p className="text-gray-600">
                Seamlessly connect to GitHub repositories, analyze PRs, and optionally post review comments directly to PR threads.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-12 bg-gray-50 rounded-3xl">
        <div className="container mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center">
              <div className="bg-primary-100 text-primary-600 rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">1</div>
              <h3 className="text-xl font-bold mb-2">Connect Repository</h3>
              <p className="text-gray-600">Provide your GitHub repository details and PR number.</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 text-primary-600 rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">2</div>
              <h3 className="text-xl font-bold mb-2">Configure Analysis</h3>
              <p className="text-gray-600">Customize strictness level, focus areas, and other review parameters.</p>
            </div>
            
            <div className="text-center">
              <div className="bg-primary-100 text-primary-600 rounded-full w-16 h-16 flex items-center justify-center text-2xl font-bold mx-auto mb-4">3</div>
              <h3 className="text-xl font-bold mb-2">Get Results</h3>
              <p className="text-gray-600">Receive detailed PR summary or code review analysis in seconds.</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-12 bg-dark text-white rounded-3xl">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to improve your code review process?</h2>
          <p className="text-xl mb-8 max-w-3xl mx-auto">
            Start using our PR Summary & Code Review Assistant today and save time while improving code quality.
          </p>
          <div className="flex flex-col md:flex-row justify-center gap-4">
            <Link 
              href="/pr-summary" 
              className="btn bg-primary-600 text-white hover:bg-primary-700 transition-colors px-8 py-3 rounded-lg font-medium text-lg"
            >
              Get Started
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
} 
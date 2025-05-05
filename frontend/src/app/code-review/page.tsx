'use client';

import { useState } from 'react';
import { FaExclamationTriangle, FaCheckCircle, FaChartBar } from 'react-icons/fa';
import RepositoryForm from '@/components/RepositoryForm';
import CodeReviewIssueCard from '@/components/CodeReviewIssueCard';
import { getCodeReview } from '@/lib/api';
import type { CodeReviewResponse } from '@/lib/api';

export default function CodeReviewPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [review, setReview] = useState<CodeReviewResponse | null>(null);
  const [activeTab, setActiveTab] = useState<string>('all');

  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Prepare request payload
      const payload = {
        repo_owner: data.repo_owner,
        repo_name: data.repo_name,
        pr_number: data.pr_number,
        github_token: data.github_token,
        config: {
          strictness_level: data.strictness_level,
        },
        post_comments: data.post_comments,
      };
      
      // Call API
      const result = await getCodeReview(payload);
      setReview(result);
    } catch (err: any) {
      console.error('Error performing code review:', err);
      setError(err.response?.data?.detail || err.message || 'An error occurred while performing the code review.');
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate total issues
  const getTotalIssues = () => {
    if (!review) return 0;
    return (
      review.security_issues.length +
      review.performance_issues.length +
      review.code_quality_issues.length +
      review.test_coverage_issues.length
    );
  };

  // Get current issues based on active tab
  const getCurrentIssues = () => {
    if (!review) return [];
    
    switch (activeTab) {
      case 'security':
        return review.security_issues;
      case 'performance':
        return review.performance_issues;
      case 'quality':
        return review.code_quality_issues;
      case 'testing':
        return review.test_coverage_issues;
      case 'all':
      default:
        return [
          ...review.security_issues,
          ...review.performance_issues,
          ...review.code_quality_issues,
          ...review.test_coverage_issues,
        ];
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Code Review</h1>
        <p className="text-gray-600">
          Automatically analyze pull requests for security issues, performance problems, 
          code quality concerns, and test coverage gaps.
        </p>
      </div>
      
      {!review ? (
        <div className="card p-6">
          <RepositoryForm
            onSubmit={handleSubmit}
            isLoading={isLoading}
            includeCodeReviewOptions={true}
          />
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-700 rounded-md flex items-start">
              <FaExclamationTriangle className="mt-1 mr-2 flex-shrink-0" />
              <p>{error}</p>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Code Review Results</h2>
            <button
              onClick={() => setReview(null)}
              className="btn btn-outline"
            >
              New Review
            </button>
          </div>
          
          {/* Stats Summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-primary-600">
                {review.statistics.files_analyzed}
              </div>
              <div className="text-sm text-gray-500">Files Analyzed</div>
            </div>
            
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-primary-600">
                {getTotalIssues()}
              </div>
              <div className="text-sm text-gray-500">Total Issues</div>
            </div>
            
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-primary-600">
                {review.statistics.lines_added}
              </div>
              <div className="text-sm text-gray-500">Lines Added</div>
            </div>
            
            <div className="card p-4 text-center">
              <div className="text-2xl font-bold text-primary-600">
                {review.statistics.lines_removed}
              </div>
              <div className="text-sm text-gray-500">Lines Removed</div>
            </div>
          </div>
          
          {/* Severity summary */}
          <div className="card p-6">
            <h3 className="text-xl font-semibold mb-3 flex items-center">
              <FaChartBar className="mr-2" />
              Issues by Severity
            </h3>
            
            <div className="grid grid-cols-4 gap-4">
              <div className="flex flex-col items-center">
                <div className="text-lg font-bold text-critical">
                  {review.statistics.severity_counts.critical}
                </div>
                <div className="text-sm text-gray-500">Critical</div>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="text-lg font-bold text-high">
                  {review.statistics.severity_counts.high}
                </div>
                <div className="text-sm text-gray-500">High</div>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="text-lg font-bold text-medium">
                  {review.statistics.severity_counts.medium}
                </div>
                <div className="text-sm text-gray-500">Medium</div>
              </div>
              
              <div className="flex flex-col items-center">
                <div className="text-lg font-bold text-low">
                  {review.statistics.severity_counts.low}
                </div>
                <div className="text-sm text-gray-500">Low</div>
              </div>
            </div>
          </div>
          
          {/* Issues List */}
          <div>
            {/* Tabs */}
            <div className="border-b border-gray-200 mb-6">
              <nav className="-mb-px flex space-x-6">
                <button
                  className={`pb-3 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'all'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                  onClick={() => setActiveTab('all')}
                >
                  All ({getTotalIssues()})
                </button>
                
                <button
                  className={`pb-3 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'security'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                  onClick={() => setActiveTab('security')}
                >
                  Security ({review.statistics.issue_counts.security})
                </button>
                
                <button
                  className={`pb-3 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'performance'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                  onClick={() => setActiveTab('performance')}
                >
                  Performance ({review.statistics.issue_counts.performance})
                </button>
                
                <button
                  className={`pb-3 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'quality'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                  onClick={() => setActiveTab('quality')}
                >
                  Quality ({review.statistics.issue_counts.code_quality})
                </button>
                
                <button
                  className={`pb-3 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'testing'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                  onClick={() => setActiveTab('testing')}
                >
                  Testing ({review.statistics.issue_counts.test_coverage})
                </button>
              </nav>
            </div>
            
            {/* Issues */}
            <div className="space-y-4">
              {getCurrentIssues().length === 0 ? (
                <div className="text-center p-6 bg-gray-50 rounded-lg">
                  <FaCheckCircle className="mx-auto mb-3 text-green-500 w-10 h-10" />
                  <h3 className="text-lg font-medium text-gray-900">No issues found!</h3>
                  <p className="mt-1 text-gray-500">
                    No issues were detected in this category. Great job!
                  </p>
                </div>
              ) : (
                getCurrentIssues().map((issue, index) => (
                  <CodeReviewIssueCard key={index} issue={issue} index={index} />
                ))
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
} 
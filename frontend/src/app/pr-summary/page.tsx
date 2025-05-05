'use client';

import { useState } from 'react';
import { FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import RepositoryForm from '@/components/RepositoryForm';
import { getPRSummary } from '@/lib/api';
import type { SummaryResponse } from '@/lib/api';

export default function PRSummaryPage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [summary, setSummary] = useState<SummaryResponse | null>(null);

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
      };
      
      // Call API
      const result = await getPRSummary(payload);
      setSummary(result);
    } catch (err: any) {
      console.error('Error generating PR summary:', err);
      setError(err.response?.data?.detail || err.message || 'An error occurred while generating the PR summary.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">PR Summary Generator</h1>
        <p className="text-gray-600">
          Generate a comprehensive summary of any GitHub pull request to quickly understand its purpose, 
          changes, and potential impact.
        </p>
      </div>
      
      {!summary ? (
        <div className="card p-6">
          <RepositoryForm
            onSubmit={handleSubmit}
            isLoading={isLoading}
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
            <h2 className="text-2xl font-bold">{summary.title}</h2>
            <button
              onClick={() => setSummary(null)}
              className="btn btn-outline"
            >
              New Summary
            </button>
          </div>
          
          <div className="card p-6">
            <h3 className="text-xl font-semibold mb-3">Overview</h3>
            <p className="text-gray-700">{summary.overview}</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-3">Key Changes</h3>
              <ul className="space-y-2">
                {summary.changes_summary.map((change, index) => (
                  <li key={index} className="flex items-start">
                    <FaCheckCircle className="text-primary-500 mt-1 mr-2 flex-shrink-0" />
                    <span>{change}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-3">Affected Components</h3>
              <ul className="space-y-1">
                {summary.affected_components.map((component, index) => (
                  <li key={index} className="px-2 py-1 bg-gray-100 rounded text-sm font-mono">
                    {component}
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          {summary.testing && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-3">Testing</h3>
              <p className="text-gray-700">{summary.testing}</p>
            </div>
          )}
          
          {summary.dependencies && summary.dependencies.length > 0 && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-3">Dependencies</h3>
              <ul className="space-y-1">
                {summary.dependencies.map((dep, index) => (
                  <li key={index} className="px-2 py-1 bg-gray-100 rounded text-sm font-mono">
                    {dep}
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {summary.migration_notes && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-3">Migration Notes</h3>
              <div className="p-3 bg-yellow-50 border-l-4 border-yellow-400 text-gray-700">
                {summary.migration_notes}
              </div>
            </div>
          )}
          
          {summary.potential_risks && summary.potential_risks.length > 0 && (
            <div className="card p-6">
              <h3 className="text-xl font-semibold mb-3">Potential Risks</h3>
              <ul className="space-y-2">
                {summary.potential_risks.map((risk, index) => (
                  <li key={index} className="flex items-start">
                    <FaExclamationTriangle className="text-amber-500 mt-1 mr-2 flex-shrink-0" />
                    <span>{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 
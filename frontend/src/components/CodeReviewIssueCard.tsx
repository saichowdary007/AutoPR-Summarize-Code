import React from 'react';
import { FaExclamationCircle, FaExclamationTriangle, FaInfoCircle, FaExternalLinkAlt } from 'react-icons/fa';
import { CodeReviewIssue } from '@/lib/api';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface CodeReviewIssueCardProps {
  issue: CodeReviewIssue;
  index: number;
}

export default function CodeReviewIssueCard({ issue, index }: CodeReviewIssueCardProps) {
  // Get appropriate severity icon and color
  const getSeverityDetails = (severity: string) => {
    switch (severity) {
      case 'critical':
        return {
          icon: <FaExclamationCircle className="w-5 h-5 text-critical" />,
          className: 'bg-red-50 border-critical',
          badge: 'bg-critical text-white'
        };
      case 'high':
        return {
          icon: <FaExclamationTriangle className="w-5 h-5 text-high" />,
          className: 'bg-orange-50 border-high',
          badge: 'bg-high text-white'
        };
      case 'medium':
        return {
          icon: <FaExclamationTriangle className="w-5 h-5 text-medium" />,
          className: 'bg-yellow-50 border-medium',
          badge: 'bg-medium text-white'
        };
      case 'low':
      default:
        return {
          icon: <FaInfoCircle className="w-5 h-5 text-low" />,
          className: 'bg-green-50 border-low',
          badge: 'bg-low text-white'
        };
    }
  };

  const severityDetails = getSeverityDetails(issue.severity);

  return (
    <div className={`border-l-4 rounded-md p-4 ${severityDetails.className}`}>
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center space-x-3">
          {severityDetails.icon}
          <div className="font-medium">{issue.issue}</div>
        </div>
        <span className={`text-xs px-2 py-1 rounded-full uppercase font-bold ${severityDetails.badge}`}>
          {issue.severity}
        </span>
      </div>

      <div className="mb-3 text-sm">
        <div className="text-gray-500 mb-1 font-mono">
          {issue.file}:{issue.line}
        </div>
        <div className="mt-2">{issue.recommendation}</div>
      </div>

      {issue.example && (
        <div className="mb-3">
          <div className="text-sm font-semibold mb-1">Example Fix:</div>
          <SyntaxHighlighter
            language="javascript"
            style={vscDarkPlus}
            customStyle={{ borderRadius: '0.375rem', fontSize: '0.8rem' }}
            wrapLines
            wrapLongLines
          >
            {issue.example}
          </SyntaxHighlighter>
        </div>
      )}

      {issue.reference && (
        <a
          href={issue.reference}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-sm text-primary-600 hover:text-primary-800"
        >
          Read more <FaExternalLinkAlt className="ml-1 w-3 h-3" />
        </a>
      )}
    </div>
  );
} 
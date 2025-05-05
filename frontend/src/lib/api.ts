import axios from 'axios';

// Types
export interface PRSummaryRequest {
  repo_owner: string;
  repo_name: string;
  pr_number: number;
  github_token: string;
  config?: Record<string, any>;
}

export interface CodeReviewRequest {
  repo_owner: string;
  repo_name: string;
  pr_number: number;
  github_token: string;
  config?: Record<string, any>;
  post_comments?: boolean;
}

export interface SummaryResponse {
  title: string;
  overview: string;
  changes_summary: string[];
  affected_components: string[];
  testing?: string;
  dependencies?: string[];
  migration_notes?: string;
  potential_risks?: string[];
}

export interface CodeReviewIssue {
  file: string;
  line: number;
  severity: 'critical' | 'high' | 'medium' | 'low';
  issue: string;
  recommendation: string;
  example?: string;
  reference?: string;
}

export interface CodeReviewResponse {
  security_issues: CodeReviewIssue[];
  performance_issues: CodeReviewIssue[];
  code_quality_issues: CodeReviewIssue[];
  test_coverage_issues: CodeReviewIssue[];
  statistics: {
    files_analyzed: number;
    lines_added: number;
    lines_removed: number;
    issue_counts: {
      security: number;
      performance: number;
      code_quality: number;
      test_coverage: number;
    };
    severity_counts: {
      critical: number;
      high: number;
      medium: number;
      low: number;
    };
  };
}

// API client setup
const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// API methods
export const getPRSummary = async (request: PRSummaryRequest): Promise<SummaryResponse> => {
  try {
    const response = await apiClient.post<SummaryResponse>('/api/pr-summary', request);
    return response.data;
  } catch (error) {
    console.error('Error fetching PR summary:', error);
    throw error;
  }
};

export const getCodeReview = async (request: CodeReviewRequest): Promise<CodeReviewResponse> => {
  try {
    const response = await apiClient.post<CodeReviewResponse>('/api/code-review', request);
    return response.data;
  } catch (error) {
    console.error('Error performing code review:', error);
    throw error;
  }
};

export default {
  getPRSummary,
  getCodeReview,
}; 
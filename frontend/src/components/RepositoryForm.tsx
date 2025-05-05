import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

// Form schema
const formSchema = z.object({
  repo_owner: z.string().min(1, 'Repository owner is required'),
  repo_name: z.string().min(1, 'Repository name is required'),
  pr_number: z.coerce.number().int().positive('PR number must be a positive integer'),
  github_token: z.string().min(1, 'GitHub token is required'),
  strictness_level: z.coerce.number().min(1).max(5).default(3),
  post_comments: z.boolean().default(false),
});

type FormValues = z.infer<typeof formSchema>;

interface RepositoryFormProps {
  onSubmit: (data: FormValues) => void;
  isLoading: boolean;
  includeCodeReviewOptions?: boolean;
}

export default function RepositoryForm({
  onSubmit,
  isLoading,
  includeCodeReviewOptions = false,
}: RepositoryFormProps) {
  const [showAdvanced, setShowAdvanced] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      strictness_level: 3,
      post_comments: false,
    },
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Repository Owner
            </label>
            <input
              {...register('repo_owner')}
              placeholder="e.g., facebook"
              className="input"
            />
            {errors.repo_owner && (
              <p className="mt-1 text-sm text-red-600">
                {errors.repo_owner.message}
              </p>
            )}
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Repository Name
            </label>
            <input
              {...register('repo_name')}
              placeholder="e.g., react"
              className="input"
            />
            {errors.repo_name && (
              <p className="mt-1 text-sm text-red-600">
                {errors.repo_name.message}
              </p>
            )}
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Pull Request Number
          </label>
          <input
            type="number"
            {...register('pr_number')}
            placeholder="e.g., 1234"
            className="input"
          />
          {errors.pr_number && (
            <p className="mt-1 text-sm text-red-600">
              {errors.pr_number.message}
            </p>
          )}
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            GitHub Token
          </label>
          <input
            type="password"
            {...register('github_token')}
            placeholder="GitHub personal access token"
            className="input"
          />
          <p className="mt-1 text-xs text-gray-500">
            Needs repo access. Will not be stored on our servers.
          </p>
          {errors.github_token && (
            <p className="mt-1 text-sm text-red-600">
              {errors.github_token.message}
            </p>
          )}
        </div>
        
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-sm text-primary-600 hover:text-primary-800 font-medium"
        >
          {showAdvanced ? 'Hide' : 'Show'} Advanced Options
        </button>
        
        {showAdvanced && (
          <div className="p-4 bg-gray-50 rounded-lg space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Strictness Level (1-5)
              </label>
              <input
                type="range"
                min="1"
                max="5"
                step="1"
                {...register('strictness_level')}
                className="w-full"
              />
              <div className="flex justify-between text-xs text-gray-500 mt-1">
                <span>Lenient</span>
                <span>Moderate</span>
                <span>Strict</span>
              </div>
            </div>
            
            {includeCodeReviewOptions && (
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="post_comments"
                  {...register('post_comments')}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label
                  htmlFor="post_comments"
                  className="ml-2 block text-sm text-gray-700"
                >
                  Post comments to GitHub PR
                </label>
              </div>
            )}
          </div>
        )}
      </div>
      
      <button
        type="submit"
        disabled={isLoading}
        className="w-full btn btn-primary py-2 px-4 rounded-md"
      >
        {isLoading ? 'Processing...' : 'Submit'}
      </button>
    </form>
  );
} 
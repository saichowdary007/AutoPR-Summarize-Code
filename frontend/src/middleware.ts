import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// This middleware ensures proper CSS caching and processing
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  
  // Add cache control header for CSS files
  if (request.nextUrl.pathname.endsWith('.css')) {
    response.headers.set('Cache-Control', 'public, max-age=0, must-revalidate');
  }
  
  return response;
}

// Only run middleware on specific paths
export const config = {
  matcher: [
    // Apply to all API routes
    '/api/:path*',
    // Apply to all CSS files
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}; 
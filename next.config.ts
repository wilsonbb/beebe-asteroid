import type { NextConfig } from 'next';
const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: false,
  basePath: process.env.BASE_PATH || '',
  images: { unoptimized: true },
};
export default nextConfig;

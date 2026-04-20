import withPWAInit from 'next-pwa';

const withPWA = withPWAInit({
  dest: 'public',
  disable: process.env.NODE_ENV === 'development', // Yeh local PC par PWA off rakhega, Vercel par automatically on kar dega
});

/** @type {import('next').NextConfig} */
const nextConfig = {};

export default withPWA(nextConfig);
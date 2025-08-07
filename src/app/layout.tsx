import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Toaster } from '@/components/ui/sonner';
import { QueryProvider } from '@/components/providers/query-provider';

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  colorScheme: 'dark',
  themeColor: '#0891b2',
};

export const metadata: Metadata = {
  title: "CuraGenie - AI-Powered Healthcare Platform",
  description: "Transform your healthcare experience with our intelligent medical platform featuring AI diagnostics, virtual consultations, and personalized health insights.",
  keywords: 'healthcare, AI, medical platform, health analytics, telemedicine, personalized medicine, genomics',
  authors: [{ name: 'Harsh Gupta', url: 'https://linkedin.com/in/harsh-gupta-kiet/' }],
  creator: 'Harsh Gupta',
  applicationName: 'CuraGenie',
  generator: 'Next.js',
  referrer: 'origin-when-cross-origin',
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    title: 'CuraGenie - AI-Powered Healthcare Platform',
    description: 'Revolutionary healthcare platform combining AI technology with personalized medicine',
    siteName: 'CuraGenie',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CuraGenie - AI-Powered Healthcare Platform',
    description: 'Transform your healthcare experience with AI-powered medical insights',
    creator: '@CuraGenie',
  },
  manifest: '/manifest.json',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <QueryProvider>
          {children}
          <Toaster />
        </QueryProvider>
      </body>
    </html>
  );
}

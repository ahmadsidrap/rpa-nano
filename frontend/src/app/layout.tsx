import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  metadataBase: new URL("https://introvesia.com"),
  keywords: [
    "RPA",
    "Nano services",
    "RPA Nano",
  ],
  title: {
    default: "RPA Nano - Nano services for your RPA needs",
    template: "%s — Introvesia",
  },
  description:
    "Nano services for your RPA needs",
  openGraph: {
    title: "RPA Nano - RPA",
    description:
      "Nano services for your RPA needs",
    images: ["/logo.jpg"],
  },
  twitter: {
    card: "summary_large_image",
  },
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
        {children}
      </body>
    </html>
  );
}

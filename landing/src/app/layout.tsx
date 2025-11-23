import type { Metadata } from "next";
import { IBM_Plex_Mono, Inter } from "next/font/google";
import { Providers } from "@/components/providers";
import { cn } from "@/lib/utils";
import "./globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });
const ibmPlexMono = IBM_Plex_Mono({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: "Metiseon Demo",
  description: "Deterministic, open-math robo-allocator landing experience.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={cn("min-h-screen bg-background font-sans antialiased", inter.variable, ibmPlexMono.variable)}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

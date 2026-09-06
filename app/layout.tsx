import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'Beebe — a small world in motion',
  description:
    'Meet asteroid (20220) Beebe. Explore real telescope images, its discovery and naming, and the science of a small world between Mars and Jupiter.',
};
export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="dark">
      <body>
        <a className="skip-link" href="#main">
          Skip to content
        </a>
        {children}
      </body>
    </html>
  );
}

import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'An asteroid named Beebe',
  description:
    'Telescope photos and a few facts about (20220) Beebe, the asteroid named after Wilson Beebe. A place for family, friends, and anyone curious.',
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

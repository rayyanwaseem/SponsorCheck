import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'SponsorCheck - UK Skilled Worker SOC Checker',
  description: 'Professional UK Skilled Worker SOC code and salary route checker.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-slate-50 flex flex-col">
        <header className="bg-white shadow-sm border-b border-slate-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-900 tracking-tight">SponsorCheck</h1>
            <nav className="hidden md:flex space-x-6 text-sm font-medium text-slate-600">
              <a href="#" className="hover:text-blue-600 transition-colors">Home</a>
              <a href="#" className="hover:text-blue-600 transition-colors">Data</a>
              <a href="#" className="hover:text-blue-600 transition-colors">About</a>
            </nav>
          </div>
        </header>

        <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>

        <footer className="bg-slate-900 text-slate-400 py-8 text-center text-sm mt-auto">
          <p>© {new Date().getFullYear()} SponsorCheck Contributors. Provided for guidance only.</p>
          <p className="mt-2 text-xs">Not affiliated with or endorsed by the UK Government.</p>
        </footer>
      </body>
    </html>
  );
}

export function Footer() {
  return (
    <footer className="bg-[var(--card)] border-t border-[var(--border)] py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-sm text-[var(--muted-foreground)]">
            © {new Date().getFullYear()} TodoPink. Simple. Productive. Secure.
          </p>
          <div className="flex gap-6 text-sm text-[var(--muted-foreground)]">
            <a href="#" className="hover:text-[var(--primary)] transition-colors">Privacy</a>
            <a href="#" className="hover:text-[var(--primary)] transition-colors">Terms</a>
            <a href="#" className="hover:text-[var(--primary)] transition-colors">Support</a>
          </div>
        </div>
      </div>
    </footer>
  );
}

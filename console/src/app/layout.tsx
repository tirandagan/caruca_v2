import type { Metadata } from "next";
import Link from "next/link";
import "./styles/console.css";

export const metadata: Metadata = {
  title: "Caruca v2 · execution console",
  description: "v1 and v2 side by side, inside and out. Local only.",
};

/**
 * The shell: masthead, navigation, page.
 *
 * The masthead states the scope in plain sight - this page is local and makes no outside
 * requests. That is a property worth showing rather than documenting, because it is the reason
 * the console may display v1's man pages and specifications at all.
 */
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <header className="masthead">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img className="masthead__logo" src="/logo.png" alt="Caruca" />
            <div className="masthead__titles">
              <div className="masthead__title">
                Caruca v2 <span>· execution console</span>
              </div>
              <div className="masthead__tagline">
                LLM-based specification mining for opaque shell commands.
              </div>
            </div>
            <div className="masthead__scope">127.0.0.1 · local only</div>
            <nav className="nav">
              <Link className="nav__item" href="/">
                Runs
              </Link>
              <Link className="nav__item" href="/pipeline">
                Pipeline
              </Link>
              <Link className="nav__item" href="/compare">
                Compare
              </Link>
              <Link className="nav__item" href="/findings">
                Findings
              </Link>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}

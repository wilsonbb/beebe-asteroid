import { href } from '@/lib/data';
export function Header() {
  return (
    <header className="site-header">
      <a className="wordmark" href={href('/')} aria-label="Beebe home">
        <span className="orbit-logo" aria-hidden="true">
          ◌
        </span>
        <span>
          (20220) <b>BEEBE</b>
        </span>
      </a>
      <nav aria-label="Main navigation">
        <a href={href('/#watch')}>Watch</a>
        <a href={href('/#story')}>Story</a>
        <a href={href('/#science')}>About</a>
        <a href={href('/archive/')}>Archive ↗</a>
      </nav>
    </header>
  );
}

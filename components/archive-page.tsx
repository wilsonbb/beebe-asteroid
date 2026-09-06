import { Header } from './site-header';
import { Footer } from './footer';
import { ArchiveBrowser } from './archive-browser';
import { nights } from '@/lib/nights';
import { sequences } from '@/lib/data';
export function ArchivePage({ page = 1 }: { page?: number }) {
  return (
    <div className="site-shell">
      <Header />
      <main id="main">
        <section className="archive-heading">
          <p className="eyebrow">THE OBSERVING JOURNAL</p>
          <h1>
            One world.
            <br />
            <em>Many nights.</em>
          </h1>
          <p>
            Real telescope images of Beebe’s predicted path. {sequences.length}{' '}
            nights have processed images; the rest remain in the work queue or
            await public pixels.
          </p>
          <p className="small-copy">
            An archive match means an exposure covers the predicted position. It
            does not, on its own, confirm a detection.
          </p>
        </section>
        <ArchiveBrowser nights={nights} initialPage={page} />
      </main>
      <Footer />
    </div>
  );
}

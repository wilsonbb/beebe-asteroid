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
          <p className="eyebrow">THE PHOTO COLLECTION</p>
          <h1>
            Browse the
            <br />
            <em>telescope photos.</em>
          </h1>
          <p>
            Telescope photos of the sky where Beebe was expected to be.{' '}
            {sequences.length} nights have photos ready to view. The other
            nights are waiting for processing or for the archive to make the
            images available.
          </p>
          <p className="small-copy">
            The circle marks the expected position. Beebe may be faint or hard
            to pick out in an individual photo.
          </p>
        </section>
        <ArchiveBrowser nights={nights} initialPage={page} />
      </main>
      <Footer />
    </div>
  );
}

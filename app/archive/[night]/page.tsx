import { Header } from '@/components/site-header';
import { Footer } from '@/components/footer';
import { Viewer } from '@/components/viewer';
import { sequences, href, dateLabel } from '@/lib/data';
import { notFound } from 'next/navigation';
export function generateStaticParams() {
  return sequences.map((s) => ({ night: s.night }));
}
export async function generateMetadata({
  params,
}: {
  params: Promise<{ night: string }>;
}) {
  const { night } = await params;
  return { title: `${night} — Beebe observing journal` };
}
export default async function Page({
  params,
}: {
  params: Promise<{ night: string }>;
}) {
  const { night } = await params;
  const s = sequences.find((s) => s.night === night);
  if (!s) notFound();
  return (
    <div className="site-shell">
      <Header />
      <main id="main" className="night-page">
        <a className="text-link" href={href('/archive/')}>
          ← All observing nights
        </a>
        <div className="night-layout">
          <div>
            <p className="eyebrow">ZTF / SAMUEL OSCHIN TELESCOPE</p>
            <h1>{dateLabel(s.night)}</h1>
            <p>
              {s.n_frames} exposures across {s.span_minutes} minutes. A small
              part of Beebe’s journey, recorded from Palomar Observatory.
            </p>
            <dl className="night-facts">
              <div>
                <dt>Filters</dt>
                <dd>{s.bands.join(', ')}</dd>
              </div>
              <div>
                <dt>Field width</dt>
                <dd>{s.field_arcsec} arcseconds</dd>
              </div>
              <div>
                <dt>Added to the journal</dt>
                <dd>{dateLabel(s.published_at)}</dd>
              </div>
              <div>
                <dt>Visibility review</dt>
                <dd>Unreviewed; marker is a prediction</dd>
              </div>
            </dl>
            {s.gif && (
              <a
                className="primary-link"
                href={href(s.gif.url)}
                download={`beebe-${s.night}.gif`}
              >
                Download GIF ↓
              </a>
            )}
            <p className="small-copy">
              The GIF contains telescope pixels without the position marker.
              Playback is accelerated, with equal time per exposure.
            </p>
            <details>
              <summary>Processing & provenance</summary>
              <p>{s.display_note}</p>
              <p className="mono">Render revision: {s.revision}</p>
              <a className="text-link" href={href('/sources/')}>
                Read the methods ↗
              </a>
            </details>
          </div>
          <Viewer sequence={s} />
        </div>
        <section className="exposure-list">
          <p className="eyebrow">THE INDIVIDUAL EXPOSURES</p>
          <h2>Take a closer look.</h2>
          <div className="journal-grid">
            {s.frames.map((f, i) => (
              <article key={f.id}>
                <a href={href(f.asset.url)}>
                  <img
                    src={href(f.asset.url)}
                    width={360}
                    height={360}
                    loading="lazy"
                    alt={`Exposure ${i + 1}, ${f.band} filter, ${f.at.slice(11, 19)} UTC; marker-free star field`}
                  />
                </a>
                <p>
                  {f.at.slice(11, 19)} UTC · {f.band} band
                </p>
                <a href={f.source_url} className="text-link">
                  Source FITS ↗
                </a>
              </article>
            ))}
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}

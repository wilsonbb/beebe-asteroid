import { ArrowUpRight } from 'lucide-react';
import { Header } from '@/components/site-header';
import { Footer } from '@/components/footer';
import { Viewer } from '@/components/viewer';
import { SizeExplorer, Prediction } from '@/components/science';
import { Orbit } from '@/components/orbit';
import {
  object,
  observations,
  ephemeris,
  sequences,
  featured,
  href,
  dateLabel,
} from '@/lib/data';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
export default function Home() {
  const orbit = object.orbit;
  const H = Number(object.physical.find((p) => p.name === 'H')?.value || 13.87);
  const recent = [...sequences]
    .sort((a, b) => b.published_at.localeCompare(a.published_at))
    .slice(0, 3);
  return (
    <div className="site-shell">
      <Header />
      <main id="main">
        <section className="hero" id="watch">
          <div className="hero-copy">
            <p className="eyebrow">FOR FAMILY, FRIENDS & THE CURIOUS</p>
            <h1>
              An asteroid
              <br />
              <em>named Beebe.</em>
            </h1>
            <p>
              In 2026, an asteroid was named after Wilson Beebe. This is a place
              for family and friends to see it in telescope photos and learn a
              little about it.
            </p>
            <p className="hero-help">
              Press play to compare the photos. The circle shows where Beebe is
              expected to be.
            </p>
            <a className="text-link" href="#story">
              How it got the name <ArrowUpRight size={16} />
            </a>
          </div>
          <div>
            <Viewer sequence={featured} />
            <a
              className="image-detail-link"
              href={href(`/archive/${featured.night}/`)}
            >
              Featured sequence · {dateLabel(featured.night)}{' '}
              <ArrowUpRight size={13} />
            </a>
          </div>
        </section>
        <div className="fact-strip">
          <div>
            <span>WHERE IT ORBITS</span>
            <strong>The main asteroid belt</strong>
          </div>
          <div>
            <span>ONE TRIP AROUND THE SUN</span>
            <strong>
              {(orbit.elements.per.value / 365.25).toFixed(2)} Earth years
            </strong>
          </div>
          <div>
            <span>NAMED ON</span>
            <strong>9 July 2026</strong>
          </div>
        </div>
        <section
          className="section additions"
          aria-labelledby="additions-title"
        >
          <div className="section-heading">
            <div>
              <p className="eyebrow">RECENTLY ADDED</p>
              <h2 id="additions-title">More telescope photos</h2>
            </div>
            <a className="text-link" href={href('/archive/')}>
              Explore the archive <ArrowUpRight size={16} />
            </a>
          </div>
          <p className="section-intro">
            New photos are added as they become available. The observing date is
            when the telescope took the photo; the added date is when it
            appeared on this site.
          </p>
          <div className="journal-grid">
            {recent.map((s) => (
              <a
                className="journal-card"
                key={s.id}
                href={href(`/archive/${s.night}/`)}
              >
                <div className="journal-image">
                  <img
                    src={href(s.poster.url)}
                    width={360}
                    height={360}
                    loading="lazy"
                    alt={`Star field around Beebe on ${dateLabel(s.night)}`}
                  />
                  <span>{s.n_frames >= 3 ? '▶ SEQUENCE' : 'STILL FRAMES'}</span>
                </div>
                <div className="journal-caption">
                  <h3>{dateLabel(s.night, true)}</h3>
                  <ArrowUpRight size={20} />
                  <p>
                    {s.n_frames} {s.n_frames === 1 ? 'exposure' : 'exposures'} ·{' '}
                    {s.bands.join(' / ')}{' '}
                    {s.bands.length === 1 ? 'band' : 'bands'}
                  </p>
                  <small>Added {dateLabel(s.published_at, true)}</small>
                </div>
              </a>
            ))}
          </div>
        </section>
        <section className="section story-section" id="story">
          <div className="story-heading">
            <p className="eyebrow">WHY BEEBE?</p>
            <h2>
              How it got
              <br />
              <em>the name.</em>
            </h2>
            <p>
              The asteroid was discovered in 1997 and received its name in 2026.
              The name recognizes Wilson’s work on software for astronomy.
            </p>
            <a
              className="text-link"
              href="https://www.wgsbn-iau.org/files/Bulletins/V006/WGSBNBull_V006_011.pdf#page=10"
            >
              Read the official naming record <ArrowUpRight size={16} />
            </a>
          </div>
          <div className="timeline">
            <article>
              <time>07 APR 1992</time>
              <h3>An earlier photo</h3>
              <p>
                The earliest observation now associated with Beebe predates its
                discovery by five years. An earlier observation linked to an
                object later is called a <em>precovery</em>.
              </p>
            </article>
            <article>
              <time>07 APR 1997</time>
              <h3>Discovery</h3>
              <p>
                Eric W. Elst discovered the asteroid at La Silla Observatory in
                Chile. Its first designation was{' '}
                <span className="mono">1997 GA40</span>.
              </p>
            </article>
            <article>
              <time>09 JUL 2026</time>
              <h3>Named Beebe</h3>
              <p>
                The name honors Wilson Beebe, whose software helps find faint
                objects beyond Neptune by aligning and adding survey images—a
                technique called <em>shift-and-stack</em>.
              </p>
              <details>
                <summary>The official citation</summary>
                <blockquote>{object.discovery.citation}</blockquote>
                <p className="citation">
                  WGSBN Bulletin 6, no. 11, p. 10 · 9 July 2026
                </p>
              </details>
            </article>
          </div>
        </section>
        <section className="section" id="science">
          <div className="section-heading">
            <div>
              <p className="eyebrow">ABOUT THE ASTEROID</p>
              <h2>
                What kind of
                <br />
                <em>asteroid is it?</em>
              </h2>
            </div>
            <p className="heading-aside">
              Beebe is one of many asteroids between Mars and Jupiter. Its name
              gives us a good reason to learn about one of them.
            </p>
          </div>
          <div className="orbit-layout">
            <Orbit />
            <div className="orbit-copy">
              <h3>
                Between Mars
                <br />
                and Jupiter.
              </h3>
              <p>
                Beebe travels around the Sun in a gently oval orbit, tilted
                about 13.5° from Earth’s orbital plane. JPL classifies it as a
                main-belt asteroid, not a near-Earth asteroid.
              </p>
              <div className="orbit-numbers">
                <div>
                  <strong>{orbit.elements.q.value.toFixed(2)}</strong>
                  <span>au, closest to the Sun</span>
                </div>
                <div>
                  <strong>{orbit.elements.ad.value.toFixed(2)}</strong>
                  <span>au, farthest from the Sun</span>
                </div>
              </div>
              <p className="small-copy">
                One astronomical unit (au) is about the distance from Earth to
                the Sun. It is a handy unit for these very large distances.
              </p>
            </div>
          </div>
          <SizeExplorer h={H} />
          <div className="science-pair">
            <div className="spin-note">
              <p className="eyebrow">ITS SPIN</p>
              <h3>
                How quickly
                <br />
                does it spin?
              </h3>
              <p>
                A published lightcurve suggests Beebe rotates once in about 3
                hours. But the coverage was incomplete: the period may be wrong
                by roughly 30%.
              </p>
              <p className="small-copy">
                A lightcurve records changing brightness as an object turns. The
                current JPL entry reports 2.99603 hours, from TESS photometry
                via the Lightcurve Database.
              </p>
            </div>
            <Prediction
              samples={ephemeris.samples}
              retrieved={ephemeris.retrieved_at}
            />
          </div>
          <details className="technical">
            <summary>
              Want the numbers? <span>Orbit details & observation records</span>
            </summary>
            <div className="technical-inner">
              <h3>The orbit, with its context</h3>
              <p>
                JPL solution {orbit.orbit_id} · computed {orbit.soln_date} ·
                epoch JD {orbit.epoch} · equinox {orbit.equinox}. Sigmas are the
                values returned by JPL; see its documentation for
                interpretation.
              </p>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Element</TableHead>
                    <TableHead>Value</TableHead>
                    <TableHead>Reported σ</TableHead>
                    <TableHead>Unit</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {Object.values(orbit.elements).map((e) => (
                    <TableRow key={e.name}>
                      <TableCell>{e.title}</TableCell>
                      <TableCell className="mono">
                        {e.value.toPrecision(9)}
                      </TableCell>
                      <TableCell className="mono">
                        {e.sigma?.toExponential(3) ?? '—'}
                      </TableCell>
                      <TableCell>{e.units || '—'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
              <p>
                {orbit.n_obs_used.toLocaleString()} observations used by JPL;
                fit arc {orbit.first_obs} to {orbit.last_obs}; RMS residual{' '}
                {orbit.rms} arcseconds; condition code {orbit.condition_code}.
                Fit residuals are not a guarantee of future prediction accuracy.
                Earth MOID: {orbit.moid} au, a distance between orbital paths,
                not today’s distance.
              </p>
              <h3>
                {observations.count.toLocaleString()} primary records in this
                MPC snapshot
              </h3>
              <p>
                The downloaded file contains{' '}
                {observations.record_count.toLocaleString()} text records,
                including {observations.continuation_count} satellite-position
                continuation records. These are counted separately. JPL’s
                orbit-fit count uses a different record selection/counting
                context.
              </p>
              <div className="station-list">
                {observations.stations.slice(0, 8).map((s) => (
                  <div key={s.code}>
                    <span>
                      {s.name} <small>({s.code})</small>
                    </span>
                    <strong>{s.count}</strong>
                  </div>
                ))}
              </div>
              <a className="text-link" href={href('/sources/')}>
                Sources, downloads & processing notes <ArrowUpRight size={16} />
              </a>
            </div>
          </details>
        </section>
        <section className="closing">
          <span className="eyebrow">THE PHOTO COLLECTION</span>
          <h2>Have a look through the photos.</h2>
          <p>
            Choose a date to view the photos, play a sequence, or download a
            copy.
          </p>
          <a className="primary-link" href={href('/archive/')}>
            Browse telescope photos <ArrowUpRight size={16} />
          </a>
        </section>
      </main>
      <Footer />
    </div>
  );
}

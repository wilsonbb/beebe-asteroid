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
            <p className="eyebrow">A FIELD JOURNAL FROM THE ASTEROID BELT</p>
            <h1>
              A small world.
              <br />
              <em>Still in motion.</em>
            </h1>
            <p>
              Discovered in 1997. Named Beebe in 2026. Follow a small world
              between Mars and Jupiter through real telescope images.
            </p>
            <div className="hero-annotation">
              <span className="annotation-line" />
              <p>
                That little point of light
                <br />
                has a story to tell.
              </p>
            </div>
            <a className="text-link" href="#story">
              Meet (20220) Beebe <ArrowUpRight size={16} />
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
            <span>AT HOME IN</span>
            <strong>The main asteroid belt</strong>
          </div>
          <div>
            <span>ONE TRIP AROUND THE SUN</span>
            <strong>
              {(orbit.elements.per.value / 365.25).toFixed(2)} Earth years
            </strong>
          </div>
          <div>
            <span>A NEW NAME SINCE</span>
            <strong>9 July 2026</strong>
          </div>
        </div>
        <section
          className="section additions"
          aria-labelledby="additions-title"
        >
          <div className="section-heading">
            <div>
              <p className="eyebrow">THE OBSERVING JOURNAL</p>
              <h2 id="additions-title">Small moments. Real motion.</h2>
            </div>
            <a className="text-link" href={href('/archive/')}>
              Explore the archive <ArrowUpRight size={16} />
            </a>
          </div>
          <p className="section-intro">
            Newly available images join the journal as public archives release
            them. The observing date tells you when the light was captured; the
            added date tells you when it arrived here.
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
            <p className="eyebrow">01 / A NAME IN THE SKY</p>
            <h2>
              Known for decades.
              <br />
              <em>Named for discovery.</em>
            </h2>
            <p>
              Beebe’s name connects a small asteroid to the search for much more
              distant worlds.
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
              <h3>Already in the picture</h3>
              <p>
                The earliest observation now associated with Beebe predates its
                discovery by five years. An earlier observation linked to an
                object later is called a <em>precovery</em>.
              </p>
            </article>
            <article>
              <time>07 APR 1997</time>
              <h3>A world is discovered</h3>
              <p>
                Eric W. Elst discovered the asteroid at La Silla Observatory in
                Chile. Its first designation was{' '}
                <span className="mono">1997 GA40</span>.
              </p>
            </article>
            <article>
              <time>09 JUL 2026</time>
              <h3>And a name finds it</h3>
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
              <p className="eyebrow">02 / GETTING TO KNOW A SMALL WORLD</p>
              <h2>
                Far away.
                <br />
                <em>Remarkably knowable.</em>
              </h2>
            </div>
            <p className="heading-aside">
              We know much more about Beebe’s orbit than its surface. Both the
              answers and the open questions are part of the science.
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
                Despite its name’s connection to research beyond Neptune, Beebe
                itself lives in the main asteroid belt.
              </p>
            </div>
          </div>
          <SizeExplorer h={H} />
          <div className="science-pair">
            <div className="spin-note">
              <p className="eyebrow">AN OPEN QUESTION</p>
              <h3>
                A day in
                <br />
                about three hours?
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
              For the scientifically curious{' '}
              <span>Elements, uncertainties & the observation record</span>
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
          <span className="eyebrow">THE STORY KEEPS MOVING</span>
          <h2>
            Another night.
            <br />
            Another point of light.
          </h2>
          <p>Explore the images that bring Beebe’s journey into view.</p>
          <a className="primary-link" href={href('/archive/')}>
            Open the observing journal <ArrowUpRight size={16} />
          </a>
        </section>
      </main>
      <Footer />
    </div>
  );
}

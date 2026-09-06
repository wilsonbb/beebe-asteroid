import { href, status } from '@/lib/data';
export function Footer() {
  return (
    <footer className="site-footer">
      <div>
        <a className="wordmark" href={href('/')}>
          (20220) <b>BEEBE</b>
        </a>
        <p>
          An asteroid with a familiar name.
          <br />
          A few photos and things to learn.
        </p>
      </div>
      <div>
        <p className="eyebrow">SOURCES & DETAILS</p>
        <div className="source-links">
          <a href="https://ssd.jpl.nasa.gov/tools/sbdb_lookup.html#/?sstr=20220">
            JPL ↗
          </a>
          <a href="https://data.minorplanetcenter.net/">
            Minor Planet Center ↗
          </a>
          <a href="https://irsa.ipac.caltech.edu/">IRSA / ZTF ↗</a>
          <a href="https://www.wgsbn-iau.org/files/Bulletins/V006/WGSBNBull_V006_011.pdf#page=10">
            Naming bulletin ↗
          </a>
          <a href={href('/sources/')}>Methods & data status ↗</a>
        </div>
        <p className="footer-meta">
          Latest successful archive search:{' '}
          {status.sources.most.last_success.slice(0, 10)}
          <br />
          Images may arrive later than observations.
        </p>
      </div>
    </footer>
  );
}

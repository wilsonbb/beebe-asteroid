/* oxlint-disable jsx-a11y/prefer-tag-over-role -- SVG diagrams need an explicit image role. */
export function Orbit() {
  return (
    <figure className="orbit-figure">
      <svg
        viewBox="0 0 580 390"
        role="img"
        aria-labelledby="orbit-title orbit-desc"
      >
        <title id="orbit-title">Beebe’s place between Mars and Jupiter</title>
        <desc id="orbit-desc">
          An orbital-distance schematic with Beebe highlighted at about 2.74
          astronomical units. Orbital tilt and eccentricity are omitted; body
          sizes are exaggerated. It does not show current positions.
        </desc>
        <g transform="translate(285 205)">
          <circle r="175" fill="none" stroke="#30404b" strokeDasharray="3 6" />
          <circle r="92" fill="none" stroke="#00e5a0" strokeWidth="1.5" />
          <circle r="51" fill="none" stroke="#30404b" />
          <circle r="34" fill="none" stroke="#30404b" />
          <circle r="7" fill="#e9bb6a" />
          <circle cx="34" cy="0" r="3" fill="#aab9c4" />
          <circle cx="0" cy="-51" r="3" fill="#b39379" />
          <circle cx="-92" cy="0" r="4" fill="#00e5a0" />
          <circle cx="175" cy="0" r="6" fill="#bda890" />
        </g>
        <g fill="#aab9c4" fontFamily="monospace" fontSize="12">
          <text x="265" y="235">
            SUN
          </text>
          <text x="329" y="223">
            EARTH
          </text>
          <text x="296" y="151">
            MARS
          </text>
          <text x="475" y="210">
            JUPITER
          </text>
          <text x="103" y="192" fill="#00e5a0">
            BEEBE
          </text>
          <text x="103" y="211" fill="#00e5a0">
            2.74 au
          </text>
        </g>
      </svg>
      <figcaption>
        Orbital-distance schematic · 1 au is Earth’s distance scale from the
        Sun.
        <br />
        Tilt and eccentricity omitted; dots are not current positions.
      </figcaption>
    </figure>
  );
}

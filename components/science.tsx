/* oxlint-disable jsx-a11y/prefer-tag-over-role -- SVG diagrams need an explicit image role. */
'use client';
import { useState, useSyncExternalStore } from 'react';
import { Slider } from '@/components/ui/slider';
export function SizeExplorer({ h }: { h: number }) {
  const [p, setP] = useState(0.1);
  const size = (1329 * Math.pow(10, -h / 5)) / Math.sqrt(p);
  return (
    <div className="size-explorer">
      <div>
        <p className="eyebrow">A QUESTION OF REFLECTIVITY</p>
        <h3>
          How big is a<br />
          point of light?
        </h3>
        <p>
          The same light could come from a small bright surface or a larger dark
          one. Change the assumed reflectivity to see why size is still a
          question.
        </p>
        <label id="reflectivity-label">
          Assumed reflectivity <strong>{Math.round(p * 100)}%</strong>
        </label>
        <Slider
          aria-labelledby="reflectivity-label"
          min={0.057}
          max={0.25}
          step={0.001}
          value={[p]}
          onValueChange={(v) => setP(Array.isArray(v) ? v[0] : v)}
        />
        <div className="slider-endpoints">
          <span>Darker surface</span>
          <span>Brighter surface</span>
        </div>
      </div>
      <div className="size-result">
        <svg
          viewBox="0 0 250 250"
          role="img"
          aria-label={`Illustrative diameter ${size.toFixed(1)} kilometers`}
        >
          <circle
            cx="125"
            cy="125"
            r={size * 10}
            fill="none"
            stroke="#00e5a0"
            strokeWidth="1"
          />
          <line
            x1={125 - size * 10}
            y1="125"
            x2={125 + size * 10}
            y2="125"
            stroke="#4b6466"
            strokeDasharray="3 5"
          />
          <circle cx="125" cy="125" r="2" fill="#00e5a0" />
        </svg>
        <output aria-live="polite">
          <strong>{size.toFixed(1)}</strong> km
        </output>
        <span>Inferred diameter, not a measurement</span>
      </div>
      <details className="size-math">
        <summary>Show the assumptions</summary>
        <p>
          For absolute magnitude H = {h}, diameter D = 1329 × 10<sup>−H/5</sup>{' '}
          / √p, in kilometers. The illustrative reflectivity range of 5.7–25%
          implies about 4.5–9.4 km. It is not a confidence interval. No diameter
          or reflectivity is listed in the current JPL record.
        </p>
      </details>
    </div>
  );
}
export function Prediction({
  samples,
  retrieved,
}: {
  samples: {
    at: string;
    ra: string;
    dec: string;
    v_mag: number;
    earth_distance_au: number;
    light_minutes: number;
  }[];
  retrieved: string;
}) {
  const day = useSyncExternalStore(
    subscribeClock,
    () => new Date().toISOString().slice(0, 10),
    () => samples[0].at.slice(0, 10),
  ); // Avoid presenting server time as the visitor's day.
  // A date chosen by the build is the SSR fallback; client selects a matching UTC sample.
  const sample = samples.find((s) => s.at.startsWith(day)) || samples.at(-1)!;
  return (
    <div className="prediction">
      <p className="eyebrow">A POSITION, NOT A LIVE PICTURE</p>
      <h3>Where is Beebe?</h3>
      <p>
        Prediction for{' '}
        <time dateTime={sample.at}>{sample.at.slice(0, 10)} at 00:00 UTC</time>
      </p>
      {!samples.some((s) => s.at.startsWith(day)) && (
        <p className="pending-copy">
          The prediction needs an update. Last available sample shown.
        </p>
      )}
      <dl>
        <div>
          <dt>Distance from Earth</dt>
          <dd>
            {sample.earth_distance_au.toFixed(2)} <small>au</small>
          </dd>
        </div>
        <div>
          <dt>Light travel time</dt>
          <dd>
            {sample.light_minutes.toFixed(1)} <small>minutes</small>
          </dd>
        </div>
      </dl>
      <details>
        <summary>Coordinates & brightness</summary>
        <p className="mono">
          RA {sample.ra}
          <br />
          Dec {sample.dec}
          <br />
          Predicted V magnitude {sample.v_mag.toFixed(2)}
        </p>
        <p>
          As seen from Earth’s center. Far too faint for unaided eyes. Retrieved{' '}
          {retrieved.slice(0, 10)}.
        </p>
      </details>
    </div>
  );
}

function subscribeClock(callback: () => void) {
  const timer = setInterval(callback, 60000);
  document.addEventListener('visibilitychange', callback);
  return () => {
    clearInterval(timer);
    document.removeEventListener('visibilitychange', callback);
  };
}

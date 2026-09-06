'use client';
import { useEffect, useRef, useState } from 'react';
import {
  Play,
  Pause,
  ChevronLeft,
  ChevronRight,
  ArrowUpRight,
} from 'lucide-react';
import { Slider } from '@/components/ui/slider';
import { Switch } from '@/components/ui/switch';
import { Button } from '@/components/ui/button';
import {
  NativeSelect,
  NativeSelectOption,
} from '@/components/ui/native-select';
import type { Sequence } from '@/lib/data';
const base = process.env.NEXT_PUBLIC_BASE_PATH || '';
export function Viewer({
  sequence,
  compact = false,
}: {
  sequence: Sequence;
  compact?: boolean;
}) {
  const [index, setIndex] = useState(0),
    [playing, setPlaying] = useState(false),
    [mark, setMark] = useState(true),
    [speed, setSpeed] = useState(1),
    [error, setError] = useState(false),
    [preparing, setPreparing] = useState(false),
    [loadedSrc, setLoadedSrc] = useState(sequence.frames[0].asset.url);
  const root = useRef<HTMLElement>(null);
  const frames = sequence.frames;
  const f = frames[index];

  useEffect(() => {
    if (!playing) return;
    const timer = setInterval(
      () => setIndex((i) => (i + 1) % frames.length),
      700 / speed,
    );
    return () => clearInterval(timer);
  }, [playing, speed, frames.length]);
  useEffect(() => {
    const stop = () => {
      if (document.hidden) setPlaying(false);
    };
    document.addEventListener('visibilitychange', stop);
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) setPlaying(false);
      },
      { threshold: 0.1 },
    );
    if (root.current) observer.observe(root.current);
    return () => {
      observer.disconnect();
      document.removeEventListener('visibilitychange', stop);
    };
  }, []);
  const togglePlayback = async () => {
    if (playing) {
      setPlaying(false);
      return;
    }
    setPreparing(true);
    try {
      await Promise.all(
        frames.map(
          (frame) =>
            new Promise<void>((resolve, reject) => {
              const image = new Image();
              image.onload = () => resolve();
              image.onerror = () => reject(new Error('Frame unavailable'));
              image.src = base + frame.asset.url;
            }),
        ),
      );
      setError(false);
      setPlaying(true);
    } catch {
      setError(true);
    } finally {
      setPreparing(false);
    }
  };
  const step = (delta: number) => {
    setPlaying(false);
    setIndex((i) => (i + delta + frames.length) % frames.length);
  };
  return (
    <figure
      ref={root}
      className={`viewer ${compact ? 'viewer-compact' : ''}`}
      aria-label={`Telescope sequence from ${sequence.night}`}
    >
      <div className="viewer-top">
        <span>
          <i className="status-dot" /> ZTF / PALOMAR OBSERVATORY
        </span>
        <span>{sequence.night}</span>
      </div>
      <div className="sky-image">
        <img
          src={base + f.asset.url}
          width={f.asset.width}
          height={f.asset.height}
          alt={`ZTF ${f.band}-band exposure at ${f.at.slice(11, 19)} UTC on ${sequence.night}; a field of stars around Beebe's predicted position.`}
          onLoad={() => {
            setLoadedSrc(f.asset.url);
            setError(false);
          }}
          onError={() => {
            setError(true);
            setPlaying(false);
          }}
          loading={compact ? 'lazy' : 'eager'}
        />
        {mark && !error && loadedSrc === f.asset.url && (
          <span
            className="target-marker"
            style={{
              left: `${f.marker.x * 100}%`,
              top: `${f.marker.y * 100}%`,
            }}
            aria-hidden="true"
          >
            <span>BEEBE</span>
          </span>
        )}
        <span className="orientation" aria-label="North up, east left">
          N ↑<br />E ←
        </span>
        <span className="image-scale">
          <i style={{ width: `${(60 / sequence.field_arcsec) * 100}%` }} />
          60″
        </span>
        {error && (
          <p className="image-error" role="alert">
            This frame could not load. Try another frame or open the source
            image.
          </p>
        )}
      </div>
      <div className="viewer-controls">
        <div className="transport">
          <Button
            className="play-button"
            aria-label={playing ? 'Pause animation' : 'Play animation'}
            onClick={togglePlayback}
            disabled={frames.length < 2 || preparing}
          >
            {playing ? <Pause size={16} /> : <Play size={16} />}
            <span>{preparing ? 'Loading…' : playing ? 'Pause' : 'Play'}</span>
          </Button>
          <Button
            variant="ghost"
            className="icon-button"
            aria-label="Previous frame"
            onClick={() => step(-1)}
          >
            <ChevronLeft />
          </Button>
          <Button
            variant="ghost"
            className="icon-button"
            aria-label="Next frame"
            onClick={() => step(1)}
          >
            <ChevronRight />
          </Button>
          <span className="frame-counter">
            {index + 1} <span>/ {frames.length}</span>
          </span>
          <NativeSelect
            aria-label="Playback speed"
            value={speed}
            onChange={(e) => setSpeed(Number(e.target.value))}
          >
            <NativeSelectOption value="0.5">0.5×</NativeSelectOption>
            <NativeSelectOption value="1">1×</NativeSelectOption>
            <NativeSelectOption value="2">2×</NativeSelectOption>
          </NativeSelect>
        </div>
        {frames.length > 1 && (
          <>
            <span id={`frame-label-${sequence.id}`} className="sr-only">
              Exposure frame
            </span>
            <Slider
              className="frame-slider"
              min={0}
              max={frames.length - 1}
              step={1}
              value={[index]}
              aria-labelledby={`frame-label-${sequence.id}`}
              onValueChange={(v) => {
                setPlaying(false);
                setIndex(Array.isArray(v) ? v[0] : v);
              }}
            />
          </>
        )}
        <div className="viewer-bottom">
          <span className="exposure">
            {f.at.slice(11, 19)} UTC <span>· {f.band} band</span>
          </span>
          <label className="marker-switch" htmlFor={`marker-${sequence.id}`}>
            <Switch
              id={`marker-${sequence.id}`}
              checked={mark}
              onCheckedChange={setMark}
              aria-label="Show predicted position"
            />
            <span>Show position</span>
          </label>
        </div>
      </div>
      <figcaption>
        <span>
          {sequence.span_minutes} minutes of observations. Playback speeds up
          time.
        </span>
        <span className="visibility-note">
          Circle = predicted position · visibility unreviewed
        </span>
      </figcaption>
      {!compact && (
        <details className="viewer-explainer">
          <summary>What am I looking at?</summary>
          <p>
            Each frame is a real telescope exposure of the same patch of sky.
            Stars stay approximately in place; an asteroid moves. The circle
            follows Beebe’s predicted location, not a measured detection. Images
            use {sequence.bands.join(', ')} filters, so stars may change
            brightness between frames. These images do not show Beebe’s surface.
          </p>
          <a className="text-link" href={f.source_url}>
            Open this source FITS image <ArrowUpRight size={14} />
          </a>
        </details>
      )}
    </figure>
  );
}

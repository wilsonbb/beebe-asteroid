export type Night = {
  night: string;
  count: number;
  bands: string[];
  availability: string;
  poster: string | null;
  n_frames: number;
  published_at: string | null;
};
export function filterNights(
  nights: Night[],
  year = 'all',
  band = 'all',
  availability = 'all',
  sort = 'added',
) {
  return nights
    .filter(
      (n) =>
        (year === 'all' || n.night.startsWith(year)) &&
        (band === 'all' || n.bands.includes(band)) &&
        (availability === 'all' ||
          (availability === 'available'
            ? n.poster !== null
            : n.poster === null)),
    )
    .sort((a, b) =>
      sort === 'observed'
        ? b.night.localeCompare(a.night)
        : (b.published_at || '').localeCompare(a.published_at || '') ||
          b.night.localeCompare(a.night),
    );
}
export const PAGE_SIZE = 24;

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { filterNights, type Night } from '../lib/archive.ts';
const nights: Night[] = [
  {
    night: '2022-01-01',
    count: 3,
    bands: ['g', 'r'],
    availability: 'available',
    poster: '/a.webp',
    n_frames: 3,
    published_at: '2026-09-05',
  },
  {
    night: '2026-09-01',
    count: 1,
    bands: ['r'],
    availability: 'pending',
    poster: null,
    n_frames: 0,
    published_at: null,
  },
  {
    night: '2025-01-01',
    count: 3,
    bands: ['i'],
    availability: 'available',
    poster: '/b.webp',
    n_frames: 3,
    published_at: '2026-08-01',
  },
];
void test('backfilled older observation leads recently added order', () =>
  assert.equal(filterNights(nights)[0].night, '2022-01-01'));
void test('observing date sort remains independent', () =>
  assert.equal(
    filterNights(nights, 'all', 'all', 'all', 'observed')[0].night,
    '2026-09-01',
  ));
void test('combined year band and availability filters', () =>
  assert.equal(filterNights(nights, '2022', 'g', 'available').length, 1));
void test('missing public pixels are filterable', () =>
  assert.equal(
    filterNights(nights, 'all', 'r', 'awaiting')[0].night,
    '2026-09-01',
  ));
void test('no matches has a stable empty result', () =>
  assert.deepEqual(filterNights(nights, '2021'), []));

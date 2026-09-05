"""Download ZTF cutouts of (20220) Beebe found via IRSA MOST and build
static PNGs plus per-night animated GIFs showing the asteroid's motion.

Frames within a night share one fixed sky center, so background stars stay
fixed and the asteroid moves between frames. Run inside the `beebe` conda env.
"""
import os
import re
import numpy as np
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
from astropy.visualization import ZScaleInterval
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
FITS_DIR = os.path.join(BASE, "cutouts", "fits")
PNG_DIR = os.path.join(BASE, "cutouts", "png")
ANIM_DIR = os.path.join(BASE, "animations")
for d in (FITS_DIR, PNG_DIR, ANIM_DIR):
    os.makedirs(d, exist_ok=True)

# Nights chosen from the MOST match table: (label, night_mjd, cutout arcsec)
ANIM_NIGHTS = [
    ("2022-11-16", 59899, 360),
    ("2025-07-20", 60876, 480),
    ("2022-10-30", 59882, 300),
]
STATIC_NIGHTS = {60392, 60393}  # 2024-03-22/23, V=16.9 opposition frames


def fetch_cutout(image_url, ra, dec, size_arcsec, out_path):
    if os.path.exists(out_path):
        return True
    url = f"{image_url}?center={ra:.6f},{dec:.6f}&size={size_arcsec}arcsec&gzip=false"
    r = requests.get(url, timeout=120)
    if r.status_code != 200:
        print(f"  ! HTTP {r.status_code} for {os.path.basename(out_path)}")
        return False
    with open(out_path, "wb") as f:
        f.write(r.content)
    return True


def filter_from_url(url):
    m = re.search(r"_(zg|zr|zi)_", url)
    return {"zg": "g", "zr": "r", "zi": "i"}.get(m.group(1) if m else "", "?")


def render_frame(fits_path, ra_obj, dec_obj, title, out_png, mark=True):
    with fits.open(fits_path) as hdul:
        data = hdul[0].data.astype(float)
        wcs = WCS(hdul[0].header)
    lo, hi = ZScaleInterval().get_limits(data)
    fig = plt.figure(figsize=(5, 5), dpi=120)
    ax = fig.add_subplot(111, projection=wcs)
    ax.imshow(data, cmap="gray", vmin=lo, vmax=hi, origin="lower")
    if mark:
        x, y = wcs.world_to_pixel_values(ra_obj, dec_obj)
        ax.scatter(x, y, s=550, facecolor="none", edgecolor="#00e5a0", lw=1.6)
    ax.set_title(title, fontsize=9)
    ax.coords[0].set_axislabel("RA")
    ax.coords[1].set_axislabel("Dec")
    fig.tight_layout()
    fig.savefig(out_png)
    plt.close(fig)


def main():
    t = Table.read(os.path.join(BASE, "ztf_matches.ecsv"))
    t["night"] = np.floor(t["mjd_obs"] + 0.5).astype(int)

    # --- per-night animations, fixed sky center ---
    for label, night, size in ANIM_NIGHTS:
        m = t[t["night"] == night]
        m.sort("mjd_obs")
        ra0 = float(np.mean(m["ra_obj"]))
        dec0 = float(np.mean(m["dec_obj"]))
        print(f"Night {label}: {len(m)} frames, center {ra0:.4f} {dec0:.4f}")
        frames = []
        for i, row in enumerate(m):
            fp = os.path.join(FITS_DIR, f"anim_{label}_{i:02d}.fits")
            if not fetch_cutout(row["image_url"], ra0, dec0, size, fp):
                continue
            band = filter_from_url(row["image_url"])
            title = f"(20220) Beebe  ZTF-{band}  {row['date_obs']} {str(row['time_obs'])[:8]} UT"
            pp = os.path.join(PNG_DIR, f"anim_{label}_{i:02d}.png")
            render_frame(fp, row["ra_obj"], row["dec_obj"], title, pp)
            frames.append(pp)
        if len(frames) >= 3:
            imgs = [Image.open(p).convert("P", palette=Image.ADAPTIVE) for p in frames]
            gif = os.path.join(ANIM_DIR, f"beebe_{label}.gif")
            imgs[0].save(gif, save_all=True, append_images=imgs[1:],
                         duration=700, loop=0)
            print(f"  -> {gif} ({len(frames)} frames)")

    # --- static cutouts of the brightest (opposition) detections ---
    s = t[np.isin(t["night"], list(STATIC_NIGHTS))]
    s.sort("vmag")
    for i, row in enumerate(s[:4]):
        fp = os.path.join(FITS_DIR, f"static_{i:02d}.fits")
        if not fetch_cutout(row["image_url"], row["ra_obj"], row["dec_obj"], 150, fp):
            continue
        band = filter_from_url(row["image_url"])
        title = (f"(20220) Beebe  V={row['vmag']:.1f}  ZTF-{band}  "
                 f"{row['date_obs']} {str(row['time_obs'])[:8]} UT")
        pp = os.path.join(PNG_DIR, f"static_{row['date_obs']}_{i:02d}.png")
        render_frame(fp, row["ra_obj"], row["dec_obj"], title, pp)
        print(f"  static -> {pp}")


if __name__ == "__main__":
    main()

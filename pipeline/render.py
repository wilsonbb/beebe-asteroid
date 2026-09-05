"""Common-WCS cutouts. Display processing is not calibrated photometry."""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u
from reproject import reproject_interp
from PIL import Image
from .core import digest

RENDER_VERSION='2'

def read_fits(path):
    with fits.open(path,checksum=True) as hdul:
        hdul.verify('exception'); data=np.asarray(hdul[0].data,dtype=float); wcs=WCS(hdul[0].header).celestial
    if data.ndim!=2 or min(data.shape)<20 or not wcs.has_celestial or np.isfinite(data).mean()<.8: raise ValueError('Invalid FITS pixels/WCS')
    return data,wcs

def sky_center(coords):
    c=SkyCoord([p[0] for p in coords]*u.deg,[p[1] for p in coords]*u.deg)
    xyz=c.cartesian.xyz.value.mean(axis=1); xyz/=np.linalg.norm(xyz)
    return SkyCoord(x=xyz[0],y=xyz[1],z=xyz[2],representation_type='cartesian').spherical

def output_wcs(coords, side_arcsec=180, pixels=360):
    c=sky_center(coords); w=WCS(naxis=2)
    w.wcs.crpix=[(pixels+1)/2]*2; w.wcs.cdelt=[-side_arcsec/pixels/3600,side_arcsec/pixels/3600]
    w.wcs.crval=[c.lon.deg,c.lat.deg]; w.wcs.ctype=['RA---TAN','DEC--TAN']
    return w

def asset(path, public):
    b=path.read_bytes()
    with Image.open(path) as im: size=im.size
    return {'url':'/'+str(path.relative_to(public)), 'width':size[0], 'height':size[1], 'bytes':len(b), 'sha256':digest(b)}

def render_sequence(rows, paths, public, timestamp, previous=None):
    rows=sorted(rows,key=lambda r:r['observed_at'])
    coords=[(r['ra'],r['dec']) for r in rows]; center=sky_center(coords)
    c=SkyCoord([x[0] for x in coords]*u.deg,[x[1] for x in coords]*u.deg)
    origin=SkyCoord(center.lon,center.lat)
    side=max(150.,min(480.,float(c.separation(origin).arcsec.max()*2+120)))
    pixels=360; w=output_wcs(coords,side,pixels)
    signature=digest(json.dumps({'ids':[r['id'] for r in rows], 'coords':coords,'side':side,'version':RENDER_VERSION,'inputs':[digest(Path(paths[r['id']]).read_bytes()) for r in rows]},sort_keys=True).encode())[:16]
    if previous and previous.get('revision')==signature and all((public/f['asset']['url'].lstrip('/')).exists() for f in previous['frames']): return previous
    media=public/'media'/signature;media.mkdir(parents=True,exist_ok=True)
    output=[]; gif_frames=[]
    for row in rows:
        data,iw=read_fits(paths[row['id']]); aligned,footprint=reproject_interp((data,iw),w,shape_out=(pixels,pixels))
        x,y=w.world_to_pixel_values(row['ra'],row['dec']);xi,yi=int(round(float(x))),int(round(float(y)))
        if not (5<=xi<pixels-5 and 5<=yi<pixels-5) or footprint[yi-4:yi+5,xi-4:xi+5].min()<.95: continue
        valid=(footprint>.95)&np.isfinite(aligned)
        if valid.mean()<.85: continue
        vals=aligned[valid]; bg=float(np.median(vals)); noise=float(np.median(np.abs(vals-bg))*1.4826)
        if noise<=0: continue
        scaled=np.arcsinh(np.maximum((aligned-bg)/noise+1,0)/2)/np.arcsinh(18/2)
        scaled=np.where(valid,np.clip(scaled,0,1),0)
        # FITS origin is lower-left; browser origin is upper-left.
        im=Image.fromarray(np.flipud(np.uint8(scaled*255)),mode='L')
        filename=media/(digest(row['id'].encode())[:12]+'.webp');im.save(filename,quality=88,method=6)
        output.append({'id':row['id'],'at':row['observed_at'],'band':row['band'],'asset':asset(filename,public),'marker':{'x':float((x+.5)/pixels),'y':float(1-(y+.5)/pixels)},'source_url':row['source_url']})
        gif_frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE))
    if not output: raise ValueError('No usable pixels at predicted positions')
    gif=None
    if len(output)>=3:
        p=media/'motion.gif';gif_frames[0].save(p,save_all=True,append_images=gif_frames[1:],duration=700,loop=0);gif=asset(p,public)
    span=(max(r['mjd'] for r in rows)-min(r['mjd'] for r in rows))*1440
    return {'id':rows[0]['night'],'night':rows[0]['night'],'revision':signature,'frames':output,'poster':output[0]['asset'],'gif':gif,'n_frames':len(output),'bands':sorted({r['band'] for r in rows}),'span_minutes':round(span,1),'field_arcsec':round(side,1),'wcs':dict(w.to_header()),'visibility':'unreviewed','published_at':previous['published_at'] if previous else timestamp,'updated_at':timestamp,'display_note':'North up; east left. Each exposure is background-normalized and resampled to a common sky grid. Mixed filters can change star brightness.'}

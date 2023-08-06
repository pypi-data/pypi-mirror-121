from __future__ import print_function
import os
import numpy as np
from astropy.table import Table
from astropy.io import ascii
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
import astropy.units as u
import requests
from PIL import Image
from io import BytesIO
import pylab
from download_panstar.download_panstar_image import download_panstar_image as dpi
from download_panstar import download_panstar_catalog as dpc
import pdb
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.colors import PowerNorm
import matplotlib.colors as mcolors
import matplotlib.cm as cm
from astropy.io import fits
from astropy.visualization import PercentileInterval, AsinhStretch
from astropy.wcs import WCS

class download_panstar(object):
    '''Download PanSTARRS1 image and catalog based on central position'''
    def __init__(self, coo_cen_skycoord, size_pixel, 
                 name='test', imgtype='stack', band3color='grz', band='r', outdir=None):
        
        coo_icrs=coo_cen_skycoord.transform_to('icrs')
        ra=coo_icrs.ra.value
        dec=coo_icrs.dec.value
        size = size_pixel
        radius=size*0.25/3600.
        self.coo_icrs=coo_icrs
        self.ra=ra
        self.dec=dec
        self.size=size
        self.radius=radius
        self.name=name
        self.imgtype=imgtype
        self.band3color=band3color
        self.band=band
        self.outdir=outdir
        self.cat_types=['mean','stack','detection']

    def image(self,fitsname=None):

        fits_filter=self.band
        if fits_filter == 'g':
            filterid=1
        elif fits_filter == 'r':
            filterid=2
        elif fits_filter == 'i':
            filterid=3
        elif fits_filter == 'z':
            filterid=4
        elif fits_filter == 'y':
            filterid=5
        else:
            raise ValueError('There is no filter of '+fits_filter+' in PanSTARRS1 survey.')
    
        if fitsname is None:
            fitsname=self.name+'_'+fits_filter+'_panstar.fits'
        #catname=fitsname.replace('_'+fits_filter+'_','_cat_')
        fitsurl = dpi(ra=self.ra,dec=self.dec,size=self.size,filters=fits_filter, 
                      format="fits",imgtype=self.imgtype).geturl()
        fh = fits.open(fitsurl[0])
        fh.writeto(self.outdir+fitsname,overwrite=True)
        data,hdr=fits.getdata(self.outdir+fitsname,0,header=True)
        if 'PC001001' in hdr:
            #hdr['CD1_1']=hdr['PC001001']
            #hdr['CD1_2']=hdr['PC001002']
            #hdr['CD2_1']=hdr['PC002001']
            #hdr['CD2_2']=hdr['PC002002']
            #del hdr['PC001001']
            #del hdr['PC001002']
            #del hdr['PC002001']
            #del hdr['PC002002']
            pass
        if 'GAIN' not in hdr:
            hdr['GAIN']=hdr['HIERARCH CELL.GAIN']
        if 'SATURATE' not in hdr:
            hdr['SATURATE'] = hdr['HIERARCH CELL.SATURATION']
        #pdb.set_trace()
        fits.writeto(self.outdir+fitsname,data,hdr,overwrite=True)
        hdu=fits.PrimaryHDU(data=data,header=hdr)
        return hdu,fitsname
    
    def catalog(self,cattype='mean', wcs=None):
        if cattype == 'stack':
            sconstraints = {'primaryDetection':1}
            scolumns = """objID,raMean,decMean,nDetections,ng,nr,ni,nz,ny,
                nStackDetections,primaryDetection,qualityFlag,
                gPSFMag,rPSFMag,iPSFMag,zPSFMag,yPSFMag,
                gPSFMagErr,rPSFMagErr,iPSFMagErr,zPSFMagErr,yPSFMagErr,
                ginfoFlag,rinfoFlag,iinfoFlag,zinfoFlag,yinfoFlag,
                ginfoFlag2,rinfoFlag2,iinfoFlag2,zinfoFlag2,yinfoFlag2,
                ginfoFlag3,rinfoFlag3,iinfoFlag3,zinfoFlag3,yinfoFlag3""".split(',')
        elif cattype == 'detection':
            sconstraints = {'filterID':filterid}
            scolumns = """objID,imageID,filterID,surveyID,obsTime,expTime,airMass,ra,dec,zp,psfFlux,psfFluxErr,
                 psfMajorFWHM,psfMinorFWHM,
                 psfTheta,psfCore,psfQf,psfQfPerfect,psfChiSq,psfLikelihood,apFlux,
                 apFluxErr,apFillF,apRadius,kronFlux,kronFluxErr,kronRad,sky,skyErr,
                 infoFlag,infoFlag2,infoFlag3""".split(',')
        elif cattype == 'mean':
            sconstraints = {'nDetections.gt':1}
            scolumns = """objID,raMean,decMean,nDetections,ng,nr,ni,nz,ny,
                qualityFlag,
                gMeanPSFMag,rMeanPSFMag,iMeanPSFMag,zMeanPSFMag,yMeanPSFMag,
                gMeanPSFMagErr,rMeanPSFMagErr,iMeanPSFMagErr,zMeanPSFMagErr,yMeanPSFMagErr,
                gFlags,rFlags,iFlags,zFlags,yFlags""".split(',')
        else:
            raise ValueError('Only support catalog types of '+self.cat_types)
        
        # strip blanks and weed out blank and commented-out values
        scolumns = [x.strip() for x in scolumns]
        scolumns = [x for x in scolumns if x and not x.startswith('#')]

        sresults = dpc.ps1cone(self.ra,self.dec,self.radius,table=cattype,
                               release="dr2",columns=scolumns,verbose=True,**sconstraints)
        #pdb.set_trace()
        stab = ascii.read(sresults)
        
        for col in scolumns:
            try:
                stab[col]
            except KeyError:
                print(col,"not found")
        # improve the format
        if cattype == 'mean':
            for filter in 'grizy':
                col = filter+'MeanPSFMag'
                try:
                    stab[col].format = ".4f"
                    stab[col][stab[col] == -999.0] = np.nan
                except KeyError:
                    print("{} not found".format(col))
        elif cattype == 'stack':
            for filter in 'grizy':
                col = filter+'PSFMag'
                try:
                    stab[col].format = ".4f"
                    stab[col][stab[col] == -999.0] = np.nan
                except KeyError:
                    print("{} not found".format(col))
        else:
            pass

        if 'objID' in stab.columns:
            stab['objID']=stab['objID'].astype(str)
        df=stab.to_pandas()
        #pdb.set_trace()
        if wcs is not None:
            if (cattype == 'mean') | (cattype == 'stack'):
                xim,yim=wcs.wcs_world2pix(df['raMean'],df['decMean'],1)
            elif cattype == 'detection':
                xim,yim=wcs.wcs_world2pix(df['ra'],df['dec'],1)
            else:
                raise ValueError(cattype+' is not supported!')
            xlim,ylim=[self.size,self.size]
            xim=np.asarray(np.round(xim),dtype=int)
            yim=np.asarray(np.round(yim),dtype=int)
            df.insert(df.columns.size,'xim',xim)
            df.insert(df.columns.size,'yim',yim)
            cond=(df['xim']>0) & (df['xim']<=xlim-1) & (df['yim']>0) & (df['yim']<=ylim-1)
            dfo=df.loc[cond,:]
        else:
            dfo=df.copy()
        if (cattype == 'mean') | (cattype == 'stack'):
            catname=self.name+'_cat_panstar.fits'
        else:
            catname=self.name+'_'+self.band+'detection_panstar.fits'
        Table.from_pandas(dfo).filled(np.nan).write(self.outdir+catname,overwrite=True)
        return dfo,catname
    
    def checkplot(self,hdu,dfcat):
        data=hdu.data
        hdr=hdu.header
        dfc=dfcat
        #pdb.set_trace()
        # replace NaN values with zero for display
        data[np.isnan(data)] = 0.0
        # set contrast to something reasonable
        transform = AsinhStretch() + PercentileInterval(99.5)
        bdata = transform(data)

        showfile=self.outdir+self.name+'_panstar.png'
        figsize=(14,7)
        fig = plt.figure(figsize=figsize)
        fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9,wspace=0.2,hspace=0.1)
        ax1 = fig.add_subplot(1, 2, 1, projection=WCS(hdr))
        axformatter='dd:mm:ss'
        im=ax1.imshow(bdata, origin='lower', cmap='gray_r',norm=PowerNorm(gamma=1))
        ax1.coords['ra'].set_axislabel('RA')
        ax1.coords['dec'].set_axislabel('DEC')
        ax1.coords['ra'].set_major_formatter(axformatter)
        ax1.coords['dec'].set_major_formatter(axformatter)
        ax1.set_title(self.name+' PanSTARRS1 '+self.band+' band')
        if 'nDetections' in dfc.columns:
            condp=dfc['nDetections']>1
            ax1.scatter(dfc.loc[condp,'xim'],dfc.loc[condp,'yim'],marker='o',s=10,edgecolor='red',facecolor='none')
        else:
            ax1.scatter(dfc['xim'],dfc['yim'],marker='o',s=10,edgecolor='red',facecolor='none')
    
        if self.band3color is not None:
            cim = dpi(ra=self.ra,dec=self.dec,size=self.size,filters=self.band3color,
                      imgtype=self.imgtype).getcolorim()
            ax2 = fig.add_subplot(1, 2, 2, projection=WCS(hdr))
            im=ax2.imshow(cim, origin='lower')
            ax2.coords['ra'].set_axislabel('RA')
            ax2.coords['dec'].set_axislabel(' ')
            ax2.coords['ra'].set_major_formatter(axformatter)
            ax2.coords['dec'].set_major_formatter(axformatter)
            ax2.set_title(self.name+' grz RGB image')


        plt.savefig(showfile,bbox_inches = "tight")
        plt.close()
        #pylab.figure(1,(12,6))
        #pylab.subplot(121)
        #pylab.imshow(gim,origin="upper")
        #pylab.title('Crab Nebula PS1 r (jpeg)')

        #pylab.subplot(122)
        #pylab.title('Crab Nebula PS1 r (fits)')
        #pylab.imshow(bfim,cmap="gray",origin="lower")

        #pylab.savefig(imgdir+'test_fits.png')
if __name__ == '__main__':
    imgdir='/Users/miaomiaozhang/Science/data/WFST-pipeline/test/detection/image/'
    l=60.
    #b=1.5
    #b=15.
    b=0.5
    coo_gal=SkyCoord(l*u.degree,b*u.degree,frame='galactic')
    coo_icrs=coo_gal.transform_to('icrs')
    size = 1280
    #name='Crab_Nebula'
    #name='test_medium'
    name='test_high'
    imgtype='stack'
    outdir='./test/'
    
    dp=download_panstar(coo_icrs, size, name=name, imgtype=imgtype, band3color='grz', band='r', outdir=imgdir)
    

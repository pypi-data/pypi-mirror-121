import os
import pdb
import numpy as np
import pandas as pd
import pathlib
import warnings
from astropy.utils.exceptions import AstropyWarning
from astropy.table import Table
from astropy.io import fits
from astropy.wcs import WCS
from astropy.nddata.utils import Cutout2D
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.modeling import models, fitting
from astropy.modeling.models import custom_model
from astropy.stats import freedman_bin_width, knuth_bin_width, sigma_clip
import matplotlib.pyplot as plt
from astropy.visualization import AsymmetricPercentileInterval,ImageNormalize,AsinhStretch,PowerStretch
from mpl_toolkits.axes_grid1 import make_axes_locatable
import seaborn as sns
from matplotlib.colors import PowerNorm,LogNorm
import logging
from subprocess import check_output, CalledProcessError, STDOUT
import shlex
import pickle
import seaborn as sns
from sklearn.cluster import DBSCAN
import cv2
from vlogging import VisualRecord as VR
from tqdm import tqdm
from PhotoSex.basic import basic
from PhotoSex.PhotoSex_config import PhotoSex_config as sexconfig
import gc
import resource
soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
resource.setrlimit(resource.RLIMIT_NOFILE, (hard, hard))
warnings.simplefilter('ignore', UserWarning)
warnings.simplefilter('ignore', category=AstropyWarning)


class PhotoSex(object):
    '''Photometry with Sextractor+PSFEX, supporting aperture and PSF photometry.'''
    
    def __init__(self, imgfile, band='r', workdir='./', config_dir=None, sexdir=None, apertures=None,
                 apc_polyorder=None,
                 apc_radius_total_flux=None,
                 apc_checkplot_curveofgrowth=None,
                 checkpro_check_fits_image=None,
                 checkpro_check_png_plot=None,
                 checkpro_checkpng_width=None,
                 checkres_reference_flag_threshold=None,
                 checkres_zmagfit_outliers_method = None,
                 checkres_zmagfit_outliers_nsig_dbscan = None,
                 checkres_zmagfit_outliers_minfrac_dbscan = None,
                 checkres_zmagfit_outliers_nsig_sigmaclip = None,
                 checkres_zmagfit_polyorder = None,
                 checkres_plot_rawimage_scalerange = None,
                 checkres_plot_zoominimage_width = None,
                 checkres_plot_zoominimage_scalerange = None,
                 checkres_keep_html_only=None,
                 show_computer_info=None):
        
        if config_dir is None:
            config_dir=workdir
        info=sexconfig(path_config_file=config_dir,name_config_file='PhotoSex_config.ini').setconfig()
        #pdb.set_trace()
        #self.band=band
        self.imgname=imgfile.split('/')[-1]
        self.imgdir='/'.join(imgfile.split('/')[:-1])+'/'
        self.imgfile=imgfile
        self.workdir=workdir
        
        
        if sexdir is not None:
            self.sexdir=sexdir
        else:
            self.sexdir=info['sexdir']
        
        self.testname='test.fits'
        
        hd=fits.getheader(imgfile)
        self.hd=hd
        wcs=WCS(hd)
        self.wcs=wcs
        self.pixscl=wcs.proj_plane_pixel_scales()[0].value*3600.
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
        self.logfmt=formatter
        
        if apertures is not None:
            apers=np.array(apertures)*u.arcsec
        else:
            apers=np.array(info['apers'])*u.arcsec#support 120 apertures at most
        apers_pix=apers.value/self.pixscl
        self.apers=apers
        self.apers_pix=apers_pix
        
        
        if apc_polyorder is not None:
            self.order_apc=apc_polyorder
        else:
            self.order_apc=info['order_apc']
        
        
        if apc_radius_total_flux is not None:
            self.apc_rad_tot=apc_radius_total_flux
        else:
            self.apc_rad_tot=info['apc_rad_tot']
        
        
        if apc_checkplot_curveofgrowth is not None:
            self.checkcog_apc=apc_checkplot_curveofgrowth
        else:
            self.checkcog_apc=info['checkcog_apc']
        
        
        if checkpro_check_fits_image is not None:
            self.checkimg=checkpro_check_fits_image
        else:
            self.checkimg=info['checkimg']
        
        
        if checkpro_check_png_plot is not None:
            self.checkplot=checkpro_check_png_plot
        else:
            self.checkplot=info['checkplot']
        
        
        if checkpro_checkpng_width is not None:
            self.checkfig_width=checkpro_checkpng_width
        else:
            self.checkfig_width=info['checkfig_width']
        
        self.psfex_checkcube=False
        
        
        if show_computer_info is not None:
            self.phot_show_env=show_computer_info
        else:
            self.phot_show_env=info['phot_show_env']
        
        
        if checkres_zmagfit_polyorder is not None:
            self.checkphot_zmag_order=checkres_zmagfit_polyorder
        else:
            self.checkphot_zmag_order=info['checkphot_zmag_order']
        
        
        if checkres_reference_flag_threshold is not None:
            self.checkphot_flag_ref_threshold=checkres_reference_flag_threshold
        else:
            self.checkphot_flag_ref_threshold=info['checkphot_flag_ref_threshold']
        
        
        if checkres_zmagfit_outliers_method is not None:
            self.checkphot_if_cali_outliers_detection_method=checkres_zmagfit_outliers_method
        else:
            self.checkphot_if_cali_outliers_detection_method=info['checkphot_if_cali_outliers_detection_method']
        
        
        if checkres_plot_zoominimage_width is not None:
            self.checkphot_zoom_width=checkres_plot_zoominimage_width
        else:
            self.checkphot_zoom_width=info['checkphot_zoom_width']
        
        
        if checkres_plot_rawimage_scalerange is not None:
            self.checkphot_imgraw_interval=checkres_plot_rawimage_scalerange
        else:
            self.checkphot_imgraw_interval=info['checkphot_imgraw_interval']
        
        
        if checkres_plot_zoominimage_scalerange is not None:
            self.checkphot_imgzoom_interval=checkres_plot_zoominimage_scalerange
        else:
            self.checkphot_imgzoom_interval=info['checkphot_imgzoom_interval']
        
        
        if checkres_zmagfit_outliers_nsig_dbscan is not None:
            self.checkphot_nsig_dbscan=checkres_zmagfit_outliers_nsig_dbscan
        else:
            self.checkphot_nsig_dbscan=info['checkphot_nsig_dbscan']
        
        
        if checkres_zmagfit_outliers_minfrac_dbscan is not None:
            self.checkphot_minfrac_dbscan=checkres_zmagfit_outliers_minfrac_dbscan
        else:
            self.checkphot_minfrac_dbscan=info['checkphot_minfrac_dbscan']
        
        
        if checkres_zmagfit_outliers_nsig_sigmaclip is not None:
            self.checkphot_nsig_sigmaclip=checkres_zmagfit_outliers_nsig_sigmaclip
        else:
            self.checkphot_nsig_sigmaclip=info['checkphot_nsig_sigmaclip']
        
        
        if checkres_keep_html_only is not None:
            self.checkphot_keep_html_only=checkres_keep_html_only
        else:
            self.checkphot_keep_html_only=info['checkphot_keep_html_only']
        
        #pdb.set_trace()
        
        
    def detect(self, indir=None, infile=None, outfile='detection.fits', outdir=None, sexconfig='use_for_psfex.sex',
               psfname=None, checkimg=False, backtype='AUTO'):
        apers=self.apers
        apers_pix=self.apers_pix
        napers=apers_pix.shape[0]
        if  napers > 120:
            raise ValueError('Support 120 apertures at most!')
        aperstr=','.join(np.asarray(np.round(apers_pix),dtype=str))
        #pdb.set_trace()
        if (indir is None) & (infile is None):
            os.system('cp '+self.imgfile+' '+self.workdir+self.testname)
        else:
            os.system('cp '+indir+infile+' '+self.workdir+self.testname)
        if outdir is None:
            outdir=self.workdir
        #Here we follow the process described in Dark Energy Survey Pipeline (2018PASP..130g4501M)
        if checkimg is True:
            checkimg_type=' BACKGROUND,FILTERED,OBJECTS,-OBJECTS,APERTURES,SEGMENTATION,BACKGROUND_RMS'
            checkimg_name=' '+outdir+self.testname.replace('.fits','_bg.fits')+','+\
            outdir+self.testname.replace('.fits','_subbg_filtered.fits')+','+\
            outdir+self.testname.replace('.fits','_obj.fits')+','+\
            outdir+self.testname.replace('.fits','_subobj.fits')+','+\
            outdir+self.testname.replace('.fits','_apertures.fits')+','+\
            outdir+self.testname.replace('.fits','_segmentation.fits')+','+\
            outdir+self.testname.replace('.fits','_bgrms.fits')
        else:
            checkimg_type=' NONE'
            checkimg_name=' check.fits'
        
        if sexconfig == 'use_for_psfex.sex':
            cmd='sex -c '+self.sexdir+sexconfig+' '+self.workdir+self.testname+\
            ' -CATALOG_NAME '+outdir+outfile+' -PARAMETERS_NAME '+self.sexdir+'use_universal.param '+\
            '-FILTER_NAME '+self.sexdir+'default.conv -STARNNW_NAME '+self.sexdir+'default.nnw '+\
            '-PHOT_APERTURES '+aperstr+' -CHECKIMAGE_TYPE'+checkimg_type+' -CHECKIMAGE_NAME'+checkimg_name+\
            ' -BACK_TYPE '+backtype
            #os.system(cmd)
        if sexconfig == 'use_psf.sex':
            cmd='sex -c '+self.sexdir+sexconfig+' '+self.workdir+self.testname+\
            ' -CATALOG_NAME '+outdir+outfile+' -PARAMETERS_NAME '+self.sexdir+'use_psf.param '+\
            '-FILTER_NAME '+self.sexdir+'default.conv -STARNNW_NAME '+self.sexdir+'default.nnw '+\
            '-PSF_NAME '+outdir+psfname+' -PHOT_APERTURES '+aperstr+' -CHECKIMAGE_TYPE -OBJECTS '+\
            '-CHECKIMAGE_NAME '+outdir+'checkimage_subobjects.fits -CHECKIMAGE_TYPE'+checkimg_type+\
            ' -CHECKIMAGE_NAME'+checkimg_name+' -BACK_TYPE '+backtype
            #outsex=os.system(cmd)
        if sexconfig == 'use_withoutpsf.sex':
            cmd='sex -c '+self.sexdir+sexconfig+' '+self.workdir+self.testname+\
            ' -CATALOG_NAME '+outdir+outfile+' -PARAMETERS_NAME '+self.sexdir+'use_universal.param '+\
            '-FILTER_NAME '+self.sexdir+'gauss_3.0_7x7.conv -STARNNW_NAME '+self.sexdir+'default.nnw '+\
            '-PHOT_APERTURES '+aperstr+' -PHOT_AUTOAPERS 0.0,'+str(apers_pix[3])+\
            ' -CHECKIMAGE_TYPE'+checkimg_type+' -CHECKIMAGE_NAME'+checkimg_name+' -BACK_TYPE '+backtype
            #os.system(cmd)
        command=shlex.split(cmd)
        outsex=check_output(command,stderr=STDOUT).decode()#basic.syscmd(cmd)
        #pdb.set_trace()
        #outsex=basic.syscmd(cmd)
        #print(outsex)
        return outsex
    
    def pack_checkimg_sexout(self,indir=None,packname='test_checkmef.fits',del_checkimg=True):
        if indir is None:
            indir=self.workdir
        if os.path.isfile(indir+self.testname.replace('.fits','_bg.fits')) == False:
            raise ValueError('There is no check images in '+indir)
        
        img_bg,hd_bg=fits.getdata(indir+self.testname.replace('.fits','_bg.fits'),0,header=True)
        img_filt,hd_filt=fits.getdata(indir+self.testname.replace('.fits','_subbg_filtered.fits'),0,header=True)
        img_seg,hd_seg=fits.getdata(indir+self.testname.replace('.fits','_segmentation.fits'),0,header=True)
        img_obj,hd_obj=fits.getdata(indir+self.testname.replace('.fits','_obj.fits'),0,header=True)
        img_aper,hd_aper=fits.getdata(indir+self.testname.replace('.fits','_apertures.fits'),0,header=True)
        img_subobj,hd_subobj=fits.getdata(indir+self.testname.replace('.fits','_subobj.fits'),0,header=True)
        img_bgrms,hd_bgrms=fits.getdata(indir+self.testname.replace('.fits','_bgrms.fits'),0,header=True)
        
        if del_checkimg is True:
            os.system('rm -f '+indir+self.testname.replace('.fits','_bg.fits'))
            os.system('rm -f '+indir+self.testname.replace('.fits','_subbg_filtered.fits'))
            os.system('rm -f '+indir+self.testname.replace('.fits','_segmentation.fits'))
            os.system('rm -f '+indir+self.testname.replace('.fits','_obj.fits'))
            os.system('rm -f '+indir+self.testname.replace('.fits','_apertures.fits'))
            os.system('rm -f '+indir+self.testname.replace('.fits','_subobj.fits'))
            os.system('rm -f '+indir+self.testname.replace('.fits','_bgrms.fits'))
        
        img,hd=fits.getdata(indir+self.testname,0,header=True)
        

        hd['EXTNAME']='image'
        hd_bg['EXTNAME']='background'
        hd_filt['EXTNAME']='filtered'
        hd_seg['EXTNAME']='segmentation'
        hd_obj['EXTNAME']='objects'
        hd_aper['EXTNAME']='apertures'
        hd_subobj['EXTNAME']='sub-objects'
        hd_bgrms['EXTNAME']='background_rms'
        hdu=fits.PrimaryHDU(data=img,header=hd)
        hdu_bg=fits.ImageHDU(data=img_bg,header=hd_bg)
        hdu_filt=fits.ImageHDU(data=img_filt,header=hd_filt)
        hdu_seg=fits.ImageHDU(data=img_seg,header=hd_seg)
        hdu_obj=fits.ImageHDU(data=img_obj,header=hd_obj)
        hdu_aper=fits.ImageHDU(data=img_aper,header=hd_aper)
        hdu_subobj=fits.ImageHDU(data=img_subobj,header=hd_subobj)
        hdu_bgrms=fits.ImageHDU(data=img_bgrms,header=hd_bgrms)
        
        #pdb.set_trace()
        hdu_pack=fits.HDUList([hdu,hdu_bg,hdu_filt,hdu_seg,hdu_obj,hdu_aper,hdu_subobj,hdu_bgrms])
        #pdb.set_trace()
        hdu_pack.writeto(indir+packname,overwrite=True)
        hdu_pack.close()
        del hdu_pack
        gc.collect()
        return 1
    
    
    def checkplot_detection(self,indir=None,packname='test_checkmef.fits',
                            fig_width=15.,figname='checkplot_detection.png'):
        
        if indir is None:
            indir=self.workdir
        if os.path.isfile(indir+packname) == False:
            raise ValueError('There is no checking MEF file!')
        
        img,hd=fits.getdata(indir+packname,0,header=True)
        img_bg=fits.getdata(indir+packname,1)
        img_filt=fits.getdata(indir+packname,2)
        img_seg=fits.getdata(indir+packname,3)
        img_obj=fits.getdata(indir+packname,4)
        img_subobj=fits.getdata(indir+packname,6)
        
        showfile=indir+figname
        xsize,ysize=img.shape
        ratio=float(ysize)/xsize*2./3.
        figsize=(fig_width,fig_width*ratio)
        fig,ax=plt.subplots(2,3,figsize=figsize)
        fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0.05,wspace=0.05)
        interval=AsymmetricPercentileInterval(2,95.)
        stretch=AsinhStretch()
        cmap='RdBu_r'#'Greys'
        ax[0][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[0][1].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[0][2].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][1].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][2].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[0][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        
        ax[0][0].imshow(img,origin='lower',cmap=cmap,norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[0][0].set_title('image')
        
        ax[0][1].imshow(img_bg,origin='lower',cmap=cmap,norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[0][1].set_title('background')
        
        ax[0][2].imshow(img_filt,origin='lower',cmap=cmap,norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[0][2].set_title('-bg filtered')
        
        img_seg[img_seg>0.]=np.percentile(img,95)
        ax[1][0].imshow(img_seg,origin='lower',cmap=cmap,norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[1][0].set_title('segmentation')
        
        ax[1][1].imshow(img_obj,origin='lower',cmap=cmap,norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[1][1].set_title('objects')
        
        ax[1][2].imshow(img_subobj,origin='lower',cmap=cmap,norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[1][2].set_title('-objects')
        fig.tight_layout(h_pad=2)
        fig.savefig(showfile,bbox_inches='tight')
        plt.cla()
        plt.close(fig)
        
        #pdb.set_trace()
        return 1
        
    def psfex(self, indir=None, infile='detection.fits', outdir=None, checkcube=False, checkimg=True):
        if indir is None:
            indir=self.workdir
        
        if outdir is None:
            outdir=self.workdir
        
        if checkimg is True:
            checkimg_type=' CHI,PROTOTYPES,SAMPLES,RESIDUALS,SNAPSHOTS,MOFFAT,-MOFFAT,-SYMMETRICAL'
            checkimg_name=' '+outdir+'chi.fits,'+outdir+'proto.fits,'+outdir+'samp.fits,'+\
            outdir+'resi.fits,'+outdir+'snap.fits,'+outdir+'moffat.fits,'+outdir+'submoffat.fits,'+\
            outdir+'subsym.fits'
        else:
            checkimg_type=' NONE'
            checkimg_name=' chi.fits'
        
        if checkcube is True:
            checkimg_cube='Y'
        else:
            checkimg_cube='N'
        
        cmd='psfex '+indir+infile+' -c '+self.sexdir+'use.psfex -OUTCAT_TYPE FITS_LDAC -OUTCAT_NAME '+outdir+\
        infile.replace('.fits','_psfexout.fits')+' -CHECKIMAGE_TYPE'+checkimg_type+\
        ' -CHECKIMAGE_NAME'+checkimg_name+' -CHECKIMAGE_CUBE '+checkimg_cube
        #outpsfex=basic.syscmd(cmd)
        #outpsfex=os.system(cmd)
        #outpsfex=basic.syscmd(cmd)  
        #print(outpsfex)
        command=shlex.split(cmd)
        outpsfex=check_output(command,stderr=STDOUT).decode()
        #pdb.set_trace()
        return outpsfex
    
    def pack_checkimg_psfexout(self,psfexinfile='detection.fits',indir=None,
                               packname='testpsfex_checkmef.fits',del_checkimg=True):
        if indir is None:
            indir=self.workdir
        if os.path.isfile(indir+'chi_'+psfexinfile) == False:
            raise ValueError('There is no PSFex check images in '+indir)
        
        img_chi,hd_chi=fits.getdata(indir+'chi_'+psfexinfile,0,header=True)
        img_proto,hd_proto=fits.getdata(indir+'proto_'+psfexinfile,0,header=True)
        img_samp,hd_samp=fits.getdata(indir+'samp_'+psfexinfile,0,header=True)
        img_resi,hd_resi=fits.getdata(indir+'resi_'+psfexinfile,0,header=True)
        img_snap,hd_snap=fits.getdata(indir+'snap_'+psfexinfile,0,header=True)
        img_moffat,hd_moffat=fits.getdata(indir+'moffat_'+psfexinfile,0,header=True)
        img_submoffat,hd_submoffat=fits.getdata(indir+'submoffat_'+psfexinfile,0,header=True)
        img_subsym,hd_subsym=fits.getdata(indir+'subsym_'+psfexinfile,0,header=True)
        
        if del_checkimg is True:
            os.system('rm -f '+indir+'chi_'+psfexinfile)
            os.system('rm -f '+indir+'proto_'+psfexinfile)
            os.system('rm -f '+indir+'samp_'+psfexinfile)
            os.system('rm -f '+indir+'resi_'+psfexinfile)
            os.system('rm -f '+indir+'snap_'+psfexinfile)
            os.system('rm -f '+indir+'moffat_'+psfexinfile)
            os.system('rm -f '+indir+'submoffat_'+psfexinfile)
            os.system('rm -f '+indir+'subsym_'+psfexinfile)
        
        hd_samp['EXTNAME']='samples'
        hd_chi['EXTNAME']='chi2'
        hd_resi['EXTNAME']='residuals'
        hd_proto['EXTNAME']='prototype'
        hd_snap['EXTNAME']='snapshots'
        hd_moffat['EXTNAME']='moffat'
        hd_submoffat['EXTNAME']='sub-moffat'
        hd_subsym['EXTNAME']='sub-symmetrical'
            
        hdu_samp=fits.PrimaryHDU(data=img_samp,header=hd_samp)
        hdu_chi=fits.ImageHDU(data=img_chi,header=hd_chi)
        hdu_resi=fits.ImageHDU(data=img_resi,header=hd_resi)
        hdu_proto=fits.ImageHDU(data=img_proto,header=hd_proto)
        hdu_snap=fits.ImageHDU(data=img_snap,header=hd_snap)
        hdu_moffat=fits.ImageHDU(data=img_moffat,header=hd_moffat)
        hdu_submoffat=fits.ImageHDU(data=img_submoffat,header=hd_submoffat)
        hdu_subsym=fits.ImageHDU(data=img_subsym,header=hd_subsym)
        
        #pdb.set_trace()
        hdu_pack=fits.HDUList([hdu_samp,hdu_chi,hdu_resi,hdu_proto,
                               hdu_snap,hdu_moffat,hdu_submoffat,hdu_subsym]).copy()
        #pdb.set_trace()
        hdu_pack.writeto(indir+packname,overwrite=True)
        hdu_pack.close()
        #hdu_samp.close()
        #hdu_chi.close()
        #hdu_resi.close()
        #hdu_proto.close()
        #hdu_snap.close()
        #hdu_moffat.close()
        #hdu_submoffat.close()
        #hdu_subsym.close()
        #del hdu_pack
        #del hdu_samp
        #del hdu_chi
        #del hdu_resi
        #del hdu_proto
        #del hdu_snap
        #del hdu_moffat
        #del hdu_submoffat
        #del hdu_subsym
        #del img_samp
        #del img_chi
        #del img_resi
        #del img_proto
        #del img_snap
        #del img_moffat
        #del img_submoffat
        #del img_subsym
        #del hd_samp
        #del hd_chi
        #del hd_resi
        #del hd_proto
        #del hd_snap
        #del hd_moffat
        #del hd_submoffat
        #del hd_subsym
        #gc.collect()
        return 1
    
    def checkplot_psfex(self, indir=None, fig_width=15.,
                        packname='testpsfex_checkmef.fits', figname='checkplot_psfex.png'):
        
        
        if indir is None:
            indir=self.workdir
        if os.path.isfile(indir+packname) == False:
            raise ValueError('There is no PSFEX checkimg MEF fits file!')
        
        img_samp=fits.getdata(indir+packname,0)
        img_chi=fits.getdata(indir+packname,1)
        img_resi=fits.getdata(indir+packname,2)
        img_proto=fits.getdata(indir+packname,3)
        img_snap=fits.getdata(indir+packname,4)
        img_moffat=fits.getdata(indir+packname,5)
        img_submoffat=fits.getdata(indir+packname,6)
        img_subsym=fits.getdata(indir+packname,7)
        
        figformat=figname.split('.')[-1]
        showfile1=indir+figname.replace('.'+figformat,'_psfsamples.'+figformat)
        ysize,xsize=img_samp.shape
        ratio=float(ysize)/xsize
        figsize=(fig_width,fig_width*ratio)
        fig,ax=plt.subplots(2,2,figsize=figsize)
        fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0.05,wspace=0.05)
        interval=AsymmetricPercentileInterval(0.1,99.)
        stretch=AsinhStretch()
        cmap='RdBu_r'#'Greys'
        
        ax[0][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[0][1].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][1].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        
        ax[0][0].imshow(img_samp,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_samp,interval=interval,stretch=stretch))
        ax[0][0].set_title('PSF stars')
        
        ax[0][1].imshow(img_proto,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_proto,interval=AsymmetricPercentileInterval(2,98.),
                                            stretch=stretch))
        ax[0][1].set_title('PSF prototype')
        
        ax[1][0].imshow(img_resi,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_samp,interval=interval,stretch=stretch))
        ax[1][0].set_title('PSF fitting residuals')
        
        ax[1][1].imshow(img_chi,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_chi,interval=interval,stretch=stretch))
        ax[1][1].set_title(r'PSF fitting $\chi^{2}$')
        
        fig.tight_layout(h_pad=2)
        fig.savefig(showfile1,bbox_inches='tight')
        plt.close(fig)
        
        showfile2=indir+figname.replace('.'+figformat,'_psf.'+figformat)
        ysize,xsize=img_snap.shape
        ratio=float(ysize)/xsize
        figsize=(fig_width,fig_width*ratio)
        fig,ax=plt.subplots(2,2,figsize=figsize)
        fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.95, hspace=0.05,wspace=0.05)
        interval=AsymmetricPercentileInterval(0.1,99.)
        stretch=AsinhStretch()
        cmap='RdBu_r'#'Greys'
        ax[0][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[0][1].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][0].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        ax[1][1].tick_params(top=False, bottom=False, left=False, right=False, 
                        labelleft=False, labelbottom=False, labelright=False, labeltop=False)
        
        fontsize=15
        ax[0][0].imshow(img_snap,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_snap,interval=interval,stretch=stretch))
        ax[0][0].set_title('PSF model',fontsize=fontsize)
        
        ax[0][1].imshow(img_moffat,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_snap,interval=interval,stretch=stretch))
        ax[0][1].set_title('PSF Moffat model',fontsize=fontsize)
        
        ax[1][0].imshow(img_submoffat,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_snap,interval=AsymmetricPercentileInterval(0.1,80.),
                                            stretch=stretch))
        ax[1][0].set_title('PSF model - Moffat',fontsize=fontsize)
        
        ax[1][1].imshow(img_subsym,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img_snap,interval=AsymmetricPercentileInterval(0.1,80.),
                                            stretch=stretch))
        ax[1][1].set_title('PSF model - symmetrical',fontsize=fontsize)
        fig.tight_layout(h_pad=2)
        fig.savefig(showfile2,bbox_inches='tight')
        plt.close(fig)
        
        #pdb.set_trace()
        return 1
    
    
    def loginfo2(self,logger,hlogger,info):
        try:
            logger.info(info)
            hlogger.info(VR(info))
            status=0
        except:
            status=1
            pass
        
        return status
    
    def log2(self,info):
        status=self.loginfo2(self.logger,self.hlogger,info)
        return status
    
    def collect_envinfo(self):
        # importing the required modules
        import platform
        from datetime import datetime
        import psutil

        # First We will print the basic system information
        # using the platform module
        
        # Using the psutil library to get the boot time of the system
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        self.log2("\n\t\t\t Basic System Information\n"+\
                  "[+] Architecture : "+platform.architecture()[0]+"\n"+\
                  "[+] Machine : "+platform.machine()+"\n"+\
                  "[+] Operating System Release : "+platform.release()+"\n"+\
                  "[+] System Name : "+platform.system()+"\n"+\
                  "[+] Operating System Version : "+platform.version()+"\n"+\
                  "[+] Node: " +platform.node()+"\n"+\
                  "[+] Platform : "+platform.platform()+"\n"+\
                  "[+] Processor : "+platform.processor()+"\n"+\
                  "[+] System Boot Time : "+str(boot_time))
        

        # Displaying The CPU information
        cpu_frequency = psutil.cpu_freq()
        self.log2("\n\t\t\t CPU Information\n"+\
                  "[+] Number of Physical cores : "+str(psutil.cpu_count(logical=False))+"\n"+\
                  "[+] Number of Total cores : "+str(psutil.cpu_count(logical=True))+"\n"+\
                  f"[+] Max Frequency : {cpu_frequency.max:.2f}Mhz\n"+\
                  f"[+] Min Frequency : {cpu_frequency.min:.2f}Mhz\n"+\
                  f"[+] Current Frequency : {cpu_frequency.current:.2f}Mhz\n")
       


        # writing a function to convert bytes to GigaByte
        def bytes_to_GB(bytes):
            gb = bytes/(1024*1024*1024)
            gb = round(gb, 2)
            return gb

        # Using the virtual_memory() function it will return a tuple
        virtual_memory = psutil.virtual_memory()
        self.log2("\n\t\t\t Memory Information\n"+\
                  "[+] Total Memory present : "+str(bytes_to_GB(virtual_memory.total))+" Gb\n"+\
                  "[+] Total Memory Available : "+str(bytes_to_GB(virtual_memory.available))+" Gb\n"+\
                  "[+] Total Memory Used : "+str(bytes_to_GB(virtual_memory.used))+" Gb\n"+\
                  "[+] Percentage Used : "+str(virtual_memory.percent)+"%\n")
        
        
        #pdb.set_trace()
        return 1
    
    
    def phot(self,psf=False, apc=True, verbose=True, show_env=True):
        imgname=self.imgname.replace('.fits','')
        photfile=imgname+'_photsex_PSF'+str(psf)+'_APC'+str(apc)+'.fits'
        
        logger = logging.getLogger('PhotoSex')
        logger.setLevel(logging.INFO)
        fh=logging.FileHandler(self.workdir+photfile.replace('.fits','.log'),'w',encoding='utf-8')
        fh.setFormatter(self.logfmt)
        logger.addHandler(fh)
        
        hlogger = logging.getLogger('PhotoSex-plot')
        hlogger.setLevel(logging.INFO)
        hfh=logging.FileHandler(self.workdir+photfile.replace('.fits','.html'),'w',encoding='utf-8')
        hfh.setFormatter(self.logfmt)
        hlogger.addHandler(hfh)
        
        self.logger=logger
        self.hlogger=hlogger
        
        self.collect_envinfo()
        
        #pdb.set_trace()
        
        if verbose is True:
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(self.logfmt)
            logger.addHandler(ch)
        
        self.log2('Photometry with source extractor...')
        self.log2('BEGIN...')
        hd=fits.getheader(self.imgfile)
        wcs=WCS(hd)
        pixscl=wcs.proj_plane_pixel_scales()[0].value*3600.
        self.log2('Input image: '+self.imgfile)
        self.log2('Image size: '+str(hd['NAXIS1'])+'x'+str(hd['NAXIS2'])+' pixels')
        
        self.log2('Pixel scale: '+'{:5.3f}'.format(pixscl)+' arcsec/pixel')
        
        #pdb.set_trace()
        if psf is False:
            self.log2('Aperture photometry...')
            outsex=self.detect(outfile=photfile, outdir=None, sexconfig='use_withoutpsf.sex', 
                               checkimg=self.checkimg)
            self.log2(outsex)
            #pdb.set_trace()
            self.log2('Photometric catalog was saved to '+self.workdir+photfile)
            
            if self.checkimg:
                packname=photfile.replace('.fits','_checkmef.fits')
                self.pack_checkimg_sexout(indir=None,packname=packname,del_checkimg=True)
                self.log2('Save check images to '+self.workdir+packname+' which is a multi-extension FITS file.')
                if self.checkplot:
                    checkfig_name=photfile.replace('.fits','_checkplot.png')
                    self.checkplot_detection(indir=None,packname=packname,figname=checkfig_name,
                                             fig_width=self.checkfig_width)
                    self.log2('Display main check images into a plot that was saved to '+\
                              self.workdir+checkfig_name)
                    cv_image = cv2.imread(self.workdir+checkfig_name)
                    self.hlogger.info(VR(self.workdir+checkfig_name, cv_image, fmt="png"))
            #pdb.set_trace()
        else:
            self.log2('PSF photometry...')
            self.log2('First run Sextractor with a relatively high detection threshold to find bright stars...')
            
            outsex1=self.detect(checkimg=False)
            #pdb.set_trace()
            self.log2(outsex1)
            self.log2('Run PSFEX on above photometric result to model PSF...')
            outpsfex=self.psfex(checkimg=self.checkimg,checkcube=self.psfex_checkcube)
            self.log2(outpsfex)
            psfstar_file=photfile.replace('.fits','_psfex_psfstarsel.fits')
            os.system('rm -f '+self.workdir+'detection.fits')
            os.system('mv '+self.workdir+'detection_psfexout.fits '+\
                      self.workdir+psfstar_file)
            self.log2('Stars used to model PSF was saved to '+self.workdir+psfstar_file)
            psf_file=photfile.replace('.fits','_psfex_psf.fits')
            os.system('mv '+self.workdir+'detection.psf '+self.workdir+psf_file)
            self.log2('PSF model was saved to '+self.workdir+psf_file)
            if self.checkimg:
                packname=photfile.replace('.fits','_psfex_checkmef.fits')
                self.pack_checkimg_psfexout(indir=None,packname=packname,del_checkimg=True)
                self.log2('Save PSFEX check images to a multi-extension FITS file: '+\
                      self.workdir+packname)
                if self.checkplot:
                    checkfig_name=photfile.replace('.fits','_psfex_checkplot.png')
                    self.checkplot_psfex(packname=packname,figname=checkfig_name,fig_width=self.checkfig_width)
                    self.log2('Display PSFEX check images to two plots: '+self.workdir+\
                              photfile.replace('.fits','_psfex_checkplot_*.png'))
                    cv_image_psfex_psfsamples=cv2.imread(self.workdir+\
                                                         photfile.replace('.fits','_psfex_checkplot_psfsamples.png'))
                    cv_image_psfex_psf=cv2.imread(self.workdir+\
                                                  photfile.replace('.fits','_psfex_checkplot_psf.png'))
                    self.hlogger.info(VR(self.workdir+photfile.replace('.fits','_psfex_checkplot_psfsamples.png'),
                                      cv_image_psfex_psfsamples,'PSF stars used to model PSF',fmt='png'))
                    self.hlogger.info(VR(self.workdir+photfile.replace('.fits','_psfex_checkplot_psf.png'),
                                      cv_image_psfex_psf,'PSF model',fmt='png'))
            #pdb.set_trace()
            self.log2('Run Sextractor to do PSF photometry with the PSF model suggested by PSFEX...')
            outsex2=self.detect(outfile=photfile,sexconfig='use_psf.sex',psfname=psf_file,checkimg=self.checkimg)
            self.log2(outsex2)
            self.log2('Photometric catalog was saved to '+self.workdir+photfile)
            
            if self.checkimg:
                packname=photfile.replace('.fits','_checkmef.fits')
                self.pack_checkimg_sexout(indir=None,packname=packname,del_checkimg=True)
                self.log2('Save check images to '+self.workdir+packname+' which is a multi-extension FITS file.')
                if self.checkplot:
                    checkfig_name=photfile.replace('.fits','_checkplot.png')
                    self.checkplot_detection(indir=None,packname=packname,figname=checkfig_name,
                                             fig_width=self.checkfig_width)
                    self.log2('Display main check images into a plot that was saved to '+\
                              self.workdir+checkfig_name)
                    cv_image = cv2.imread(self.workdir+checkfig_name)
                    self.hlogger.info(VR(self.workdir+checkfig_name, cv_image, fmt="png"))
            #pdb.set_trace()
            
            
        if apc is True:
            apc_model_func=self.apc_pan(self.workdir+photfile, psf=psf, checkfig_width=self.checkfig_width, 
                                        logger=logger, hlogger=hlogger, order_apc=self.order_apc, verbose=verbose)
            
        dfo=self.tab2df(photfile,apc=apc)
        photo_result_file=photfile.replace('.fits','_photodf.fits')
        Table.from_pandas(dfo).filled(np.nan).write(self.workdir+photo_result_file,overwrite=True)
        self.log2('Save the final photometric catalog to '+self.workdir+photo_result_file)
        
        os.system('rm -f '+self.workdir+self.testname)
        self.log2('FINISHED!')
        self.logger.handlers.clear()
        self.hlogger.handlers.clear()
        return dfo
    
    def tab2df(self, photfile, apc=True, return_vignet=False):
        tab=Table.read(self.workdir+photfile,hdu=2)
        tem=tab.copy()
        tem.remove_columns(['MAG_APER','MAGERR_APER','VIGNET','FLUX_APER','FLUXERR_APER'])
        df=tem.to_pandas()
        if return_vignet:
            vignet=tab['VIGNET']
            vignet_cube=vignet.data
            #pdb.set_trace()
        mag_aper=tab['MAG_APER']
        naper=self.apers_pix.shape[0]
        for iaper in np.arange(naper):
            df.insert(df.columns.size,'FLUX_APER'+str(iaper),tab['FLUX_APER'][:,iaper].byteswap().newbyteorder())
            df.insert(df.columns.size,'FLUXERR_APER'+str(iaper),tab['FLUXERR_APER'][:,iaper].byteswap().newbyteorder())
            df.insert(df.columns.size,'MAG_APER'+str(iaper),tab['MAG_APER'][:,iaper].byteswap().newbyteorder())
            df.insert(df.columns.size,'MAGERR_APER'+str(iaper),tab['MAGERR_APER'][:,iaper].byteswap().newbyteorder())
            condflux=df['FLUX_APER'+str(iaper)]<0.
            condmag=df['MAG_APER'+str(iaper)]==99.
            df.loc[condflux,'FLUX_APER'+str(iaper)]=np.nan
            df.loc[condflux,'FLUXERR_APER'+str(iaper)]=np.nan
            df.loc[condmag,'MAG_APER'+str(iaper)]=np.nan
            df.loc[condmag,'MAGERR_APER'+str(iaper)]=np.nan
        if 'MAG_PSF' in df.columns:
            cond=df['MAG_PSF']>=99.
            df.loc[cond,'MAG_PSF']=np.nan
            df.loc[cond,'MAGERR_PSF']=np.nan
            df.insert(df.columns.size,'MAG_INS',df['MAG_PSF'])
            df.insert(df.columns.size,'MAGERR_INS',df['MAGERR_PSF'])    
        else:
            cond=df['MAG_AUTO']>=99.
            df.loc[cond,'MAG_AUTO']=np.nan
            df.loc[cond,'MAGERR_AUTO']=np.nan
            df.insert(df.columns.size,'MAG_INS',df['MAG_AUTO'])
            df.insert(df.columns.size,'MAGERR_INS',df['MAGERR_AUTO'])
        
        if apc is True:
            if os.path.isfile(self.workdir+photfile.replace('.fits','_apc_model.pickle')) == False:
                raise ValueError('There is no aperture correction model pickle file: '+\
                                 self.workdir+photfile.replace('.fits','_apc_model.pickle'))
            else:
                with open(self.workdir+photfile.replace('.fits','_apc_model.pickle'),'rb') as pfile:
                    apcmodel_dict=pickle.load(pfile)
                    apcmodel=apcmodel_dict['func']
                    apcerr=apcmodel_dict['err']
                    apcstatus=apcmodel_dict['status']
                if apcstatus == 1:
                    apc_value=apcmodel(df['X_IMAGE'],df['Y_IMAGE'])
                    apc_error=apcerr(df['X_IMAGE'],df['Y_IMAGE'])
                elif apcstatus == 0:
                    apc_value=apcmodel
                    apc_error=apcerr
                else:
                    raise ValueError('Unknown APC model status!')
            df.loc[:,'MAG_INS']=df['MAG_INS']+apc_value
            df.loc[:,'MAGERR_INS']=(df['MAGERR_INS']**2+apc_error**2)**0.5
        
        if ('ALPHAWIN_J2000' in df.columns) & ('DELTAWIN_J2000' in df.columns):
            raj2000=df['ALPHAWIN_J2000']
            dej2000=df['DELTAWIN_J2000']
            coo_j2000=SkyCoord(raj2000*u.degree,dej2000*u.degree,frame='fk5')
            coo_icrs=coo_j2000.transform_to('icrs')
            coo_gal=coo_j2000.transform_to('galactic')
            ra=coo_icrs.ra.value
            dec=coo_icrs.dec.value
            glon=coo_gal.l.value
            glat=coo_gal.b.value
        if 'RA' not in df.columns:
            df.insert(df.columns.size,'RA',ra)
        if 'DEC' not in df.columns:
            df.insert(df.columns.size,'DEC',dec)
        if 'GLON' not in df.columns:
            df.insert(df.columns.size,'GLON',glon)
        if 'GLAT' not in df.columns:
            df.insert(df.columns.size,'GLAT',glat)
        
        
        #pdb.set_trace()
        if return_vignet:
            dfout={'df':df,'vignet':vignet_cube}
        else:
            dfout=df.copy()
        return dfout
    
    def interpsfex(self, dotpsfpath, pos):
        '''Use PSFEx generated model to perform spatial PSF interpolation.
            Parameters
            ----------
            dotpsfpath : string
                Path to psf model file (PSFEx output).
            pos : np.ndaray
                Positions where the PSF model should be evaluated.
            Returns
            -------
            PSFs : np.ndarray
                Each row is the PSF imagette at the corresponding asked position.
            !!!from github/MorganSchmitz/PySFEx 
            !!!now only support psf model as function of x,y position
        '''
        # read PSF model and extract basis and polynomial degree and scale position
        PSF_model = fits.open(dotpsfpath)[1]
        PSF_basis = np.array(PSF_model.data)[0][0]
        try:
            deg = PSF_model.header['POLDEG1']
        except KeyError:
            # constant PSF model
            return PSF_basis[0,:,:]
    
        # scale coordinates
        x_interp, x_scale = PSF_model.header['POLZERO1'], PSF_model.header['POLSCAL1']
        y_interp, y_scale = PSF_model.header['POLZERO2'], PSF_model.header['POLSCAL2']
        xs, ys = (pos[:,0]-x_interp)/x_scale, (pos[:,1]-y_interp)/y_scale
    
        # compute polynomial coefficients
        coeffs = np.array([[x**i for i in range(deg+1)] for x in xs])
        cross_coeffs = np.array([np.concatenate([[(x**j)*(y**i) for j in range(deg-i+1)] for i in range(1, deg+1)]) for x,y in zip(xs,ys)])
        coeffs = np.hstack((coeffs,cross_coeffs))
    
        # compute interpolated PSF
        PSFs = np.array([np.sum([coeff * atom for coeff,atom in zip(coeffs_posi,PSF_basis)], axis=0) for coeffs_posi in coeffs])
        return PSFs
    
    def apc_pan(self, photfile, psf=False, checkfig_width=15., logger=None, order_apc=2, hlogger=None, verbose=True):
        self.log2('Begin to do aperture correction...')
        photfile_name=photfile.split('/')[-1]
        df_dict=self.tab2df(photfile_name,apc=False,return_vignet=True)
        df=df_dict['df']
        vignet=df_dict['vignet']
        #hd=fits.getheader(self.imgfile)
        #wcs=WCS(hd)
        
        if psf is False:
            self.log2('Select good quality sources with PSFEX...')
            outpsfex_apc=self.psfex(infile=photfile_name,checkimg=False,checkcube=False)
            self.log2(outpsfex_apc)
            os.system('mv '+self.workdir+photfile_name.replace('.fits','.psf')+' '+\
                      self.workdir+photfile_name.replace('.fits','_psfex_psf.fits'))
            os.system('mv '+self.workdir+photfile_name.replace('.fits','_psfexout.fits')+' '+\
                      self.workdir+photfile_name.replace('.fits','_psfex_psfstarsel.fits'))
            self.log2('PSF model was saved to '+self.workdir+photfile_name.replace('.fits','_psfex_psf.fits'))
            self.log2('PSF stars was saved to '+self.workdir+photfile_name.replace('.fits','_psfex_psfstarsel.fits'))
        else:
            self.log2('Select good quality sources from PSFEX output...')
        
        tab_psfstars=Table.read(self.workdir+photfile_name.replace('.fits','_psfex_psfstarsel.fits'),
                                hdu=2,format='fits')
        dfsel=pd.DataFrame({'xim_psf':tab_psfstars['X_IMAGE'],'yim_psf':tab_psfstars['Y_IMAGE'],
                            'flags':tab_psfstars['FLAGS_PSF'],'chi2':tab_psfstars['CHI2_PSF']})
        dfsel=basic.df_to_little_endian(dfsel)
        dfsel=dfsel.loc[(dfsel['flags'] == 0) & (dfsel['chi2']>0) & (dfsel['chi2']<2),['xim_psf','yim_psf']]
        dfo=dfsel.join(df)
        dfo.drop(columns=['xim_psf','yim_psf'],inplace=True)
        vigneto=vignet[dfo.index.values,:,:]
        Table.from_pandas(dfo).filled(np.nan).write(self.workdir+\
                                                    photfile_name.replace('.fits','_psfex_psfstarsel_photo.fits'),
                                                    overwrite=True)
        self.log2('Select stars that are used for aperture correction and save them to '+\
                  self.workdir+photfile_name.replace('.fits','_psfex_psfstarsel_photo.fits'))
            
            
        psfmodel_file=self.workdir+photfile_name.replace('.fits','_psfex_psf.fits')
        hdpsf=fits.getheader(psfmodel_file,1)
        fwhm_psf=hdpsf['PSF_FWHM']
        psfimg=self.interpsfex(psfmodel_file, dfo.loc[:,['X_IMAGE','Y_IMAGE']].values)
        star_psfrec=self.workdir+photfile_name.replace('.fits','_apc_psfstar_psfrec_cube.fits')
        fits.writeto(star_psfrec,psfimg,overwrite=True)
        self.log2('Reconstruct PSF images of selected stars based on the PSFEX generated PSF model '+\
                  'and save the image cube to '+star_psfrec)
        checkdir_apcstar=self.workdir+photfile_name.replace('.fits','_apc_psfstar_checkdir')
        
        
        self.log2('Loop for each selected star: construct aperture curve-of-growth (cog) and fit cog '+\
                  'with PSF profile...')
        if self.checkcog_apc:
            pathlib.Path(checkdir_apcstar).mkdir(parents=True,exist_ok=True)
            checkdir_apc=checkdir_apcstar
        else:
            checkdir_apc=None
        dfoo=self.magtot_grow(dfo,vigneto,psfimg,hdpsf,checkdir=checkdir_apc, verbose=verbose)
        self.log2('Get total flux of each selected star by extrapolate flux to aperture with infinite radius.')
        
        
        if psf is False:
            fluxin=dfoo['MAG_AUTO']
            fluxerrin=dfoo['MAGERR_AUTO']
            self.log2('Grep MAG_AUTO...')
        else:
            fluxin=dfoo['MAG_PSF']
            fluxerrin=dfoo['MAGERR_PSF']
            self.log2('Grep MAG_PSF...')
        
        dfa=pd.DataFrame()
        dfa.insert(dfa.columns.size,'xim',dfoo['X_IMAGE'])
        dfa.insert(dfa.columns.size,'yim',dfoo['Y_IMAGE'])
        dfa.insert(dfa.columns.size,'x',np.asarray(np.round(dfoo['X_IMAGE']),dtype=int))
        dfa.insert(dfa.columns.size,'y',np.asarray(np.round(dfoo['Y_IMAGE']),dtype=int))
        dfa.insert(dfa.columns.size,'mag',fluxin)
        dfa.insert(dfa.columns.size,'magerr',fluxerrin)
        dfa.insert(dfa.columns.size,'magtot',dfoo['MAG_TOT'])
        dfa.insert(dfa.columns.size,'magerrtot',dfoo['MAGERR_TOT'])
        dfa.insert(dfa.columns.size,'mag_apc',dfa['magtot']-dfa['mag'])
        dfa.insert(dfa.columns.size,'magerr_apc',(dfa['magerr']**2+dfa['magerrtot']**2)**0.5)
        dfa=dfa.loc[(dfa['mag_apc']<0.) & (dfa['mag']<99.),:]
        #pdb.set_trace()
        
        Table.from_pandas(dfa).filled(np.nan).write(self.workdir+photfile_name.replace('.fits','_apc_cat.fits'),
                                                    overwrite=True)
        if psf is True:
            self.log2('Caculate MAG_APC (aperture correction) = MAG_TOTAL - MAG_PSF...')
        else:
            self.log2('Caculate MAG_APC (aperture correction) = MAG_TOTAL - MAG_AUTO...')
        self.log2('Save aperture correction catalog into file: '+\
                  self.workdir+photfile_name.replace('.fits','_apc_cat.fits'))
        self.log2('Fit stars with aperture correction with '+\
                  str(order_apc)+' order polynomial function...')
        
        hdraw=fits.getheader(self.imgfile)
        p_init = models.Polynomial2D(degree=order_apc)
        fit_p = fitting.LevMarLSQFitter()
        #pdb.set_trace()
        if dfa.shape[0] > 5:
            with warnings.catch_warnings():
                # Ignore model linearity warning from the fitter
                warnings.simplefilter('ignore')
                pp = fit_p(p_init, dfa['xim'], dfa['yim'], dfa['mag_apc'], weights=1./dfa['magerr_apc'])
                err_params = np.sqrt(np.diag(fit_p.fit_info['param_cov']))
                pp_err = pp.copy()
                fitting._fitter_to_model_params(pp_err, err_params)
            ygrid,xgrid=np.mgrid[:hdraw['NAXIS1'],:hdraw['NAXIS2']]
            img_apc=pp(xgrid,ygrid)
            imgerr_apc=pp_err(xgrid,ygrid)
            func_apc={'func':pp,'err':pp_err,'status':1}
        else:
            self.log2('Fitting fail! Only '+str(dfa.shape[0])+' APC sources. Will use the constent median value'+\
                      ' to do aperture correction which means no aperture correction applied!')
            xlim=hdraw['NAXIS1']
            ylim=hdraw['NAXIS2']
            if dfa.shape[0] > 0:
                apc_value=np.nanmedian(dfa['mag_apc'])
            else:
                apc_value=0.
            img_apc=np.full([ylim,xlim],apc_value)
            imgerr_apc=np.full([ylim,xlim],0.)
            func_apc={'func':apc_value,'err':0.,'status':0}
            #pdb.set_trace()
        with open(self.workdir+photfile_name.replace('.fits','_apc_model.pickle'), 'wb') as handle:
            pickle.dump(func_apc, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.log2('Save fitting model into pickle file: '+\
                  self.workdir+photfile_name.replace('.fits','_apc_model.pickle'))    
            
        
        
        hd_apc=hdraw.copy()
        hderr_apc=hdraw.copy()
        hd_apc['EXTNAME']='value'
        hderr_apc['EXTNAME']='error'
        hdu_apc=fits.PrimaryHDU(data=img_apc,header=hd_apc)
        hdu_err=fits.ImageHDU(data=imgerr_apc,header=hderr_apc)
        hduapc=fits.HDUList([hdu_apc,hdu_err])
        hduapc.writeto(self.workdir+photfile_name.replace('.fits','_apc_mef.fits'),overwrite=True)
        self.log2('Save fitting image and associated uncertainty map into MEF file: '+\
                  self.workdir+photfile_name.replace('.fits','_apc_mef.fits'))
        self.log2('Aperture correction image was aligned to source image pixel-to-pixel.')
        
        if self.checkimg is True:
            if dfa.shape[0] > 0:
                self.checkplot_apc(photfile_name,dfa,hdu_apc,checkfig_width=checkfig_width)
        
        
                self.log2('Display apc image into checkplot: '+self.workdir+\
                          photfile_name.replace('.fits','_apc_checkplot.png'))
                if hlogger is not None:
                    cv_image_apc=cv2.imread(self.workdir+photfile_name.replace('.fits','_apc_checkplot.png'))
                    hlogger.info(VR(self.workdir+photfile_name.replace('.fits','_apc_checkplot.png'),
                                    cv_image_apc,'display apc checkplot',fmt='png'))
        
        
        #pdb.set_trace()
        
        return func_apc
    
    
    def magtot_grow(self, df, vignet, psfrec, hdpsf, checkdir=None, verbose=True):
        '''Calcute total flux inside aperture with infinite radius based on aperture curve-of-growth.
           Here we use psf model to fit the curve-of-growth.
           
           Parameters
            ----------
            df : pandas.dataframe
                sources with position and flux (series of different apertures).
            vignet : np.ndarray
                vignets of sources cut from original image, returned by Sextractor.
            psfrec: np.ndarray
                vignets of sources constructed with PSF model that is generated by PSFEX.
            hdpsf: fits.header
                header of psf model returned by PSFEX
            checkdir: str
                create the checkdir and plot fitting result for each source. 
            Returns
            -------
            dfout : pandas.dataframe
                appended with total flux.'''
        naper=self.apers.shape[0]
        df.reset_index(inplace=True,drop=False)
        fluxtot=np.full(df.shape[0],np.nan)
        fluxerrtot=np.full(df.shape[0],np.nan)
        chi2fit=np.full(df.shape[0],np.nan)
        fwhmpsf=hdpsf['PSF_FWHM']
        
        if verbose is True:
            for index,row in tqdm(df.iterrows(), total=df.shape[0]):
                mag=np.array([row['MAG_APER'+str(i)] for i in range(naper)])
                merr=np.array([row['MAGERR_APER'+str(i)] for i in range(naper)])
                flux=np.array([row['FLUX_APER'+str(i)] for i in range(naper)])
                eflux=np.array([row['FLUXERR_APER'+str(i)] for i in range(naper)])
            
                psf=psfrec[index,:,:]
                imgraw=vignet[index,:,:]
            
                fluxtot_now, fluxtoterr_now, chi2_now=self.fluxtot_cal(mag, merr, flux, eflux, imgraw, psf, 
                                                                       rad_tot=self.apc_rad_tot,fwhm=fwhmpsf, 
                                                                       checkdir=checkdir, starid=row['index'])
                fluxtot[index]=fluxtot_now
                fluxerrtot[index]=fluxtoterr_now
                chi2fit[index]=chi2_now
        else:
            for index,row in df.iterrows():
                mag=np.array([row['MAG_APER'+str(i)] for i in range(naper)])
                merr=np.array([row['MAGERR_APER'+str(i)] for i in range(naper)])
                flux=np.array([row['FLUX_APER'+str(i)] for i in range(naper)])
                eflux=np.array([row['FLUXERR_APER'+str(i)] for i in range(naper)])
            
                psf=psfrec[index,:,:]
                imgraw=vignet[index,:,:]
            
                fluxtot_now, fluxtoterr_now, chi2_now=self.fluxtot_cal(mag, merr, flux, eflux, imgraw, psf, 
                                                                       rad_tot=self.apc_rad_tot,fwhm=fwhmpsf, 
                                                                       checkdir=checkdir, starid=row['index'])
                fluxtot[index]=fluxtot_now
                fluxerrtot[index]=fluxtoterr_now
                chi2fit[index]=chi2_now
            #pdb.set_trace()
            
        df.insert(df.columns.size,'FLUX_TOT',fluxtot)
        df.insert(df.columns.size,'FLUXERR_TOT',fluxerrtot)
        df.insert(df.columns.size,'APC_CHI2',chi2fit)
        df.insert(df.columns.size,'MAG_TOT',-2.5*np.log10(df['FLUX_TOT']))
        df.insert(df.columns.size,'MAGERR_TOT',1.0857*df['FLUXERR_TOT']/df['FLUX_TOT'])
        
        #pdb.set_trace()
        return df
    
    def fluxtot_cal(self, mag, merr, flux, eflux, vignet, psf, fwhm=None, rad_tot=100., checkdir=None, starid=None):
        '''Calcute total flux of one star based on a series of aperture photometry.
           
           Parameters
            ----------
            mag : np.ndarray
                magnitudes of different aperture photometry.
            merr : np.ndarray
                error of magnitude.
            flux: np.ndarray
                corresponding flux.
            eflux: np.ndarray
                error of flux
            vignet: np.ndarray
                cutout image centered with source
            psf: np.ndarray
                psf image
            rad_tot: scalar
                radius of aperture used to estimate total flux. Default value is 100 pixels.
            checkdir: str
                directory of output check plots
            Returns
            -------
            fluxtot : scalar
                total flux at radius of rad_tot.
            chi2: scalar
                chi-square of fitting.'''
        from photutils.aperture import CircularAperture,aperture_photometry
        from photutils.detection import DAOStarFinder
        
        imgraw=vignet
        xlim_psf,ylim_psf=psf.shape
        xlim_raw,ylim_raw=imgraw.shape
        xrad_psf,yrad_psf=(xlim_psf-1)/2, (ylim_psf-1)/2
        xc_raw,yc_raw=(xlim_raw-1)/2, (ylim_raw-1)/2
        img=imgraw[np.int32(yc_raw-yrad_psf):np.int32(yc_raw+yrad_psf+1),
                   np.int32(xc_raw-xrad_psf):np.int32(xc_raw+xrad_psf+1)]
        xc,yc=xrad_psf,yrad_psf
        r_arr=np.arange(0.5,xrad_psf,0.5)
        fp=np.full(len(r_arr),np.nan)
        #first get source center with photutils detection routine
        if fwhm is None:
            fwhm = 5.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            daofind = DAOStarFinder(fwhm=fwhm, threshold=np.nanmin(psf))
            psf_source=daofind(psf)
        #pdb.set_trace()
        try:
            dfs=psf_source.to_pandas()
        except:
            pdb.set_trace()
        dfs.sort_values(by='peak',ascending=False,ignore_index=True,inplace=True)
        pos_psf=dfs.loc[0,['xcentroid','ycentroid']].values
        for idr,rnow in enumerate(r_arr):
            aperture = CircularAperture(pos_psf, r=rnow)
            phot_table = aperture_photometry(psf, aperture)
            fp[idr]=phot_table['aperture_sum'].data
        xa=self.apers_pix/2.
        yf=flux
        yferr=eflux
        #pdb.set_trace()
        condfit=(yf>0) & (merr<0.05)
        xfit=xa[condfit]
        yfit=yf[condfit]
        yfiterr=yferr[condfit]
        nfit=xfit.shape[0]
        flux_total=np.nan
        fluxerr_total=np.nan
        chi2_total=np.nan
        #pdb.set_trace()
        if nfit >= 5:
            try:
                cog,cog_err,pfile,chi2=self.apfit_psf(xfit,yfit,yfiterr,r_arr,fp)
                scale=cog.parameters[0]
                
                fluxtot=cog(rad_tot)
                fluxtot_err=cog_err(rad_tot)
                flux_total=fluxtot
                fluxerr_total=fluxtot_err
                chi2_total=chi2
                if checkdir is not None:
                    parafit={'xfit':xfit, 'yfit':yfit, 'yfiterr':yfiterr, 'result':cog, 
                             'result_err':cog_err, 'scale':scale}
                    #pdb.set_trace()
                    stp=self.checkplot_apfit(checkdir,starid, img, psf, parafit)   
                    #pdb.set_trace()
            except:
                pass
        else:
            pass
        #pdb.set_trace()
        return flux_total,fluxerr_total,chi2_total
    
    def checkplot_apfit(self, checkdir, starid, img, psf, parafit):
        
        if checkdir is None:
            raise ValueError('You choose to plot apc checking image, but did not offer checking directory!')
        if starid is None:
            starid=0
          
        xfit=parafit['xfit']
        yfit=parafit['yfit']
        yfiterr=parafit['yfiterr']
        cog=parafit['result']
        cog_err=parafit['result_err']
        scale=parafit['scale']
        
        interval=AsymmetricPercentileInterval(1.,99.)
        stretch=AsinhStretch()
        cmap='RdBu_r'#'Greys'
        
        
        plt.close('all')
        showfile=checkdir+'/star_'+str(np.int32(starid))+'.png'
        fig,ax=plt.subplots(2,2,figsize=(8,8))
        fig.subplots_adjust(left=0.1,right=0.9,bottom=0.1,top=0.9,wspace=0.1,hspace=0.2)
        img[img<-1e10]=0.
        
        ax[0][0].imshow(img,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img,interval=interval,stretch=stretch))
        
        ax[0][0].set_title('image')
        ax[0][1].imshow(psf,origin='lower',cmap=cmap,
                        norm=ImageNormalize(psf,interval=interval,stretch=stretch))
        ax[0][1].set_title('PSF') 
        ax[1][0].errorbar(xfit,yfit,yerr=yfiterr,fmt='o')
        ax[1][0].plot(xfit,cog(xfit),color='red')
        ax[1][0].plot(xfit,cog(xfit)+cog_err(xfit),color='blue',linestyle='dashed')
        ax[1][0].plot(xfit,cog(xfit)-cog_err(xfit),color='blue',linestyle='dashed')
        ax[1][0].set_xlabel('Aperture radius (pixels)')
        ax[1][0].set_ylabel('Flux (counts)')
        ax[1][0].set_title('curve-of-growth fit')
        ax[1][1].imshow(img-psf*scale,origin='lower',cmap=cmap,
                        norm=ImageNormalize(img,interval=interval,stretch=stretch))
        ax[1][1].set_title('residuals')
        #pdb.set_trace()
        fig.suptitle('Star ID: '+str(np.int32(starid)))
        #fits.writeto(checkdir+'/test.fits',img-psf*scale,overwrite=True)
        
        fig.savefig(showfile,bbox_inches='tight')
         
        plt.cla()
        fig.clf()
        plt.close(fig)
        
        return 1
    
    def apfit_psf(self, xfit, yfit, yfiterr, xpsf, ypsf):
        from scipy.interpolate import interp1d
        #pdb.set_trace()
        fin=interp1d(xpsf,ypsf,kind='zero',fill_value='extrapolate')
        
        pfile=self.workdir+'testinterfin.pickle'
        with open(pfile, 'wb') as handle:
            pickle.dump(fin, handle, protocol=pickle.HIGHEST_PROTOCOL)
        @custom_model
        def psf_profile(x,a=1.):
            with open(pfile,'rb') as handle:
                fin=pickle.load(handle)
            return fin(x)*a
        
        scale_ini=yfit[0]/fin(xfit[0])
        psfm=psf_profile(scale_ini)
        fitter = fitting.LevMarLSQFitter(calc_uncertainties=True)
        yprime=np.diff(yfit)/np.diff(xfit)
        sp=np.argwhere(yprime<=0)
        spp=sp[:,0]
        xfituse=xfit[:spp[0]+1]
        yfituse=yfit[:spp[0]+1]
        yfiterruse=yfiterr[:spp[0]+1]
        grow = fitter(psfm, xfituse, yfituse)#, weights = 1.0/yfiterruse**2)
        err_params = np.sqrt(np.diag(fitter.fit_info['param_cov']))
        grow_err = grow.copy()
        fitting._fitter_to_model_params(grow_err, err_params)
        chi2=np.nansum( ((yfituse-grow(xfituse))/yfiterruse)**2. )/(yfituse.shape[0]-2)
        #pdb.set_trace()    
        return grow,grow_err,pfile,chi2
    
    
    def apc(self, photfile, psf=False, checkfig_width=15., logger=None, order_apc=2, hlogger=None):
        '''-----------------------------------------------------
        This routine is not corrected and out of use!!!
        --------------------------------------------------------'''
        
        self.log2('Begin to do aperture correction...')
        self.log2('Here use PSF model to estimate the aperture correction...')
        tab=Table.read(photfile,hdu=2)
        photfile_name=photfile.split('/')[-1]
        if psf is False:
            self.log2('Previous photometry is aperture photometry, thus firstly construct a PSF model with PSFex...')
            self.log2('Run PSFEX on result photometric result: '+photfile)
            outpsfex_apc=self.psfex(infile=photfile_name,checkimg=True,checkcube=False)
            #pdb.set_trace()
            self.log2(outpsfex_apc)
            os.system('mv '+self.workdir+photfile_name.replace('.fits','.psf')+' '+\
                      self.workdir+photfile_name.replace('.fits','_psfex_psf.fits'))
        
            self.checkplot_psfex(psfexinfile=photfile_name,
                                 packname=photfile_name.replace('.fits','_psfex_checkmef.fits'),
                                 figname=photfile_name.replace('.fits','_psfex_checkplot.png'),
                                 fig_width=checkfig_width)
            
            
            self.log2('PSF model was saved to '+self.workdir+photfile_name.replace('.fits','_psfex_psf.fits'))
            self.log2('Save PSFEX check images to a multi-extension FITS file: '+\
                      self.workdir+photfile_name.replace('.fits','_psfex_checkmef.fits'))
            self.log2('Display PSFEX check images to two plots: '+self.workdir+\
                      photfile_name.replace('.fits','_psfex_checkplot_*.png'))
            if hlogger is not None:
                cv_image_apc_psfex_samples=cv2.imread(self.workdir+\
                                                      photfile_name.replace('.fits','_psfex_checkplot_psfsamples.png'))
                cv_image_apc_psfex_psf=cv2.imread(self.workdir+\
                                                  photfile_name.replace('.fits','_psfex_checkplot_psf.png'))
                hlogger.info(VR(self.workdir+photfile_name.replace('.fits','_psfex_checkplot_psfsamples.png'),
                                cv_image_apc_psfex_samples,'PSF stars used to model PSF'))
                hlogger.info(VR(self.workdir+photfile_name.replace('.fits','_psfex_checkplot_psf.png'),
                                cv_image_apc_psfex_psf,'PSF model'))
                
        
        self.log2('Extract snapshots from MEF check image...')
        hdpsf=fits.getheader(self.workdir+photfile_name.replace('.fits','_psfex_psf.fits'),1)
        img,hd=fits.getdata(self.workdir+photfile_name.replace('.fits','_psfex_checkmef.fits'),4,header=True)
        xs_psf=hdpsf['PSFAXIS1']
        ys_psf=hdpsf['PSFAXIS2']
        fits.writeto(self.workdir+'snap.fits',img,hd,overwrite=True)
        xlim=hd['NAXIS1']
        ylim=hd['NAXIS2']
        nx_psf=xlim/xs_psf
        ny_psf=ylim/ys_psf
        self.log2('Snapshots shows '+str(nx_psf)+'x'+str(ny_psf)+' PSF model grid.')
        self.log2('Each PSF is a '+str(xs_psf)+'x'+str(ys_psf)+' pix image.')
        
        psfname=None
        self.log2('Run Sextractor on snapshots...')
        
        sexconfig='use_withoutpsf.sex'
        outsex=self.detect(indir=self.workdir, infile='snap.fits', outfile='detection.fits', 
                           outdir=None, sexconfig=sexconfig,psfname=psfname, checkimg=False, backtype='MANUAL')
        self.log2(outsex)
        os.system('rm -f '+self.workdir+'snap.fits')
        tab=Table.read(self.workdir+'detection.fits',hdu=2)
        os.system('rm -f '+self.workdir+'detection.fits')
        if psf is False:
            fluxin=tab['MAG_AUTO']
            fluxerrin=tab['MAGERR_AUTO']
            self.log2('Grep MAG_AUTO...')
        else:
            fluxin=tab['MAG_APER'][:,6]
            fluxerrin=tab['MAGERR_APER'][:,6]
            self.log2('Grep MAG_APER(7)...')
        df=pd.DataFrame()
        df.insert(df.columns.size,'x',np.asarray(np.round(tab['X_IMAGE']-1),dtype=int))
        df.insert(df.columns.size,'y',np.asarray(np.round(tab['Y_IMAGE']-1),dtype=int))
        df.insert(df.columns.size,'mag',fluxin)
        df.insert(df.columns.size,'magerr',fluxerrin)
        magtot=np.full(df.shape[0],np.nan)
        for index,row in df.iterrows():
            xim=row['x']
            yim=row['y']
            xrad=np.floor(xs_psf/2.)
            yrad=np.floor(ys_psf/2.)
            xmin=xim-xrad
            xmax=xim+xrad
            ymin=yim-yrad
            ymax=yim+yrad
            xmin=np.where(xmin<0,0,xmin)
            xmax=np.where(xmax>xlim-1,xlim-1,xmax)
            ymin=np.where(ymin<0,0,ymin)
            ymax=np.where(ymax>ylim-1,ylim-1,ymax)
            subimg=img[np.int32(ymin):np.int32(ymax),np.int32(xmin):np.int32(xmax)]
            fluxnow=np.nansum(subimg)
            magtot[index]=-2.5*np.log10(fluxnow)
        self.log2('Calculate MAG_TOTAL by summing pixel values of '+\
                  str(xs_psf)+'x'+str(ys_psf)+' PSF model image...')
        
        df.insert(df.columns.size,'magtot',magtot)
        mag_apc=magtot-df['mag']
        mag_apc=np.where(mag_apc>0,0,mag_apc)
        df.insert(df.columns.size,'mag_apc',mag_apc)
        hdraw=fits.getheader(self.imgfile,0)
        scalex=hdraw['NAXIS1']/float(xlim)
        scaley=hdraw['NAXIS2']/float(ylim)
        df.insert(df.columns.size,'xim',df['x']*scalex)
        df.insert(df.columns.size,'yim',df['y']*scaley)
        Table.from_pandas(df).filled(np.nan).write(self.workdir+photfile_name.replace('.fits','_apc_cat.fits'),
                                                   overwrite=True)
        if psf is True:
            self.log2('Caculate MAG_APC (aperture correction) = MAG_TOTAL - MAG_APER...')
        else:
            self.log2('Caculate MAG_APC (aperture correction) = MAG_TOTAL - MAG_AUTO...')
        self.log2('Save aperture correction catalog into file: '+\
                  self.workdir+photfile_name.replace('.fits','_apc_cat.fits'))
        self.log2('Fit '+str(nx_psf)+'x'+str(ny_psf)+' aperture correction grid with '+\
                  str(order_apc)+' order polynomial function...')
        
        
        p_init = models.Polynomial2D(degree=order_apc)
        fit_p = fitting.LevMarLSQFitter()
        with warnings.catch_warnings():
            # Ignore model linearity warning from the fitter
            warnings.simplefilter('ignore')
            p = fit_p(p_init, df['xim'], df['yim'], df['mag_apc'])
        ygrid,xgrid=np.mgrid[:hdraw['NAXIS1'],:hdraw['NAXIS2']]
        img_apc=p(xgrid,ygrid)
        with open(self.workdir+photfile_name.replace('.fits','_apc_model.pickle'), 'wb') as handle:
            pickle.dump(p, handle, protocol=pickle.HIGHEST_PROTOCOL)
        fits.writeto(self.workdir+photfile_name.replace('.fits','_apc_img.fits'),img_apc,hdraw,overwrite=True)
        hdu_apc=fits.PrimaryHDU(data=img_apc,header=hdraw)
        self.checkplot_apc(photfile_name,df,hdu_apc,checkfig_width=checkfig_width)
        self.log2('Save fitting model into pickle file: '+\
                  self.workdir+photfile_name.replace('.fits','_apc_model.pickle'))
        self.log2('Save fitting image into file: '+self.workdir+photfile_name.replace('.fits','_apc_img.fits'))
        self.log2('Aperture correction image is aligned to source image pixel-to-pixel.')
        self.log2('Display apc image into checkplot: '+self.workdir+\
                  photfile_name.replace('.fits','_apc_checkplot.png'))
        if hlogger is not None:
            cv_image_apc=cv2.imread(self.workdir+photfile_name.replace('.fits','_apc_checkplot.png'))
            hlogger.info(VR(self.workdir+photfile_name.replace('.fits','_apc_checkplot.png'),
                            cv_image_apc,'display apc checkplot',fmt='png'))
        #pdb.set_trace()
        #os.system('rm -f '+self.workdir+'detection.fits')
        
        
        return p
    
    def checkplot_fitimg(self,df,hdu,checkfig_width=15.,outfile='test.png',outdir='./',
                         value_name='MAG_APC',fit_model=None):
        img=hdu.data
        hd=hdu.header
        xlim=hd['NAXIS1']
        ylim=hd['NAXIS2']
        xsize=checkfig_width
        if fit_model is None:
            ratio=ylim/np.float32(xlim)/2.
            ncol=2
        else:
            ratio=ylim/np.float32(xlim)/3.
            ncol=3
        ysize=xsize*ratio
        fig,ax=plt.subplots(1,ncol,figsize=(xsize,ysize))
        fig.subplots_adjust(top=0.95,bottom=0.1,left=0.1,right=0.9,wspace=0.3,hspace=0.1)
        colormap='gist_rainbow_r'
        sns.scatterplot(x='xim',y='yim',data=df,hue='value',ax=ax[0],palette=colormap,s=100)
        normdist = plt.Normalize(df['value'].min(), df['value'].max())
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=normdist)
        sm.set_array([])
        ax[0].get_legend().remove()
        divider = make_axes_locatable(ax[0])
        cax = divider.append_axes("right", size="5%", pad=0.1)
        ax[0].set_ylabel('Y_IMAGE')
        ax[0].set_xlabel('X_IMAGE')
        cbar=ax[0].figure.colorbar(sm, cax=cax)
        #cbar.set_label('test',rotation=270)
        ax[0].set_aspect('equal')
        
        normdist = plt.Normalize(np.nanmin(img), np.nanmax(img))
        ax[1].imshow(img,origin='lower', cmap=colormap,norm=normdist)
        divider2 = make_axes_locatable(ax[1])
        cax2 = divider2.append_axes("right", size="5%", pad=0.1)
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=normdist)
        cbar2=ax[1].figure.colorbar(sm, cax=cax2)
        cbar2.set_label(value_name,rotation=90, labelpad=2)
        #ax[1].set_ylabel('Y_IMAGE')
        ax[1].set_xlabel('X_IMAGE')
        ax[1].set_aspect('equal')
        
        if fit_model is not None:
            res=df['value']-fit_model(df['xim'],df['yim'])
            df['res']=res
            sns.scatterplot(x='xim',y='yim',data=df,hue='res',ax=ax[2],palette=colormap,s=100)
            normdist = plt.Normalize(df['res'].min(), df['res'].max())
            sm = plt.cm.ScalarMappable(cmap=colormap, norm=normdist)
            sm.set_array([])
            ax[2].get_legend().remove()
            divider = make_axes_locatable(ax[2])
            cax = divider.append_axes("right", size="5%", pad=0.1)
            ax[2].set_ylabel(' ')
            ax[2].set_xlabel('X_IMAGE')
            cbar=ax[2].figure.colorbar(sm, cax=cax)
            cbar.set_label('residual',rotation=90,labelpad=2)
            ax[2].set_aspect('equal')
        fig.savefig(outdir+outfile,bbox_inches='tight')
        plt.close(fig)
        return 1
    
    
    def checkplot_apc(self, photfile, df, hdu_apc, checkfig_width=15., fit_model=None):
        outdir=self.workdir
        outfile=photfile.replace('.fits','_apc_checkplot.png')
        dfsel=df.copy()
        dfsel.insert(dfsel.columns.size,'value',df['mag_apc'])
        self.checkplot_fitimg(dfsel,hdu_apc,checkfig_width=checkfig_width,
                              outfile=outfile,outdir=outdir,value_name='MAG_APC')
        
        
        #pdb.set_trace()
        return 1
    
    def check_phot(self, dfphotin, dfref=None, apc=None, flag_ref_threshold=128, 
                   if_cali_outliers_detection_method=0,zoom_width=60,imgraw_interval=[0.1,99.],
                   imgzoom_interval=[0.1,97],nsig_dbscan=1.5,minfrac_dbscan=0.5,nsig_sigmaclip=3,
                   zmag_order=0, keep_html_only=False):
        '''Plot some basic photometric information in a html file.
           
           Parameters:
           ------------
            dfphotin : pandas.dataframe
                   photometric result returned by phot.
           
            dfref : pandas.dataframe
                   reference catalog that must include columns of [ra,dec,mag,merr,flag]
                   default is None which means we will not compare photometric result with reference catalog.
            flag_ref_threshold: np.int
                   threshold to select high-quality sources(flag<threshold) from reference catalog.
            if_cali_outliers_detection_method : np.int
                   if dfref is not None, we will calibrate dfphotin to dfref photometric system by simply
                   fitting a zero magnitude (zmag). We will exclude some outliers before fitting. 0 means
                   excluding with sigma-clipping technique; 1 means excluding with DBSCAN.
            zoom_width : np.float
                   The width of zoom-in plot. Unit is arcseconds.
            imgraw_interval : list
                   Scale range that is used to display raw image.
            imgzoom_interval : list
                   Scale range that is used to display zoom-in image.
            nsig_dbscan : np.float
                   epsilon value used for DBSCAN if if_cali_outliers_detection_method=1.
            min_frac_dbscan : np.float
                   min_samples used for DBSCAN will be estimated by sample size*min_frac_dbscan.
            nsig_sigmaclip : np.float
                   sigma used for sigma-clipping if if_cali_outliers_detection_method=0.
            zmag_order : np.int
                   We use a 2D polynomial function to fit good sources and obtain zmag. zmag_order give the
                   order of polynomial function. default 0 means a constant independant of image positions.
            keep_html_only : boolean
                   if keep_html_only is True, we shall delete all checkplots and only keep the output html.
                   '''
        
        dfphot=dfphotin.copy()
        if 'MAG_PSF' in dfphot.columns:
            psf=True
        else:
            psf=False
        checkfig_width=self.checkfig_width 
        kho=keep_html_only
        
        condphot=(dfphot['MAG_INS'].isnull()==False) & \
                 (dfphot['MAGERR_INS'].isnull()==False) & (dfphot['MAGERR_INS']<1.) & (dfphot['MAG_INS']>-99.) & \
                 (dfphot['MAG_INS']<99.)
        dfphot=dfphot.loc[condphot,:]
        dfphot.reset_index(drop=True,inplace=True)
        nsex=dfphot.shape[0]
        condhq=dfphot['FLAGS']<4
        dfphot.insert(dfphot.columns.size,'hq',0)
        dfphot.loc[condhq,'hq']=1
        nsex_hq=dfphot.loc[condhq,:].shape[0]
        #pdb.set_trace()
        if dfref is not None:
            if ('ra' not in dfref.columns) | ('dec' not in dfref.columns) |\
               ('mag' not in dfref.columns) | ('merr' not in dfref.columns) |\
               ('flag' not in dfref.columns):
                raise ValueError('pandas.DataFrame dfref must have columns ["ra","dec","mag","merr","flag"]')
            condref=(dfref['mag'].isnull()==False) & (dfref['merr'].isnull()==False) & \
                    (dfref['mag']>0) & (dfref['merr']>0) & \
                    (dfref['mag']<99) & (dfref['merr']<1)
            dfref=dfref.loc[condref,:]
            dfref.reset_index(drop=True,inplace=True)
            nref=dfref.shape[0]
            condrefhq=dfref['flag']<flag_ref_threshold
            dfref.insert(dfref.columns.size,'hq',0)
            dfref.loc[condrefhq,'hq']=1
            nref_hq=dfref.loc[condrefhq,:].shape[0]
        
        #pdb.set_trace()  
        
        if apc is None:
            raise ValueError('You must choose apc=True or False!')
        
        photfile=self.imgname.replace('.fits','_photsex_PSF'+str(psf)+'_APC'+str(apc)+'.fits')
        clogger = logging.getLogger('PhotoSex-checkphoto')
        clogger.setLevel(logging.INFO)
        cfh=logging.FileHandler(self.workdir+photfile.replace('.fits','_checkphoto.html'),'w',encoding='utf-8')
        cfh.setFormatter(self.logfmt)
        clogger.addHandler(cfh)
        
        clogger.info(VR('Check photometric result...'))
        if dfref is None:
            clogger.info(VR('No reference catalog offered.'))
        else:
            clogger.info(VR('Reference catalog offered.'))
        clogger.info(VR('BEGIN...'))
        img,hd=fits.getdata(self.imgfile,0,header=True)
        wcs=WCS(hd)
        showfile1=self.workdir+photfile.replace('.fits','_checkphoto_imgcat.png')
        self.check_phot_imgshow(img, hd, showfile=showfile1, checkfig_width=checkfig_width,
                                dfref=dfref, dfphot=dfphot,zoom_width=zoom_width, 
                                imgraw_interval=imgraw_interval,imgzoom_interval=imgzoom_interval)
        cv_image_showfile1=cv2.imread(showfile1)
        clogger.info(VR('Display image and catalog in '+showfile1, cv_image_showfile1, fmt='png'))
        if kho:
            os.system('rm -f '+showfile1)
        clogger.info(VR('Number of Sextractor detections: '+str(nsex)+\
                        ', in which '+str(nsex_hq)+' are high-quality (hq) sources (FLAGS<4).'))
        if dfref is not None:
            clogger.info(VR('Number of reference sources: '+str(nref)+\
                            ', in which '+str(nref_hq)+\
                            ' are high-quality (hq) sources (flag<'+str(flag_ref_threshold)+').'))
            
        
        if dfref is not None:
            clogger.info(VR('Do a simple calibration with reference catalog...'))
            clogger.info(VR('Crossmatch Sextractor detection with the reference catalog...'))
            dfx=basic.crossmatch_2dfs(dfphot,dfref,
                                      coo_cols=['ALPHAWIN_J2000','DELTAWIN_J2000','ra','dec'],
                                      frame='icrs', maxdist=1)
            dfxx=dfx.loc[dfx['FLAGS']==0,:]
            dfxx.reset_index(drop=True,inplace=True)
            dfxx.insert(dfxx.columns.size,'zmag',dfxx['mag']-dfxx['MAG_INS'])
            dfxx.insert(dfxx.columns.size,'zmag_err',((dfxx['merr'])**2+(dfxx['MAGERR_INS'])**2)**0.5)
            clogger.info(VR('Calculate zmag = MAG(ref) - MAG_INS'))
            if if_cali_outliers_detection_method == 1:
                clogger.info(VR('Exclude outliers with DBSCAN...'))
                #pdb.set_trace()
                dfxu=basic.outliers_detection_dbscan(dfxx,cols=['FWHM_IMAGE','zmag'],
                                                     nsig=nsig_dbscan,min_cluster_size_fraction=minfrac_dbscan)
            
            
            if if_cali_outliers_detection_method == 0:
                clogger.info(VR('Exclude outliers with sigma-clipping...'))
                sigma=nsig_sigmaclip
                temfwhm,fwhm_min,fwhm_max=sigma_clip(dfxx['FWHM_IMAGE'].values,sigma=sigma,maxiters=50,
                                               masked=False,return_bounds=True,cenfunc='median')
                temzmag,zmag_min,zmag_max=sigma_clip(dfxx.loc[(dfxx['FWHM_IMAGE']>fwhm_min)&(dfxx['FWHM_IMAGE']<fwhm_max),
                                                              'zmag'].values,
                                                     sigma=sigma,maxiters=50,
                                                     masked=False,return_bounds=True,cenfunc='median')
                dfxu=dfxx.copy()
                dfxu.insert(dfxu.columns.size,'Outlier','Y')
                cond_fwhm=(dfxu['FWHM_IMAGE']>fwhm_min) & (dfxu['FWHM_IMAGE']<fwhm_max)
                cond_zmag=(dfxu['zmag']>zmag_min) & (dfxu['zmag']<zmag_max)
                dfxu.loc[cond_fwhm&cond_zmag,'Outlier']='N'
                #pdb.set_trace()
            
            showfileo=self.workdir+photfile.replace('.fits','_checkphoto_simcal_outliers.png')
            dftem=dfxu.loc[dfxu['Outlier']=='N',['FWHM_IMAGE','zmag']]
            pmra_len=np.percentile(dftem['FWHM_IMAGE'],95)-np.percentile(dftem['FWHM_IMAGE'],5)
            pmdec_len=np.percentile(dftem['zmag'],95)-np.percentile(dftem['zmag'],5)
            noff=3.
            pmra_range=np.array([0.,dftem['FWHM_IMAGE'].median()+pmra_len*noff])
            pmdec_range=np.array([dftem['zmag'].median()-pmdec_len*noff,dftem['zmag'].median()+pmdec_len*noff])
            #pdb.set_trace()
            g1=sns.JointGrid(x='FWHM_IMAGE', y='zmag', data=dfxu, space=0.2,ratio=3,marginal_ticks=True,
                             xlim=pmra_range,ylim=pmdec_range,height=5)
            sns.scatterplot(x='FWHM_IMAGE',y='zmag',data=dfxu,hue='Outlier',ax=g1.ax_joint,s=10)
            xbin_width=knuth_bin_width(dfxu.loc[dfxu['FWHM_IMAGE'].isnull()==False,'FWHM_IMAGE'])
            ybin_width=knuth_bin_width(dfxu.loc[dfxu['zmag'].isnull()==False,'zmag'])
    
            sns.kdeplot(x='FWHM_IMAGE',data=dfxu,ax=g1.ax_marg_x,hue='Outlier',legend=False)
            sns.kdeplot(y='zmag',data=dfxu,ax=g1.ax_marg_y,hue='Outlier',legend=False)
    
            g1.savefig(showfileo,bbox_inches='tight')
            cv_image_showfileo=cv2.imread(showfileo)
            clogger.info(VR('Display outlier excluding check file: '+showfileo, cv_image_showfileo, fmt='png'))
            if kho:
                os.system('rm -f '+showfileo)
            
            dfuse=dfxu.loc[dfxu['Outlier']=='N',:]
            xim,yim=wcs.wcs_world2pix(dfuse['ALPHAWIN_J2000'],dfuse['DELTAWIN_J2000'],0)
            dfuse.insert(dfuse.columns.size,'xim',xim)
            dfuse.insert(dfuse.columns.size,'yim',yim)
            
            clogger.info(VR('Fit zmag of sources with a '+str(zmag_order)+'-order 2D polynomial function...'))
            p_init = models.Polynomial2D(degree=zmag_order)
            fit_p = fitting.LevMarLSQFitter()
            with warnings.catch_warnings():
                # Ignore model linearity warning from the fitter
                warnings.simplefilter('ignore')
                pp = fit_p(p_init, dfuse['xim'], dfuse['yim'], dfuse['zmag'], weights=1./(dfuse['zmag_err']))
            ygrid,xgrid=np.mgrid[:hd['NAXIS1'],:hd['NAXIS2']]
            img_zmag=pp(xgrid,ygrid)
            #pdb.set_trace()
            if kho is False:
                clogger.info(VR('Save fitting model in pickle file: '+\
                                self.workdir+photfile.replace('.fits','_checkphoto_simcal_zmag_model.pickle')))
                with open(self.workdir+photfile.replace('.fits','_checkphoto_simcal_zmag_model.pickle'), 'wb') as handle:
                    pickle.dump(pp, handle, protocol=pickle.HIGHEST_PROTOCOL)
                fits.writeto(self.workdir+photfile.replace('.fits','_checkphoto_simcal_zmag_img.fits'),
                             img_zmag,hd,overwrite=True)
            hdu_zmag=fits.PrimaryHDU(data=img_zmag,header=hd)
            dfp=pd.DataFrame()
            dfp.insert(dfp.columns.size,'xim',dfuse['xim'])
            dfp.insert(dfp.columns.size,'yim',dfuse['yim'])
            dfp.insert(dfp.columns.size,'value',dfuse['zmag'])
            zmag_checkfile=photfile.replace('.fits','_checkphoto_simcal_zmag_img_checkplot.png')
            self.checkplot_fitimg(dfp,hdu_zmag,checkfig_width=checkfig_width,
                                  outfile=zmag_checkfile,outdir=self.workdir,
                                  value_name='zmag',fit_model=pp)
            cv_image_zmag=cv2.imread(self.workdir+zmag_checkfile)
            clogger.info(VR('Display zmag image file: '+self.workdir+zmag_checkfile, 
                            cv_image_zmag, fmt='png'))
            if kho:
                os.system('rm -f '+self.workdir+zmag_checkfile)
            zmago=pp(dfphot['X_IMAGE'],dfphot['Y_IMAGE'])
            dfphot.insert(dfphot.columns.size,'MAG_CAL',dfphot['MAG_INS']+zmago)
            clogger.info(VR('Get MAG_CAL = MAG_INS + zmag'))
        else:
            dfphot.insert(dfphot.columns.size,'MAG_CAL',dfphot['MAG_INS'])
        
        
        clogger.info(VR('Now plot several checkplots...'))
        ########################
        ######magnitude histogram#####
        ########################
        showfile2=self.workdir+photfile.replace('.fits','_checkphoto_maghist.png')
        self.check_phot_maghist(dfphot, dfref=dfref, flag_ref_threshold=flag_ref_threshold, showfile=showfile2)
        cv_image_checkphoto_magdist=cv2.imread(showfile2)
        clogger.info(VR('Display source magnitude distribution in file: '+showfile2, 
                        cv_image_checkphoto_magdist,fmt='png'))
        if kho:
            os.system('rm -f '+showfile2)
        ########################
        ######mag-err plot######
        ########################
        
        showfile3=self.workdir+photfile.replace('.fits','_checkphoto_magerror.png')
        nthres_histplot=10000
        self.check_phot_magerr(dfphot, dfref=dfref, nthres_histplot=nthres_histplot, showfile=showfile3)
        cv_image_checkphoto_magerr=cv2.imread(showfile3)
        clogger.info(VR('Display source magnitude-error relation in file: '+showfile3, 
                        cv_image_checkphoto_magerr,fmt='png'))
        if kho:
            os.system('rm -f '+showfile3)
        ######################
        #####compare with ref
        ######################
        if dfref is not None:
            showfile4=self.workdir+photfile.replace('.fits','_checkphoto_magdiff.png')
            self.check_phot_magdiff(dfphot, dfref=dfref, photerr=0.1, flag_ref_threshold=flag_ref_threshold, 
                                    nthres_histplot=nthres_histplot, ms=5, showfile=showfile4)
            #Table.from_pandas(dfx).filled(np.nan).write(self.workdir+'testcat.fits',overwrite=True)
            cv_image_checkphoto_magdiff=cv2.imread(showfile4)
            clogger.info(VR('Compare Sextractor photometry with reference catalog (only hq sources): '+showfile4, 
                            cv_image_checkphoto_magdiff,fmt='png'))
            if kho:
                os.system('rm -f '+showfile4)
        clogger.info(VR('FINISHED.'))
        clogger.handlers.clear()
        return dfphot
    
    def check_phot_imgshow(self, img, hd, showfile='check_phot_imgshow.png', checkfig_width=12., 
                           dfref=None, dfphot=None,
                           zoom_width=60, imgraw_interval=[0.1,99.], imgzoom_interval=[0.1,97]):
        wcs=WCS(hd)
        xlim=hd['NAXIS1']
        ylim=hd['NAXIS2']
        xc=xlim/2.
        yc=ylim/2.
        rac,decc=wcs.wcs_pix2world(xc,yc,0)
        xsize=checkfig_width
        if dfref is None:
            ratio=0.33
            nrow=1
            ncol=3
        else:
            ratio=1
            nrow=2
            ncol=2
        ysize=xsize*ratio*(np.float32(ylim)/xlim)
        norm=ImageNormalize(img,interval=AsymmetricPercentileInterval(imgraw_interval[0],imgraw_interval[1]),
                                                                                      stretch=AsinhStretch())
        cmap='Greys'#'RdBu_r'
        fig = plt.figure(figsize=(xsize,ysize))
        fig.subplots_adjust(left=0.1, right=0.9, bottom=0.1, top=0.9,wspace=0.1,hspace=0.2)
        ax1 = fig.add_subplot(nrow, ncol, 1, projection=wcs)
        im1=ax1.imshow(img, origin='lower', cmap=cmap, norm=norm)
        ax1.coords['ra'].set_axislabel('RA')
        ax1.coords['dec'].set_axislabel('Dec')
        ax1.coords['ra'].set_major_formatter('hh:mm:ss')
        ax1.coords['dec'].set_major_formatter('dd:mm')
        ax1.set_title('Image')
        
        ms=50
        ax2 = fig.add_subplot(nrow, ncol, 2, projection=wcs)
        im2=ax2.imshow(img, origin='lower', cmap=cmap, norm=norm)
        ax2.coords['ra'].set_axislabel('RA')
        ax2.coords['dec'].set_axislabel(' ')
        ax2.coords['ra'].set_major_formatter('hh:mm:ss')
        ax2.coords['dec'].set_major_formatter('dd:mm')
        ax2.set_title('Image with Sextractor detections')
        xim,yim=wcs.wcs_world2pix(dfphot['ALPHAWIN_J2000'],dfphot['DELTAWIN_J2000'],0)
        ax2.scatter(xim,yim,marker='o',s=ms,facecolor='none',edgecolor='red',linewidth=1)
        
        if dfref is not None:
            ax3 = fig.add_subplot(nrow, ncol, 3, projection=wcs)
            im3=ax3.imshow(img, origin='lower', cmap=cmap, norm=norm)
            ax3.coords['ra'].set_axislabel('RA')
            ax3.coords['dec'].set_axislabel('Dec')
            ax3.coords['ra'].set_major_formatter('hh:mm:ss')
            ax3.coords['dec'].set_major_formatter('dd:mm')
            ax3.set_title('Image with reference catalog')
            ximref,yimref=wcs.wcs_world2pix(dfref['ra'],dfref['dec'],1)
            ax3.scatter(ximref,yimref,marker='o',s=ms,facecolor='none',edgecolor='green',linewidth=1)
            zoomnum=4
        else:
            zoomnum=3
        
        center=SkyCoord(rac*u.degree,decc*u.degree,frame='icrs')
        size=(zoom_width,zoom_width)*u.arcsec
        subimg=Cutout2D(img,center,size,wcs=wcs)
        ax4 = fig.add_subplot(nrow, ncol, zoomnum, projection=subimg.wcs)
        subnorm=ImageNormalize(subimg.data,interval=AsymmetricPercentileInterval(imgzoom_interval[0],
                                                                                 imgzoom_interval[1]),
                               stretch=AsinhStretch())
        im4=ax4.imshow(subimg.data, origin='lower', cmap=cmap, norm=subnorm)
        ax4.coords['ra'].set_axislabel('RA')
        ax4.coords['dec'].set_axislabel(' ')
        ax4.coords['ra'].set_major_formatter('hh:mm:ss')
        ax4.coords['dec'].set_major_formatter('dd:mm:ss')
        ax4.set_title('Zoom-in image')
        xlim_sub,ylim_sub=subimg.data.shape
        ximp,yimp=subimg.wcs.wcs_world2pix(dfphot['ALPHAWIN_J2000'],dfphot['DELTAWIN_J2000'],0)
        ax4.scatter(ximp,yimp,marker='o',s=ms*2,facecolor='none',edgecolor='red',linewidth=2)
        if dfref is not None:
            ximr,yimr=subimg.wcs.wcs_world2pix(dfref['ra'],dfref['dec'],1)
            ax4.scatter(ximr,yimr,marker='+',s=ms*2,facecolor='green',edgecolor='green',linewidth=2)
        ax4.set_xlim(0,xlim_sub)
        ax4.set_ylim(0,ylim_sub)
        
        fig.savefig(showfile,bbox_inches='tight')
        plt.close(fig)
        return 1 
    
    def check_phot_maghist(self, dfphot, dfref=None, flag_ref_threshold=128, showfile='check_phot_maghist.png'):
        fig,ax=plt.subplots(2,1,figsize=(8,8))
        fig.subplots_adjust(bottom=0.1,top=0.9,left=0.1,right=0.9,wspace=0.1,hspace=0.1)
        sns.histplot(dfphot['MAG_CAL'],ax=ax[0],color='red',element='step',fill=False,label='Sextractor detections')
        if dfref is not None:
            sns.histplot(dfref['mag'],ax=ax[0],color='green',element='step',fill=False,label='reference catalog')
        ax[0].legend()
        ax[0].set_xlabel(' ')
        
        xp_range=ax[0].get_xlim()
        yp_range=ax[0].get_ylim()
        sns.histplot(dfphot.loc[dfphot['FLAGS']<4,'MAG_CAL'],ax=ax[1],
                     color='red',element='step',fill=False,label='Sextractor hq (FLAGS<4)')
        if dfref is not None:
            sns.histplot(dfref.loc[dfref['flag']<flag_ref_threshold,'mag'],ax=ax[1],
                         color='green',element='step',fill=False,
                         label='reference hq (flag<'+str(flag_ref_threshold)+')')
        ax[1].set_xlim(xp_range)
        #ax[1].set_ylim(yp_range)
        ax[1].legend()
        ax[1].set_xlabel('MAG')
        
        fig.savefig(showfile,bbox_inches='tight')
        plt.close(fig)
        return 1
    
    def check_phot_magerr(self, dfphot, dfref=None, nthres_histplot=10000, showfile='check_phot_magerr.png'):
        nsex=dfphot.shape[0]
        if dfref is not None:
            nref=dfref.shape[0]
            nn=np.nanmax([nsex,nref])
            nthres=nthres_histplot
            fig,ax=plt.subplots(2,2,figsize=(14,8))
            fig.subplots_adjust(bottom=0.1,top=0.9,left=0.1,right=0.9,wspace=0.1,hspace=0.3)
            ms=5
            magrange_sex=[dfphot['MAG_CAL'].min(),dfphot['MAG_CAL'].max()]
            magrange_ref=[dfref['mag'].min(),dfref['mag'].max()]
            magrange=[np.nanmin([magrange_sex[0],magrange_ref[0]]),
                      np.nanmax([magrange_sex[1],magrange_ref[1]])]
            magoff=(magrange[1]-magrange[0])/10.
            magrange=np.array([magrange[0]-magoff,magrange[1]+magoff])
            errrange=[np.nanmin([dfphot['MAGERR_INS'].min(),dfref['merr'].min()])/2.,
                      np.nanmax([dfphot['MAGERR_INS'].max(),dfref['merr'].max()])*1.2]
            std_err=np.nanmax([dfphot['MAGERR_INS'].std(),dfref['merr'].std()])
            
            if nn <= nthres:
                #pdb.set_trace()
                #print(dfphot['hq'])
                sns.scatterplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[0][0],hue='hq',s=ms/2)
            else:
                sns.histplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[0][0],hue='hq',bins=100)
            ax[0][0].set_xlabel(' ')
            ax[0][0].set_ylabel('MAG_ERR')
            ax[0][0].set_title('Sextractor detections')
            ax[0][0].set_xlim(magrange[0],magrange[1])
            ax[0][0].set_ylim(-std_err,errrange[1])
            if nn <= nthres:
                sns.scatterplot(x='mag',y='merr',data=dfref,ax=ax[0][1],hue='hq',s=ms/2)
            else:
                sns.histplot(x='mag',y='merr',data=dfref,ax=ax[0][1],hue='hq',bins=100)
            ax[0][1].set_xlabel(' ')
            ax[0][1].set_ylabel(' ')
            ax[0][1].set_title('reference catalog')
            ax[0][1].set_xlim(magrange[0],magrange[1])
            ax[0][1].set_ylim(-std_err,errrange[1])
            
            if nn <= nthres:
                sns.scatterplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[1][0],hue='hq',s=ms)
                ax[1][0].set_yscale('log')
            else:
                sns.histplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[1][0],hue='hq',
                             bins=100,log_scale=(False,True))
            ax[1][0].set_xlabel('MAG')
            ax[1][0].set_ylabel('MAG_ERR')
            ax[1][0].set_title('Sextractor detections')
            ax[1][0].set_xlim(magrange[0],magrange[1])
            ax[1][0].set_ylim(errrange[0],errrange[1])
            
            if nn <= nthres:
                sns.scatterplot(x='mag',y='merr',data=dfref,ax=ax[1][1],hue='hq',s=ms)
                ax[1][1].set_yscale('log')
            else:
                sns.histplot(x='mag',y='merr',data=dfref,ax=ax[1][1],hue='hq',bins=100,log_scale=(False,True))
            ax[1][1].set_xlabel('MAG')
            ax[1][1].set_ylabel(' ')
            ax[1][1].set_title('reference catalog')
            ax[1][1].set_xlim(magrange[0],magrange[1])
            ax[1][1].set_ylim(errrange[0],errrange[1])
        else:
            nn=nsex
            nthres=nthres_histplot
            fig,ax=plt.subplots(2,1,figsize=(7,7))
            fig.subplots_adjust(bottom=0.1,top=0.9,left=0.1,right=0.9,wspace=0.1,hspace=0.3)
            ms=5
            
            magrange=[dfphot['MAG_CAL'].min(),dfphot['MAG_CAL'].max()]
            magoff=(magrange[1]-magrange[0])/10.
            magrange=np.array([magrange[0]-magoff,magrange[1]+magoff])
            errrange=[dfphot['MAGERR_INS'].min()/2.,dfphot['MAGERR_INS'].max()*1.1]
            std_err=np.nanmax([dfphot['MAGERR_INS'].std()])
            
            if nn <= nthres:
                sns.scatterplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[0],hue='hq',s=ms/2)
            else:
                sns.histplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[0],hue='hq',bins=100)
            ax[0].set_xlabel(' ')
            ax[0].set_ylabel('MAG_ERR')
            ax[0].set_title('Sextractor detections')
            ax[0].set_xlim(magrange[0],magrange[1])
            ax[0].set_ylim(-std_err,errrange[1])
            
            if nn <= nthres:
                sns.scatterplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[1],hue='hq',s=ms)
                ax[1].set_yscale('log')
            else:
                sns.histplot(x='MAG_CAL',y='MAGERR_INS',data=dfphot,ax=ax[1],hue='hq',
                             bins=100,log_scale=(False,True))
            ax[1].set_xlabel('MAG')
            ax[1].set_ylabel('MAG_ERR')
            ax[1].set_title('Sextractor detections')
            ax[1].set_xlim(magrange[0],magrange[1])
            ax[1].set_ylim(errrange[0],errrange[1])
        
        
        fig.savefig(showfile,bbox_inches='tight')
        plt.close(fig)
        return 1
    
    def check_phot_magdiff(self, dfphot, dfref=None, photerr=0.1, flag_ref_threshold=128, 
                           nthres_histplot=10000, ms=5, showfile='check_phot_magdiff.png',xrange=None):
        fig,ax=plt.subplots(1,1,figsize=(8,4))
        fig.subplots_adjust(bottom=0.1,top=0.9,left=0.1,right=0.9,wspace=0.1,hspace=0.1)
        
        dfphot_hq=dfphot.loc[(dfphot['FLAGS']<4)&(dfphot['MAGERR_INS']<photerr),
                             ['ALPHAWIN_J2000','DELTAWIN_J2000','MAG_INS','MAGERR_INS','MAG_CAL','FLAGS']]
        dfphot_hq.reset_index(drop=True, inplace=True)
        dfref_hq=dfref.loc[(dfref['flag']<flag_ref_threshold)&(dfref['merr']<photerr),:]
        dfref_hq.reset_index(drop=True, inplace=True)
        dfx=basic.crossmatch_2dfs(dfphot_hq,dfref_hq,coo_cols=['ALPHAWIN_J2000','DELTAWIN_J2000','ra','dec'],
                                  frame='icrs', maxdist=0.5)
        dfx.insert(dfx.columns.size,'magdiff',dfx['mag']-dfx['MAG_CAL'])
        label='median: '+'{:5.3f}'.format(dfx['magdiff'].median())+\
                '\n std: '+'{:5.3f}'.format(dfx['magdiff'].std())
        if dfx.shape[0] <= nthres_histplot:
            sns.scatterplot(x='mag',y='magdiff',data=dfx,s=ms,label=label)
            ax.legend(loc='best')
        else:
            dfx.insert(dfx.columns.size,'dummy',0)
            sns.histplot(x='mag',y='magdiff',data=dfx,bins=500,hue='dummy')
            legend = ax.get_legend()
            handles = legend.legendHandles
            legend.remove()
            ax.legend(handles,[label],loc='best')
        ax.set_ylim(-1,1)
        if xrange is not None:
            ax.set_xlim(xrange)
        ax.set_xlabel('mag_ref')
        ax.set_ylabel('mag_ref-mag_sex')
            
        fig.savefig(showfile,bbox_inches='tight')
        plt.close(fig)
        return 1
    
    def photpipe(self, psf=False, apc=False, verbose=True, checkphot=True, dfref=None):
        photfile=self.imgname.replace('.fits','_photsex_PSF'+str(psf)+'_APC'+str(apc)+'.fits')
        dfphot=self.phot(psf=psf,apc=apc,verbose=verbose, show_env=self.phot_show_env)
        df=dfphot.copy()
        if checkphot:
            dfc=self.check_phot(dfphot, dfref=dfref, apc=apc,
                                flag_ref_threshold=self.checkphot_flag_ref_threshold, 
                                if_cali_outliers_detection_method=self.checkphot_if_cali_outliers_detection_method,
                                zoom_width=self.checkphot_zoom_width,
                                imgraw_interval=self.checkphot_imgraw_interval,
                                imgzoom_interval=self.checkphot_imgzoom_interval,
                                nsig_dbscan=self.checkphot_nsig_dbscan,
                                minfrac_dbscan=self.checkphot_minfrac_dbscan,
                                nsig_sigmaclip=self.checkphot_nsig_sigmaclip,
                                zmag_order=self.checkphot_zmag_order,
                                keep_html_only=self.checkphot_keep_html_only)
            dfc_file=photfile.replace('.fits','_photodf_checkout.fits')
            Table.from_pandas(dfc).filled(np.nan).write(self.workdir+dfc_file,overwrite=True)
        else:
            dfc=pd.DataFrame()
        dfout={'df':df,'dfc':dfc}
        return dfout
    
    
if __name__ == '__main__':
    pydir=os.getcwd()+'/'
    imgdir=os.path.abspath(pydir+'../image/')+'/'
    #name='test_medium'
    name='test_high'
    band='r'
    filename=name+'_'+band+'_panstar.fits'
    imgfile=imgdir+filename
    catfile=imgdir+filename.replace('_r_','_cat_')
    dfcat=Table.read(catfile).to_pandas()
    dfref=pd.DataFrame()
    dfref.insert(dfref.columns.size,'objname',dfcat['objID'])
    dfref.insert(dfref.columns.size,'ra',dfcat['raMean'])
    dfref.insert(dfref.columns.size,'dec',dfcat['decMean'])
    dfref.insert(dfref.columns.size,'mag',dfcat['rMeanPSFMag'])
    dfref.insert(dfref.columns.size,'merr',dfcat['rMeanPSFMagErr'])
    dfref.insert(dfref.columns.size,'flag',dfcat['qualityFlag'])
    cond=(dfref['mag'].isnull()==False) & (dfref['merr'].isnull()==False) & (dfref['merr']>0)
    dfref=dfref.loc[cond,:]
    dfref.reset_index(drop=True,inplace=True)
    workdir=os.path.abspath(pydir+'../')+'/test_detection/'
    pathlib.Path(workdir).mkdir(parents=True, exist_ok=True)
    sexdir=str(pathlib.Path.home())+'/Science/data/models/sextractor/'
    
    ps=PhotoSex(imgfile, workdir=workdir, sexdir=sexdir, config_dir=pydir)
    df=ps.photpipe(psf=True, apc=False, verbose=True, checkphot=True, dfref=dfref)
    pdb.set_trace()

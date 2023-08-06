import numpy as np
import os
import time
import pandas as pd
from astropy.io import fits
from astropy.table import Table
import math
import pdb
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.wcs.utils import proj_plane_pixel_scales as pixel_scale
from matplotlib.patches import Rectangle
from tqdm import tqdm
from subprocess import Popen, PIPE, STDOUT
import gc
from sklearn.cluster import DBSCAN

class basic(object):
    def axis2map(nx,ny,subval=None):
        if subval==None:
            subval=0.
        x=np.array(np.arange(nx)-subval).reshape(1,-1)
        y=np.array(np.arange(ny)-subval).reshape(-1,1)
        #print(x)
        #print(y)
        mx=np.repeat(x,ny,axis=0)
        my=np.repeat(y,nx,axis=1)
        return mx,my
    def gcirc(ra1,dc1,ra2,dc2):
        #input coordinate must be in decimal degrees
        d2r=np.pi/180.
        as2r=np.pi/648000.
        h2r=np.pi/12.0
        
        rarad1=ra1*d2r
        rarad2=ra2*d2r
        dcrad1=dc1*d2r
        dcrad2=dc2*d2r
        
        deldec2=(dcrad2-dcrad1)/2.0
        delra2=(rarad2-rarad1)/2.0
        sindis=(np.sin(deldec2)*np.sin(deldec2)+\
                np.cos(dcrad1)*np.cos(dcrad2)*np.sin(delra2)*np.sin(delra2))**0.5
        dis=2.0*np.arcsin(sindis)
        
        dis=dis/as2r
        return dis#in arcsecs
    
    def spawn(cmd,silent=False):
        import subprocess
        try:
            output=subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT)
            if silent == False:
                if (not isinstance(output, int)):
                    print(output.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            output=e.output
            code=e.returncode
            if silent == False:
                if (not isinstance(code,int)) and (not isinstance(output,int)):
                    print(code.decode('utf-8'),output.decode('utf-8'))
        return output
    
    def extinction_law_mydef(select='wang19'):
        if select == 'xue16':
            ks={'j':2.72, 'h':1.6, 'k':1.0, 
                'irac1':0.553, 'irac2':0.461, 'irac3':0.389, 'irac4': 0.426, 'mips24':0.264,
                'w1':0.591, 'w2':0.463, 'w3':0.537, 'w4':0.364,
                'v':1./0.112}
        
        if select == 'rieke85':
            ks = {'u':1.531, 'b':1.324, 'v':1.0, 'r':0.748, 'i':0.482, 
                  'j':0.282, 'h':0.175, 'k':0.112, 'l':0.058, 'm':0.023, 'n':0.052,
                  '8.0':0.02, '8.5':0.043, '9.0':0.074, '9.5':0.087,
                  '10.0':0.083, '10.5':0.074, '11.0':0.060, '11.5':0.047, '12.0':0.037, '12.5':0.030, '13.0':0.027}
    
        if select == 'ind05':
            ks={'j':2.50, 'h':1.55, 'k':1.0, 
                'irac1':0.56, 'irac2':0.43, 'irac3':0.43, 'irac4': 0.43,
                'w1':0.56, 'w2':0.43, 'w3':0.43,
                'v':1./0.112}
        
        if select == 'wang19':
            ks0={'g_bp':1.002, 'g_rp':0.589, 'b':1.317, 
                'v':1.0, 'u_sdss':1.584, 'g_sdss':1.205,
                'r_sdss':0.848, 'i_sdss':0.630, 'z_sdss':0.458,
                'g_pan':1.155, 'r_pan':0.843, 'i_pan':0.628,
                'z_pan':0.487, 'y_pan':0.395, 'j':0.243,
                'h':0.131, 'k':0.078, 'w1':0.039,
                'w2':0.026, 'w3':0.04, 'g_gaia':0.789,
                'irac1':0.037, 'irac2':0.026, 'irac3':0.019,
                'irac4':0.025}
            ks=ks0.copy()
            factor=ks0['k']
            for kkk in ks0:
                ks[kkk]=ks0[kkk]/factor
            
            
        return ks
    
    def range_extend(range_in,extend=0.1):
        xmin=range_in[0]
        xmax=range_in[1]
        size_in=xmax-xmin
        range_out=np.array([xmin-size_in*extend,xmax+size_in*extend])
        return range_out
    
    def convert_dfcol_int2float(df1):
        ncol=df1.shape[1]
        for icol in np.arange(ncol):
            cond=(df1.dtypes[icol].type is np.int) | (df1.dtypes[icol].type is np.int16) | \
                 (df1.dtypes[icol].type is np.int32) | (df1.dtypes[icol].type is np.int64)
            #print(cond)
            #pdb.set_trace()
            if cond is True:
                #print(df1.columns[icol],df1.dtypes[icol])
                df1[df1.columns[icol]]=df1[df1.columns[icol]].astype(float)
        return df1
    
    def convert_tabcol_int2float(tab):
        cols=tab.colnames
        for icol in cols:
            cond=(tab[icol].dtype.type is np.int) | (tab[icol].dtype.type is np.int16) | \
                 (tab[icol].dtype.type is np.int32) | (tab[icol].dtype.type is np.int64)
            if cond is True:
                tab[icol]=tab[icol].astype(float)
        return tab
    
    def crossmatch_2dfs(df1,df2,coo_cols=['ra','dec','RAJ2000','DEJ2000'],
                        frame='icrs',maxdist=None):
        c1=SkyCoord(df1[coo_cols[0]].values*u.degree,df1[coo_cols[1]].values*u.degree,frame=frame)
        c2=SkyCoord(df2[coo_cols[2]].values*u.degree,df2[coo_cols[3]].values*u.degree,frame=frame)
        idx, dist2d, dist3d = c1.match_to_catalog_sky(c2)
        df2s=df2.loc[idx,:]
        df2s.reset_index(inplace=True)
        df1.reset_index(inplace=True)
        df1.drop(columns=['index'],inplace=True)
        df2s.drop(columns=['index'],inplace=True)
        dfc=pd.concat([df1,df2s],axis=1)
        #pdb.set_trace()
        dfc.insert(dfc.columns.size,'d_arcsec',dist2d.value*3600.)
        if maxdist is not None:
            dfc=dfc[dfc['d_arcsec']<maxdist]
        return dfc
    
    
    def str2float_one(string):
        try:
            f=np.float(string)
        except:
            f=np.nan
        return f
    
    def syscmd(cmd, encoding=''):
        """
        Runs a command on the system, waits for the command to finish, and then
        returns the text output of the command. If the command produces no text
        output, the command's return code will be returned instead.
        """
        p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
            close_fds=True)
        p.wait()
        output = p.stdout.read()
        if len(output) > 1:
            if encoding: return output.decode(encoding)
            else: return output
        return p.returncode
    
    def patch_slit(ra_cen,dec_cen,wcs=None,slit_len=7*u.arcmin,slit_width=1*u.arcsec,slit_posang=45.,
                   edgecolor='red',facecolor='none'):
        ra=ra_cen
        dec=dec_cen
        if wcs is None:
            raise ValueError('Please offer wcs!')
        subwcs=wcs
        pixscl=pixel_scale(subwcs)[0]*3600.
        xc,yc=subwcs.wcs_world2pix(ra,dec,0)
        width=slit_len.to(u.arcsec).value/pixscl
        height=slit_width.to(u.arcsec).value/pixscl
        posang=slit_posang
        posang_rad=posang/180*np.pi
        xim=xc - ((width / 2) * np.cos(posang_rad)) + ((height / 2) * np.sin(posang_rad))
        yim=yc - ((width / 2) * np.sin(posang_rad)) - ((height / 2) * np.cos(posang_rad))
        rr=Rectangle((xim,yim), width, height,
                     angle=posang,
                     edgecolor=edgecolor, facecolor=facecolor,zorder=10)
        #pdb.set_trace()
        return rr
    
    def outliers_detection_dbscan(df, cols=['pmra','pmdec'],nsig=2.5,min_cluster_size_fraction=0.5):
        dfuse=df.copy()
        pmra=(dfuse[cols[0]].values-dfuse[cols[0]].median())/dfuse[cols[0]].std()
        pmdec=(dfuse[cols[1]].values-dfuse[cols[1]].median())/dfuse[cols[1]].std()
        X=np.vstack([pmra,pmdec]).T
        num_diff=1
        labels=np.zeros(X.shape[0])
        nsig_dbscan=nsig
        
        while num_diff > 0:
            no_noise_before=labels[labels==-1].shape[0]
            x0=X[:,0]
            x1=X[:,1]
            std0=np.nanstd(x0[labels>-1])
            std1=np.nanstd(x1[labels>-1])
            #pdb.set_trace()
            stdmax=np.nanmax([std0,std1])
            epsilon=stdmax*nsig_dbscan#2.85
            min_samples=x0[labels>-1].shape[0]*min_cluster_size_fraction
            db = DBSCAN(eps=epsilon, min_samples=min_samples).fit(X)
            labels = db.labels_
            no_clusters = len(np.unique(labels) )
            no_noise = np.sum(np.array(labels) == -1, axis=0)
            #print(no_noise)
            num_diff=no_noise-no_noise_before
    #pdb.set_trace()
        dfuse.insert(dfuse.columns.size,'clusters',labels)
        dfuse.insert(dfuse.columns.size,'Outlier','N')
        dfuse.loc[dfuse['clusters']==-1,'Outlier']='Y'
        return dfuse
    
    def df_to_little_endian(df):
        dftem=df.copy()
        for col in dftem.columns:
            bo=dftem[col].values.dtype.byteorder
            if bo == '>':
                dftem[col]=dftem[col].values.byteswap().newbyteorder()
        return dftem

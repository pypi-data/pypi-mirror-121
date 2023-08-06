
from __future__ import print_function
import numpy
from astropy.table import Table
import requests
from PIL import Image
from io import BytesIO
import pylab
import pdb

class download_panstar_image(object):
    def __init__(self, ra=83.633210, dec=22.014460, size=1280, filters='grizy', format='jpg',imgtype='warp'):
        self.ra=ra
        self.dec=dec
        self.size=size
        self.filters=filters
        self.format=format
        self.imgtype=imgtype
        
    def getimages(self):
    
        """Query ps1filenames.py service to get a list of images
    
        ra, dec = position in degrees
        size = image size in pixels (0.25 arcsec/pixel)
        filters = string with filters to include
        Returns a table with the results
        """
    
        service = "https://ps1images.stsci.edu/cgi-bin/ps1filenames.py"
        url = service+("?ra={ra}&dec={dec}&size={size}&format=fits"
               "&filters={filters}&type={imgtype}").format(ra=self.ra,dec=self.dec,
                                                        size=self.size,filters=self.filters,imgtype=self.imgtype)
        table = Table.read(url, format='ascii')
        return table


    def geturl(self, output_size=None, color=False):
    
        """Get URL for images in the table
    
        ra, dec = position in degrees
        size = extracted image size in pixels (0.25 arcsec/pixel)
        output_size = output (display) image size in pixels (default = size).
                      output_size has no effect for fits format images.
        filters = string with filters to include
        format = data format (options are "jpg", "png" or "fits")
        color = if True, creates a color image (only for jpg or png format).
                Default is return a list of URLs for single-filter grayscale images.
        Returns a string with the URL
        """
    
        if color and self.format == "fits":
            raise ValueError("color images are available only for jpg or png formats")
        if self.format not in ("jpg","png","fits"):
            raise ValueError("format must be one of jpg, png, fits")
        table = self.getimages()
        url = ("https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?"
               "ra={ra}&dec={dec}&size={size}&format={format}&type={imgtype}").format(ra=self.ra,dec=self.dec,
                                                                                      size=self.size,
                                                                                      format=self.format,
                                                                                      imgtype=self.imgtype)
        if output_size:
            url = url + "&output_size={}".format(output_size)
        # sort filters from red to blue
        flist = ["yzirg".find(x) for x in table['filter']]
        table = table[numpy.argsort(flist)]
        if color:
            if len(table) > 3:
                # pick 3 filters
                table = table[[0,len(table)//2,len(table)-1]]
            for i, param in enumerate(["red","green","blue"]):
                url = url + "&{}={}".format(param,table['filename'][i])
        else:
            urlbase = url + "&red="
            url = []
            for filename in table['filename']:
                url.append(urlbase+filename)
        #pdb.set_trace()
        return url


    def getcolorim(self, output_size=None):
    
        """Get color image at a sky position
    
        ra, dec = position in degrees
        size = extracted image size in pixels (0.25 arcsec/pixel)
        output_size = output (display) image size in pixels (default = size).
                  output_size has no effect for fits format images.
        filters = string with filters to include
        format = data format (options are "jpg", "png")
        Returns the image
        """
    
        if self.format not in ("jpg","png"):
            raise ValueError("format must be jpg or png")
        url = self.geturl(output_size=output_size, color=True)
        r = requests.get(url)
        im = Image.open(BytesIO(r.content))
        return im


    def getgrayim(self, output_size=None):
    
        """Get grayscale image at a sky position
    
        ra, dec = position in degrees
        size = extracted image size in pixels (0.25 arcsec/pixel)
        output_size = output (display) image size in pixels (default = size).
                      output_size has no effect for fits format images.
        filter = string with filter to extract (one of grizy)
        format = data format (options are "jpg", "png")
        Returns the image
        """
    
        if self.format not in ("jpg","png"):
            raise ValueError("format must be jpg or png")
        if self.filters not in list("grizy"):
            raise ValueError("filter must be one of grizy")
        url = self.geturl(output_size=output_size)
        r = requests.get(url[0])
        im = Image.open(BytesIO(r.content))
        return im

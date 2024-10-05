# # opening and extracting the information from a .tar file

# import tarfile
# # the tar file may need to be downloaded from CADCs website into the input directory
# # if you already have a fits file ready for use in the output folder, then this step is not needed
# tar = tarfile.open('input/tar_files/JWST-jw02738002002_02201_00002_nis-jw02738002002_02201_00002_nis-CALIBRATED.tar', "r:")

# tar.extractall('output\extracted_tar')
# tar.close()

# #Another option if you know exactly which file you wish to download is to go on CADC and in the metadata, find the files URI
# # and plug it into the cadcget below.

# from cadcdata import StorageInventoryClient
# client = StorageInventoryClient()
# client.cadcget('cadc:MOST/268_GSC0168801944_2014_gs.fits','268_GSC0168801944_2014_gs.fits') #this takes the chosen fits file and
#                                                                                             # download it to your computer
# #You can also use astro querry to filter fits files similar to the CADC website.
# # This will give you a list of all the different fits files that match your filter which you can then download using the URL.
# from astroquery.cadc import Cadc
# cadc = Cadc()
# results = cadc.query_name('NGC253') # filter by target name
# results = results[results['collection']=='JWST']# filter by archive 
# results = results[results['dataRelease'] > '2022-10-29T00:00:00.000'] # filter by release date
# Download_urls = cadc.get_data_urls(results)

# #lastly, you can also automate the downloading process by following steps below.
# numberOfFiles = 5
# for urls in np.arange(0,numberOfFiles,1):
#     r = requests.get(w[urls])
#     open('test_fits/file_'+str(urls)+'.fits','wb').write(r.content)

# # Below shows the steps to accessing a certain fits files and opening it
# import matplotlib.pyplot as plt
# from astropy.visualization import astropy_mpl_style
# plt.style.use(astropy_mpl_style)


# from astropy.utils.data import get_pkg_data_filename
# from astropy.io import fits

# #call in the file and extract in image
# file_name = 'output/extracted_tar/JWST/product/jw01521-o001_t001_miri_f770w_segm.fits'  #specify your path and fits file here
# image_file = get_pkg_data_filename(file_name)
# image_data = fits.getdata(image_file, ext=1)

# plt.axis ('off')
# # The data can be in the form of a 2D or 3D array

# plt.imshow(image_data[0,:,:],origin = 'lower' ,cmap='gray')  # 3D version
# # plt.imshow(image_data,cmap='gray')  # 2D version

# #creating a saving the image
# image_name = 'created_image.png'
# fig1 = plt.gcf()
# plt.imsave('output/images/'+ image_name ,image_data,cmap = 'Greys_r')a
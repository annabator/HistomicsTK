from matplotlib import pyplot as plt
import numpy as np
import os
import glob
from skimage import color

from histomicstk.preprocessing.color_normalization import deconvolution_based_normalization
from histomicstk.preprocessing.color_conversion import sda_to_rgb

#from PIL import ImageFile
#ImageFile.LOAD_TRUNCATED_IMAGES = True # this is needed to load K4L-064_8192_36864fib.png which is truncated

#TEST_TILES = '/Users/awabator/Documents/colnorm_experiments/test_tiles_separate/TRC/'
#MASKS = '/Users/awabator/Documents/colnorm_experiments/fg_masks/TRC/'
#SAVE_DIR = '/Users/awabator/Documents/colnorm_experiments/macenko/fuchsin_methyl/'

DIR_NAME = '/Users/awabator/Documents/colnorm_experiments/qupath_stain_vector_experiment/'

if __name__ == '__main__':

    tiles = glob.glob(os.path.join(DIR_NAME, '*.png'))
    

    for tile in tiles:
        tile_fname = tile.split('/')[-1]
        mask_path = os.path.join(DIR_NAME, 'fg_masks', tile_fname)

        wsi = plt.imread(tile)  
        wsi = (wsi * 255).astype(np.uint8)
        wsi = wsi[...,:3] # remove the alpha channel
        
        fore_mask = plt.imread(mask_path)
        fore_mask = fore_mask > 0.5 # binarise
        fore_mask = fore_mask[:,:,0]
        # note this is slightly counterintuitive
        fore_mask = ~fore_mask 
        # 'stains' is needed to determine the order
        wsi_norm = deconvolution_based_normalization(im_src=wsi,
                                                    stains=['methyl_blue', 'ponceau_fuchsin'],
                                                    mask_out=fore_mask,
                                                    stain_unmixing_routine_params={'stain_unmixing_method': 'macenko_pca'})
        
        plt.imsave(os.path.join(DIR_NAME, 'norm', tile_fname), wsi_norm)
    
    '''
    for tile in tiles:

        wsi = plt.imread(tile)  
        wsi = (wsi * 255).astype(np.uint8)
        wsi = wsi[...,:3] # remove the alpha channel

        # mask out whites
        wsi_mean = np.mean(wsi, axis=2) # this converts it back to 0-1
        fore_mask = ~(wsi_mean>178) * (wsi_mean>0.0) # mask out any black edges
        # PCA breaks with fg thresh ("SVD did not converge...") == 0.8 but with 0.7 it's okay..
        # still it's trying to normalise the bg for some reason??
        
        # 'stains' is needed to determine the order
        wsi_norm = deconvolution_based_normalization(im_src=wsi,
                                                    stains=['ponceau_fuchsin', 'methyl_blue'],
                                                    mask_out=fore_mask,
                                                    stain_unmixing_routine_params={'stain_unmixing_method': 'macenko_pca'})
        tile_fname = tile.split('/')[-1]
        plt.imsave(os.path.join(SAVE_DIR, 'fore_' + tile_fname), fore_mask)
        plt.imsave(os.path.join(SAVE_DIR, tile_fname), wsi_norm)
    '''
    print('x')
 
 
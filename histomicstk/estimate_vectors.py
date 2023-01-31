from matplotlib import pyplot as plt
import numpy as np
import os
import glob
from histomicstk.preprocessing.color_deconvolution import stain_unmixing_routine
from histomicstk.preprocessing.color_deconvolution import color_deconvolution
import json

DIR_NAME = '/Users/awabator/Documents/colnorm_experiments/qupath_stain_vector_experiment/'

if __name__ == '__main__':

    with open(os.path.join(DIR_NAME, 'qupath_form.json'), 'r') as f:
        json_template = json.load(f)
    
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

        '''
        # fg mask generation:
        wsi_mean = np.mean(wsi, axis=2) # this converts it back to 0-1
        fore_mask = ~(wsi_mean>178) * (wsi_mean>0.0) # mask out any black edges
        plt.imsave(os.path.join(DIR_NAME, 'fg_masks', tile_fname), fore_mask)
        '''

        # run stain estimation (PCA) = color_deconvolution_routine
        estimated_stain_matrix = stain_unmixing_routine(wsi, stains=['methyl_blue', 'ponceau_fuchsin'], mask_out=fore_mask)
        #w_source = estimated_stain_matrix
        json_template[tile_fname]['auto_vectors'] = estimated_stain_matrix.tolist()

        '''
        Stains, StainsFloat, wc = color_deconvolution(wsi, w=w_source, I_0=255.0)

        for i in range(3):
            Stains[..., i][fore_mask] = 255
            StainsFloat[..., i][fore_mask] = 255.
            plt.imsave(os.path.join(DIR_NAME, ('dye_' + str(i) + '.png')), Stains[..., i])
        
        print('x')
        '''
        
    with open(os.path.join(DIR_NAME, 'qupath_form_Awa.json'), 'w') as f:
        json.dump(json_template, f)
    
    print('All done :)')
# remember using white light as I_0
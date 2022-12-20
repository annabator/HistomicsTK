from matplotlib import pyplot as plt
import numpy as np
import os

from histomicstk.preprocessing.color_normalization import deconvolution_based_normalization

DATA_DIR = '/Users/awabator/Documents/colnorm_experiments/macenko'

if __name__ == '__main__':

    image_path = f'{DATA_DIR}/wsi.png'
    mask_path = f'{DATA_DIR}/fg_mask.png'

    wsi = plt.imread(image_path)  # check shape here: should be 3D
    wsi = (wsi * 255).astype(np.uint8)
    wsi = wsi[..., :3]

    fore_mask = plt.imread(mask_path)
    fore_mask = fore_mask[:, :, 0]
    fore_mask = fore_mask > 0.5

    
    # 'stains' is needed to determine the order
    wsi_norm = deconvolution_based_normalization(im_src=wsi,
                                                 stains=['ponceau_fuchsin', 'methyl_blue'],
                                                 mask_out=fore_mask,
                                                 stain_unmixing_routine_params={'stain_unmixing_method': 'macenko_pca'})
    
    plt.imsave(os.path.join(DATA_DIR, 'Colour_Deconvolution_2', 'TRC_norm_ponceau_fuchsin_methyl_blue.png'), wsi_norm)
    print('x')
 
 
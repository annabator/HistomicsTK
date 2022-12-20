# Edit: the stain map needs to be defined as part of the main function 
# for it to be imported as a script and not a package.
# If it's imported as a package, we can't make edits to the stain vector values
#if __name__ == '__main__':
stain_map = {
    'hematoxylin': [0.65, 0.70, 0.29],
    'eosin':       [0.07, 0.99, 0.11],
    'dab':         [0.27, 0.57, 0.78],
    'ponceau_fuchsin': [0.7995107, 0.5913521, 0.10528667], # orange [203.8752285, 150.79478550000002, 26.848100849999998]
    'methyl_blue': [0.09997159, 0.73738605, 0.6680326], # turquoise 25.49275545, 188.03344275, 170.348313
    'null':        [0.0, 0.0, 0.0]
}

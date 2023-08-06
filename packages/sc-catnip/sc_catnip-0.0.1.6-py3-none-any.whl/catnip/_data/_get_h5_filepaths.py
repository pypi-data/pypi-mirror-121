def _get_h5_filepaths(path, use_raw=False, use_peaks=True, use_TFs=False, silent=False):
    
    """
    Add the filepaths of the h5 files to be analyzed to the main ATAC class. 
    
    Parameters:
    -----------
    path
        Path to the cellranger-atac outputs. For multiple samples, use the directory that contains all of them.
        type: str
        
    use_raw
        type: boolean
    
    use_peaks
        type: boolean
    
    use_TFs
        type: boolean
    
    silent
    
    Returns:
    --------
    h5_filepaths
    
    Notes:
    ------
    (1) This function first determines which h5 file to grab from the standard 10x cellranger-atac outputs 
    directory through the user-specified parameters for raw/peaks/tfs.
    
    (2) As an example: /home/mvinyard/data/preprocessed/cellranger-outs/ which assumes a substructure of:

            /home/mvinyard/data/preprocessed/cellranger-outs/[SAMPLE_ID_01]/outs/
            /home/mvinyard/data/preprocessed/cellranger-outs/[SAMPLE_ID_02]/outs/
            /home/mvinyard/data/preprocessed/cellranger-outs/[SAMPLE_ID_03]/outs/
            ...
            /home/mvinyard/data/preprocessed/cellranger-outs/[SAMPLE_ID_0N]/outs/
    
    """
    
    ### DETERMINE WHICH h5 FILE TO GRAB FROM THE STANDARD 10x CELLRANGER-ATAC OUTPUTS
    
    if use_raw:
        processing_status = 'raw'
    else:
        processing_status = 'filtered'
        
    if use_peaks:
        specification = "{}_peak".format(processing_status)
    elif use_TFs:
        specification = "{}_tf".format(processing_status)
    
    h5_path_finder = os.path.join(path, '*/outs/{}*.h5'.format(specification))
    
    if not silent:
        print("Loading h5 files from...{}".format(path))
        
    h5_filepaths = glob.glob(h5_path_finder)
        
    return h5_filepaths
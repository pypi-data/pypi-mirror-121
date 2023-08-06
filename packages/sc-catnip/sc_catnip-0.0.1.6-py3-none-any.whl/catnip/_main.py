
from ._data._get_h5_filepaths import _get_h5_filepaths

class ATAC:
    
    def __init__(self):
        
        """
        
        """
        
        
        print("Class for merging ATAC data samples.")
        
    def load_data(self, data_path):
        
        self.h5_filepaths = _get_h5_filepaths(data_path)
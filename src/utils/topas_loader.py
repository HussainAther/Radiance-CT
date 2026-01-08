import numpy as np
import pandas as pd
import os

class TopasLoader:
    def __init__(self, output_dir):
        self.output_dir = output_dir

    def load_scorer_output(self, filename):
        """
        Parses TOPAS ASCII output files. 
        Usually, these contain a header with dimension info followed by data.
        """
        path = os.path.join(self.output_dir, filename)
        
        # TOPAS files often have a '#' at the start of header lines
        with open(path, 'r') as f:
            lines = f.readlines()
            
        # Extract metadata (assuming Binned Scorer)
        metadata = {}
        data_start = 0
        for i, line in enumerate(lines):
            if line.startswith("#"):
                if "Number of Bins:" in line:
                    # e.g., # Number of Bins: 256 256 80
                    metadata['bins'] = [int(x) for x in line.split(":")[-1].split()]
                continue
            else:
                data_start = i
                break
        
        # Load the raw values (Dose, Fluence, etc.)
        data = np.loadtxt(lines[data_start:])
        
        # Reshape into the 3D volume (X, Y, Z)
        if 'bins' in metadata:
            volume = data.reshape(metadata['bins'], order='F') # TOPAS uses Fortran order
            return volume, metadata
        
        return data, metadata

    def get_phase_space_data(self, filename):
        """
        Loads TOPAS Phase Space files (.phsp).
        Crucial for tracking individual ray/particle trajectories for RBYRCT.
        """
        # TOPAS Phase Space files are usually columnar: 
        # X, Y, Z, Px, Py, Pz, Energy, ParticleType...
        column_names = ['x', 'y', 'z', 'px', 'py', 'pz', 'energy', 'weight', 'type']
        df = pd.read_csv(os.path.join(self.output_dir, filename), 
                         sep=r'\s+', names=column_names, comment='#')
        return df

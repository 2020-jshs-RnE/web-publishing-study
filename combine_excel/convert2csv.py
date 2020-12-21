import pandas as pd
import tabula

import os, glob

path = r'D:\RnE\combine_excel\test_pdf'
files = glob.glob(path + '/*.pdf')

tabula.convert_into_by_batch(path, lattice=True, output_format='csv', pages='all')
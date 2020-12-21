import pandas as pd
import tabula

import os, glob

path = r'D:\RnE\combine_excel\test_pdf' # pdf에서 csv로 바꿀 디렉토리 위치 입력

# 디렉토리 내에 있는 pdf를 csv로 바꿈
tabula.convert_into_by_batch(path, lattice=True, output_format='csv', pages='all')
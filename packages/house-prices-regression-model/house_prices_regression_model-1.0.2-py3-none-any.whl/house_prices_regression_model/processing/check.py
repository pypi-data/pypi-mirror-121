#import os
#print('PYTHONPATH:',os.environ['PYTHONPATH'])

import sys
#sys.path.append("../")
print('SYSPATH:',sys.path)

from house_prices_regression_model.config.core import DATASET_DIR

if __name__ == "__main__":
   print(DATASET_DIR)
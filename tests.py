# import numpy as np
# import matplotlib.pyplot as plt

# from astropy.visualization import (MinMaxInterval, SqrtStretch,
#                                    ImageNormalize)

# # Generate a test image
# image = np.arange(65536).reshape((256, 256))

# # Create an ImageNormalize object
# norm = ImageNormalize(image, interval=MinMaxInterval(),
#                       stretch=SqrtStretch())

# # or equivalently using positional arguments
# # norm = ImageNormalize(image, MinMaxInterval(), SqrtStretch())

# # Display the image
# fig = plt.figure()
# ax = fig.add_subplot(1, 1, 1)
# im = ax.imshow(image, origin='lower', norm=norm)
# fig.colorbar(im)
# plt.show()
# print(fig, ax, im)

import numpy as np 

dic = { 12 : list(list([1,2])), 13: list([1,3]) }
# print(dic)
# dic[12].append(list([2,3]))
# print(dic)
a = list([[1, 2]])
b = list([3, 4])

a.append(b)
print(a)

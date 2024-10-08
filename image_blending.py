import cv2 as cv
import numpy as np
apple = cv.imread('./image_blending/apple.jpg')
orange = cv.imread('./image_blending/orange.jpg')
apple_orange = np.hstack((apple[:, :256], orange[:, 256:]))



#generate gaussian pyramid for apple
apple_copy = apple.copy()
gp_apple = [apple_copy]

for i in range(6):
    apple_copy = cv.pyrDown(apple_copy)
    gp_apple.append(apple_copy)


#generate gaussian pyramid for orange
orange_copy = orange.copy()
gp_orange = [orange_copy]
for i in range(6):
    orange_copy = cv.pyrDown(orange_copy)
    gp_orange.append(orange_copy)

#get laplacian pyramid for apple

apple_copy = gp_apple[5]
lp_apple = [apple_copy]

for i in range(5, 0, -1):
    gaussian_extended = cv.pyrUp(gp_apple[i])
    laplacian = cv.subtract(gp_apple[i-1], gaussian_extended)
    lp_apple.append(laplacian)

 #get laplacian pyramid for orange
orange_copy = gp_orange[5]
lp_orange = [orange_copy]
for i in range(5, 0, -1):
    gaussian_extended = cv.pyrUp(gp_orange[i])
    laplacian = cv.subtract(gp_orange[i-1], gaussian_extended)
    lp_orange.append(laplacian)

#now add left and right halves of images in each level
apple_orange_pyramid = []
for apple_lap, orange_lap in zip(lp_apple, lp_orange):

    rows, cols, ch = apple_lap.shape
    laplacian = np.hstack((apple_lap[:, :cols//2], orange_lap[:, cols//2:]))
    apple_orange_pyramid.append(laplacian)   

#now reconstruct

apple_orange_reconstruct = apple_orange_pyramid[0]
for i in range(1, 6):
    apple_orange_reconstruct = cv.pyrUp(apple_orange_reconstruct)
    apple_orange_reconstruct = cv.add(apple_orange_pyramid[i], apple_orange_reconstruct)



cv.imshow('Apple', apple)
cv.imshow('Orange', orange)
cv.imshow('Apple_orange', apple_orange)
cv.imshow('Apple_orange_reconstruct', apple_orange_reconstruct)
cv.waitKey(0)
cv.destroyAllWindows()    
import cv2

# Read images
img_hv_ls = cv2.imread(r'C:\Users\User\PycharmProjects\cell_gap_matching_to_michel_levy\images\edited_image.jpg')
img_lv_hs = cv2.imread(r'C:\Users\User\PycharmProjects\cell_gap_matching_to_michel_levy\images\edited_image.jpg')

# Calculate means in HSV color space
mean_hv_ls = cv2.mean(cv2.cvtColor(img_hv_ls, cv2.COLOR_BGR2HSV))
mean_lv_hs = cv2.mean(cv2.cvtColor(img_lv_hs, cv2.COLOR_BGR2HSV))

# Put information on images
font = cv2.FONT_HERSHEY_DUPLEX
cv2.putText(img_hv_ls, 'Mean brightness: ' + '{:.4f}'.format(mean_hv_ls[2]/255), (10, 30), font, 1, (255,255,255), 1)
cv2.putText(img_hv_ls, 'Mean saturation: ' + '{:.4f}'.format(mean_hv_ls[1]/255), (10, 60), font, 1, (255,255,255), 1)
cv2.putText(img_lv_hs, 'Mean brightness: ' + '{:.4f}'.format(mean_lv_hs[2]/255), (10, 30), font, 1, (255, 255, 255), 1)
cv2.putText(img_lv_hs, 'Mean saturation: ' + '{:.4f}'.format(mean_lv_hs[1]/255), (10, 60), font, 1, (255, 255, 255), 1)

cv2.imshow('High brightness, low saturation', img_hv_ls)
cv2.imshow('Low brightness, high saturation', img_lv_hs)
cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessingService:
    def __init__(self, image=None):
        print("Image Processing Services Calling")
        self.image = image
        pass

    def show_single_image(self, image=None):
        """
        A new Window will open with an image
        press any key for dismiss the window
        """
        cv2.imshow("image", image)
        cv2.waitKey(0)

    def plot_image(self, original_image, processed_image):
        """
        ploting image using matplotlib
        1st one is original image and second one is processed image
        """
        plt.subplot(121), plt.imshow(original_image), plt.title('original_image')
        plt.xticks([]), plt.yticks([])
        plt.subplot(122), plt.imshow(processed_image), plt.title('processed_image')
        plt.xticks([]), plt.yticks([])
        plt.show()

    def process_back_image(self):
        rectangular_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        square_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        kernel = np.ones((3, 3), np.uint8)

        print(self.image.shape)
        image = cv2.resize(self.image, (680, 550))
        print(image.shape)

        # image = imutils.resize(self.image, width=600)
        image = cv2.resize(image, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)
        print(image.shape)

        # image = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
        # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 5, 5)
        image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # TODO Final

        # self.process_nid_info(image)
        # self.show_image(image)
        return image

    def smothing_image(self, image):
        # Apply blur to smooth out the edges
        """
        Average: After convolving an image with a normalized box filter, this simply takes the average
        of all the pixels under the kernel area and replaces the central element
        Median blurring: is a non-linear filter. Unlike linear filters,median blurring replaces
        the pixel values with the median value available in the neighborhood values
        Bilateral: Similar to gaussian blurring, bilateral filtering also uses a gaussian filter
        to find the gaussian weighted average in the neighborhood. it ensures only those pixels with similar
        intensity to the central pixel are blurred, whereas the pixels with distinct pixel values are not blurred.
        """
        # image = cv2.blur(image, (5, 5))  # Average
        image = cv2.GaussianBlur(image, (5, 5), 0)  # similar to average but using Kernel ex (5,5)
        # image = cv2.medianBlur(image, 3)  # Median
        # image = cv2.bilateralFilter(image, 9, 75, 75)
        return image

    def noise_remove_from_image(self, image):
        # Apply dilation and erosion to remove some noise
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.erode(image, kernel, iterations=0)
        # image = cv2.dilate(image, kernel, iterations=2)
        return image

    def thresholding_image(self, image):
        """
        Image Must be gray-scale image
        everything eventually boils down to 1’s and 0’s,
        converting image to black and white immensely helps Tesseract recognize characters
        :param image:
        :return:
        """
        # image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 21)

        # cv2.adaptiveThreshold(cv2.medianBlur(img, 7), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        # cv2.adaptiveThreshold(cv2.medianBlur(img, 5), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2),
        # cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
        return image

    def rescalling_image(self, image):
        """
         Tesseract works best on images that are 300 dpi, or more.
         If you’re working with images that have a DPI of less than 300 dpi you might consider rescaling.
        :param image:
        :return:
        CUBIC -> larger size, INTER_AREA -> Shrunk, INTER_LINEAR -> enlarging
        """
        image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        # image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        # image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        image = imutils.resize(image, width=900)
        return image

    def morphological_operation(self, image):
        """
        initialize a rectangular and a square structuring kernel
        which we’ll later use when applying "morphological" operations, specifically the "closing" operation.
        :return:
        """
        print("blackhaed calling")
        rectangular_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
        square_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))
        gray = cv2.GaussianBlur(image, (3, 3), 1)
        blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, square_kernel)  # black-hat operation
        return blackhat


if __name__ == "__main__":
    image = cv2.imread('images/analog/sharif_nid.jpg', 0)  # nid_back

    # call image process module for processing the image
    # """
    image_process_service = ImageProcessingService()  # creating object
    rescale_image = image_process_service.rescalling_image(image)
    blured_image = image_process_service.smothing_image(rescale_image)

    thresholding_image = image_process_service.thresholding_image(blured_image)
    erode_image = image_process_service.noise_remove_from_image(thresholding_image)
    image_process_service.show_single_image(erode_image)

    image_process_service.plot_image(image, erode_image)




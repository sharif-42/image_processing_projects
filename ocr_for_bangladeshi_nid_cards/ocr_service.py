import cv2
import pytesseract

from OCR.image_processing_services import ImageProcessingService


class OcrService:
    def __init__(self, image=None):
        print("OCR service Constructor Calling")
        self.image = image

    def get_nid_info(self):
        # s = str(pytesseract.image_to_string(img))
        # config = ("-l ben --oem 1 --psm 7")
        data = pytesseract.image_to_string(self.image, lang='Bengali', output_type='dict')
        # data = pytesseract.image_to_string(self.image, output_type='dict')
        return data

    def process_nid_info(self, image):
        config = ("-l ben --oem 1 --psm 6")
        data = pytesseract.image_to_string(self.image, lang='Bengali', config=config, output_type='dict')
        # print(data)
        processed_data = {}
        i = 0
        for row in data['text'].split("\n"):
            # new = row.split(':')
            processed_data[i] = row
            i += 1
        for k, v in processed_data.items():
            print(k, v)

        text = "".join([c if ord(c) > 128 else " " for c in processed_data[3]]).strip()
        print(text)


if __name__ == '__main__':
    # image = cv2.imread('images/analog/nid2.jpg', 0)  # nid_back
    image = cv2.imread('images/analog/reza_vai_front.jpg', 0)  # nid_front
    # image = cv2.imread('images/smart/mash.jpeg', 0)  # nid_front
    # image = cv2.imread('images/akib_nid.png', 0)  # nid_front

    # call image processing services for process the image

    image_process_service = ImageProcessingService()  # creating object
    # rescale_image = image_process_service.rescalling_image(image)
    blured_image = image_process_service.rescalling_image(image)
    thresholding_image = image_process_service.thresholding_image(blured_image)
    erode_iamge = image_process_service.noise_remove_from_image(thresholding_image)

    # image_process_service.plot_image(image, erode_iamge)  # ploting image
    ocr = OcrService(erode_iamge)
    data = ocr.get_nid_info()
    processed_data = ocr.process_nid_info(data)

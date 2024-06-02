from encoder import Encoder


def test():
    encoder = Encoder()
    encoder.fill_db('/Users/dmytro.hushchin/Documents/repos/diploma-project/roses')

    # img = cv2.imread('/Users/dmytro.hushchin/Documents/repos/diploma-project/rose.jpeg')

    # print(f'Original image size: {img.nbytes} bytes')
    # compressed_img = encoder.encode(img)
    # reconstructed_img = encoder.decode(compressed_img, img.shape[:2])

    # print(f'Structural similarity index: {encoder.get_ssim(img, reconstructed_img)}')
    # cv2.imwrite('/Users/dmytro.hushchin/Documents/repos/diploma-project/result.jpeg', reconstructed_img)
        

if __name__ == "__main__":
    test()

import streamlit as st
import numpy as np
import cv2
from encoder import Encoder


@st.cache_resource
def load_encoder():
    return Encoder()


class App:
    def __init__(self):
        self.encoder = load_encoder()


    def encode_image(self, img):
        print("Encoding image...")
        compressed_data = self.encoder.encode(img)
        print("Image encoded.")
        return compressed_data


    def decode_image(self, compressed_data, img_shape):
        print("Decoding image...")
        reconstructed_img = self.encoder.decode(compressed_data, img_shape)
        print("Image decoded.")
        return reconstructed_img
    

    def get_ssim(self, img1, img2):
        """Обчислює індекс схожості структури (SSIM) між двома зображеннями."""
        return self.encoder.get_ssim(img1, img2)
    

    def get_compression_ratio(self, original_img: np.ndarray, compressed_data: bytes) -> float:
        """Обчислює відсоток стиснення."""
        original_size = original_img.size
        compressed_size = len(compressed_data)
        return 100 * (1 - compressed_size / original_size)


    def save_image_as_bmp(self, img, filename):
        """Зберігає зображення у форматі BMP."""
        cv2.imwrite(filename + '.bmp', img)
        print("Image saved as BMP.")


    def run(self):
        st.title("Кодування растрових зображень на основі подібності фрагментів з оператором зсуву")

        mode = st.radio("Оберіть дію:", ("Кодування", "Декодування"))

        if mode == "Кодування":
            uploaded_img = st.file_uploader("Обрати файл для кодування", type=["jpg", "jpeg", "png"])
            if uploaded_img is not None:
                img_array = np.array(bytearray(uploaded_img.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, 1)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                st.image(img, caption="Оригінальне зображення", use_column_width=True)

                if st.button("Стиснути зображення"):
                    compressed_data = self.encode_image(img)
                    st.success("Зображення успішно закодоване.")

                    reconstructed_img = self.decode_image(compressed_data, img.shape[:2])
                    st.image(reconstructed_img, caption="Декодоване зображення", use_column_width=True)

                    st.write("Індекс схожості: {:.2f}%".format(self.get_ssim(img, reconstructed_img)))
                    st.write("Відсоток стиснення: {:.2f}%".format(self.get_compression_ratio(img, compressed_data)))
                    st.download_button(label="Завантажити стиснене зображення", data=compressed_data, file_name="compressed_data.bin", mime="application/octet-stream")

        elif mode == "Декодування":
            uploaded_file = st.file_uploader("Обрати файл для декодування", type=["bin"])
            if uploaded_file is not None:
                compressed_data = uploaded_file.getvalue()
                img_shape = st.text_input("Введіть розмір зображення у форматі 'висота,ширина'", "1024,768")
                img_shape = tuple(map(int, img_shape.split(',')))

                if st.button("Відновити зображення"):
                    reconstructed_img = self.decode_image(compressed_data, img_shape)
                    st.image(reconstructed_img, caption="Декодоване зображення", use_column_width=True)

                    if st.button("Зберегти як BMP"):
                        self.save_image_as_bmp(reconstructed_img, 'decoded_image')
                        st.success("Зображення збережено у форматі BMP.")



if __name__ == "__main__":
    app = App()
    app.run()

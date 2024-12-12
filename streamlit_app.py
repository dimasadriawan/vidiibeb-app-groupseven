import streamlit as st
from PIL import Image
from io import BytesIO
import base64

def convert_image(img, format):
    buf = BytesIO()
    img.save(buf, format=format)
    byte_im = buf.getvalue()
    return byte_im

def download_button(data, filename, label):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/{filename.split(".")[-1]};base64,{b64}" download="{filename}">{label}</a>'
    st.markdown(href, unsafe_allow_html=True)

def main():
    st.title("Rotate Image")

    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        # Open image
        image = Image.open(uploaded_file)

        # Rotation
        angle = st.slider("Rotate image by angle (degrees):", min_value=0, max_value=360, value=0, step=1)
        rotated_image = image.rotate(angle, expand=True)
        
        st.image(rotated_image, caption="Rotated Image", use_column_width=True)

        # Format selection for download
        st.write("### Download Processed Image")
        file_format = st.selectbox("Select format:", ["PNG", "JPG", "PDF"])

        if st.button("Download Image"):
            # Convert image to selected format
            if file_format == "JPG":
                image_data = convert_image(rotated_image.convert("RGB"), format="JPEG")
                filename = "processed_image.jpg"
            elif file_format == "PNG":
                image_data = convert_image(rotated_image, format="PNG")
                filename = "processed_image.png"
            elif file_format == "PDF":
                image_data = convert_image(rotated_image.convert("RGB"), format="PDF")
                filename = "processed_image.pdf"

            download_button(image_data, filename, f"Download {file_format} File")

if __name__ == "__main__":
    main()

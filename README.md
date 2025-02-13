# Watermark App

A watermark application with a **Flask backend** and a **JS frontend** 
that applies a watermark to your image files based on the position and scalesettings provided by the user. The tool takes in two inputs:

1. A watermark image.
2. An image file or a set of image files to which the watermark will be applied.

The user can select the watermark position via a datalist box. Once the settings are chosen, a preview of the output image is displayed and upon pressing the "Submit" button, the processed file is automatically downloaded.

## Features

- **Watermark Position Options**: 
  - Right Top
  - Right Bottom
  - Left Top
  - Left Bottom

- **Watermark Scale**: Adjust the watermark size between 0% and 100% of the original watermark image.

- **Preview**: A preview of the image with the applied watermark will be shown below the datalist box.

- **Download**: After applying the watermark, the processed file will be automatically downloaded.

## Setup

### Backend (Flask)
1. **Clone the Repository**:
   ```
   git clone https://github.com/poujoux/watermark.git
   cd watermark
   ```

2. **Set Up a Virtual Environment and Install Dependencies**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the Flask Server**:
   ```
   flask run
   ```

### Frontend (JavaScript)
1. **Open index.html in your browser or type ```http://localhost:5000``` in the address bar of your browser.***
2. **The frontend will communicate with the Flask backend to fetch weather data.**


## Usage

1. **Select a Watermark Image**:
   - Choose an image that will be used as a watermark.
  
2. **Select Image Files**:
   - Upload the image files you wish to apply the watermark to.
  
3. **Configure Watermark Position and Scale**:
   - Select the watermark position from the options available in the datalist box (`righttop`, `rightbottom`, `lefttop`, `leftbottom`).
   - Adjust the scale percentage of the watermark to be applied on the image. It should be between 0 and 100 with a single space just to the left of the number and a percentage symbol adjacent to the number.

   
4. **Preview**:
   - After filling the inputs and configuring the settings, 32 a preview image will be displayed on a black square(80x80px)depending on the reduction percentage that is applied on a gray squre(20x20px) 32

5. **Submit and Download**:
   - Press the "Submit" button to apply the watermark to the selected files. The processed file will be downloaded automatically.


## License
This project is licensed under the MIT License.

# IDVision

**IDVision** is a desktop application for seamless ID verification and face authentication.  
It leverages [IDAnalyzer](https://www.idanalyzer.com/) for extracting information from both sides of identity documents, then verifies user authenticity with live facial checks.

## Features

- **Dual-Side ID OCR**: Extracts and matches data from front and back of ID cards.
- **ID Verification**: Checks document authenticity and expiration using IDAnalyzer API.
- **Face Verification**: Live webcam face matching with ID photo.
- **Liveness Detection**: Prevents spoofing using blink, expression, and movement checks.
- **Modern OOP Python Codebase**: Easy to extend, integrate, or maintain.

---

## Tech Stack

- **Python 3.7+**
- [PyQt5](https://pypi.org/project/PyQt5/): GUI framework
- [OpenCV](https://opencv.org/): Camera and image processing
- **IDAnalyzer API**: OCR and ID verification
- **Torch / Facenet / VGGFace2**: Face recognition
- Custom liveness modules (blink, face orientation, emotion prediction)

---

## Setup

### 1. Clone the Repo

```sh
git clone https://github.com/your-org/idvision.git
cd idvision
````

### 2. Install Dependencies

You can use pip (preferably in a virtual environment):

```sh
pip install -r requirements.txt
```

Main dependencies (see `requirements.txt`):

* PyQt5
* opencv-python
* torch
* facenet-pytorch (or your face models)
* requests
* python-dotenv

### 3. Configure API Key

Obtain your API key from [IDAnalyzer](https://www.idanalyzer.com/).

Create a `.env` file in your project root:

```
IDANALYZER_API_KEY=your_api_key_here
IDANALYZER_REGION=US
```

### 4. Run the App

```sh
python main.py
```

---

## Usage

1. **Select ID Images:**
   Upload both the front and back images of an ID card.
2. **Extract & Verify:**
   Click the "Verify" button to extract and display information and status.
3. **Face Verification:**
   Proceed to face authentication and liveness checks using your webcam.
4. **Result:**
   The app displays the match status and verification result.

---

## Project Structure

```
idvision/
├── gui/
│   ├── page1_idcard.py   # ID card selection & OCR page
│   ├── page2.py          # Face verification page
│   ├── page3.py          # Liveness challenge page
│   └── utils.py
├── idanalyzer_api.py      # IDAnalyzer API integration class
├── liveness_detection/
│   └── ...               # Blink, emotion, orientation detection
├── verification_models.py # Face verification models
├── main.py               # Main app entry point
├── requirements.txt
└── .env                  # Environment config (not in git)
```

---

## Customization

* **Switching API Providers:**
  Update `idanalyzer_api.py` for a different OCR or KYC provider.
* **Adding Fields:**
  Extend `_extract_fields` in `idanalyzer_api.py` to extract more data.
* **Changing GUI:**
  All screens are in `gui/` as PyQt widgets—extend or restyle as needed.

---

## License

[MIT](LICENSE)
*This project is provided as-is for demo and integration purposes. Always comply with privacy and legal guidelines in your jurisdiction when handling user ID data.*

---

## Credits

* [IDAnalyzer](https://www.idanalyzer.com/) for the KYC API
* [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) for GUI
* [OpenCV](https://opencv.org/) and [Torch](https://pytorch.org/) for face/liveness processing

---

## Contact

For questions or contributions, open an issue or contact the maintainer.

```

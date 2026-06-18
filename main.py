import re
import sys
import json

from PIL import Image
import pytesseract
import numpy as np

class IneReverseOCR:

    def __init__(self, image_path: str):
        self.image_path = image_path
        self.result_content = ""
        self.ocr_cic = ""

    def get_text(self):

        image = Image.open(self.image_path)

        image = image.convert("L")

        img = np.array(image)

        text = pytesseract.image_to_string(
            img,
            config="--oem 3 --psm 6"
        )

        return text

    def extract_cic(self):

        if not self.result_content.strip():
            raise Exception(
                "No se encontraron datos"
            )

        print("=== TEXTO OCR ===")
        print(self.result_content)

        patterns = [
            r"MEX\d{10}",
            r"\d{13}"
        ]

        for pattern in patterns:

            result = re.findall(
                pattern,
                self.result_content
            )

            if result:

                value = result[0]

                if value.startswith("MEX"):
                    value = value.replace(
                        "MEX",
                        ""
                    )

                self.ocr_cic = value
                return

        raise Exception(
            "No se encontró CIC válido"
        )

    def process(self):

        self.result_content = self.get_text()

        self.extract_cic()

        return {
            "message": "ok",
            "data": {
                "ocr_cic": self.ocr_cic
            }
        }


if __name__ == "__main__":    
    if len(sys.argv) != 2:

        print(
            json.dumps(
                {
                    "message": "Uso: python main.py imagen.jpg",
                    "data": {}
                }
            )
        )

        sys.exit(1)

    try:

        processor = IneReverseOCR(
            sys.argv[1]
        )

        response = processor.process()

        print(
            json.dumps(
                response,
                indent=2,
                ensure_ascii=False
            )
        )

    except Exception as e:

        print(
            json.dumps(
                {
                    "message": str(e),
                    "data": {}
                },
                indent=2,
                ensure_ascii=False
            )
        )

        sys.exit(1)

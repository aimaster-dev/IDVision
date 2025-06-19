# idanalyzer_api.py

import requests
import os
import base64

class IDAnalyzerClient:
    def __init__(self, api_key, region="US"):
        assert api_key, "API key required"
        self.api_key = api_key
        self.api_url = (
            "https://api-eu.idanalyzer.com/" if region.upper() == "EU"
            else "https://api.idanalyzer.com/"
        )

    def scan_id(self, front_image_path, back_image_path=None):
        if not os.path.exists(front_image_path):
            raise FileNotFoundError(f"Front image not found: {front_image_path}")

        with open(front_image_path, "rb") as f:
            file_base64 = base64.b64encode(f.read()).decode("utf-8")
        print("back_image_path: ", back_image_path)
        payload = {
            "apikey": self.api_key,
            "file_base64": file_base64,
            "outputmode": "json",
            "dualsidecheck": True if back_image_path else False,
            "verify_expiry": True,
        }

        if back_image_path:
            if not os.path.exists(back_image_path):
                raise FileNotFoundError(f"Back image not found: {back_image_path}")
            with open(back_image_path, "rb") as f2:
                file_back_base64 = base64.b64encode(f2.read()).decode("utf-8")
            payload["file_back_base64"] = file_back_base64

        response = requests.post(self.api_url, data=payload)
        response.raise_for_status()
        data = response.json()
        print("DEBUG IDAnalyzer response:", data)
        return self._extract_fields(data)

    def _extract_fields(self, data):
        # You can customize this further
        doc = data.get("result", {})
        name = doc.get("fullName", "")
        # Optionally, construct name from parts if fullName is missing:
        if not name:
            first = doc.get("firstName", "")
            middle = doc.get("middleName", "")
            last = doc.get("lastName", "")
            name = " ".join(x for x in [first, middle, last] if x)

        address1 = doc.get("address1", "")
        address2 = doc.get("address2", "")
        address = address1
        if address2:
            address = address1 + ", " + address2 if address1 else address2

        return {
            "name": name,
            "dob": doc.get("dob", ""),
            "id_number": doc.get("documentNumber", ""),
            "expiry": doc.get("expiry", ""),
            "address": address,
            "raw": data,
        }
        # return {
        #     "name": result.get("name", ""),
        #     "dob": result.get("dob", ""),
        #     "id_number": result.get("documentNumber", ""),
        #     "expiry": result.get("expiry", ""),
        #     "address": result.get("address", ""),
        #     "raw": data,
        # }
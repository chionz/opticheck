import os
import json
import google.generativeai as genai

from api.core.base.services import Service

GM_API = os.getenv("GEMINI_API")


class AiService(Service):
    '''FAQ service functionality'''

    def create(self):
        pass

    def fetch_all(self):
        pass

    def fetch(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


    def ai_response(self, text: str) -> dict:
        genai.configure(api_key=GM_API)
        """ for m in genai.list_models():
            print(m.name) """

        model = genai.GenerativeModel(model_name="models/gemini-2.5-flash")
        print("Generating response from AI model...", text)

        response = model.generate_content(f"""
                                            You are a friendly digital optometrist assistant. 
                                            Explain the result visual acuity of {text} to the user in a calm, supportive, 
                                            and slightly conversational tone. 

                                            Your structure should be:
                                            1. A short friendly acknowledgment.
                                            2. A simple explanation in plain English.
                                            3. Reassurance.
                                            4. What it means clinically.
                                            5. Gentle advice on next steps.
                                            6. Encouraging closing line.

                                            Avoid sounding robotic or overly formal.
                    """
            
                )


        raw_text = response.text.strip()

        # Remove surrounding code block (e.g. ```json\n...\n```)
        if raw_text.startswith("```") and raw_text.endswith("```"):
            raw_text = raw_text.strip("```").strip()
            if raw_text.startswith("json"):
                raw_text = raw_text[len("json"):].strip()

        return raw_text
        
        


ai_service = AiService()
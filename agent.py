from google import genai
from dotenv import load_dotenv
from google.genai import types
import os, base64

load_dotenv()

class prompts:
  @staticmethod
  def descrpition():
    return """
      Describe this image regarding everything about it. The description must hold which animal it is, 
      in which position it is sitting in, 
      what is the color of all the features of the animal,
      what are its outstanding accessories.
      Make accurate description of the size of the pet within the frame as well using
      pixels as a metric.
    """

  @staticmethod
  def evolution(output, artStyle):
    return f"""You are an AI agent that generates NFT pets.
    Instructions:
    • Always generate a *square* image of a MORE MATURED VERSION of the animal described in the prompt.
    • Ensure the animal looks like a cartoonistic evolution of the user prompted animal.
    • Use the reference of POKEMON for evolution of the animals.
    • Ensure the pet is centered with soft, aesthetic backgrounds.
    Prompt from user: "{output}"
    Art Style: "{artStyle or 'Flat vector cartoon'}"
    """

class Agent:
    @staticmethod
    def describe(file_path):
        API = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=API)
        my_file = client.files.upload(file=file_path)
        desc = prompts.descrpition()
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[my_file, desc],
        )
        return response.text

    @staticmethod
    def evolve(file_path, art_style):
        API = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=API)

        image_description = Agent.describe(file_path)
        prompt = prompts.evolution(image_description, art_style)

        response = client.models.generate_images(
            model="imagen-4.0-generate-preview-06-06",
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1)
        )

        img_bytes = response.generated_images[0].image.image_bytes
        return img_bytes

from google import genai
from dotenv import load_dotenv
from google.genai import types
import os, base64

load_dotenv()

class prompts:
  @staticmethod
  def descrpition(animal):
    return f"""
      You have been given an image of a {animal}.
      Describe this image regarding everything about it. The decription must hold which animal it is, 
      in which position it is sitting in, 
      what is the color of all the features of the animal.
      Including the accessories of the animal is ABSOLUTELY NESSESARY!!
      Make accurate description of the size of the pet within the frame as well using pixels as a metrics
    """

  @staticmethod
  def evolution(output, artStyle,animal):
    return f"""
    You are an AI agent that generates NFT pets.
    Instructions:
    •⁠  ⁠Always generate a *square* image that is JUST A LITTLE MORE MATURED VERSION of the {animal} described in the prompt.
    •⁠  The generated image should look JUST A FEW YEARS older than the orignal image, without loosing its core features.
    •⁠  ⁠Ensure the animal looks like a cartoonistic evolution of the user prompted animal.
    •⁠  ⁠Ensure the pet is centered with soft, aesthetic backgrounds (minimal, pastel, or abstract).
    •⁠  ⁠Make the pet visually unique and collectible — suitable for OpenSea-style NFT marketplaces.
    Prompt from user: "{output}"
    Art Style: "{artStyle}"
    If no art style is specified:
    •⁠  ⁠Default to popular NFT art styles like:
      - Flat vector cartoon
      - Cute hand-drawn sketch
      - Watercolor illustration
      - Soft pixel art
    •⁠  ⁠Avoid 3D realism unless explicitly requested.
    •⁠  ⁠Avoid photographic or lifelike rendering.

    If the user specifies a style, *strictly follow it*, but still ensure the result looks collectible, visually pleasing, and uniquely stylized.
    Generate a high-quality, aesthetic image in the standard collectible NFT format."
    """

class Agent:
    @staticmethod
    def describe(file_path,animal):
        API = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=API)
        my_file = client.files.upload(file=file_path)
        desc = prompts.descrpition(animal)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[my_file, desc],
        )
        return response.text

    @staticmethod
    def evolve(file_path, art_style,animal):
        API = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=API)

        image_description = Agent.describe(file_path,animal)
        prompt = prompts.evolution(image_description, art_style,animal)

        response = client.models.generate_images(
            model="imagen-4.0-generate-preview-06-06",
            prompt=prompt,
            config=types.GenerateImagesConfig(number_of_images=1)
        )

        img_bytes = response.generated_images[0].image.image_bytes
        return img_bytes

import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the model from Hugging Face Hub 
# See https://huggingface.co/Salesforce/blip-image-captioning-large for more details

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")


# image captioning
def caption_image(image_path):
    """Generate image caption"""

    # Load the image, convert it to RGB and generate caption using the model
    raw_image = Image.open(image_path).convert('RGB')
    inputs = processor(raw_image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)
    caption = caption.capitalize() + "." # Capitalize the first letter and add a period

    return caption

if __name__ == "__main__":
    # Test the caption_image function
    image_path = "static/images/dog-puppy-on-garden.jpg"
    caption = caption_image(image_path)
    print(caption)
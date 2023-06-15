import os
import urllib
import random
import replicate

USERNAME = 'tostangs'
MODEL_NAME = 'cby1'
MODEL_SLUG = f'{USERNAME}/{MODEL_NAME}'

# Grab the model from replicate
model = replicate.models.get(MODEL_SLUG)
# Grab the latest version
version = model.versions.list()[0]
print(model.versions.list())

NEGATIVE_PROMPT = "cartoon, blurry, deformed, watermark, dark lighting, image caption, caption, text, cropped, low quality, low resolution, malformed, messy, blurry, watermark"

def download_prompt(prompt, negative_prompt=NEGATIVE_PROMPT, num_outputs=1):
    print("=====================================================================")
    print("prompt:", prompt)
    print("negative_prompt:", negative_prompt)
    print("num_outputs:", num_outputs)
    print("=====================================================================")
    image_urls = version.predict(
        prompt=prompt,
        width=512,
        height=512,
        negative_prompt=negative_prompt,
        num_outputs=num_outputs,
    )
    for url in image_urls:
        img_id = url.split("/")[4][:6]
        prompt = prompt.replace(" ", "-").replace(",", "").replace(".", "-")
        out_file = f"data/{MODEL_NAME}/{img_id}--{prompt}"[:200]
        out_file = out_file + ".jpg"

        # if folder doesn't exist, create it
        os.makedirs(os.path.dirname(out_file), exist_ok=True)

        print("Downloading to", out_file)
        urllib.request.urlretrieve(url, out_file)
    print("=====================================================================")

with open('prompts.txt', 'r') as f:
    lines = f.readlines()

prompts_list = []
for line in lines:
    if line.startswith("p - "):
        prompts_list.append((line[4:].strip(), NEGATIVE_PROMPT))
    elif line.startswith("np - "):
        try:
            prompts_list[-1] = (prompts_list[-1][0], line[5:].strip())
        except IndexError:
            pass  # Ignore negative_prompt if there is no prompt yet
random.shuffle(prompts_list)

# loop 10 times, generate 100 images
for i in range(10):
    for prompt, negative_prompt in prompts_list:
        download_prompt(prompt, negative_prompt)

# PROMPTS = [
#     "Adorably cute bella dog portrait, artstation winner by Victo Ngai, Kilian Eng and by Jake Parker, vibrant colors, winning-award masterpiece, fantastically gaudy, aesthetic octane render, 8K HD Resolution",
#     "Incredibly cute golden retriever bella dog portrait, artstation winner by Victo Ngai, Kilian Eng and by Jake Parker, vibrant colors, winning-award masterpiece, fantastically gaudy, aesthetic octane render, 8K HD Resolution",
#     "a high quality painting of a very cute golden retriever bella dog puppy, friendly, curious expression. painting by artgerm and greg rutkowski and alphonse mucha ",
#     "magnificent bella dog portrait masterpiece work of art. oil on canvas. Digitally painted. Realistic. 3D. 8k. UHD.",
#     "intricate five star bella dog facial portrait by casey weldon, oil on canvas, hdr, high detail, photo realistic, hyperrealism, matte finish, high contrast, 3 d depth, centered, masterpiece, vivid and vibrant colors, enhanced light effect, enhanced eye detail, artstationhd ",
#     "a portrait of a bella dog in a scenic environment by mary beale and rembrandt, royal, noble, baroque art, trending on artstation ",
#     "a painted portrait of a bella dog with brown fur, no white fur, wearing a sea captain's uniform and hat, sea in background, oil painting by thomas gainsborough, elegant, highly detailed, anthro, anthropomorphic dog, epic fantasy art, trending on artstation, photorealistic, photoshop, behance winner ",
#     "bella dog guarding her home, dramatic sunset lighting, mat painting, highly detailed, ",
#     "bella dog, realistic shaded lighting poster by ilya kuvshinov katsuhiro otomo, magali villeneuve, artgerm, jeremy lipkin and michael garmash and rob rey ",
#     "a painting of a bella dog dog, greg rutkowski, cinematic lighting, hyper realistic painting",
# ]
output = replicate.run(
    "conorbyrnes04/matrka_glyph_1:bce3b7b3017a5ad64f2b43c8bdaec606a4f64e8a5e0671243a9f53e9c37a7e75",
    input={
        "model": "dev",
        "go_fast": False,
        "lora_scale": 1,
        "megapixels": "1",
        "num_outputs": 1,
        "aspect_ratio": "1:1",
        "output_format": "webp",
        "guidance_scale": 3,
        "output_quality": 80,
        "prompt_strength": 0.8,
        "extra_lora_scale": 1,
        "num_inference_steps": 28
    }
)

# To access the file URL:
print(output[0].url())
#=> "http://example.com"

# To write the file to disk:
with open("my-image.png", "wb") as file:
    file.write(output[0].read())
import pandas as pd
from transformers import pipeline
from transformers import FlaxGPT2LMHeadModel, GPT2Tokenizer
import jax
import jax.numpy as jnp

# Încarcă modelul Flax GPT-2 și tokenizer-ul
model_name = "gpt2"  # Folosim GPT-2 care este disponibil în Flax
model = FlaxGPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Setăm pad_token_id pentru GPT-2
tokenizer.pad_token = tokenizer.eos_token

race_dict = {
    "BEN": "Bengal",
    "SBI": "Birman",
    "BRI": "British Shorthair",
    "CHA": "Chartreux",
    "EUR": "European",
    "MCO": "Maine coon",
    "PER": "Persian",
    "RAG": "Ragdoll",
    "SPH": "Sphynx",
    "SAV": "Savannah",  #nu exista mentionata SVA
    "ORI": "Sphynx",
    "TUV": "Turkish angora",
    "Autre": "No Breed/ Other",
    "NSP": "Unkown"
}

def generate_breed_description(breed_code):
    if breed_code not in race_dict:
        return "Rasa de pisică nu este recunoscută."

    breed_name = race_dict[breed_code]

    # Construim promptul pentru generarea descrierii
    prompt = f"Tell me the most important traits of {breed_name} cats."


    # Tokenizăm promptul
    inputs = tokenizer(prompt, return_tensors="jax", padding=True, truncation=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    # Generăm text folosind modelul
    outputs = model.generate(input_ids, 
                             attention_mask=attention_mask, 
                             max_length=150,  # Limităm lungimea la 100 de tokenuri
                             pad_token_id=tokenizer.pad_token_id,
                             do_sample=True,  # Permitem generarea aleatorie a textului
                             temperature=0.5,  # Temperatura mai scăzută pentru mai puțină aleatorizare
                             top_p=0.85,        # top_p mai scăzut pentru a reduce diversitatea extreme
                             top_k=50,         # Setăm top_k pentru limitarea alegerii
                             num_return_sequences=1)  # Doar o secvență generată

    # Extragem doar tokenii generati
    generated_tokens = outputs.sequences[0]  # accesează secvența generată

    # Decodificăm tokenii în text
    generated_text = tokenizer.decode(generated_tokens, skip_special_tokens=True)

    # Înlăturăm promptul pentru a lăsa doar descrierea generată
    description = generated_text.replace(prompt, "").strip()

    return description

print(generate_breed_description("PER"))








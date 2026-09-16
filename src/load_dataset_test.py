from datasets import load_dataset

# Example: Let's load a small language split or check available configurations 
# (UniMorph data is structured cleanly by language codes like 'eng', 'spa', 'swe')
try:
    # If loading a specific mirror/subset from Hugging Face:
    dataset = load_dataset("unimorph/universal_morphologies", "eng", split="train", streaming=True)
    
    # Grab just the first 5 rows to see what it looks like
    print("Successfully connected to Hugging Face dataset!")
    for i, sample in enumerate(dataset):
        print(sample)
        if i >= 4:
            break
except Exception as e:
    print("Note: If the repo structure requires a specific subset name, you can fallback to local TSV files. Error:", e)
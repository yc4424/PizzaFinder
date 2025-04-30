# Pizza Finder.app

A Streamlit app that recommends pizza spots tailored to your taste. Upload a photo of a pizza, describe the flavors you like, and get personalized results powered by OpenAI and the Yelp API.

---

## 🔍 Features

- **Image Agent** (GPT-4o): Extracts ≥10 visual tags and a 2–3 sentence review from a pizza photo.  
- **Flavor Agent** (GPT-4): Parses your text description into a JSON flavor profile (cheesiness, spiciness, etc.).  
- **Recommendation Engine**: Searches Yelp for pizza shops using your visual tags and flavor profile, then aggregates and deduplicates the results
- **Summary Agent** (GPT-4): Combines the visual tags and flavor characteristics with the shops found by the Recommendation Engine to produce a matched summary for each recommended spot.
- **Interactive UI**: Built in Streamlit—no boilerplate UI code required.

---

## 📋 Prerequisites

- **Python 3.8+**  
- **pip** package manager  
- **Yelp API key** (get one at https://www.yelp.com/developers)  
- **OpenAI API key** (get one at https://platform.openai.com)

---

## 🚀 Installation & Setup

1. **Unzip** the submission archive and open a terminal in its root folder.  
2. **(Optional)** Create & activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate       # Windows
   ```

3. **Install** the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure** your API keys. In your shell, run:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export YELP_API_KEY="your_yelp_api_key"
   ```

   > **Tip:** The code reads these values from environment variables.  
   > Hard-coding keys in `pizzafinder.py` is possible but less secure.

---

## ▶️ Running the App

1. **Launch** the app:
   ```bash
   streamlit run pizzafinder.py
   ```
2. **Open** your browser at `http://localhost:8501`.  
3. **Upload** a pizza image (JPG/PNG).  
4. **Describe** your pizza experience in the text box (e.g., “crispy thin crust with extra cheese and a hint of spice”).  
5. **Enter** a location (e.g., `Manhattan, NY`) and adjust the search radius slider.  
6. **Click** **Search for Pizza Places**. This step processes your image & description—when done, you’ll see **“Data processed successfully!”**.  
7. **Browse** the recommended pizza spots listed below.

---

## 🗂️ Project Structure

```
pizza-finder.zip  
├── pizzafinder.py       # Main Streamlit application  
├── requirements.txt     # Python dependencies (streamlit, openai, requests)  
├── README.md            # This installation & usage guide  
└── assets/              # (optional) sample images or extra files  
```

---

## 📝 Sample Workflow

1. **Upload** your favorite slice.  
2. **Type**:
   ```
   I love a chewy, slightly charred crust, extra mozzarella, herb-forward sauce, and a touch of heat.
   ```
3. **Set** Location: `Manhattan, NY`  
4. **Set** Radius: `3 miles`  
5. **Click** **Search for Pizza Places** and watch for **“Data processed successfully!”**.  
6. **Explore** your personalized pizza recommendations! 🍕

---

## 📄 License

This project is released under the **MIT License**. Feel free to fork, modify, and share!


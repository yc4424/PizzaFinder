# PizzaFinder
```markdown

A Streamlit app that helps you discover pizza places tailored to your taste. Upload a photo of a pizza, describe the flavors you like, and get personalized recommendations from Yelp.

---

## 🚀 Features

- **Image Agent**: Uses OpenAI vision model (GPT-4o) to extract detailed pizza tags and a short review.
- **Flavor Agent**: Uses GPT-4 to parse your text description into flavor profiles (cheesiness, spiciness, etc.).
- **Recommendation Engine**: Searches Yelp API for pizza spots matching your tags & flavor profile.
- **Interactive UI**: Built with Streamlit—upload image, enter text, adjust location & radius.

---

## 🛠️ Prerequisites

- **Python** 3.8 or higher  
- **pip** (Python package manager)  
- **Yelp API key**  
- **OpenAI API key**

---

## 📥 Installation

1. **Unzip** the project archive.  
2. **(Optional)** Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install** required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set** your API keys as environment variables:

   ```bash
   export OPENAI_API_KEY="your_openai_key_here"
   export YELP_API_KEY="your_yelp_key_here"
   ```

5. **Run** the Streamlit app:

   ```bash
   streamlit run pizzafinder.py
   ```

   > If your main file is named differently (e.g. `streamlit_app.py`), replace `pizzafinder.py` accordingly.

---

## 🎯 Usage

1. **Open** your browser to `http://localhost:8501`.  
2. **Upload** a pizza image (JPG/PNG).  
3. **Describe** your pizza experience in the text box (e.g. “crispy thin crust with extra cheese and a hint of spice”).  
4. When you see **“Data processed successfully!”**, scroll down to **Find Top Pizza Places Nearby**.  
5. **Enter** a location (e.g. “Manhattan, NY”) and adjust the search radius slider.  
6. **Click** “Search for Pizza Places” and explore your personalized recommendations!

---

## 📄 Sample Input

- **Image**: Any clear photo of your favorite slice.  
- **Text**:
  ```
  I love a chewy, slightly charred crust with melty mozzarella, a touch of herbiness, and medium spiciness from pepper flakes.
  ```
- **Location**: `Manhattan, NY`  
- **Radius**: `3 miles`

---

## 📁 Project Structure

```
├── pizzafinder.py        # Main Streamlit app
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # (optional) license file
└── assets/               # (optional) sample images or data
```

---

## ⚖️ License

This project is licensed under the MIT License. Feel free to use and modify!

---

Enjoy discovering your next favorite pizza spot! 🍕  
```

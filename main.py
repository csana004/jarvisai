import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import datetime
import random
from tkinter import *
from tkinter import messagebox
import nltk
from textblob import TextBlob
from newspaper import Article
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import requests


def say(text):
    """Speaks the provided text using pyttsx3."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def takeCommand():
    r = sr.Recognizer()  # Create a recognizer object
    with sr.Microphone(
    ) as source:  # Use Microphone() as source within the with block
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            query = r.recognize_google_cloud(audio, language="en-in")
            print(f"user said: {query}")  # Corrected formatting
            return query  # Return the recognized text
        except Exception as e:
            print("Some Error Occured:", e)
            return None  # Indicate speech recognition error


def clean_query(query):
    return query.strip().rstrip('?').strip()


def summarize_text(text, max_length=1500):
    if len(text) > max_length:
        return text[:max_length].rsplit(' ', 1)[0] + '...'
    return text


def get_vals(operation, inputvalue, inputvalue2, output_label):
    try:
        num1 = float(inputvalue.get())
        num2 = float(inputvalue2.get())
        if operation == "addition":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "division":
            if num2 == 0:
                result = "Error: Cannot divide by zero"
            else:
                result = num1 / num2
        else:
            result = "Invalid operation"
        output_label.config(text=f"Output: {result}")
    except ValueError:
        output_label.config(text="Error: Invalid input")


def get_24hr_clock(output_label):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%H:%M:%S")
    output_label.config(text=f"Output: {formatted_time} (24hr)")


def get_12hr_clock(output_label):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%I:%M:%S %p")
    output_label.config(text=f"Output: {formatted_time} (12hr)")


def get_temperature(output_label):
    temp_value_window = Toplevel()
    temp_value_window.title("Temperature Input")
    temp_value_window.geometry("300x200")
    temp_value_window.geometry("500x500")
    temp_value_window.configure(bg='#f0f0f0')

    Label(temp_value_window, text="Enter temperature value:",
          bg='#f0f0f0').pack(pady=5)
    temp_value_entry = Entry(temp_value_window)
    temp_value_entry.pack(pady=5)

    Label(temp_value_window,
          text="Enter current unit (C, F, or K):",
          bg='#f0f0f0').pack(pady=5)
    temp_unit_entry = Entry(temp_value_window)
    temp_unit_entry.pack(pady=5)

    Label(temp_value_window,
          text="Enter target unit (C, F, or K):",
          bg='#f0f0f0').pack(pady=5)
    target_unit_entry = Entry(temp_value_window)
    target_unit_entry.pack(pady=5)

    def get_temp_and_convert():
        try:
            temp_value = float(temp_value_entry.get())
            temp_unit = temp_unit_entry.get().upper()
            target_unit = target_unit_entry.get().upper()
            convert_temperature(temp_value, temp_unit, target_unit,
                                output_label)
            temp_value_window.destroy()
        except ValueError:
            output_label.config(text="Error: Invalid temperature value")

    Button(temp_value_window,
           text="Submit",
           command=get_temp_and_convert,
           bg="#4CAF50",
           fg="white").pack(pady=10)
    temp_value_window.mainloop()


def convert_temperature(temp_value, temp_unit, target_unit, output_label):
    if temp_unit == target_unit:
        converted_temp = temp_value
    elif temp_unit == "C":
        if target_unit == "F":
            converted_temp = (temp_value * 9 / 5) + 32
        elif target_unit == "K":
            converted_temp = temp_value + 273.15
        else:
            output_label.config(text="Error: Invalid target unit")
            return
    elif temp_unit == "F":
        if target_unit == "C":
            converted_temp = (temp_value - 32) * 5 / 9
        elif target_unit == "K":
            converted_temp = (temp_value - 32) * 5 / 9 + 273.15
        else:
            output_label.config(text="Error: Invalid target unit")
            return
    elif temp_unit == "K":
        if target_unit == "C":
            converted_temp = temp_value - 273.15
        elif target_unit == "F":
            converted_temp = (temp_value - 273.15) * 9 / 5 + 32
        else:
            output_label.config(text="Error: Invalid target unit")
            return
    else:
        output_label.config(text="Error: Invalid temperature unit")
        return
    output_label.config(text=f"Output: {converted_temp} °{target_unit}")


def simple_interest(output_label):
    si_value_window = Toplevel()
    si_value_window.title("Simple Interest Input")
    si_value_window.geometry("300x250")
    si_value_window.geometry("500x500")
    si_value_window.configure(bg='#f0f0f0')

    Label(si_value_window, text="Enter principal:", bg='#f0f0f0').pack(pady=5)


def compound_interest(output_label):
    ci_value_window = Toplevel()
    ci_value_window.title("Compound Interest Input")
    ci_value_window.geometry("300x300")
    ci_value_window.geometry("500x500")
    ci_value_window.configure(bg='#f0f0f0')

    Label(ci_value_window, text="Enter principal:", bg='#f0f0f0').pack(pady=5)
    ci_principal_entry = Entry(ci_value_window)
    ci_principal_entry.pack(pady=5)

    Label(ci_value_window, text="Enter time in months:",
          bg='#f0f0f0').pack(pady=5)
    ci_time_entry = Entry(ci_value_window)
    ci_time_entry.pack(pady=5)

    Label(ci_value_window, text="Enter rate of interest:",
          bg='#f0f0f0').pack(pady=5)
    ci_rate_entry = Entry(ci_value_window)
    ci_rate_entry.pack(pady=5)

    Label(ci_value_window,
          text="Enter no. of times interest is compounded per year:",
          bg='#f0f0f0').pack(pady=5)
    ci_n_entry = Entry(ci_value_window)
    ci_n_entry.pack(pady=5)

    def calculate_ci():
        try:
            principal = float(ci_principal_entry.get())
            time = float(ci_time_entry.get())
            rate = float(ci_rate_entry.get())
            n = float(ci_n_entry.get())
            ci = principal * (1 + rate / (n * 100))**(n * time)
            output_label.config(
                text=
                f"Output: Compound Interest is Rs {ci - principal}\nAmount after adding CI is Rs {ci}"
            )
            ci_value_window.destroy()
        except ValueError:
            output_label.config(text="Error: Invalid input for CI calculation")

    Button(ci_value_window,
           text="Submit",
           command=calculate_ci,
           bg="#4CAF50",
           fg="white").pack(pady=10)
    ci_value_window.mainloop()


def unit_conversion(output_label):
    conversion_window = Toplevel()
    conversion_window.title("Unit Conversion")
    conversion_window.geometry("500x500")
    conversion_window.configure(bg='#f0f0f0')

    Label(conversion_window, text="Choose conversion type:",
          bg='#f0f0f0').pack(pady=5)
    conversion_type = StringVar(value="Length")

    Radiobutton(conversion_window,
                text="Length",
                variable=conversion_type,
                value="Length",
                bg='#f0f0f0').pack(anchor=W)
    Radiobutton(conversion_window,
                text="Weight",
                variable=conversion_type,
                value="Weight",
                bg='#f0f0f0').pack(anchor=W)
    Radiobutton(conversion_window,
                text="Money",
                variable=conversion_type,
                value="Money",
                bg='#f0f0f0').pack(anchor=W)

    Label(conversion_window, text="Enter value to convert:",
          bg='#f0f0f0').pack(pady=5)
    value_entry = Entry(conversion_window)
    value_entry.pack(pady=5)

    Label(conversion_window, text="Enter current unit:",
          bg='#f0f0f0').pack(pady=5)
    current_unit_entry = Entry(conversion_window)
    current_unit_entry.pack(pady=5)

    Label(conversion_window, text="Enter target unit:",
          bg='#f0f0f0').pack(pady=5)
    target_unit_entry = Entry(conversion_window)
    target_unit_entry.pack(pady=5)

    def convert_units():
        try:
            value = float(value_entry.get())
            current_unit = current_unit_entry.get().upper()
            target_unit = target_unit_entry.get().upper()
            conversion_type_value = conversion_type.get()

            if conversion_type_value == "Length":
                result = convert_length(value, current_unit, target_unit)
            elif conversion_type_value == "Weight":
                result = convert_weight(value, current_unit, target_unit)
            elif conversion_type_value == "Money":
                result = convert_money(value, current_unit, target_unit)
            else:
                result = "Error: Invalid conversion type"

            output_label.config(text=f"Output: {result}")
            conversion_window.destroy()
        except ValueError:
            output_label.config(
                text="Error: Invalid input for unit conversion")

    Button(conversion_window,
           text="Submit",
           command=convert_units,
           bg="#4CAF50",
           fg="white").pack(pady=10)
    conversion_window.mainloop()


def convert_length(value, current_unit, target_unit):
    length_units = {
        "m": 1,
        "km": 1000,
        "cm": 0.01,
        "mm": 0.001,
        "inches": 0.0254,
        "ft": 0.3048,
        "yards": 0.9144,
        "mili inches": 1609.34
    }
    if current_unit in length_units and target_unit in length_units:
        result = value * length_units[target_unit] / length_units[current_unit]
        return f"{value} {current_unit} is {result} {target_unit}"
    else:
        return "Error: Invalid length unit"


def convert_weight(value, current_unit, target_unit):
    weight_units = {
        "kg": 1,
        "g": 0.001,
        "mg": 0.000001,
        "lb": 0.453592,
        "oz": 0.0283495
    }
    if current_unit in weight_units and target_unit in weight_units:
        result = value * weight_units[target_unit] / weight_units[current_unit]
        return f"{value} {current_unit} is {result} {target_unit}"
    else:
        return "Error: Invalid weight unit"


def convert_money(value, current_unit, target_unit):
    # Note: In a real application, you would use an API to get the latest exchange rates.
    # Here, we use some example rates for demonstration purposes.
    exchange_rates = {
        "USD": 1,
        "EUR": 0.85,
        "GBP": 0.75,
        "INR": 74.57,
        "JPY": 110.62,
        "CNY": 6.45
    }
    if current_unit in exchange_rates and target_unit in exchange_rates:
        result = value * exchange_rates[target_unit] / exchange_rates[
            current_unit]
        return f"{value} {current_unit} is {result} {target_unit}"
    else:
        return "Error: Invalid currency unit"


def open_calculator():
    root = Tk()
    root.title("Calculation Application")
    root.geometry("600x700")
    root.geometry("700x700")
    root.configure(bg='#e0e0e0')

    title_frame = Frame(root, bg="#3E4149", relief=RAISED, bd=2)
    title_frame.pack(side=TOP, fill="x")
    title_label = Label(title_frame,
                        text="Calculation Application",
                        bg="#3E4149",
                        fg="white",
                        font=("Helvetica", 16))
    title_label.pack(pady=10)

    input_frame = Frame(root, bg="#f0f0f0", bd=2, relief=SUNKEN)
    input_frame.pack(pady=10, padx=10, fill="x")

    Label(input_frame,
          text="Input the first value:",
          bg="#f0f0f0",
          font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
    inputvalue = DoubleVar()
    Entry(input_frame, textvariable=inputvalue,
          font=("Helvetica", 12)).grid(row=0, column=1, padx=5, pady=5)

    Label(input_frame,
          text="Input the second value:",
          bg="#f0f0f0",
          font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
    inputvalue2 = DoubleVar()
    Entry(input_frame, textvariable=inputvalue2,
          font=("Helvetica", 12)).grid(row=1, column=1, padx=5, pady=5)

    output_frame = Frame(root, bg="#f0f0f0", bd=2, relief=SUNKEN)
    output_frame.pack(pady=10, padx=10, fill="x")

    output_label = Label(output_frame,
                         text="",
                         bg="#f0f0f0",
                         font=("Helvetica", 12))
    output_label.pack(pady=10)

    button_frame = Frame(root, bg="#e0e0e0")
    button_frame.pack(pady=10)

    button_options = [
        ("Addition",
         lambda: get_vals("addition", inputvalue, inputvalue2, output_label)),
        ("Subtract",
         lambda: get_vals("subtract", inputvalue, inputvalue2, output_label)),
        ("Multiply",
         lambda: get_vals("multiply", inputvalue, inputvalue2, output_label)),
        ("Division",
         lambda: get_vals("division", inputvalue, inputvalue2, output_label)),
        ("24hr Clock", lambda: get_24hr_clock(output_label)),
        ("12hr Clock", lambda: get_12hr_clock(output_label)),
        ("Temperature", lambda: get_temperature(output_label)),
        ("Simple Interest", lambda: simple_interest(output_label)),
        ("Compound Interest", lambda: compound_interest(output_label)),
        ("Unit Conversion", lambda: unit_conversion(output_label)),
    ]

    for text, command in button_options:
        Button(button_frame,
               text=text,
               command=command,
               bg="#4CAF50",
               fg="white",
               width=20,
               font=("Helvetica", 12)).pack(pady=5)

    root.mainloop()


def rock_paper():
    user_choice = ""
    while user_choice not in ("rock", "paper", "scissors"):
        say("Choose rock, paper, or scissors:")
        # Get user choice (speak or type)
        user_choice = listen_or_type()

    computer_choice = random.choice(["rock", "paper", "scissors"])
    print(f"You chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")

    # Determine the winner (use a dictionary for easier readability)
    winner_map = {
        "rock": {
            "scissors": "Rock smashes scissors! You win!",
            "paper": "Paper covers rock! You lose."
        },
        "paper": {
            "rock": "Paper covers rock! You win!",
            "scissors": "Scissors cuts paper! You lose."
        },
        "scissors": {
            "paper": "Scissors cuts paper! You win!",
            "rock": "Rock smashes scissors! You lose."
        }
    }

    if user_choice == computer_choice:
        say("It's a tie!")
    else:
        say(winner_map[user_choice][computer_choice])


def open_camera():
    """Opens the default camera application."""
    try:
        # Use the appropriate command for your operating system
        if os.name == 'nt':  # Windows
            os.system('start microsoft.windows.camera:')
        elif os.name == 'posix':  # Linux or macOS
            os.system('open /Applications/Photo Booth.app'
                      )  # Replace with your default camera app if needed
        else:
            print("Camera access not supported on your operating system.")
    except Exception as e:
        print(f"Error opening camera: {e}")


def analyze():
    nltk.download('punkt')

    # Function to fetch article and analyze sentiment
    def fetch_article():
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        # Reset previous content
        clear_content()

        # Start the progress bar
        progress_bar.start()

        def fetch_and_analyze():
            try:
                article = Article(url)
                article.download()
                article.parse()
                article.nlp()

                title_var.set(f"Title: {article.title}")

                # Display authors in a frame
                authors_var.set(f"Authors: {', '.join(article.authors)}")
                authors_label.config(text=authors_var.get())

                # Display publication date in a frame
                pub_date_var.set(f"Publication Date: {article.publish_date}")
                pub_date_label.config(text=pub_date_var.get())

                # Display summary in a frame
                summary_var.set(f"Summary: {article.summary}")
                summary_label.config(text=summary_var.get())

                # Analyze sentiment
                analysis = TextBlob(article.text)
                polarity = analysis.polarity
                sentiment = "positive" if polarity > 0 else "negative" if polarity < 0 else "neutral"
                sentiment_var.set(
                    f"Sentiment: {sentiment} (Polarity: {polarity:.2f})")
                sentiment_label.config(text=sentiment_var.get())

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

            finally:
                # Stop the progress bar
                progress_bar.stop()

        # Run the fetching and analysis in a separate thread
        threading.Thread(target=fetch_and_analyze).start()

    def clear_content():
        # Clear all labels
        title_var.set("")
        authors_var.set("")
        pub_date_var.set("")
        summary_var.set("")
        sentiment_var.set("")

    # Set up the Tkinter window
    root = tk.Tk()
    root.title("Scrollable Article Sentiment Analyzer")
    root.title("Article Analyzer")

    # Styling
    root.geometry("800x600")  # Set initial window size
    root.configure(bg="#f0f0f0")  # Set background color

    # URL entry
    url_label = tk.Label(root,
                         text="Enter Article URL:",
                         bg="#f0f0f0",
                         font=("Arial", 12))
    url_label.pack(pady=(20, 5))
    url_entry = tk.Entry(root, width=80, font=("Arial", 12))
    url_entry.pack(pady=5)

    # Fetch button
    fetch_button = tk.Button(root,
                             text="Fetch and Analyze",
                             command=fetch_article,
                             bg="#4CAF50",
                             fg="white",
                             font=("Arial", 12))
    fetch_button.pack(pady=10)

    # Clear button
    clear_button = tk.Button(root,
                             text="Clear",
                             command=clear_content,
                             bg="#f44336",
                             fg="white",
                             font=("Arial", 12))
    clear_button.pack(pady=10)

    # Create a frame to hold the canvas and scrollbars
    scrollable_frame = tk.Frame(root, bg="#e0e0e0", padx=20, pady=20)
    scrollable_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    # Horizontal scrollbar
    xscrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.HORIZONTAL)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    # Vertical scrollbar
    yscrollbar = ttk.Scrollbar(scrollable_frame, orient=tk.VERTICAL)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Canvas to hold labels
    canvas = tk.Canvas(scrollable_frame,
                       bg="#e0e0e0",
                       highlightthickness=0,
                       xscrollcommand=xscrollbar.set,
                       yscrollcommand=yscrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure scrollbars to work with canvas
    xscrollbar.config(command=canvas.xview)
    yscrollbar.config(command=canvas.yview)

    # Frame inside canvas to contain labels
    content_frame = tk.Frame(canvas, bg="#e0e0e0")
    canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)

    # Title label
    title_var = tk.StringVar()
    title_label = tk.Label(content_frame,
                           textvariable=title_var,
                           wraplength=700,
                           justify='left',
                           font=("Arial", 14, "bold"),
                           bg="#e0e0e0")
    title_label.pack(pady=(0, 10), anchor=tk.W)

    # Frame for publication date
    pub_date_var = tk.StringVar()
    pub_date_frame = tk.Frame(content_frame, bg="#e0e0e0")
    pub_date_frame.pack(pady=(0, 10), anchor=tk.W)
    pub_date_label = tk.Label(pub_date_frame,
                              textvariable=pub_date_var,
                              wraplength=700,
                              justify='left',
                              font=("Arial", 12),
                              bg="#e0e0e0")
    pub_date_label.pack()

    # Frame for authors
    authors_var = tk.StringVar()
    authors_frame = tk.Frame(content_frame, bg="#e0e0e0")
    authors_frame.pack(pady=(0, 10), anchor=tk.W)
    authors_label = tk.Label(authors_frame,
                             textvariable=authors_var,
                             wraplength=700,
                             justify='left',
                             font=("Arial", 12),
                             bg="#e0e0e0")
    authors_label.pack()

    # Frame for summary
    summary_var = tk.StringVar()
    summary_frame = tk.Frame(content_frame, bg="#e0e0e0")
    summary_frame.pack(pady=(0, 10), anchor=tk.W)
    summary_label = tk.Label(summary_frame,
                             textvariable=summary_var,
                             wraplength=700,
                             justify='left',
                             font=("Arial", 12),
                             bg="#e0e0e0")
    summary_label.pack()

    # Frame for sentiment analysis
    sentiment_var = tk.StringVar()
    sentiment_frame = tk.Frame(content_frame, bg="#e0e0e0")
    sentiment_frame.pack(pady=(0, 10), anchor=tk.W)
    sentiment_label = tk.Label(sentiment_frame,
                               textvariable=sentiment_var,
                               wraplength=700,
                               justify='left',
                               font=("Arial", 12),
                               bg="#e0e0e0")
    sentiment_label.pack()

    # Update canvas scroll region
    def update_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    content_frame.bind("<Configure>", update_scroll_region)

    # Progress bar
    progress_bar = ttk.Progressbar(root, mode="indeterminate")
    progress_bar.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()


def listen_or_type():
    while True:
        # Ask the user if they want to speak or type
        say("How would you like to give your command? Speak or type?")
        print("speak or type?")
        choice = input().lower()
        if choice in ("speak", "type"):
            break
        else:
            say("Invalid choice. Please say 'speak' or 'type'.")

    if choice == "speak":
        return takeCommand()
    else:
        # Get user input from the console
        print("Type your command:")
        return input()  # Get input from standard input


def fetch_wikipedia_data(query):

    def clean_query(query):
        """Remove common punctuation and extra spaces."""
        return query.strip().rstrip('?').strip()

    def summarize_text(text, max_length=1500):
        """Summarize the text to the specified maximum length."""
        if len(text) > max_length:
            return text[:max_length].rsplit(' ', 1)[0] + '...'
        return text

    def search_wikipedia(query):
        """Search Wikipedia for the given query and return the page title."""
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "srlimit": 1
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            search_results = data.get("query", {}).get("search", [])
            if not search_results:
                return "Sorry, I couldn't find any relevant information."
            return search_results[0]["title"]
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            return f"Request error occurred: {req_err}"
        except Exception as err:
            return f"An error occurred: {err}"

    def fetch_wikipedia_summary(title):
        """Fetch the summary of the Wikipedia page."""
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if 'extract' in data:
                summary = data['extract']
                if len(summary) < 200:
                    return fetch_wikipedia_full_article(title)
                return summarize_text(summary)
            return "No summary available for this page."
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            return f"Request error occurred: {req_err}"
        except Exception as err:
            return f"An error occurred: {err}"

    def fetch_wikipedia_full_article(title):
        """Fetch the full article text from Wikipedia."""
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": title,
            "prop": "extracts",
            "explaintext": True
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if "extract" in page_data:
                    return summarize_text(page_data["extract"])
            return "No detailed content available."
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"
        except requests.exceptions.RequestException as req_err:
            return f"Request error occurred: {req_err}"
        except Exception as err:
            return f"An error occurred: {err}"

    # Main logic to process the query
    cleaned_query = clean_query(query)

    # Extract topic from the query
    keywords = [
        "what", "define", "explain", "describe", "how", "who", "why", "where"
    ]
    topic = next((cleaned_query.replace(keyword, "").strip()
                  for keyword in keywords if keyword in cleaned_query.lower()),
                 cleaned_query)

    # Search Wikipedia and fetch the summary
    page_title = search_wikipedia(topic)
    if "Sorry" in page_title:
        return page_title
    return fetch_wikipedia_summary(page_title)


if __name__ == '__main__':
    print("Pycharm")
    say("Hello, this is JARVIS AI.")
    print("hello, This is Jarvis AI")
    while True:
        query = listen_or_type()
        if query is None:  # Handle speech recognition error
            say("Sorry, I couldn't understand you. Please try again.")
            continue
        # Check for exit keyword (modify as needed)
        sites = [
            ["youtube", "https://www.youtube.com"],
            ["wikipedia", "https://www.wikipedia.com"],
            ["google", "https://www.google.com"],
        ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                print(f"opening {site}")
                webbrowser.open(site[1])
        if f"time".lower() in query.lower():
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"the time is {strfTime}")
            print(f"time is {strfTime} ")
        game = ["rock paper", "tic tac toe"]
        if f"game" in query.lower():
            say("i can play rock paper... lets play")
            print("i can play rock paper... lets play")
            rock_paper()
        if f"camera".lower() in query.lower():
            say("opening camera")
            print(f"opening camera")

        if f"calculate".lower() in query.lower():
            print("opening calculator")
            say("opening calculator")
            open_calculator()

        if f"analyze".lower() in query.lower():
            print("opening article analyzer")
            say("opening article analyzer")
            analyze()

        if any(keyword in query.lower()
               for keyword in ["what", "who", "why", "where", "how"]):
            response = fetch_wikipedia_data(query)
            print(response)
            say(response)

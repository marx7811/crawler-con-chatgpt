import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests
from bs4 import BeautifulSoup
import openai

# introduce clave de chat gpt
openai.api_key = "clave"

# Función para extraer texto de una URL
def extraer_texto(url, limite_palabras):
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            texto = soup.get_text()  # Extraer solo el texto
            palabras = texto.split()[:limite_palabras]  # Limitar la cantidad de palabras
            return ' '.join(palabras)
        else:
            return f"Error al acceder a {url}: {respuesta.status_code}"
    except Exception as e:
        return f"Error: {e}"

# Función para procesar texto con ChatGPT
def procesar_con_chatgpt(texto, prompt):
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente útil."},
                {"role": "user", "content": f"{prompt}\n\n{texto}"}
            ]
        )
        return respuesta.choices[0].message.content
    except Exception as e:
        return f"Error al procesar con ChatGPT: {e}"

# intefaz
def iniciar_proceso():
    url = url_entry.get()
    try:
        limite_palabras = int(word_limit_entry.get())
    except ValueError:
        messagebox.showerror("Error", "El límite de palabras debe ser un número.")
        return
    prompt = prompt_entry.get()

    texto = extraer_texto(url, limite_palabras)
    if "Error" in texto:
        messagebox.showerror("Error", texto)
        return

    # Mostrar texto extraído
    texto_area.delete(1.0, tk.END)
    texto_area.insert(tk.END, texto)

    # Procesar con ChatGPT
    respuesta_gpt = procesar_con_chatgpt(texto, prompt)
    respuesta_area.delete(1.0, tk.END)
    respuesta_area.insert(tk.END, respuesta_gpt)

# ventana principal
ventana = tk.Tk()
ventana.title("Procesamiento con ChatGPT")
ventana.geometry("800x600")

# Entrada de URL
tk.Label(ventana, text="URL:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
url_entry = tk.Entry(ventana, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=5)

# Entrada de límite de palabras
tk.Label(ventana, text="Límite de palabras:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
word_limit_entry = tk.Entry(ventana, width=10)
word_limit_entry.grid(row=1, column=1, sticky="w", padx=10, pady=5)
word_limit_entry.insert(0, "5000")  # Valor predeterminado

# Entrada de prompt
tk.Label(ventana, text="Prompt para GPT:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
prompt_entry = tk.Entry(ventana, width=50)
prompt_entry.grid(row=2, column=1, padx=10, pady=5)

# Botón para iniciar
iniciar_btn = tk.Button(ventana, text="Iniciar", command=iniciar_proceso)
iniciar_btn.grid(row=3, column=0, columnspan=2, pady=10)

# Área para mostrar texto extraído
tk.Label(ventana, text="Texto extraído:").grid(row=4, column=0, sticky="nw", padx=10, pady=5)
texto_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=90, height=10)
texto_area.grid(row=4, column=1, padx=10, pady=5)

# Área para mostrar respuesta de GPT
tk.Label(ventana, text="Respuesta de GPT:").grid(row=5, column=0, sticky="nw", padx=10, pady=5)
respuesta_area = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=90, height=10)
respuesta_area.grid(row=5, column=1, padx=10, pady=5)

# Ejecutar la ventana principal
ventana.mainloop()

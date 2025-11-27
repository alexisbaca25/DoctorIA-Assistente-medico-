import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import os
from PIL import Image # Necesario para cargar tu nuevo logo

# --- Importaciones de lógica ---
try:
    from base_conocimiento import ENFERMEDADES
    from motor_inferencia import diagnosticar
    from recomendaciones import RECOMENDACIONES
    from utils import generar_pdf_diagnostico
except ImportError:
    # Datos dummy para que no falle si faltan archivos
    ENFERMEDADES = {"Prueba": ["tos"]}
    RECOMENDACIONES = {}
    def diagnosticar(s): return {"diagnostico": None, "detalles": []}
    def generar_pdf_diagnostico(*args): pass

# --- CONFIGURACIÓN VISUAL ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

APP_NAME = "DoctorIA"

# Colores
COLOR_FONDO_APP = "#0F1115"
COLOR_TARJETA = "#1D2129"
COLOR_PRIMARIO = "#1E88E5" 
COLOR_TEXTO_SEC = "#B0BEC5"
COLOR_INPUT = "#282C34"

#
CATEGORIAS = {
    "General y Estado de Ánimo": ("🩺", [
        "fiebre", "fiebre baja", "fiebre alta", "fiebre alta repentina",
        "escalofríos", "cuerpo cortado", "malestar general", 
        "cansancio", "cansancio extremo", "fatiga", "fatiga leve",
        "mareo", "deshidratacion", "perdida de peso repentina",
        "mucha sed", "mucha hambre", "palpitaciones"
    ]),
    
    "Cabeza, Ojos y Oídos": ("🧠", [
        "dolor de cabeza", "dolor de cabeza fuerte", "dolor de cabeza frontal", 
        "dolor de cabeza unilateral", "dolor de nuca", "pulsaciones en la cabeza",
        "dolor detras de los ojos", "sensibilidad a la luz", "vision borrosa", 
        "ver lucesitas", "ojos rojos", "ojos llorosos", "lagrimeo", 
        "lagañas o secrecion", "sensacion de arena en ojos", "parpados pegados", 
        "picazon en ojos", "zumbido en oidos", "dolor de oido punzante", 
        "sensacion de oido tapado", "secrecion del oido", 
        "perdida de olfato", "perdida de gusto"
    ]),

    "Respiratorio y Garganta": ("🫁", [
        "tos leve", "tos seca", "tos seca persistente", "tos con flema", 
        "estornudos", "estornudos frecuentes", "escurrimiento nasal", 
        "goteo nasal claro", "congestion nasal", "picazon en nariz",
        "dificultad para respirar", "dificultad para respirar leve", 
        "silbido al respirar", "presion en el pecho", 
        "dolor de garganta", "dolor de garganta intenso", "dificultad para tragar", 
        "ganglios inflamados", "placas de pus", "mal aliento", "boca seca"
    ]),

    "Digestivo y Abdomen": ("🤢", [
        "dolor abdominal", "dolor abdominal punzante", "dolor en la boca del estomago",
        "retortijones", "inflamacion abdominal", "sensacion de plenitud",
        "nauseas", "vomito", "acidez", "ardor estomacal", "gases", 
        "diarrea", "diarrea liquida", "estreñimiento o diarrea"
    ]),

    "Piel, Dolor y Orina": ("➕", [
        "dolor muscular", "dolor muscular intenso", "dolor articular severo", "dolor pelvico",
        "sarpullido", "ampollas en la piel", "costras", "comezon intensa", "piel seca",
        "ardor al orinar", "necesidad frecuente de orinar", "orinar muy frecuente",
        "sensacion de no terminar de orinar", "orina turbia", "orina oscura"
    ])
}


class DoctorIA_App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1280x768")
        self.configure(fg_color=COLOR_FONDO_APP)
        

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.check_vars = {}
        self.check_widgets = [] 

        self._setup_ui()

    def _setup_ui(self):
        #HEADER 
        self.top_bar = ctk.CTkFrame(self, height=70, corner_radius=0, fg_color="#161920")
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.top_bar.grid_propagate(False)

        ctk.CTkFrame(self.top_bar, height=2, fg_color=COLOR_PRIMARIO).pack(side="bottom", fill="x")

        # Container para agrupar Logo + Texto principal
        logo_container = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        logo_container.pack(side="left", padx=(25, 5), pady=10)

        # 1. Cargar Imagen
        img_path = os.path.join(os.path.dirname(__file__), "assets", "logo_header.png")
        
        if os.path.exists(img_path):
            try:
                pil_img = Image.open(img_path)
                my_image = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(140, 98))
                
                icon_label = ctk.CTkLabel(logo_container, text="", image=my_image)
                icon_label.pack(side="left", padx=(0, 3)) 
            except Exception as e:
                print(f"Error cargando imagen: {e}")
        else:
            ctk.CTkLabel(logo_container, text="✚", font=("Arial", 28), text_color=COLOR_PRIMARIO).pack(side="left", padx=(0, 5))

        #"DoctorIA"
        ctk.CTkLabel(logo_container, text=APP_NAME, font=("Segoe UI", 26, "bold"), text_color="white").pack(side="left")

        # 3. Subtítulo
    
        ctk.CTkLabel(self.top_bar, text="| Asistente Virtual", font=ctk.CTkFont(size=19), text_color=COLOR_TEXTO_SEC).pack(side="left", padx=(5,0))

        #  PANEL IZQUIERDO 
        self.left_panel = ctk.CTkFrame(self, width=400, corner_radius=10, fg_color=COLOR_TARJETA)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.left_panel.grid_propagate(False)

        ctk.CTkLabel(self.left_panel, text="Buscar Síntoma", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=20, pady=(20, 5))
        self.search_entry = ctk.CTkEntry(self.left_panel, placeholder_text="🔍 Filtrar...", height=40, corner_radius=8, border_width=0, fg_color=COLOR_INPUT, text_color="white")
        self.search_entry.pack(fill="x", padx=20, pady=(5, 10))
        self.search_entry.bind("<KeyRelease>", self.filtrar_sintomas)

        self.scroll_categorias = ctk.CTkScrollableFrame(self.left_panel, label_text="", fg_color="transparent")
        self.scroll_categorias.pack(expand=True, fill="both", padx=5, pady=5)

        for nombre_cat, (icono, lista_sintomas) in CATEGORIAS.items():
            lbl_cat = ctk.CTkLabel(self.scroll_categorias, text=f"{icono} {nombre_cat}", font=ctk.CTkFont(size=13, weight="bold"), text_color=COLOR_PRIMARIO, anchor="w")
            lbl_cat.pack(fill="x", pady=(15, 5), padx=10)
            
            frame_checks = ctk.CTkFrame(self.scroll_categorias, fg_color="#232730", corner_radius=6)
            frame_checks.pack(fill="x", pady=(0, 5), padx=5)
            frame_checks.grid_columnconfigure(0, weight=1)
            
            idx_cat = 0
            for sintoma in lista_sintomas:
                var = ctk.BooleanVar()
                chk = ctk.CTkCheckBox(frame_checks, text=sintoma.capitalize(), variable=var, font=ctk.CTkFont(size=13), text_color="#E0E0E0", hover_color=COLOR_PRIMARIO, fg_color=COLOR_PRIMARIO, border_width=2, corner_radius=4, height=24)
                chk.grid(row=idx_cat, column=0, sticky="w", padx=15, pady=8)
                self.check_vars[sintoma] = var
                self.check_widgets.append({"s": sintoma, "w": chk})
                idx_cat += 1

        frame_btns = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        frame_btns.pack(fill="x", padx=20, pady=20)
        ctk.CTkButton(frame_btns, text="CONSULTAR", height=45, corner_radius=8, font=ctk.CTkFont(weight="bold", size=15), fg_color="#00C853", hover_color="#009624", text_color="white", command=self.on_diagnosticar).pack(fill="x", pady=(0,10))
        ctk.CTkButton(frame_btns, text="Exportar PDF", height=35, corner_radius=8, fg_color="#37474F", hover_color="#455A64", font=ctk.CTkFont(size=13), command=self.on_export).pack(fill="x")

        #  DERECHO
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.right_panel.grid_rowconfigure(0, weight=2) 
        self.right_panel.grid_rowconfigure(1, weight=3) 
        self.right_panel.grid_columnconfigure(0, weight=1)

        self.card_result = ctk.CTkFrame(self.right_panel, corner_radius=10, fg_color=COLOR_TARJETA)
        self.card_result.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        ctk.CTkLabel(self.card_result, text="Resultado del Análisis", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="nw", padx=20, pady=15)

        self.frame_barras = ctk.CTkScrollableFrame(self.card_result, fg_color="transparent")
        self.frame_barras.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.lbl_inicial = ctk.CTkLabel(self.frame_barras, text="Seleccione síntomas y presione CONSULTAR.", text_color="gray", font=ctk.CTkFont(size=14))
        self.lbl_inicial.pack(pady=40)

        self.card_recs = ctk.CTkFrame(self.right_panel, corner_radius=10, fg_color=COLOR_TARJETA)
        self.card_recs.grid(row=1, column=0, sticky="nsew")
        ctk.CTkLabel(self.card_recs, text="Recomendaciones / Información", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="nw", padx=20, pady=15)

        self.tab_view = ctk.CTkTabview(self.card_recs, fg_color="transparent", segmented_button_fg_color="#282C34", segmented_button_selected_color=COLOR_PRIMARIO, segmented_button_unselected_color="#282C34", text_color="white", height=40)
        self.tab_view.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.tab_cuidados = self.tab_view.add(" Cuidados Generales ")
        self.tab_meds = self.tab_view.add(" Medicamentos Sugeridos ")

        self.txt_recs_cuidados = ctk.CTkTextbox(self.tab_cuidados, font=ctk.CTkFont(size=14), fg_color=COLOR_INPUT, text_color="#E0E0E0", corner_radius=8, wrap="word")
        self.txt_recs_cuidados.pack(fill="both", expand=True, padx=2, pady=5)
        self.txt_recs_cuidados.configure(state="disabled")

        self.txt_meds = ctk.CTkTextbox(self.tab_meds, font=ctk.CTkFont(size=14), fg_color=COLOR_INPUT, text_color="#E0E0E0", corner_radius=8, wrap="word")
        self.txt_meds.pack(fill="both", expand=True, padx=2, pady=5)
        self.txt_meds.insert("1.0", "\n⚠️ Importante: Esta aplicación es informativa.\n\nConsulte siempre a un médico profesional antes de tomar cualquier medicamento.")
        self.txt_meds.configure(state="disabled")

    # LÓGICA
    def filtrar_sintomas(self, event=None):
        query = self.search_entry.get().lower().strip()
        for item in self.check_widgets:
            sintoma_texto = item["s"].lower()
            widget = item["w"]
            if query == "" or query in sintoma_texto: widget.grid()
            else: widget.grid_remove()

    def on_diagnosticar(self):
        for widget in self.frame_barras.winfo_children(): widget.destroy()
        sintomas_seleccionados = {s for s, v in self.check_vars.items() if v.get()}
        
        if not sintomas_seleccionados:
             ctk.CTkLabel(self.frame_barras, text="⚠️ Seleccione al menos un síntoma.", text_color="#FFB74D", font=ctk.CTkFont(size=14)).pack(pady=20)
             self.limpiar_recomendaciones()
             return

        try: resultado = diagnosticar(sintomas_seleccionados)
        except Exception as e:
            ctk.CTkLabel(self.frame_barras, text=f"Error interno: {e}", text_color="red").pack(); return
        
        if not resultado["diagnostico"]:
            ctk.CTkLabel(self.frame_barras, text="No se encontraron coincidencias.", text_color="gray", font=ctk.CTkFont(size=14)).pack(pady=20)
            self.limpiar_recomendaciones()
        else:
            for det in resultado["detalles"][:5]:
                row = ctk.CTkFrame(self.frame_barras, fg_color="transparent")
                row.pack(fill="x", pady=8, padx=5)
                txt_label = f"{det['enfermedad'].upper()}  ({det['porcentaje']:.0f}%)"
                ctk.CTkLabel(row, text=txt_label, anchor="w", font=ctk.CTkFont(size=13, weight="bold"), text_color="white").pack(fill="x", pady=(0, 2))
                progress = ctk.CTkProgressBar(row, height=12, corner_radius=6, progress_color=COLOR_PRIMARIO, fg_color="#2A2D3E")
                progress.set(det['porcentaje'] / 100)
                progress.pack(fill="x")
            self.mostrar_recomendaciones(resultado["diagnostico"])

    def limpiar_recomendaciones(self):
        self.txt_recs_cuidados.configure(state="normal")
        self.txt_recs_cuidados.delete("1.0", "end")
        self.txt_recs_cuidados.configure(state="disabled")

    def mostrar_recomendaciones(self, enfermedad_top):
        self.txt_recs_cuidados.configure(state="normal")
        self.txt_recs_cuidados.delete("1.0", "end")
        recs = RECOMENDACIONES.get(enfermedad_top)
        self.tab_view.set(" Cuidados Generales ")
        self.txt_recs_cuidados.insert("end", f"POSIBLE DIAGNÓSTICO: {enfermedad_top.upper()}\n\n")
        if recs:
            for r in recs: self.txt_recs_cuidados.insert("end", f"✅ {r}\n\n")
        else: self.txt_recs_cuidados.insert("end", "Consulte a un médico.")
        self.txt_recs_cuidados.configure(state="disabled")

    def on_export(self):
        sintomas = [s for s, v in self.check_vars.items() if v.get()]
        if not sintomas:
             messagebox.showwarning("Exportar", "Seleccione síntomas primero.")
             return
        try:
            resultado = diagnosticar(set(sintomas))
            ruta_guardar = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], title="Guardar Diagnóstico")
            if not ruta_guardar: return
            recs_list = RECOMENDACIONES.get(resultado["diagnostico"]) if resultado["diagnostico"] else None
            generar_pdf_diagnostico(APP_NAME, sintomas, resultado, recomendaciones_list=recs_list, salida_path=ruta_guardar)
            messagebox.showinfo("PDF", f"Archivo guardado en:\n{ruta_guardar}")
        except Exception as e: messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "assets")):
        try: os.makedirs(os.path.join(os.path.dirname(__file__), "assets"))
        except: pass
    app = DoctorIA_App()
    app.mainloop()
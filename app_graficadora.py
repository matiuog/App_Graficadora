import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sympy as sp
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.style as mplstyle
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

# --- CONFIGURACIÓN ESTÉTICA GLOBAL DE MATPLOTLIB ---
MY_DARK_STYLE = {
    'figure.facecolor': '#090D16',  # Azul noche profundo
    'axes.facecolor': '#090D16',    # Fondo del área de dibujo
    'axes.edgecolor': '#1E293B',    # Bordes de ejes gris pizarra tenue
    'axes.labelcolor': '#94A3B8',   # Etiquetas de ejes
    'axes.grid': True,
    'grid.color': '#1E293B',        # Cuadrícula sutil
    'grid.linestyle': '--',
    'grid.linewidth': 0.6,
    'grid.alpha': 0.7,
    'xtick.color': '#64748B',       # Marcas de ejes gris claro
    'ytick.color': '#64748B',
    'text.color': '#F8FAFC',        # Texto general claro
    'font.family': 'sans-serif',
    'font.sans-serif': ['Segoe UI', 'SF Pro Text', 'Helvetica', 'Arial', 'DejaVu Sans'],
}
mplstyle.use(MY_DARK_STYLE)

class ParametricDashboardChivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador Cinemático de Trayectorias Neón")
        self.root.geometry("1050x700")
        self.root.configure(bg="#0B0F19")
        
        # --- Variables de estado ---
        self.t_val = tk.DoubleVar(value=0.0)
        self.t_vec = []
        self.is_playing = False
        
        # --- OPCIONES DE CAPAS ---
        self.var_equal_aspect = tk.BooleanVar(value=True)
        self.var_show_v = tk.BooleanVar(value=True)
        self.var_show_a = tk.BooleanVar(value=True)
        self.var_show_hud = tk.BooleanVar(value=True)
        
        # --- PALETA NEÓN FUTURISTA ---
        self.COLOR_TRAYECTORIA_BASE = '#1E293B'  # Gris azulado tenue
        self.COLOR_PROGRESO = '#00F0FF'         # Cian Neón vibrante
        self.COLOR_GLOW = '#00F0FF'             # Halo Neón
        self.COLOR_PUNTO = '#FFFFFF'            # Núcleo blanco brillante
        self.COLOR_VELOCIDAD = '#00FF9D'        # Verde Lima Eléctrico
        self.COLOR_ACELERACION = '#FF007A'     # Magenta / Rosa Neón
        
        # --- PANEL DE CONTROL (Izquierda) ---
        control_frame = tk.Frame(root, width=320, bg="#111827", bd=0)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)
        control_frame.pack_propagate(False)
        
        # Título principal del panel
        header_frame = tk.Frame(control_frame, bg="#1E293B", pady=12)
        header_frame.pack(fill=tk.X)
        tk.Label(
            header_frame, 
            text="⚡ CINEMÁTICA PARAMÉTRICA", 
            bg="#1E293B", 
            fg="#00F0FF", 
            font=("Segoe UI", 11, "bold")
        ).pack()
        
        # Área escroleable / contenedores estilizados
        main_container = tk.Frame(control_frame, bg="#111827", padx=15, pady=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Estilos generales para inputs
        lbl_style = {"bg": "#111827", "fg": "#94A3B8", "font": ("Segoe UI", 9, "bold")}
        entry_style = {
            "font": ("Consolas", 11), 
            "justify": "center", 
            "bg": "#090D16", 
            "fg": "#00F0FF", 
            "insertbackground": "#00F0FF", 
            "relief": tk.FLAT,
            "highlightbackground": "#1E293B",
            "highlightcolor": "#00F0FF",
            "highlightthickness": 1
        }
        
        # --- SECCIÓN: PRESETS DE CURVAS ---
        tk.Label(main_container, text="PRESETS DE CURVAS", **lbl_style).pack(anchor="w", pady=(5, 4))
        
        self.presets = {
            "🌀 Espiral de Arquímedes": ("t * cos(t)", "t * sin(t)", "0", "20"),
            "🌸 Rosa Paramétrica (5 pétalos)": ("cos(5*t) * cos(t)", "cos(5*t) * sin(t)", "0", "6.28"),
            "♾️ Figura de Lissajous (3:4)": ("sin(3*t)", "cos(4*t)", "0", "6.28"),
            "🦋 Curva Mariposa": ("sin(t)*(exp(cos(t)) - 2*cos(4*t))", "cos(t)*(exp(cos(t)) - 2*cos(4*t))", "0", "12.56"),
            "🌟 Astroide (Estrella)": ("4 * cos(t)**3", "4 * sin(t)**3", "0", "6.28"),
        }
        
        self.combo_presets = ttk.Combobox(
            main_container, 
            values=list(self.presets.keys()), 
            state="readonly",
            font=("Segoe UI", 9)
        )
        self.combo_presets.current(0)
        self.combo_presets.pack(fill=tk.X, pady=(0, 15))
        self.combo_presets.bind("<<ComboboxSelected>>", self.load_preset)
        
        # --- SECCIÓN: ECUACIONES Y RANGO ---
        tk.Label(main_container, text="ECUACIONES PARAMÉTRICAS", **lbl_style).pack(anchor="w", pady=(0, 4))
        
        def create_input(frame, label_text, default_val):
            sub_frame = tk.Frame(frame, bg="#111827")
            sub_frame.pack(fill=tk.X, pady=3)
            tk.Label(sub_frame, text=label_text, bg="#111827", fg="#CBD5E1", font=("Segoe UI", 9, "bold"), width=6, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(sub_frame, **entry_style)
            entry.insert(0, default_val)
            entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
            return entry

        self.entry_x = create_input(main_container, "x(t):", "t * cos(t)")
        self.entry_y = create_input(main_container, "y(t):", "t * sin(t)")
        
        rango_frame = tk.Frame(main_container, bg="#111827")
        rango_frame.pack(fill=tk.X, pady=(8, 15))
        
        tk.Label(rango_frame, text="t min:", bg="#111827", fg="#94A3B8", font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w")
        self.entry_tmin = tk.Entry(rango_frame, width=8, **entry_style)
        self.entry_tmin.insert(0, "0")
        self.entry_tmin.grid(row=0, column=1, padx=(4, 15))
        
        tk.Label(rango_frame, text="t max:", bg="#111827", fg="#94A3B8", font=("Segoe UI", 8)).grid(row=0, column=2, sticky="w")
        self.entry_tmax = tk.Entry(rango_frame, width=8, **entry_style)
        self.entry_tmax.insert(0, "20")
        self.entry_tmax.grid(row=0, column=3, padx=(4, 0))
        
        # --- SECCIÓN: OPCIONES DE VISUALIZACIÓN ---
        tk.Label(main_container, text="CAPAS Y AJUSTES", **lbl_style).pack(anchor="w", pady=(0, 4))
        
        opts_frame = tk.Frame(main_container, bg="#1F293D", padx=10, pady=8, highlightbackground="#374151", highlightthickness=1)
        opts_frame.pack(fill=tk.X, pady=(0, 15))
        
        def create_check(frame, text, variable, fg_color):
            chk = tk.Checkbutton(
                frame, text=text, variable=variable, 
                bg="#1F293D", fg=fg_color, activebackground="#1F293D", activeforeground=fg_color,
                selectcolor="#090D16", font=("Segoe UI", 9, "bold"), bd=0, command=self.on_option_change
            )
            chk.pack(anchor="w", pady=2)
            return chk

        create_check(opts_frame, "📐 Aspecto Real 1:1 (Sin distorsión)", self.var_equal_aspect, "#F8FAFC")
        create_check(opts_frame, "🟢 Vector Velocidad (v)", self.var_show_v, self.COLOR_VELOCIDAD)
        create_check(opts_frame, "💗 Vector Aceleración (a)", self.var_show_a, self.COLOR_ACELERACION)
        create_check(opts_frame, "📊 Telemetría HUD en pantalla", self.var_show_hud, "#00F0FF")

        # --- BOTONES DE ACCIÓN Y REPRODUCCIÓN ---
        self.btn_plot = tk.Button(
            main_container, text="🚀 GENERAR TRAYECTORIA", command=self.plot_graph, 
            bg="#00F0FF", fg="#090D16", font=("Segoe UI", 10, "bold"), 
            pady=8, relief=tk.FLAT, cursor="hand2", activebackground="#38BDF8"
        )
        self.btn_plot.pack(fill=tk.X, pady=(5, 8))
        self.add_hover_effect(self.btn_plot, "#00F0FF", "#38BDF8")

        self.btn_play = tk.Button(
            main_container, text="▶ REPRODUCIR ANIMACIÓN", command=self.toggle_play, 
            bg="#1F293D", fg="#FF007A", font=("Segoe UI", 10, "bold"), 
            pady=8, relief=tk.FLAT, cursor="hand2", activebackground="#374151"
        )
        self.btn_play.pack(fill=tk.X, pady=(0, 15))
        self.add_hover_effect(self.btn_play, "#1F293D", "#374151")

        # --- DESLIZADOR DE TIEMPO ---
        tk.Label(main_container, text="TIEMPO ACTUAL (t)", **lbl_style).pack(anchor="w", pady=(0, 2))
        
        self.slider = tk.Scale(
            main_container, variable=self.t_val, orient=tk.HORIZONTAL, 
            command=self.update_anim, resolution=0.05, from_=0, to=10,
            bg="#111827", fg="#00F0FF", troughcolor="#090D16", activebackground="#00F0FF",
            highlightthickness=0, relief=tk.FLAT, font=("Consolas", 9, "bold")
        )
        self.slider.pack(fill=tk.X)

        # Footer
        tk.Label(
            control_frame, 
            text="Motor Cinemático Analítico • SymPy + Matplotlib", 
            bg="#111827", fg="#475569", font=("Segoe UI", 7)
        ).pack(side=tk.BOTTOM, pady=10)
        
        # --- PANEL DEL GRÁFICO (Derecha) ---
        self.fig = Figure(figsize=(7, 7), dpi=105)
        self.ax = self.fig.add_subplot(111)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Inicializar gráfica por defecto
        self.plot_graph()

    def add_hover_effect(self, widget, bg_normal, bg_hover):
        widget.bind("<Enter>", lambda e: widget.config(bg=bg_hover))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg_normal))

    def load_preset(self, event=None):
        preset_name = self.combo_presets.get()
        if preset_name in self.presets:
            fx, fy, tmin, tmax = self.presets[preset_name]
            self.entry_x.delete(0, tk.END)
            self.entry_x.insert(0, fx)
            self.entry_y.delete(0, tk.END)
            self.entry_y.insert(0, fy)
            self.entry_tmin.delete(0, tk.END)
            self.entry_tmin.insert(0, tmin)
            self.entry_tmax.delete(0, tk.END)
            self.entry_tmax.insert(0, tmax)
            self.plot_graph()

    def on_option_change(self):
        if len(self.t_vec) > 0:
            if self.var_equal_aspect.get():
                x_min, x_max = np.min(self.x_vec), np.max(self.x_vec)
                y_min, y_max = np.min(self.y_vec), np.max(self.y_vec)
                x_mid, y_mid = (x_min + x_max) / 2.0, (y_min + y_max) / 2.0
                max_range = max(x_max - x_min, y_max - y_min) * 1.15 + 1.0
                self.ax.set_xlim(x_mid - max_range / 2.0, x_mid + max_range / 2.0)
                self.ax.set_ylim(y_mid - max_range / 2.0, y_mid + max_range / 2.0)
                self.ax.set_aspect('equal', adjustable='box')
            else:
                margin_x = (np.max(self.x_vec) - np.min(self.x_vec)) * 0.15 + 0.5
                margin_y = (np.max(self.y_vec) - np.min(self.y_vec)) * 0.15 + 0.5
                self.ax.set_xlim(np.min(self.x_vec) - margin_x, np.max(self.x_vec) + margin_x)
                self.ax.set_ylim(np.min(self.y_vec) - margin_y, np.max(self.y_vec) + margin_y)
                self.ax.set_aspect('auto')
            self.update_anim(None)

    def plot_graph(self):
        try:
            # Detener reproducción si está activa
            if self.is_playing:
                self.toggle_play()

            # Leer entradas
            t_min = float(self.entry_tmin.get())
            t_max = float(self.entry_tmax.get())
            str_x = self.entry_x.get()
            str_y = self.entry_y.get()
            
            # --- Matemáticas Simbólicas Analíticas con SymPy ---
            t_sym = sp.Symbol('t')
            expr_x = sp.sympify(str_x)
            expr_y = sp.sympify(str_y)
            
            # Calcular derivadas analíticas exactas
            vx_sym, vy_sym = sp.diff(expr_x, t_sym), sp.diff(expr_y, t_sym)
            ax_sym, ay_sym = sp.diff(vx_sym, t_sym), sp.diff(vy_sym, t_sym)
            
            # Convertir a funciones evaluables de NumPy
            fx, fy = sp.lambdify(t_sym, expr_x, "numpy"), sp.lambdify(t_sym, expr_y, "numpy")
            fvx, fvy = sp.lambdify(t_sym, vx_sym, "numpy"), sp.lambdify(t_sym, vy_sym, "numpy")
            fax, fay = sp.lambdify(t_sym, ax_sym, "numpy"), sp.lambdify(t_sym, ay_sym, "numpy")
            
            # Generar malla de tiempo fina
            self.t_vec = np.linspace(t_min, t_max, 600)
            
            def eval_func(func, t_array):
                res = func(t_array)
                return np.ones_like(t_array) * res if isinstance(res, (int, float)) else res
            
            self.x_vec, self.y_vec = eval_func(fx, self.t_vec), eval_func(fy, self.t_vec)
            self.vx_vec, self.vy_vec = eval_func(fvx, self.t_vec), eval_func(fvy, self.t_vec)
            self.ax_vec, self.ay_vec = eval_func(fax, self.t_vec), eval_func(fay, self.t_vec)

            # --- PREPARAR LIENZO MATPLOTLIB NEÓN ---
            self.ax.clear()
            
            # Título futurista
            self.ax.set_title(
                "S I M U L A C I Ó N   C I N E M Á T I C A   2 D", 
                fontsize=11, fontweight='bold', color="#F8FAFC", pad=12
            )
            
            # Formato de bordes (Spines) minimalista
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['left'].set_color('#1E293B')
            self.ax.spines['bottom'].set_color('#1E293B')
            
            # Ejes de origen (x=0, y=0) sutiles
            self.ax.axhline(0, color='#334155', linestyle=':', linewidth=0.8, alpha=0.6)
            self.ax.axvline(0, color='#334155', linestyle=':', linewidth=0.8, alpha=0.6)

            # 1. Trayectoria Base (Estilo tenue)
            self.ax.plot(self.x_vec, self.y_vec, color=self.COLOR_TRAYECTORIA_BASE, linestyle='-', linewidth=1.2, alpha=0.6)
            
            # 2. Trayectoria en Progreso (EFECTO GLOW NEÓN MULTICAPA)
            # Capa externa de resplandor (Glow)
            self.line_glow, = self.ax.plot([], [], color=self.COLOR_GLOW, linewidth=6.5, alpha=0.25)
            # Capa interna nítida y brillante
            self.line_prog, = self.ax.plot([], [], color=self.COLOR_PROGRESO, linewidth=2.0, alpha=0.95)
            
            # 3. Partícula Móvil (EFECTO ORBE CONCÉNTRICO)
            self.halo_outer, = self.ax.plot([], [], 'o', color=self.COLOR_GLOW, markersize=16, alpha=0.25)
            self.halo_inner, = self.ax.plot([], [], 'o', color=self.COLOR_PROGRESO, markersize=9, alpha=0.6)
            self.point_core, = self.ax.plot([], [], 'o', color=self.COLOR_PUNTO, markersize=4, alpha=1.0)
            
            # 4. VECTORES DE VELOCIDAD Y ACELERACIÓN ESTILIZADOS
            quiver_config = {
                'scale_units': 'xy', 
                'angles': 'xy', 
                'scale': 1, 
                'pivot': 'tail',
                'width': 0.006,        # Flecha delgada y estilizada
                'headwidth': 3.5,      
                'headlength': 4.5,     
                'headaxislength': 4.0, 
            }
            
            # Quivers principales
            self.quiver_v = self.ax.quiver([], [], [], [], color=self.COLOR_VELOCIDAD, label='Velocidad (v)', zorder=5, **quiver_config)
            self.quiver_a = self.ax.quiver([], [], [], [], color=self.COLOR_ACELERACION, label='Aceleración (a)', zorder=5, **quiver_config)
            
            # 5. TELEMETRÍA HUD FLOTANTE
            self.hud_text = self.ax.text(
                0.03, 0.95, '', transform=self.ax.transAxes, 
                verticalalignment='top', fontsize=9, fontfamily='monospace',
                color='#F8FAFC',
                bbox=dict(boxstyle='round,pad=0.7', facecolor='#0F172A', edgecolor='#334155', alpha=0.88)
            )

            # Leyenda elegante
            leg = self.ax.legend(loc='upper right', frameon=True, fontsize='small')
            leg.get_frame().set_facecolor('#0F172A')
            leg.get_frame().set_edgecolor('#334155')
            leg.get_frame().set_alpha(0.85)

            # Aspect Ratio 1:1 o Auto con límites simétricos
            if self.var_equal_aspect.get():
                x_min, x_max = np.min(self.x_vec), np.max(self.x_vec)
                y_min, y_max = np.min(self.y_vec), np.max(self.y_vec)
                x_mid, y_mid = (x_min + x_max) / 2.0, (y_min + y_max) / 2.0
                max_range = max(x_max - x_min, y_max - y_min) * 1.15 + 1.0
                self.ax.set_xlim(x_mid - max_range / 2.0, x_mid + max_range / 2.0)
                self.ax.set_ylim(y_mid - max_range / 2.0, y_mid + max_range / 2.0)
                self.ax.set_aspect('equal', adjustable='box')
            else:
                margin_x = (np.max(self.x_vec) - np.min(self.x_vec)) * 0.15 + 0.5
                margin_y = (np.max(self.y_vec) - np.min(self.y_vec)) * 0.15 + 0.5
                self.ax.set_xlim(np.min(self.x_vec) - margin_x, np.max(self.x_vec) + margin_x)
                self.ax.set_ylim(np.min(self.y_vec) - margin_y, np.max(self.y_vec) + margin_y)
                self.ax.set_aspect('auto')
            
            # Configurar slider y renderizar tiempo inicial
            self.slider.config(from_=t_min, to=t_max)
            self.t_val.set(t_min)
            self.update_anim(None)
            
        except Exception as e:
            messagebox.showerror("Error de Sintaxis", f"Por favor usa notación matemática válida de Python.\n\nDetalle: {e}")

    def update_anim(self, val):
        if len(self.t_vec) == 0: return
        t_current = self.t_val.get()
        
        # Encontrar índice más cercano
        idx = np.searchsorted(self.t_vec, t_current)
        if idx >= len(self.t_vec): idx = len(self.t_vec) - 1
        
        curr_x, curr_y = self.x_vec[idx], self.y_vec[idx]
        
        # 1. Actualizar trayectorias con resplandor neón
        self.line_glow.set_data(self.x_vec[:idx+1], self.y_vec[:idx+1])
        self.line_prog.set_data(self.x_vec[:idx+1], self.y_vec[:idx+1])
        
        # 2. Actualizar orbe concéntrico
        self.halo_outer.set_data([curr_x], [curr_y])
        self.halo_inner.set_data([curr_x], [curr_y])
        self.point_core.set_data([curr_x], [curr_y])
        
        # 3. Actualizar vectores según visibilidad seleccionada
        if self.var_show_v.get():
            self.quiver_v.set_offsets([curr_x, curr_y])
            self.quiver_v.set_UVC(self.vx_vec[idx], self.vy_vec[idx])
            self.quiver_v.set_visible(True)
        else:
            self.quiver_v.set_visible(False)
            
        if self.var_show_a.get():
            self.quiver_a.set_offsets([curr_x, curr_y])
            self.quiver_a.set_UVC(self.ax_vec[idx], self.ay_vec[idx])
            self.quiver_a.set_visible(True)
        else:
            self.quiver_a.set_visible(False)
            
        # 4. Actualizar Telemetría HUD
        if self.var_show_hud.get():
            mag_v = np.hypot(self.vx_vec[idx], self.vy_vec[idx])
            mag_a = np.hypot(self.ax_vec[idx], self.ay_vec[idx])
            
            hud_str = (
                f" t   : {t_current:6.2f} s\n"
                f" Pos : ({curr_x:6.2f}, {curr_y:6.2f})\n"
                f" |v| : {mag_v:6.2f} m/s\n"
                f" |a| : {mag_a:6.2f} m/s^2"
            )
            self.hud_text.set_text(hud_str)
            self.hud_text.set_visible(True)
        else:
            self.hud_text.set_visible(False)
            
        self.canvas.draw_idle()

    def toggle_play(self):
        if len(self.t_vec) == 0: return
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.btn_play.config(text="⏸ PAUSAR ANIMACIÓN", fg="#F59E0B")
            # Reiniciar si está al final del intervalo
            t_max = float(self.entry_tmax.get())
            if self.t_val.get() >= t_max - 0.05:
                self.t_val.set(float(self.entry_tmin.get()))
            self.play_step()
        else:
            self.btn_play.config(text="▶ REPRODUCIR ANIMACIÓN", fg=self.COLOR_ACELERACION)

    def play_step(self):
        if not self.is_playing: return
        current_t = self.t_val.get()
        t_max = float(self.entry_tmax.get())
        t_min = float(self.entry_tmin.get())
        
        t_range = t_max - t_min
        step = t_range / 350.0  # Velocidad fluida de reproducción
        
        if current_t < t_max:
            new_t = current_t + step
            if new_t > t_max: new_t = t_max
            self.t_val.set(new_t)
            self.update_anim(None)
            self.root.after(16, self.play_step) # ~60 FPS
        else:
            self.is_playing = False
            self.btn_play.config(text="▶ REPRODUCIR ANIMACIÓN", fg=self.COLOR_ACELERACION)

if __name__ == "__main__":
    root = tk.Tk()
    app = ParametricDashboardChivo(root)
    root.mainloop()
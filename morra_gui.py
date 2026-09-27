import random
import asyncio
import json
import os
import ssl
import threading
import urllib.request
import tkinter as tk
from tkinter import messagebox
from collections import Counter
from datetime import datetime
import urllib.request

# Gestione dinamica dell'importazione di websockets per evitare blocchi
try:
    import websockets
except ImportError:
    websockets = None
    
VERSIONE_ATTUALE = "1.1.0" 
GITHUB_REPO = "apexbytestudios/Morra"  # Sostituisci con la tua repo GitHub reale

def verifica_aggiornamenti_github(parent):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            tag_latest = data.get("tag_name", "").strip("v")
            
            if tag_latest and tag_latest != VERSIONE_ATTUALE:
                mostra_warning_win95(
                    parent,
                    "Aggiornamento Disponibile",
                    f"È disponibile una nuova versione ({tag_latest})!\n"
                    f"Versione attuale: {VERSIONE_ATTUALE}\n\n"
                    f"Scarica l'aggiornamento da GitHub."
                )
    except Exception as e:
        print(f"Impossibile verificare gli aggiornamenti: {e}")

# =============================================================================
# FILE SALVATAGGIO LOCALE
# =============================================================================
RECORD_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "morra_record.json")

# =============================================================================
# PALETTE E STILI WINDOWS 95
# =============================================================================
W = {
    "bg":           "#c0c0c0",   # grigio classico
    "bg_dark":      "#808080",   # grigio scuro (bordi ombra)
    "bg_light":     "#ffffff",   # bianco (bordi luce)
    "title_bg":     "#000080",   # blu navy titlebar
    "title_fg":     "#ffffff",
    "btn_bg":       "#c0c0c0",
    "btn_active":   "#c0c0c0",
    "text":         "#000000",
    "text_inv":     "#ffffff",
    "sunken_bg":    "#ffffff",
    "select_bg":    "#000080",
    "select_fg":    "#ffffff",
    "green":        "#008000",
    "red":          "#800000",
    "win_bg":       "#c0c0c0",
}

FONT_NORMAL  = ("MS Sans Serif", 8)
FONT_BOLD    = ("MS Sans Serif", 8, "bold")
FONT_TITLE   = ("MS Sans Serif", 12, "bold")
FONT_SCORE   = ("MS Sans Serif", 14, "bold")
FONT_MONO    = ("Courier New", 8)
FONT_LOGO    = ("MS Sans Serif", 24, "bold")

# Helper UI stile Win95
def win95_frame(parent, **kwargs):
    kw = {"bg": W["bg"], "relief": "raised", "bd": 2}
    kw.update(kwargs)
    return tk.Frame(parent, **kw)

def win95_label_frame(parent, text="", **kwargs):
    kw = {"bg": W["bg"], "fg": W["text"], "font": FONT_BOLD,
          "relief": "groove", "bd": 2}
    kw.update(kwargs)
    return tk.LabelFrame(parent, text=text, **kw)

def win95_button(parent, text, command, width=10, **kwargs):
    kw = {
        "text": text, "command": command,
        "font": FONT_NORMAL,
        "bg": W["btn_bg"], "fg": W["text"],
        "activebackground": W["btn_active"], "activeforeground": W["text"],
        "relief": "raised", "bd": 2,
        "cursor": "arrow", "width": width,
        "padx": 4, "pady": 2,
    }
    kw.update(kwargs)
    return tk.Button(parent, **kw)

def win95_entry(parent, width=8, **kwargs):
    kw = {
        "width": width, "font": FONT_NORMAL,
        "bg": W["sunken_bg"], "fg": W["text"],
        "insertbackground": W["text"],
        "relief": "sunken", "bd": 2,
    }
    kw.update(kwargs)
    return tk.Entry(parent, **kw)

def win95_radiobutton(parent, text, variable, value, **kwargs):
    kw = {
        "text": text, "variable": variable, "value": value,
        "font": FONT_NORMAL, "bg": W["bg"], "fg": W["text"],
        "activebackground": W["bg"], "selectcolor": W["bg"],
        "relief": "flat",
    }
    kw.update(kwargs)
    return tk.Radiobutton(parent, **kw)

def win95_titlebar(parent, title, close_cmd=None):
    bar = tk.Frame(parent, bg=W["title_bg"], pady=3)
    bar.pack(fill="x")
    tk.Label(bar, text=title, font=FONT_BOLD,
             bg=W["title_bg"], fg=W["title_fg"],
             padx=4).pack(side=tk.LEFT)
    if close_cmd:
        tk.Button(bar, text=" X ", command=close_cmd,
                  font=FONT_BOLD, bg=W["btn_bg"], fg=W["text"],
                  relief="raised", bd=2, padx=2, pady=0,
                  cursor="arrow").pack(side=tk.RIGHT, padx=2, pady=1)

def mostra_warning_win95(parent, titolo, messaggio, on_close=None):
    win = tk.Toplevel(parent)
    win.title(titolo)
    win.resizable(False, False)
    win.configure(bg=W["bg"])
    win.grab_set()  # Rende la finestra modale

    def chiudi():
        win.destroy()
        if on_close:
            on_close()

    win.protocol("WM_DELETE_WINDOW", chiudi)
    win95_titlebar(win, f"  {titolo}", close_cmd=chiudi)

    outer = tk.Frame(win, bg=W["bg"], padx=12, pady=12)
    outer.pack(fill="both", expand=True)

    body = tk.Frame(outer, bg=W["bg"])
    body.pack(fill="both", expand=True, pady=(0, 12))

    # Canvas per l'icona Warning classica Win95 (Triangolo giallo)
    canvas = tk.Canvas(body, width=32, height=32, bg=W["bg"], highlightthickness=0)
    canvas.pack(side=tk.LEFT, padx=(0, 12))

    canvas.create_polygon(16, 2, 30, 28, 2, 28, fill="#FFFF00", outline="#000000", width=2)
    canvas.create_rectangle(15, 8, 17, 18, fill="#000000", outline="#000000")
    canvas.create_rectangle(15, 21, 17, 23, fill="#000000", outline="#000000")

    lbl = tk.Label(body, text=messaggio, font=FONT_NORMAL, bg=W["bg"], fg=W["text"], justify="left", wraplength=280)
    lbl.pack(side=tk.LEFT, fill="both", expand=True)

    btn_frame = tk.Frame(outer, bg=W["bg"])
    btn_frame.pack()
    win95_button(btn_frame, "OK", command=chiudi, width=8).pack()
    
def mostra_info_win95(parent, titolo, messaggio, on_close=None):
    popup = tk.Toplevel(parent)
    popup.transient(parent)
    popup.grab_set()
    win95_titlebar(popup, f"  {titolo}", close_cmd=lambda: _chiudi_popup(popup, on_close))
    
    outer = tk.Frame(popup, bg=W["bg"], padx=12, pady=12)
    outer.pack(fill="both", expand=True)

    f_content = tk.Frame(outer, bg=W["bg"])
    f_content.pack(fill="both", expand=True, pady=(0, 10))

    # Icona di informazione Win95
    lbl_icon = tk.Label(f_content, text="i", font=("Courier", 16, "bold"), fg="white", bg="#000080", width=2, height=1)
    lbl_icon.pack(side=tk.LEFT, padx=(0, 10), anchor="n")

    lbl_msg = tk.Label(f_content, text=messaggio, font=FONT_NORMAL, bg=W["bg"], fg=W["text"], justify="left", wraplength=300)
    lbl_msg.pack(side=tk.LEFT, fill="both", expand=True)

    btn_ok = win95_button(outer, "OK", command=lambda: _chiudi_popup(popup, on_close), width=10)
    btn_ok.pack(anchor="e")


def _chiudi_popup(popup, callback):
    popup.destroy()
    if callback:
        callback()

# =============================================================================
# GESTIONE NETWORK / RETE RENDER
# =============================================================================
class NetworkConnection:
    def __init__(self, host, player_name, room_code, room_pass, punti, on_message=None, on_disconnect=None, on_init=None):
        self.host = host
        self.player_name = player_name
        self.room_code = room_code
        self.room_pass = room_pass
        self.punti = punti
        
        self.on_message = on_message
        self.on_disconnect = on_disconnect
        self.on_init = on_init

        self.ws = None
        self.ws_loop = None

    def start(self):
        """Avvia la connessione in un thread separato."""
        if websockets is None:
            if self.on_disconnect:
                self.on_disconnect("Modulo 'websockets' non installato su questo sistema.")
            return
        threading.Thread(target=self._connetti_websocket, daemon=True).start()

    def send(self, data):
        """Invia un messaggio al server in modo thread-safe."""
        if self.ws and self.ws_loop and self.ws_loop.is_running():
            msg = json.dumps(data) if isinstance(data, dict) else data
            asyncio.run_coroutine_threadsafe(self.ws.send(msg), self.ws_loop)

    def close(self):
        """Chiude la connessione WebSocket in modo pulito."""
        if self.ws and self.ws_loop and self.ws_loop.is_running():
            asyncio.run_coroutine_threadsafe(self.ws.send(json.dumps({"type": "leave"})), self.ws_loop)
            asyncio.run_coroutine_threadsafe(self.ws.close(), self.ws_loop)
        self.ws = None
        self.ws_loop = None

    def _connetti_websocket(self):
        ws_url = f"wss://{self.host}" if not self.host.startswith("ws") else self.host

        ssl_ctx = ssl.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl.CERT_NONE

        async def ws_handler():
            try:
                async with websockets.connect(
                    ws_url,
                    ssl=ssl_ctx,
                    ping_interval=20,
                    ping_timeout=20,
                ) as ws:
                    self.ws = ws
                    self.ws_loop = asyncio.get_running_loop()

                    join_data = {
                        "type": "join",
                        "player_name": self.player_name,
                        "room_code": self.room_code,
                        "room_pass": self.room_pass,
                        "punti_vittoria": self.punti,
                    }
                    await ws.send(json.dumps(join_data))

                    async for message in ws:
                        data = json.loads(message)
                        msg_type = data.get("type")

                        if msg_type == "error":
                            err_msg = data.get("msg")
                            if self.on_disconnect:
                                self.on_disconnect(err_msg)
                            break

                        elif msg_type == "init":
                            opp_name = data.get("opponent_name", "Avversario")
                            if self.on_init:
                                self.on_init(opp_name)

                        # All'interno di _connetti_websocket in morra_gui_4.py
                        elif msg_type in ("round_result", "player_left", "opponent_left", "restart_requested_by", "restart_game"):
                            if self.on_message:
                                self.on_message(data)

            except Exception as e:
                if self.on_disconnect:
                    self.on_disconnect(str(e))

        asyncio.run(ws_handler())

# =============================================================================
# GESTIONE RECORD LOCALI (SINGLE PLAYER)
# =============================================================================
def carica_record():
    struttura_base = {
        "facile":    {"vittorie": 0, "sconfitte": 0, "partite": []},
        "medio":     {"vittorie": 0, "sconfitte": 0, "partite": []},
        "difficile": {"vittorie": 0, "sconfitte": 0, "partite": []},
    }
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, "r", encoding="utf-8") as f:
                dati = json.load(f)
            if isinstance(dati, dict):
                for diff in struttura_base:
                    if diff not in dati or not isinstance(dati[diff], dict):
                        dati[diff] = struttura_base[diff]
                    else:
                        for k in ("vittorie", "sconfitte", "partite"):
                            if k not in dati[diff]:
                                dati[diff][k] = struttura_base[diff][k]
                return dati
        except Exception:
            pass
    return struttura_base

def salva_record(dati):
    try:
        with open(RECORD_FILE, "w", encoding="utf-8") as f:
            json.dump(dati, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Errore Salvataggio", f"Impossibile salvare i record: {e}")

def registra_risultato(diff, puntiplayer, puntiai, punti_vittoria, esito_tipo):
    dati = carica_record()
    if diff not in dati:
        dati[diff] = {"vittorie": 0, "sconfitte": 0, "partite": []}
    
    if esito_tipo is True or esito_tipo == "Vittoria":
        dati[diff]["vittorie"] += 1
        esito_str = "Vittoria"
    elif esito_tipo is False or esito_tipo == "Sconfitta":
        dati[diff]["sconfitte"] += 1
        esito_str = "Sconfitta"
    else:
        esito_str = "Pareggio"
        
    voce = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "esito": esito_str,
        "punteggio": f"{puntiplayer}-{puntiai}",
        "punti_vittoria": punti_vittoria,
    }
    dati[diff]["partite"].insert(0, voce)
    dati[diff]["partite"] = dati[diff]["partite"][:20]
    salva_record(dati)

def azzera_record(callback=None):
    if messagebox.askyesno("Morra", "Azzerare tutti i record locali?"):
        struttura_vuota = {
            "facile":    {"vittorie": 0, "sconfitte": 0, "partite": []},
            "medio":     {"vittorie": 0, "sconfitte": 0, "partite": []},
            "difficile": {"vittorie": 0, "sconfitte": 0, "partite": []},
        }
        salva_record(struttura_vuota)
        messagebox.showinfo("Morra", "Tutti i record locali sono stati cancellati.")
        if callback:
            callback()

# =============================================================================
# FINESTRA LEADERBOARD MONDIALE MULTIPLAYER
# =============================================================================
def apri_leaderboard_mondiale(parent, host="morra-server.onrender.com"):
    win = tk.Toplevel(parent)
    win.title("Leaderboard Mondiale Multiplayer")
    win.geometry("540x480")
    win.resizable(False, False)
    win.configure(bg=W["bg"])
    win.grab_set()

    win95_titlebar(win, "  Leaderboard Mondiale - Multiplayer", close_cmd=win.destroy)

    outer = tk.Frame(win, bg=W["bg"], padx=8, pady=8)
    outer.pack(fill="both", expand=True)

    frame_st = win95_label_frame(outer, text=" Partite Multiplayer Globali ")
    frame_st.pack(fill="both", expand=True, pady=(0, 8))

    frame_lb = tk.Frame(frame_st, bg=W["bg"])
    frame_lb.pack(fill="both", expand=True, padx=4, pady=4)

    listbox = tk.Listbox(frame_lb, font=FONT_MONO, height=14,
                         activestyle="none",
                         bg=W["sunken_bg"], fg=W["text"],
                         selectbackground=W["select_bg"],
                         selectforeground=W["select_fg"],
                         relief="sunken", bd=2)
    sb = tk.Scrollbar(frame_lb, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=sb.set)
    listbox.pack(side=tk.LEFT, fill="both", expand=True)
    sb.pack(side=tk.RIGHT, fill="y")

    lbl_status = tk.Label(outer, text="Caricamento in corso dal server...", font=FONT_NORMAL, bg=W["bg"], fg=W["text"])
    lbl_status.pack(pady=(0, 4))

    def carica_dati():
        ws_url = host
        if ws_url.startswith("http://"):
            ws_url = ws_url.replace("http://", "ws://")
        elif ws_url.startswith("https://"):
            ws_url = ws_url.replace("https://", "wss://")
        elif not ws_url.startswith("ws://") and not ws_url.startswith("wss://"):
            ws_url = "wss://" + ws_url

        ws_url = ws_url.split("/api")[0]

        async def fetch():
            max_tentativi = 5
            timeout_per_tentativo = 12
            
            for tentativo in range(1, max_tentativi + 1):
                try:
                    win.after(0, lambda t=tentativo: lbl_status.config(
                        text=f"Sveglio il server Render... Tentativo {t}/{max_tentativi}"
                    ))
                    
                    async def do_connect():
                        async with websockets.connect(ws_url, open_timeout=10) as ws:
                            await ws.send(json.dumps({"type": "get_leaderboard"}))
                            response = await ws.recv()
                            return json.loads(response)

                    data = await asyncio.wait_for(do_connect(), timeout=timeout_per_tentativo)
                    
                    if data.get("type") == "leaderboard_data":
                        partite = data.get("data", [])
                        win.after(0, lambda: aggiorna_ui(partite))
                        return

                except (asyncio.TimeoutError, Exception):
                    if tentativo == max_tentativi:
                        win.after(0, lambda: lbl_status.config(
                            text="Il server non ha risposto in tempo. Riprova tra 10 secondi."
                        ))
                    else:
                        await asyncio.sleep(1)

        asyncio.run(fetch())

    def aggiorna_ui(partite):
        listbox.delete(0, tk.END)
        lbl_status.config(text=f"Totale partite registrate: {len(partite)}")

        if not partite:
            listbox.insert(tk.END, "  (Nessuna partita multiplayer registrata sul server)")
        else:
            listbox.insert(tk.END, f"  {'DATA':<16} {'VINCITORE':<12} {'PERDENTE':<12} {'SCORE':<7} STANZA")
            listbox.insert(tk.END, "  " + "-" * 62)
            for p in partite:
                data_str = p.get("data", "N/D")
                vincitore = p.get("vincitore", "Ignoto")[:11]
                perdente = p.get("perdente", "Ignoto")[:11]
                score = p.get("punteggio", "0-0")
                stanza = p.get("stanza", "-")[:10]

                riga = f"  {data_str:<16} {vincitore:<12} {perdente:<12} {score:<7} {stanza}"
                listbox.insert(tk.END, riga)

    threading.Thread(target=carica_dati, daemon=True).start()

    frame_btn = tk.Frame(outer, bg=W["bg"])
    frame_btn.pack()
    win95_button(frame_btn, "Aggiorna", command=lambda: threading.Thread(target=carica_dati, daemon=True).start(), width=12).pack(side=tk.LEFT, padx=6)
    win95_button(frame_btn, "Chiudi", command=win.destroy, width=10).pack(side=tk.LEFT, padx=6)

# =============================================================================
# FINESTRA RECORD LOCALI
# =============================================================================
def apri_finestra_record(parent):
    dati = carica_record()
    win = tk.Toplevel(parent)
    win.title("Record Partite Single Player")
    win.geometry("500x480")
    win.resizable(False, False)
    win.configure(bg=W["bg"])
    win.grab_set()

    win95_titlebar(win, "  Record Partite Single Player", close_cmd=lambda: _chiudi_record(win, parent))

    outer = tk.Frame(win, bg=W["bg"], padx=8, pady=8)
    outer.pack(fill="both", expand=True)

    DIFF_LIST = [
        ("Facile",    "facile"),
        ("Medio",     "medio"),
        ("Difficile", "difficile"),
    ]

    frame_tot = win95_label_frame(outer, text=" Statistiche Generali ")
    frame_tot.pack(fill="x", pady=(0, 8))

    header = tk.Frame(frame_tot, bg=W["bg"])
    header.pack(fill="x", pady=4)

    for col, (label, chiave) in enumerate(DIFF_LIST):
        v   = dati[chiave]["vittorie"]
        s   = dati[chiave]["sconfitte"]
        tot = v + s
        perc = f"{round(v / tot * 100)}%" if tot > 0 else "N/D"

        cell = win95_frame(header, relief="raised", bd=2)
        cell.grid(row=0, column=col, padx=6, pady=2, sticky="nsew")
        header.columnconfigure(col, weight=1)

        tk.Label(cell, text=label, font=FONT_BOLD,
                 bg=W["bg"], fg=W["text"]).pack(pady=(4, 2))
        tk.Label(cell, text=f"Vittorie:  {v}",
                 font=FONT_NORMAL, bg=W["bg"], fg=W["green"],
                 anchor="w").pack(fill="x", padx=6)
        tk.Label(cell, text=f"Sconfitte: {s}",
                 font=FONT_NORMAL, bg=W["bg"], fg=W["red"],
                 anchor="w").pack(fill="x", padx=6)
        tk.Label(cell, text=f"Win rate:  {perc}",
                 font=FONT_NORMAL, bg=W["bg"], fg=W["text"],
                 anchor="w").pack(fill="x", padx=6, pady=(0, 4))

    frame_st = win95_label_frame(outer, text=" Ultime Partite vs AI ")
    frame_st.pack(fill="both", expand=True, pady=(0, 8))

    var_tab = tk.StringVar(value="facile")
    frame_tabs = tk.Frame(frame_st, bg=W["bg"])
    frame_tabs.pack(anchor="w", pady=(2, 4))

    for label, chiave in DIFF_LIST:
        win95_radiobutton(frame_tabs, label, var_tab, chiave).pack(side=tk.LEFT, padx=6)

    frame_lb = tk.Frame(frame_st, bg=W["bg"])
    frame_lb.pack(fill="both", expand=True)

    listbox = tk.Listbox(frame_lb, font=FONT_MONO, height=8,
                         activestyle="none",
                         bg=W["sunken_bg"], fg=W["text"],
                         selectbackground=W["select_bg"],
                         selectforeground=W["select_fg"],
                         relief="sunken", bd=2)
    sb = tk.Scrollbar(frame_lb, orient="vertical", command=listbox.yview)
    listbox.config(yscrollcommand=sb.set)
    listbox.pack(side=tk.LEFT, fill="both", expand=True)
    sb.pack(side=tk.RIGHT, fill="y")

    def aggiorna_listbox(*_):
        listbox.delete(0, tk.END)
        partite = dati.get(var_tab.get(), {}).get("partite", [])
        if not partite:
            listbox.insert(tk.END, "  (Nessuna partita registrata)")
        else:
            listbox.insert(tk.END, f"  {'DATA':<17}{'ESITO':<12}{'SCORE':<8}OBJ")
            listbox.insert(tk.END, "  " + "-" * 44)
            for p in partite:
                if p["esito"] == "Vittoria":
                    ic = "[V]"
                elif p["esito"] == "Sconfitta":
                    ic = "[S]"
                else:
                    ic = "[P]"
                riga = (f"  {p['data']:<17}{ic} {p['esito']:<10}"
                        f"{p['punteggio']:<8}(a {p['punti_vittoria']})")
                listbox.insert(tk.END, riga)

    aggiorna_listbox()
    var_tab.trace_add("write", aggiorna_listbox)

    frame_btn = tk.Frame(outer, bg=W["bg"])
    frame_btn.pack()

    win95_button(frame_btn, "Azzera Record",
                 command=lambda: azzera_record(lambda: _chiudi_record(win, parent)),
                 width=14).pack(side=tk.LEFT, padx=6)
    win95_button(frame_btn, "Chiudi",
                 command=lambda: _chiudi_record(win, parent), width=10).pack(side=tk.LEFT, padx=6)

def _chiudi_record(win, parent):
    win.destroy()
    if hasattr(parent, "_frame_corrente") and isinstance(parent._frame_corrente, SchermataMenu):
        parent._frame_corrente.aggiorna_status()

# =============================================================================
# LOGICA AI
# =============================================================================
def mossa_ai_facile():
    x_ai = random.randint(1, 5)
    y_ai = random.randint(x_ai + 1, x_ai + 5)
    return x_ai, y_ai

def mossa_ai_medio(storico_x, storico_y):
    x_ai = random.randint(1, 5)
    if len(storico_x) < 2:
        return mossa_ai_facile()
    if random.random() < 0.7:
        x_pred = Counter(storico_x[-5:]).most_common(1)[0][0]
        y_ai = x_ai + x_pred
    else:
        y_ai = random.randint(x_ai + 1, x_ai + 5)

    y_ai = min(max(y_ai, x_ai + 1), x_ai + 5)
    return x_ai, y_ai

def mossa_ai_difficile(storico_x, storico_y):
    if len(storico_x) < 3:
        return mossa_ai_medio(storico_x, storico_y)

    ultima_mossa_player = storico_x[-1]
    seguiti = [storico_x[i + 1] for i in range(len(storico_x) - 1) if storico_x[i] == ultima_mossa_player]
    if seguiti:
        x_pred = Counter(seguiti).most_common(1)[0][0]
    else:
        ultime_x = storico_x[-10:]
        pesi = {}
        for idx, val in enumerate(ultime_x):
            pesi[val] = pesi.get(val, 0) + (idx + 1)
        x_pred = max(pesi, key=pesi.get)

    x_ai = random.randint(1, 5)
    if random.random() < 0.95:
        y_ai = x_ai + x_pred
    else:
        y_ai = random.randint(x_ai + 1, x_ai + 5)

    y_ai = min(max(y_ai, x_ai + 1), x_ai + 5)
    return x_ai, y_ai

def scegli_mossa_ai(diff, storico_x, storico_y):
    if diff == "facile":
        return mossa_ai_facile()
    elif diff == "medio":
        return mossa_ai_medio(storico_x, storico_y)
    else:
        return mossa_ai_difficile(storico_x, storico_y)

# =============================================================================
# APPLICAZIONE MAIN
# =============================================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gioco della Morra")
        self.geometry("520x630")
        self.resizable(False, False)
        self.configure(bg=W["bg"])
        self.after(2000, lambda: verifica_aggiornamenti_github(self))

        try:
            icon = tk.PhotoImage(width=16, height=16)
            for y in range(16):
                for x in range(16):
                    icon.put("#000080", (x, y))
            self.iconphoto(True, icon)
        except Exception:
            pass

        self.var_difficolta = tk.StringVar(value="facile")
        self.var_punti      = tk.StringVar(value="3")
        self._frame_corrente = None
        self.mostra_menu()

    def mostra_frame(self, FrameClass, **kwargs):
        if self._frame_corrente:
            self._frame_corrente.destroy()
        self._frame_corrente = FrameClass(self, **kwargs)
        self._frame_corrente.pack(fill="both", expand=True)

    def mostra_menu(self):
        self.mostra_frame(SchermataMenu)

    def mostra_gioco(self, difficolta, punti_vittoria):
        self.mostra_frame(SchermataGioco,
                          difficolta=difficolta,
                          punti_vittoria=punti_vittoria)

    def mostra_multiplayer_lobby(self):
        self.mostra_frame(SchermataMultiplayerLobby)

    def mostra_gioco_multiplayer(self, net, my_name, opp_name, room_code, punti_vittoria):
        self.mostra_frame(SchermataGiocoMultiplayer,
                          net=net,
                          my_name=my_name,
                          opp_name=opp_name,
                          room_code=room_code,
                          punti_vittoria=punti_vittoria)

# =============================================================================
# SCHERMATA MENU PRINCIPALE
# =============================================================================
class SchermataMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=W["bg"])
        self._costruisci()

    def _costruisci(self):
        win95_titlebar(self, "  Gioco della Morra v2.5 - Online Edition")

        logo_frame = tk.Frame(self, bg=W["bg"], pady=12)
        logo_frame.pack(fill="x")

        tk.Label(logo_frame, text="MORRA",
                 font=FONT_LOGO, bg=W["bg"], fg=W["title_bg"],
                 relief="flat").pack()

        tk.Frame(self, bg=W["bg_dark"], height=2).pack(fill="x", padx=8)
        tk.Frame(self, bg=W["bg_light"], height=1).pack(fill="x", padx=8)

        outer = tk.Frame(self, bg=W["bg"], padx=12, pady=10)
        outer.pack(fill="x")

        # Selezione Punti
        frame_punti = win95_label_frame(outer, text=" Punti per Vincere (Modalita' AI) ")
        frame_punti.pack(fill="x", pady=(0, 8))

        fp1 = tk.Frame(frame_punti, bg=W["bg"])
        fp1.pack(pady=(4, 2))
        for val in ("3", "5", "7", "10", "random"):
            label = "Random" if val == "random" else val
            win95_radiobutton(fp1, label, self.master.var_punti, val).pack(side=tk.LEFT, padx=6)

        fp2 = tk.Frame(frame_punti, bg=W["bg"])
        fp2.pack(pady=(2, 6))
        win95_radiobutton(fp2, "Personalizzato:", self.master.var_punti, "custom").pack(side=tk.LEFT, padx=(6, 2))
        self.entry_custom_punti = win95_entry(fp2, width=5)
        self.entry_custom_punti.insert(0, "8")
        self.entry_custom_punti.pack(side=tk.LEFT, padx=4)

        frame_diff = win95_label_frame(outer, text=" Difficolta' AI ")
        frame_diff.pack(fill="x", pady=(0, 8))

        fd = tk.Frame(frame_diff, bg=W["bg"])
        fd.pack(pady=6)
        for label, val in [("Facile", "facile"), ("Medio", "medio"), ("Difficile", "difficile")]:
            win95_radiobutton(fd, label, self.master.var_difficolta, val).pack(side=tk.LEFT, padx=10)

        tk.Frame(self, bg=W["bg_dark"], height=2).pack(fill="x", padx=8)
        tk.Frame(self, bg=W["bg_light"], height=1).pack(fill="x", padx=8)

        frame_btn = tk.Frame(self, bg=W["bg"], pady=14)
        frame_btn.pack()

        win95_button(frame_btn, "Partita vs AI", command=self._avvia, width=12, font=FONT_BOLD).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn, "Online Render", command=self.master.mostra_multiplayer_lobby, width=13, font=FONT_BOLD).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn, "Leaderboard", command=lambda: apri_leaderboard_mondiale(self.master), width=11, font=FONT_BOLD).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn, "Record AI", command=lambda: apri_finestra_record(self.master), width=9).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn, "Esci", command=self.master.destroy, width=6).pack(side=tk.LEFT, padx=4)

        tk.Frame(self, bg=W["bg_dark"], height=2).pack(fill="x", side=tk.BOTTOM)
        status = tk.Frame(self, bg=W["bg"], pady=3)
        status.pack(fill="x", side=tk.BOTTOM)

        self.label_status = tk.Label(status, text="", font=FONT_NORMAL, bg=W["bg"], fg=W["text"], relief="sunken", bd=1, anchor="w")
        self.label_status.pack(fill="x", padx=4)
        self.aggiorna_status()

    def aggiorna_status(self):
        dati = carica_record()
        tot_v = sum(dati[d]["vittorie"] for d in dati if d in dati)
        tot_s = sum(dati[d]["sconfitte"] for d in dati if d in dati)
        self.label_status.config(text=f"  Vittorie totali vs AI: {tot_v}   Sconfitte: {tot_s}")

    def _avvia(self):
        scelta = self.master.var_punti.get()
        if scelta == "random":
            punti = random.randint(3, 15)
            messagebox.showinfo("Punti Casuali", f"I punti per questa partita saranno: {punti}")
        elif scelta == "custom":
            try:
                punti = int(self.entry_custom_punti.get())
                if punti <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Errore", "Inserisci un numero intero valido maggiore di 0 per i punti personalizzati.")
                return
        else:
            try:
                punti = int(scelta)
            except ValueError:
                messagebox.showerror("Errore", "Seleziona un numero di punti valido.")
                return

        self.master.mostra_gioco(
            difficolta=self.master.var_difficolta.get(),
            punti_vittoria=punti
        )

# =============================================================================
# LOBBY MULTIPLAYER CON PASSWORD E RICERCA STANZE (SERVER RENDER)
# =============================================================================
class SchermataMultiplayerLobby(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=W["bg"])
        self.net = None
        self._costruisci()

    def _costruisci(self):
        win95_titlebar(self, "  Multiplayer Online - Stanza Privata", close_cmd=self._torna_menu)

        outer = tk.Frame(self, bg=W["bg"], padx=10, pady=8)
        outer.pack(fill="both", expand=True)

        sl = {"font": FONT_NORMAL, "bg": W["bg"], "fg": W["text"], "anchor": "w"}

        # CONFIGURAZIONE SERVER
        frame_config = win95_label_frame(outer, text=" Connessione al Server ")
        frame_config.pack(fill="x", pady=(0, 6))

        tk.Label(frame_config, text="Host Render:", **sl).grid(row=0, column=0, sticky="w", padx=6, pady=3)
        self.entry_server_host = win95_entry(frame_config, width=22)
        self.entry_server_host.insert(0, "morra-server.onrender.com")
        self.entry_server_host.grid(row=0, column=1, padx=6, pady=3)

        tk.Label(frame_config, text="Porta SSL/TCP:", **sl).grid(row=1, column=0, sticky="w", padx=6, pady=3)
        self.entry_server_port = win95_entry(frame_config, width=8)
        self.entry_server_port.insert(0, "443")
        self.entry_server_port.grid(row=1, column=1, sticky="w", padx=6, pady=3)

        # CONFIGURAZIONE STANZA E CREDENZIALI
        frame_player = win95_label_frame(outer, text=" Stanza Privata ")
        frame_player.pack(fill="x", pady=(0, 6))

        tk.Label(frame_player, text="Il tuo Nome:", **sl).grid(row=0, column=0, sticky="w", padx=6, pady=3)
        self.entry_player_name = win95_entry(frame_player, width=16)
        self.entry_player_name.insert(0, f"Giocatore_{random.randint(100, 999)}")
        self.entry_player_name.grid(row=0, column=1, padx=6, pady=3)

        tk.Label(frame_player, text="Nome/ID Stanza:", **sl).grid(row=1, column=0, sticky="w", padx=6, pady=3)
        self.entry_room_code = win95_entry(frame_player, width=16)
        self.entry_room_code.insert(0, "StanzaPrivata")
        self.entry_room_code.grid(row=1, column=1, padx=6, pady=3)

        tk.Label(frame_player, text="Password Stanza:", **sl).grid(row=2, column=0, sticky="w", padx=6, pady=3)
        self.entry_room_pass = win95_entry(frame_player, width=16, show="*")
        self.entry_room_pass.insert(0, "1234")
        self.entry_room_pass.grid(row=2, column=1, padx=6, pady=3)

        tk.Label(frame_player, text="Punti Vittoria:", **sl).grid(row=3, column=0, sticky="w", padx=6, pady=3)
        self.entry_punti = win95_entry(frame_player, width=8)
        self.entry_punti.insert(0, "5")
        self.entry_punti.grid(row=3, column=1, sticky="w", padx=6, pady=3)

        # PULSANTI D'AZIONE
        frame_btn_actions = tk.Frame(outer, bg=W["bg"])
        frame_btn_actions.pack(pady=8)

        win95_button(frame_btn_actions, "Crea o Entra in Stanza", command=self._connetti_server, width=18, font=FONT_BOLD).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn_actions, "Cerca Stanze", command=self._apri_ricerca_stanze, width=14, font=FONT_BOLD).pack(side=tk.LEFT, padx=4)

        # BARRA INFERIORE
        frame_bottom = tk.Frame(outer, bg=W["bg"])
        frame_bottom.pack(fill="x", pady=4, side=tk.BOTTOM)

        win95_button(frame_bottom, "< Indietro", command=self._torna_menu, width=10).pack(side=tk.LEFT)
        self.label_status = tk.Label(frame_bottom, text="Imposta Nome e Password Stanza.", font=FONT_NORMAL, bg=W["bg"], fg=W["text"])
        self.label_status.pack(side=tk.RIGHT, padx=6)

    def _apri_ricerca_stanze(self):
        host = self.entry_server_host.get().strip()
        ws_url = host
        if ws_url.startswith("http://"):
            ws_url = ws_url.replace("http://", "ws://")
        elif ws_url.startswith("https://"):
            ws_url = ws_url.replace("https://", "wss://")
        elif not ws_url.startswith("ws://") and not ws_url.startswith("wss://"):
            ws_url = "wss://" + ws_url

        win = tk.Toplevel(self)
        win.title("Stanze Disponibili")
        win.geometry("450x380")
        win.resizable(False, False)
        win.configure(bg=W["bg"])
        win.grab_set()

        win95_titlebar(win, "  Stanze Online in Attesa", close_cmd=win.destroy)

        outer = tk.Frame(win, bg=W["bg"], padx=8, pady=8)
        outer.pack(fill="both", expand=True)

        frame_st = win95_label_frame(outer, text=" Stanze Attive ")
        frame_st.pack(fill="both", expand=True, pady=(0, 8))

        frame_lb = tk.Frame(frame_st, bg=W["bg"])
        frame_lb.pack(fill="both", expand=True, padx=4, pady=4)

        listbox = tk.Listbox(frame_lb, font=FONT_MONO, height=10,
                             activestyle="none",
                             bg=W["sunken_bg"], fg=W["text"],
                             selectbackground=W["select_bg"],
                             selectforeground=W["select_fg"],
                             relief="sunken", bd=2)
        sb = tk.Scrollbar(frame_lb, orient="vertical", command=listbox.yview)
        listbox.config(yscrollcommand=sb.set)
        listbox.pack(side=tk.LEFT, fill="both", expand=True)
        sb.pack(side=tk.RIGHT, fill="y")

        lbl_status = tk.Label(outer, text="Richiesta elenco stanze...", font=FONT_NORMAL, bg=W["bg"], fg=W["text"])
        lbl_status.pack(pady=(0, 4))

        def seleziona_stanza(event=None):
            selection = listbox.curselection()
            if not selection:
                return
            index = selection[0]
            val = listbox.get(index)
            if not val or val.startswith("  (") or val.startswith("  STANZA"):
                return
            parti = val.strip().split()
            if parti:
                room_code = parti[0]
                self.entry_room_code.delete(0, tk.END)
                self.entry_room_code.insert(0, room_code)
                win.destroy()

        listbox.bind("<Double-Button-1>", seleziona_stanza)

        def carica_stanze():
            async def fetch():
                try:
                    ssl_ctx = ssl.create_default_context()
                    ssl_ctx.check_hostname = False
                    ssl_ctx.verify_mode = ssl.CERT_NONE

                    async with websockets.connect(ws_url, ssl=ssl_ctx, open_timeout=10) as ws:
                        await ws.send(json.dumps({"type": "get_rooms"}))
                        res = await asyncio.wait_for(ws.recv(), timeout=8)
                        data = json.loads(res)
                        if data.get("type") == "rooms_list":
                            stanze = data.get("rooms", [])
                            win.after(0, lambda: aggiorna_ui(stanze))
                except Exception as e:
                    win.after(0, lambda: lbl_status.config(text=f"Errore caricamento: {e}"))

            asyncio.run(fetch())

        def aggiorna_ui(stanze):
            listbox.delete(0, tk.END)
            lbl_status.config(text="Doppio clic su una stanza per selezionarla.")

            if not stanze:
                listbox.insert(tk.END, "  (Nessuna stanza disponibile al momento)")
            else:
                listbox.insert(tk.END, f"  {'STANZA':<15} {'CREATORE':<12} {'PUNTI':<6} {'PROTETTA':<8}")
                listbox.insert(tk.END, "  " + "-" * 45)
                for s in stanze:
                    nome = s.get("room_code", "N/D")[:14]
                    host_player = s.get("host", "Ignoto")[:11]
                    punti = s.get("punti_vittoria", "5")
                    has_pass = "Sì" if s.get("has_password", False) else "No"

                    riga = f"  {nome:<15} {host_player:<12} {punti:<6} {has_pass:<8}"
                    listbox.insert(tk.END, riga)

        threading.Thread(target=carica_stanze, daemon=True).start()

        frame_btn = tk.Frame(outer, bg=W["bg"])
        frame_btn.pack()
        win95_button(frame_btn, "Seleziona", command=seleziona_stanza, width=12).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn, "Aggiorna", command=lambda: threading.Thread(target=carica_stanze, daemon=True).start(), width=10).pack(side=tk.LEFT, padx=4)
        win95_button(frame_btn, "Chiudi", command=win.destroy, width=10).pack(side=tk.LEFT, padx=4)

    def _connetti_server(self):
        host = self.entry_server_host.get().strip()
        name = self.entry_player_name.get().strip() or "Giocatore"
        room = self.entry_room_code.get().strip()
        password = self.entry_room_pass.get().strip()
        
        try:
            punti = int(self.entry_punti.get().strip())
        except ValueError:
            messagebox.showerror("Errore", "Inserire un numero di punti valido.")
            return

        self.label_status.config(text="Connessione via WebSocket...")

        def on_init(opp_name):
            self.after(0, lambda: self._avvia_multiplayer(name, opp_name, room, punti))

        def on_disconnect(err):
            self.after(0, lambda: mostra_warning_win95(self, "Errore Connessione", f"Connessione interrotta:\n{err}"))

        self.net = NetworkConnection(
            host=host,
            player_name=name,
            room_code=room,
            room_pass=password,
            punti=punti,
            on_init=on_init,
            on_disconnect=on_disconnect
        )
        self.net.start()

    def _avvia_multiplayer(self, my_name, opp_name, room_code, punti_vittoria):
        self.master.mostra_gioco_multiplayer(
            net=self.net,
            my_name=my_name,
            opp_name=opp_name,
            room_code=room_code,
            punti_vittoria=punti_vittoria
        )

    def _torna_menu(self):
        if self.net:
            self.net.close()
        self.master.mostra_menu()

# =============================================================================
# SCHERMATA DI GIOCO MULTIPLAYER ONLINE (CON TIMER E POPUP WIN95)
# =============================================================================
class SchermataGiocoMultiplayer(tk.Frame):
    def __init__(self, master, net, my_name, opp_name, room_code, punti_vittoria, tempo_turno=10):
        super().__init__(master, bg=W["bg"])
        self.net = net
        self.my_name = my_name
        self.opp_name = opp_name
        self.room_code = room_code
        self.punti_vittoria = punti_vittoria

        self.tempo_turno = tempo_turno       # Durata in secondi per ogni turno
        self.tempo_rimasto = tempo_turno
        self.timer_job = None               # Riferimento per annullare il timer dopo l'invio

        self.my_score = 0
        self.opp_score = 0
        self.game_over = False

        self._costruisci()

        # Collega i callback della connessione di rete a questa GUI
        self.net.on_message = lambda msg: self.after(0, self._on_network_msg, msg)
        self.net.on_disconnect = lambda err: self.after(0, self._on_disconnect, err)

        # Avvia il timer per il primo turno
        self._avvia_timer()

    def _costruisci(self):
        win95_titlebar(self, f"  Online - Stanza: {self.room_code}", close_cmd=self._abbandona)

        outer = tk.Frame(self, bg=W["bg"], padx=10, pady=8)
        outer.pack(fill="both", expand=True)

        frame_score = win95_label_frame(outer, text=f" Punteggio (Obiettivo: {self.punti_vittoria}) ")
        frame_score.pack(fill="x", pady=(0, 6))

        s_box = tk.Frame(frame_score, bg=W["bg"], pady=4)
        s_box.pack()

        self.lbl_me = tk.Label(s_box, text=f"{self.my_name} (Tu): 0", font=FONT_SCORE, bg=W["bg"], fg=W["green"])
        self.lbl_me.pack(side=tk.LEFT, padx=10)

        tk.Label(s_box, text="-", font=FONT_SCORE, bg=W["bg"], fg=W["text"]).pack(side=tk.LEFT)

        self.lbl_opp = tk.Label(s_box, text=f"{self.opp_name}: 0", font=FONT_SCORE, bg=W["bg"], fg=W["red"])
        self.lbl_opp.pack(side=tk.LEFT, padx=10)

        # --- LABEL TIMER ---
        self.lbl_timer = tk.Label(outer, text=f"Tempo rimasto: {self.tempo_turno}s", font=FONT_BOLD, bg=W["bg"], fg=W["red"])
        self.lbl_timer.pack(pady=(0, 4))

        frame_input = win95_label_frame(outer, text=" La tua Mossa ")
        frame_input.pack(fill="x", pady=(0, 6))

        f_dita = tk.Frame(frame_input, bg=W["bg"], pady=2)
        f_dita.pack()
        tk.Label(f_dita, text="Dita da mostrare (1-5):", font=FONT_NORMAL, bg=W["bg"], fg=W["text"]).pack(side=tk.LEFT, padx=4)
        self.var_dita = tk.IntVar(value=1)
        for i in range(1, 6):
            win95_radiobutton(f_dita, str(i), self.var_dita, i).pack(side=tk.LEFT, padx=2)

        f_somma = tk.Frame(frame_input, bg=W["bg"], pady=4)
        f_somma.pack()
        tk.Label(f_somma, text="Somma prevista (2-10):", font=FONT_NORMAL, bg=W["bg"], fg=W["text"]).pack(side=tk.LEFT, padx=4)
        self.entry_somma = win95_entry(f_somma, width=6)
        self.entry_somma.insert(0, "2")
        self.entry_somma.pack(side=tk.LEFT, padx=4)

        self.btn_invia = win95_button(frame_input, "Invia Mossa a Render", command=self._invia_mossa, width=18, font=FONT_BOLD)
        self.btn_invia.pack(pady=6)

        frame_log = win95_label_frame(outer, text=" Stato Partita ")
        frame_log.pack(fill="both", expand=True, pady=(0, 6))

        self.lbl_status = tk.Label(frame_log, text="Partita avviata! Fai la tua mossa.", font=FONT_NORMAL, bg=W["bg"], fg=W["text"], wraplength=420)
        self.lbl_status.pack(fill="both", expand=True, padx=6, pady=6)

        # BARRA PULSANTI DI NAVIGAZIONE E RIVINCIATA
        frame_btn_bottom = tk.Frame(outer, bg=W["bg"])
        frame_btn_bottom.pack(pady=4)

        self.btn_restart = win95_button(frame_btn_bottom, "Nuova Partita", command=self._richiedi_restart, width=14, font=FONT_BOLD)
        self.btn_restart.config(state="disabled")
        self.btn_restart.pack(side=tk.LEFT, padx=6)

        win95_button(frame_btn_bottom, "Abbandona Partita", command=self._abbandona, width=14).pack(side=tk.LEFT, padx=6)

    # =========================================================================
    # GESTIONE TIMER CONTO ALLA ROVESCIA
    # =========================================================================
    def _avvia_timer(self):
        self._ferma_timer()
        if not self.game_over:
            self.tempo_rimasto = self.tempo_turno
            self._aggiorna_timer()

    def _aggiorna_timer(self):
        self.lbl_timer.config(text=f"Tempo rimasto: {self.tempo_rimasto}s")
        if self.tempo_rimasto > 0:
            self.tempo_rimasto -= 1
            self.timer_job = self.after(1000, self._aggiorna_timer)
        else:
            self.lbl_timer.config(text="Tempo scaduto! Mossa automatica inviata.")
            self._mossa_automatica()

    def _ferma_timer(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def _mossa_automatica(self):
        """Invia una mossa predefinita se il tempo scade."""
        if str(self.btn_invia["state"]) != "disabled" and not self.game_over:
            try:
                dita = int(self.var_dita.get())
            except ValueError:
                dita = 1
            try:
                somma = int(self.entry_somma.get().strip())
                if not (2 <= somma <= 10):
                    somma = 2
            except ValueError:
                somma = 2

            self.btn_invia.config(state="disabled")
            self.net.send({"type": "move", "dita": dita, "somma": somma})
            self.lbl_status.config(text="Tempo scaduto! Mossa automatica inviata al server. In attesa dell'avversario...")

    # =========================================================================
    # AZIONI DI GIOCO E RETE
    # =========================================================================
    def _invia_mossa(self):
        try:
            dita = int(self.var_dita.get())
            somma = int(self.entry_somma.get().strip())
            if not (1 <= dita <= 5) or not (2 <= somma <= 10):
                raise ValueError
        except ValueError:
            mostra_warning_win95(self, "Errore Mossa", "Inserisci dita tra 1 e 5 e una somma prevista tra 2 e 10.")
            return

        self._ferma_timer()
        self.lbl_timer.config(text="Mossa inviata!")
        self.btn_invia.config(state="disabled")
        self.net.send({"type": "move", "dita": dita, "somma": somma})
        self.lbl_status.config(text="Mossa inviata al server. In attesa dell'avversario...")

    def _richiedi_restart(self):
        self.btn_restart.config(state="disabled")
        self.lbl_status.config(text="Richiesta di nuova partita inviata. In attesa della conferma dell'avversario...")
        self.net.send({"type": "restart_request"})

    def _on_network_msg(self, msg):
        msg_type = msg.get("type")
        
        if msg_type == "round_result":
            self._aggiorna_esito_turno(msg)

        elif msg_type == "restart_requested_by":
            sender = msg.get("player_name", "L'avversario")
            self.lbl_status.config(
                text=f"AVVISO: {sender} ha richiesto una Nuova Partita!\nPremi 'Nuova Partita' per accettare la sfida."
            )

        elif msg_type == "restart_game":
            self.game_over = False
            scores = msg.get("scores", {})
            self.my_score = scores.get(self.my_name, 0)
            self.opp_score = scores.get(self.opp_name, 0)

            self.lbl_me.config(text=f"{self.my_name} (Tu): {self.my_score}")
            self.lbl_opp.config(text=f"{self.opp_name}: {self.opp_score}")
            self.lbl_status.config(text="Nuova sessione avviata. Effettuare la mossa...")
            
            self.btn_invia.config(state="normal")
            self.btn_restart.config(state="disabled")
            self._avvia_timer()
            
        elif msg_type in ("player_left", "opponent_left"):
            self._ferma_timer()
            testo_msg = msg.get("message") or f"{msg.get('player_name', 'L\'avversario')} ha abbandonato la sessione."
            mostra_warning_win95(self, "Connessione Interrotta", testo_msg, on_close=self._abbandona)

    def _aggiorna_esito_turno(self, data):
        my_dita = data["moves"][self.my_name]["dita"]
        my_somma = data["moves"][self.my_name]["somma"]
        opp_dita = data["moves"][self.opp_name]["dita"]
        opp_somma = data["moves"][self.opp_name]["somma"]

        totale = data["totale"]
        self.my_score = data["scores"][self.my_name]
        self.opp_score = data["scores"][self.opp_name]

        self.lbl_me.config(text=f"{self.my_name} (Tu): {self.my_score}")
        self.lbl_opp.config(text=f"{self.opp_name}: {self.opp_score}")

        dettagli = (
            f"--- Risultato Turno ---\n"
            f"Tu ({self.my_name}): {my_dita} dita | Somma: {my_somma}\n"
            f"{self.opp_name}: {opp_dita} dita | Somma: {opp_somma}\n"
            f"Totale dita: {totale}\n\n"
            f"Esito: {data.get('esito_testo', '')}"
        )

        if self.my_score >= self.punti_vittoria or self.opp_score >= self.punti_vittoria:
            self._ferma_timer()
            self.game_over = True
            vincitore = self.my_name if self.my_score >= self.punti_vittoria else self.opp_name
            ho_vinto = (vincitore == self.my_name)
            
            # Disabilita l'invio e abilita il tasto per la rivincita
            self.btn_invia.config(state="disabled")
            self.btn_restart.config(state="normal")
            self.lbl_timer.config(text="STATO: Partita Conclusa")
            
            self.lbl_status.config(
                text=f"{dettagli}\n\n========================================\n"
                     f"  SESSIONE TERMINATA - VINCITORE: {vincitore}\n"
                     f"========================================\n"
                     f"Fare clic su 'Nuova Partita' per avviare una rivincita."
            )

            # Mostra il popup Win95 di fine partita
            if ho_vinto:
                mostra_info_win95(
                    self, 
                    "Vittoria!", 
                    f"Hai raggiunto {self.my_score} punti e hai vinto la partita contro {self.opp_name}!"
                )
            else:
                mostra_warning_win95(
                    self, 
                    "Sconfitta", 
                    f"{self.opp_name} ha raggiunto {self.opp_score} punti e ha vinto la partita.\nPuoi richiedere una rivincita cliccando 'Nuova Partita'."
                )
        else:
            self.lbl_status.config(text=dettagli)
            self.btn_invia.config(state="normal")
            self._avvia_timer()

    def _on_disconnect(self, err):
        self._ferma_timer()
        mostra_warning_win95(
            self,
            "Connessione Interrotta",
            f"La connessione con il server o con l'avversario è caduta:\n{err}"
        )
        self._abbandona()

    def _abbandona(self):
        self._ferma_timer()
        if hasattr(self, "net") and self.net:
            self.net.close()
        self.master.mostra_menu()
# =============================================================================
# SCHERMATA DI GIOCO SINGLE PLAYER (VS AI)
# =============================================================================
class SchermataGioco(tk.Frame):
    def __init__(self, master, difficolta, punti_vittoria):
        super().__init__(master, bg=W["bg"])
        self.difficolta = difficolta
        self.punti_vittoria = punti_vittoria

        self.player_score = 0
        self.ai_score = 0
        self.storico_x = []
        self.storico_y = []

        self._costruisci()

    def _costruisci(self):
        win95_titlebar(self, f"  Morra vs AI ({self.difficolta.capitalize()})", close_cmd=self._torna_menu)

        outer = tk.Frame(self, bg=W["bg"], padx=10, pady=8)
        outer.pack(fill="both", expand=True)

        frame_score = win95_label_frame(outer, text=f" Punteggio (Obiettivo: {self.punti_vittoria}) ")
        frame_score.pack(fill="x", pady=(0, 6))

        s_box = tk.Frame(frame_score, bg=W["bg"], pady=4)
        s_box.pack()

        self.lbl_player = tk.Label(s_box, text="Tu: 0", font=FONT_SCORE, bg=W["bg"], fg=W["green"])
        self.lbl_player.pack(side=tk.LEFT, padx=20)

        tk.Label(s_box, text="-", font=FONT_SCORE, bg=W["bg"], fg=W["text"]).pack(side=tk.LEFT)

        self.lbl_ai = tk.Label(s_box, text="AI: 0", font=FONT_SCORE, bg=W["bg"], fg=W["red"])
        self.lbl_ai.pack(side=tk.LEFT, padx=20)

        frame_input = win95_label_frame(outer, text=" La tua Mossa ")
        frame_input.pack(fill="x", pady=(0, 6))

        f_dita = tk.Frame(frame_input, bg=W["bg"], pady=2)
        f_dita.pack()
        tk.Label(f_dita, text="Dita da mostrare (1-5):", font=FONT_NORMAL, bg=W["bg"], fg=W["text"]).pack(side=tk.LEFT, padx=4)
        self.var_dita = tk.IntVar(value=1)
        for i in range(1, 6):
            win95_radiobutton(f_dita, str(i), self.var_dita, i).pack(side=tk.LEFT, padx=2)

        f_somma = tk.Frame(frame_input, bg=W["bg"], pady=4)
        f_somma.pack()
        tk.Label(f_somma, text="Somma prevista (2-10):", font=FONT_NORMAL, bg=W["bg"], fg=W["text"]).pack(side=tk.LEFT, padx=4)
        self.entry_somma = win95_entry(f_somma, width=6)
        self.entry_somma.insert(0, "2")
        self.entry_somma.pack(side=tk.LEFT, padx=4)

        win95_button(frame_input, "Gioca Turno", command=self._gioca_turno, width=14, font=FONT_BOLD).pack(pady=6)

        frame_log = win95_label_frame(outer, text=" Ultimo Esito ")
        frame_log.pack(fill="both", expand=True, pady=(0, 6))

        self.lbl_status = tk.Label(frame_log, text="Fai la tua mossa e premi 'Gioca Turno'!", font=FONT_NORMAL, bg=W["bg"], fg=W["text"], wraplength=420)
        self.lbl_status.pack(fill="both", expand=True, padx=6, pady=6)

        frame_nav = tk.Frame(outer, bg=W["bg"])
        frame_nav.pack()
        win95_button(frame_nav, "< Menu Principale", command=self._torna_menu, width=16).pack()

    def _gioca_turno(self):
        try:
            x_p = int(self.var_dita.get())
            y_p = int(self.entry_somma.get().strip())
            if not (1 <= x_p <= 5) or not (2 <= y_p <= 10):
                raise ValueError
        except ValueError:
            mostra_warning_win95(self, "Errore Mossa", "Inserisci dita tra 1 e 5 e una somma prevista tra 2 e 10.")
            return

        x_ai, y_ai = scegli_mossa_ai(self.difficolta, self.storico_x, self.storico_y)

        self.storico_x.append(x_p)
        self.storico_y.append(y_p)

        totale = x_p + x_ai
        p_win = (y_p == totale)
        ai_win = (y_ai == totale)

        if p_win and not ai_win:
            self.player_score += 1
            esito = "Punto per Te!"
        elif ai_win and not p_win:
            self.ai_score += 1
            esito = "Punto per l'AI!"
        elif p_win and ai_win:
            esito = "Entrambi avete indovinato! Nessun punto."
        else:
            esito = "Nessuno ha indovinato."

        self.lbl_player.config(text=f"Tu: {self.player_score}")
        self.lbl_ai.config(text=f"AI: {self.ai_score}")

        dettagli = (
            f"--- Risultato Turno ---\n"
            f"Tu: {x_p} dita (Previsto: {y_p})\n"
            f"AI: {x_ai} dita (Previsto: {y_ai})\n"
            f"Somma Totale dita: {totale}\n\n"
            f"--> {esito}"
        )
        self.lbl_status.config(text=dettagli)

        if self.player_score >= self.punti_vittoria or self.ai_score >= self.punti_vittoria:
            vinto = self.player_score >= self.punti_vittoria
            registra_risultato(self.difficolta, self.player_score, self.ai_score, self.punti_vittoria, vinto)

            msg_vittoria = "Complimenti, hai vinto la partita!" if vinto else "L'AI ha vinto la partita!"
            messagebox.showinfo("Fine Partita", msg_vittoria)
            self._torna_menu()

    def _torna_menu(self):
        self.master.mostra_menu()

# =============================================================================
# AVVIO APPLICAZIONE
# =============================================================================
if __name__ == "__main__":
    app = App()
    app.mainloop()
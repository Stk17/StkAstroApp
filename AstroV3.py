#!/usr/bin/env python3
"""
STK's Astro — Professional Tamil Marriage Matchmaker (V3 / AstroV3)
Project Owner: Thirukumaran S (STK)
----------------------------------------------------------------------------------------
Features:
  - STRICT TOP-TO-BOTTOM ORDERING: Zero NameErrors. All tabs and engines declared first.
  - SKEUOMORPHIC & PURE TAMIL UI: Wood/Parchment theme, English text stripped.
  - GLOBAL ZOOM CONTROL: Top bar zoom controls all tabs, tables, and fonts simultaneously.
  - ELEMENT & ANIMAL LOGOS: Visual Emojis (🔥, 🐅, 🐘, 💧) flanking the Match Score Box.
  - STRICT NUMBER-ONLY SPIN-PICKERS: Up/Down arrow & mousewheel stepping clamped to valid bounds.
  - SUB-TAB 1.2 (KUDUMPA JOTHIDAM REFERENCE): Full classical rule tables from LIFCO book.
  - SUB-TAB 1.3 (BHAVA & MARRIAGE SYNERGY): Individual predictions for ALL PLANETS.
  - 0-DRIFT VIMSHOTTARI ENGINE & KUDUMPA JOTHIDAM CANON.
"""

import os
import sys
import json
import math
import re
import calendar
import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Dict, List, Tuple, Any, Optional

try:
    import swisseph as swe
    HAS_SWISSEPH = True
except ImportError:
    swe = None
    HAS_SWISSEPH = False


# =====================================================================
# 1. CONSTANTS, ICONS & COORDINATES
# =====================================================================
YONI_ICONS = {
    "குதிரை": "🐎", "யானை": "🐘", "ஆடு": "🐐", "பாம்பு": "🐍",
    "நாய்": "🐕", "பூனை": "🐈", "எலி": "🐀", "பசு": "🐄",
    "எருமை": "🐃", "புலி": "🐅", "மான்": "🦌", "குரங்கு": "🐒",
    "கீரி": "🦦", "சிங்கம்": "🦁"
}

ELEMENT_ICONS = {
    "அக்னி": "🔥", "நிலம்": "🌍", "காற்று": "💨", "நீர்": "💧"
}

CITY_COORDINATES = {
    "Coimbatore (கோயம்புத்தூர்)": (11.0168, 76.9558),
    "Coimbatore North (கோயம்புத்தூர் வடக்கு)": (11.0510, 76.9628),
    "Coimbatore South (கோயம்புத்தூர் தெற்கு)": (10.9830, 76.9600),
    "Tiruppur (திருப்பூர்)": (11.1085, 77.3411),
    "Pollachi (பொள்ளாச்சி)": (10.6580, 77.0088),
    "Mettupalayam (மேட்டுப்பாளையம்)": (11.3000, 76.9500),
    "Avinashi (அவிநாசி)": (11.1925, 77.2688),
    "Sulur (சூலூர்)": (11.0258, 77.1242),
    "Palladam (பல்லடம்)": (10.9989, 77.2905),
    "Udumalpet (உடுமலைப்பேட்டை)": (10.5828, 77.2505),
    "Dharapuram (தாராபுரம்)": (10.7328, 77.5255),
    "Kangeyam (காங்கேயம்)": (11.0040, 77.5613),
    "Vellakoil (வெள்ளக்கோவில்)": (10.9388, 77.7125),
    "Erode (ஈரோடு)": (11.3410, 77.7172),
    "Gobichettipalayam (கோபிசெட்டிபாளையம்)": (11.4550, 77.4380),
    "Bhavani (பவானி)": (11.4511, 77.6811),
    "Perundurai (பெருந்துறை)": (11.2750, 77.5850),
    "Sathyamangalam (சத்தியமங்கலம்)": (11.5039, 77.2436),
    "Anthiyur (அந்தியூர்)": (11.5794, 77.5925),
    "Modakurichi (மொடக்குறிச்சி)": (11.2333, 77.7833),
    "Salem (சேலம்)": (11.6643, 78.1460),
    "Attur (ஆத்தூர்)": (11.5950, 78.5950),
    "Omalur (ஓமலூர்)": (11.7420, 78.0460),
    "Mettur (மேட்டூர்)": (11.7950, 77.8050),
    "Edappadi (எடப்பாடி)": (11.5830, 77.8500),
    "Sankari (சங்ககிரி)": (11.4780, 77.8720),
    "Namakkal (நாமக்கல்)": (11.2189, 78.1674),
    "Tiruchengode (திருச்செங்கோடு)": (11.3780, 77.8960),
    "Rasipuram (ராசிபுரம்)": (11.4630, 78.1720),
    "Paramathi Velur (பரமத்தி வேலூர்)": (11.1120, 78.0050),
    "Karur (கரூர்)": (10.9601, 78.0766),
    "Kulithalai (குளித்தலை)": (10.9360, 78.4230),
    "Dharmapuri (தருமபுரி)": (12.1211, 78.1582),
    "Harur (ஹாரூர்)": (12.0620, 78.4900),
    "Palacode (பாலக்கோடு)": (12.3060, 78.0690),
    "Krishnagiri (கிருஷ்ணகிரி)": (12.5266, 78.2140),
    "Hosur (ஓசூர்)": (12.7409, 77.8253),
    "Nilgiris / Ooty (நீலகிரி)": (11.4102, 76.6950),
    "Coonoor (குன்னூர்)": (11.3530, 76.7959),
    "Gudalur (கூடலூர்)": (11.5060, 76.4910),
    "Dindigul (திண்டுக்கல்)": (10.3673, 77.9803),
    "Palani (பழனி)": (10.4500, 77.5167),
    "Oddanchatram (ஒட்டன்சத்திரம்)": (10.5050, 77.7460),
    "Kodaikanal (கொடைக்கானல்)": (10.2381, 77.4892),
    "Madurai (மதுரை)": (9.9252, 78.1198),
    "Melur (மேலூர்)": (10.0350, 78.3360),
    "Thirumangalam (திருமங்கலம்)": (9.9860, 77.9880),
    "Usilampatti (உசிலம்பட்டி)": (9.9670, 77.7980),
    "Tiruchirappalli / Trichy (திருச்சி)": (10.7905, 78.7047),
    "Srirangam (ஸ்ரீரங்கம்)": (10.8633, 78.6917),
    "Manapparai (மணப்பாறை)": (10.6080, 78.4160),
    "Thuraiyur (துறையூர்)": (11.1440, 78.5990),
    "Thanjavur (தஞ்சாவூர்)": (10.7870, 79.1378),
    "Kumbakonam (கும்பகோணம்)": (10.9602, 79.3788),
    "Pattukkottai (பட்டுக்கோட்டை)": (10.2600, 79.3170),
    "Mayiladuthurai (மயிலாடுதுறை)": (11.1018, 79.6524),
    "Sirkazhi (சீர்காழி)": (11.2360, 79.7340),
    "Nagapattinam (நாகப்பட்டினம்)": (10.7672, 79.8449),
    "Tiruvarur (திருவாரூர்)": (10.7714, 79.6368),
    "Mannargudi (மன்னார்குடி)": (10.6680, 79.4380),
    "Pudukkottai (புதுக்கோட்டை)": (10.3833, 78.8001),
    "Aranthangi (அறந்தாங்கி)": (10.1650, 78.9950),
    "Sivaganga / Sivakasi (சிவகங்கை)": (9.8433, 78.4809),
    "Karaikudi (காரைக்குடி)": (10.0688, 78.7842),
    "Virudhunagar (விருதுநகர்)": (9.5872, 77.9514),
    "Rajapalayam (ராஜபாளையம்)": (9.4533, 77.5533),
    "Aruppukottai (அருப்புக்கோட்டை)": (9.5130, 78.0980),
    "Theni (தேனி)": (10.0104, 77.4768),
    "Periyakulam (பெரியகுளம்)": (10.1230, 77.5450),
    "Cumbum (கம்பம்)": (9.7360, 77.2970),
    "Bodi (போடி)": (9.8330, 77.3480),
    "Ramanathapuram (ராமநாதபுரம்)": (9.3639, 78.8395),
    "Paramakudi (பரமக்குடி)": (9.5390, 78.5910),
    "Tirunelveli (திருநெல்வேலி)": (8.7139, 77.7567),
    "Tenkasi (தென்காசி)": (8.9594, 77.3152),
    "Sankarankovil (சங்கரன்கோவில்)": (9.1670, 77.5330),
    "Thoothukudi (தூத்துக்குடி)": (8.7642, 78.1348),
    "Kovilpatti (கோவில்பட்டி)": (9.1720, 77.8690),
    "Kanyakumari / Nagercoil (கன்னியாகுமரி)": (8.1833, 77.4119),
    "Marthandam (மார்த்தாண்டம்)": (8.3030, 77.2210),
    "Chennai (சென்னை)": (13.0827, 80.2707),
    "Tambaram (தாம்பரம்)": (12.9249, 80.1000),
    "Chengalpattu (செங்கல்பட்டு)": (12.6939, 79.9757),
    "Kanchipuram (காஞ்சிபுரம்)": (12.8342, 79.7036),
    "Tiruvallur (திருவள்ளூர்)": (13.1432, 79.9090),
    "Vellore (வேலூர்)": (12.9165, 79.1325),
    "Ranipet (ராணிப்பேட்டை)": (12.9272, 79.3331),
    "Tirupathur (திருப்பத்தூர்)": (12.4925, 78.5678),
    "Tiruvannamalai (திருவண்ணாமலை)": (12.2253, 79.0747),
    "Viluppuram (விழுப்புரம்)": (11.9401, 79.4861),
    "Tindivanam (திண்டிவனம்)": (12.2350, 79.6540),
    "Kallakurichi (கள்ளக்குறிச்சி)": (11.7384, 78.9639),
    "Cuddalore (கடலூர்)": (11.7480, 79.7714),
    "Chidambaram (சிதம்பரம்)": (11.3990, 79.6930),
    "Ariyalur (அரியலூர்)": (11.1401, 79.0786),
    "Perambalur (பெரம்பலூர்)": (11.2342, 78.8806)
}

# =====================================================================
# 2. UNIVERSAL SCROLL BINDER
# =====================================================================
def bind_universal_mousewheel(root):
    def _on_mousewheel(event):
        delta = 0
        if event.num == 4: delta = -1
        elif event.num == 5: delta = 1
        elif event.delta: delta = int(-1 * (event.delta / 120)) if os.name == "nt" else int(-1 * event.delta)
        
        widget_under = root.winfo_containing(event.x_root, event.y_root)
        if widget_under:
            curr = widget_under
            while curr:
                if isinstance(curr, ttk.Treeview):
                    curr.yview_scroll(delta, "units")
                    return
                if type(curr) is tk.Canvas and curr.__class__.__name__ != "SouthIndianChartCanvas":
                    curr.yview_scroll(delta, "units")
                    return
                curr = getattr(curr, "master", None)

    root.bind_all("<MouseWheel>", _on_mousewheel, add="+")
    root.bind_all("<Button-4>", _on_mousewheel, add="+")
    root.bind_all("<Button-5>", _on_mousewheel, add="+")

# =====================================================================
# 3. STRICT NUMBER-ONLY SPIN-PICKERS (HORIZONTAL AM/PM)
# =====================================================================
class StrictNumberEntry(tk.Entry):
    def __init__(self, parent, min_val: int, max_val: int, initial_val: Any, width: int = 3, **kwargs):
        defaults = {
            "font": ("Helvetica", 12, "bold"), "bg": "#FEFBEA", "fg": "#2C1A14",
            "insertbackground": "#2C1A14", "justify": "center", "relief": "sunken", "bd": 3
        }
        defaults.update(kwargs)
        super().__init__(parent, width=width, **defaults)
        self.min_val = min_val; self.max_val = max_val

        vcmd = (self.register(self._validate), '%P')
        self.config(validate="key", validatecommand=vcmd)
        
        if initial_val == "": self.insert(0, "")
        else: self.insert(0, f"{initial_val:02d}" if max_val < 100 else str(initial_val))

        self.bind("<Up>", lambda e: self._step(1)); self.bind("<Down>", lambda e: self._step(-1))
        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<FocusOut>", self._clamp_on_blur)

    def _validate(self, proposed: str) -> bool:
        if proposed == "": return True
        if proposed.isdigit() and len(proposed) <= 4: return True
        return False

    def _clamp_on_blur(self, event=None):
        txt = self.get().strip()
        if not txt: return
        try:
            val = max(self.min_val, min(self.max_val, int(txt)))
            self.delete(0, tk.END); self.insert(0, f"{val:02d}" if self.max_val < 100 else str(val))
        except ValueError:
            self.delete(0, tk.END); self.insert(0, "")

    def _step(self, delta: int):
        txt = self.get().strip()
        val = int(txt) + delta if txt else self.min_val
        if val > self.max_val: val = self.min_val
        elif val < self.min_val: val = self.max_val
        self.delete(0, tk.END); self.insert(0, f"{val:02d}" if self.max_val < 100 else str(val))
        return "break"

    def _on_mousewheel(self, event):
        self._step(1 if event.delta > 0 else -1)
        return "break"

    def get_int(self) -> int:
        txt = self.get().strip()
        return int(txt) if txt else -1

    def set_int(self, val: Any):
        self.delete(0, tk.END)
        if val == "": self.insert(0, "")
        else:
            val = max(self.min_val, min(self.max_val, int(val)))
            self.insert(0, f"{val:02d}" if self.max_val < 100 else str(val))

class ExecutiveFastDateTimePicker(tk.Frame):
    def __init__(self, parent, default_date: str = "", default_time: str = "", default_ampm: str = "AM", default_dt: Optional[datetime.datetime] = None, **kwargs):
        super().__init__(parent, bg="#EAE0C8", **kwargs)
        day_val = month_val = year_val = hr_val = min_val = ""
        
        if default_dt:
            day_val = default_dt.day; month_val = default_dt.month; year_val = default_dt.year
            hr_val = default_dt.hour % 12 or 12; min_val = default_dt.minute
            default_ampm = "PM" if default_dt.hour >= 12 else "AM"
        elif default_date and default_time:
            try:
                parts_d = re.split(r"[-/.]", default_date.strip())
                day_val, month_val, year_val = int(parts_d[0]), int(parts_d[1]), int(parts_d[2])
                parts_t = default_time.strip().split(":")
                hr_val, min_val = int(parts_t[0]), int(parts_t[1])
            except Exception: pass

        self.ent_day = StrictNumberEntry(self, min_val=1, max_val=31, initial_val=day_val, width=3)
        self.ent_day.pack(side="left", padx=1)
        tk.Label(self, text="/", font=("Helvetica", 11, "bold"), bg="#EAE0C8", fg="#2C1A14").pack(side="left")

        self.ent_month = StrictNumberEntry(self, min_val=1, max_val=12, initial_val=month_val, width=3)
        self.ent_month.pack(side="left", padx=1)
        tk.Label(self, text="/", font=("Helvetica", 11, "bold"), bg="#EAE0C8", fg="#2C1A14").pack(side="left")

        self.ent_year = StrictNumberEntry(self, min_val=1950, max_val=2050, initial_val=year_val, width=5)
        self.ent_year.pack(side="left", padx=1)
        tk.Label(self, text="  ", font=("Helvetica", 10), bg="#EAE0C8").pack(side="left")

        self.ent_hour = StrictNumberEntry(self, min_val=1, max_val=12, initial_val=hr_val, width=3)
        self.ent_hour.pack(side="left", padx=1)
        tk.Label(self, text=":", font=("Helvetica", 11, "bold"), bg="#EAE0C8", fg="#2C1A14").pack(side="left")

        self.ent_min = StrictNumberEntry(self, min_val=0, max_val=59, initial_val=min_val, width=3)
        self.ent_min.pack(side="left", padx=1)

        self.ampm_var = tk.StringVar(value=default_ampm)
        radio_box = tk.Frame(self, bg="#EAE0C8")
        radio_box.pack(side="left", padx=4)
        tk.Radiobutton(radio_box, text="AM", variable=self.ampm_var, value="AM", font=("Helvetica", 10, "bold"), bg="#EAE0C8", fg="#2C1A14", activebackground="#EAE0C8").pack(side="left", padx=1)
        tk.Radiobutton(radio_box, text="PM", variable=self.ampm_var, value="PM", font=("Helvetica", 10, "bold"), bg="#EAE0C8", fg="#4A0E0E", activebackground="#EAE0C8").pack(side="left", padx=1)

    def get_datetime_values(self) -> Tuple[str, str, str]:
        d = self.ent_day.get_int(); m = self.ent_month.get_int(); y = self.ent_year.get_int()
        hr = self.ent_hour.get_int(); mn = self.ent_min.get_int(); ampm = self.ampm_var.get()

        if -1 in [d, m, y, hr, mn]: return "", "", ""
        d = min(d, calendar.monthrange(y, m)[1])
        if ampm == "PM" and hr < 12: hr += 12
        elif ampm == "AM" and hr == 12: hr = 0

        dt = datetime.datetime(y, m, d, hr, mn)
        return dt.strftime("%Y-%m-%d"), dt.strftime("%H:%M"), dt.strftime("%d-%m-%Y %I:%M %p")

    def set_datetime(self, dt: datetime.datetime):
        self.ent_day.set_int(dt.day); self.ent_month.set_int(dt.month); self.ent_year.set_int(dt.year)
        self.ent_hour.set_int(dt.hour % 12 or 12); self.ent_min.set_int(dt.minute)
        self.ampm_var.set("PM" if dt.hour >= 12 else "AM")

class ExecutiveEntry(tk.Entry):
    def __init__(self, parent, **kwargs):
        defaults = {
            "font": ("Helvetica", 13, "bold"), "bg": "#FEFBEA", "fg": "#2C1A14",
            "insertbackground": "#2C1A14", "insertwidth": 2, "relief": "sunken", "bd": 3
        }
        defaults.update(kwargs)
        super().__init__(parent, **defaults)

class SmoothFilterCombobox(ttk.Combobox):
    def __init__(self, parent, completevalues, on_select_callback=None, **kwargs):
        super().__init__(parent, values=sorted(completevalues), **kwargs)
        self.completevalues = sorted(completevalues)
        self.on_select_callback = on_select_callback
        self.bind("<KeyRelease>", self._on_keyrelease)
        self.bind("<<ComboboxSelected>>", self._on_selected)

    def _on_keyrelease(self, event):
        if event.keysym in ("Down", "Up", "Return", "Escape", "Left", "Right", "Tab", "Shift_L", "Shift_R", "Control_L", "Meta_L", "Meta_R"): return
        typed = self.get()
        if not typed: self["values"] = self.completevalues
        else:
            filtered = [val for val in self.completevalues if typed.lower() in val.lower()]
            self["values"] = filtered if filtered else self.completevalues

    def _on_selected(self, event=None):
        if self.on_select_callback: self.on_select_callback(self.get())

# =====================================================================
# 4. CANONICAL TAMIL ASTROLOGICAL CONSTANTS
# =====================================================================
class TamilAstroConstants:
    RASIS = ["மேஷம்", "ரிஷபம்", "மிதுனம்", "கடகம்", "சிம்மம்", "கன்னி", "துலாம்", "விருச்சிகம்", "தனுசு", "மகரம்", "கும்பம்", "மீனம்"]
    RASI_LORDS = ["செ", "சுக்", "புத", "சந்", "சூரி", "புத", "சுக்", "செ", "குரு", "சனி", "சனி", "குரு"]
    NAKSHATRAS = ["அஸ்வினி", "பரணி", "கார்த்திகை", "ரோஹிணி", "மிருகசீரிடம்", "திருவாதிரை", "புனர்பூசம்", "பூசம்", "ஆயில்யம்", "மகம்", "பூரம்", "உத்திரம்", "ஹஸ்தம்", "சித்திரை", "சுவாதி", "விசாகம்", "அனுஷம்", "கேட்டை", "மூலம்", "பூராடம்", "உத்திராடம்", "திருவோணம்", "அவிட்டம்", "சதயம்", "பூரட்டாதி", "உத்திரட்டாதி", "ரேவதி"]
    ALL_STAR_RASI_VARIANTS = [
        ("அஸ்வினி", 0, 0), ("பரணி", 1, 0), ("கார்த்திகை 1", 2, 0), ("கார்த்திகை 2,3,4", 2, 1), ("ரோஹிணி", 3, 1),
        ("மிருகசீரிடம் 1,2", 4, 1), ("மிருகசீரிடம் 3,4", 4, 2), ("திருவாதிரை", 5, 2), ("புனர்பூசம் 1,2,3", 6, 2),
        ("புனர்பூசம் 4", 6, 3), ("பூசம்", 7, 3), ("ஆயில்யம்", 8, 3), ("மகம்", 9, 4), ("பூரம்", 10, 4),
        ("உத்திரம் 1", 11, 4), ("உத்திரம் 2,3,4", 11, 5), ("ஹஸ்தம்", 12, 5), ("சித்திரை 1,2", 13, 5),
        ("சித்திரை 3,4", 13, 6), ("சுவாதி", 14, 6), ("விசாகம் 1,2,3", 15, 6), ("விசாகம் 4", 15, 7),
        ("அனுஷம்", 16, 7), ("கேட்டை", 17, 7), ("மூலம்", 18, 8), ("பூராடம்", 19, 8), ("உத்திராடம் 1", 20, 8),
        ("உத்திராடம் 2,3,4", 20, 9), ("திருவோணம்", 21, 9), ("அவிட்டம் 1,2", 22, 9), ("அவிட்டம் 3,4", 22, 10),
        ("சதயம்", 23, 10), ("பூரட்டாதி 1,2,3", 24, 10), ("பூரட்டாதி 4", 24, 11), ("உத்திரட்டாதி", 25, 11), ("ரேவதி", 26, 11)
    ]
    DASA_CYCLE = [("கேது", 7), ("சுக்கிரன்", 20), ("சூரியன்", 6), ("சந்திரன்", 10), ("செவ்வாய்", 7), ("ராகு", 18), ("குரு", 16), ("சனி", 19), ("புதன்", 17)]
    LAGNA_DARK_HOUSES_MAP = {0: "2-8", 1: "6-8", 2: "7-10", 3: "8", 4: "1-7", 5: "4-10", 6: "6-8", 7: "2-7", 8: "3-8", 9: "3-9", 10: "4-10", 11: "5-11"}
    RAJJU_MAP = {
        0: "பாதம்", 8: "பாதம்", 9: "பாதம்", 17: "பாதம்", 18: "பாதம்", 26: "பாதம்",
        1: "தொடை", 7: "தொடை", 10: "தொடை", 16: "தொடை", 19: "தொடை", 25: "தொடை",
        2: "வயிறு", 6: "வயிறு", 11: "வயிறு", 15: "வயிறு", 20: "வயிறு", 24: "வயிறு",
        3: "கழுத்து", 5: "கழுத்து", 12: "கழுத்து", 14: "கழுத்து", 21: "கழுத்து", 23: "கழுத்து",
        4: "சிரசு", 13: "சிரசு", 22: "சிரசு"
    }
    GANA_MAP = {
        0: "தேவ", 4: "தேவ", 6: "தேவ", 7: "தேவ", 12: "தேவ", 14: "தேவ", 16: "தேவ", 21: "தேவ", 26: "தேவ",
        1: "மனுஷ", 3: "மனுஷ", 5: "மனுஷ", 10: "மனுஷ", 11: "மனுஷ", 19: "மனுஷ", 20: "மனுஷ", 24: "மனுஷ", 25: "மனுஷ",
        2: "ராட்சச", 8: "ராட்சச", 9: "ராட்சச", 13: "ராட்சச", 15: "ராட்சச", 17: "ராட்சச", 18: "ராட்சச", 22: "ராட்சச", 23: "ராட்சச"
    }
    VASYA_MAP = {0: [4, 7], 1: [3], 2: [5], 3: [7, 8], 4: [9], 5: [1, 11], 6: [9], 7: [3, 5], 8: [11], 9: [0, 10], 10: [0], 11: [9]}
    PLANETARY_ENEMIES_MAP = {"சூரி": ["சுக்", "சனி"], "சந்": [], "செ": ["புத", "சுக்"], "புத": ["சந்"], "குரு": ["புத", "சுக்"], "சுக்": ["சூரி", "செ"], "சனி": ["சூரி", "சந்", "செ"]}
    YONI_ANIMALS = {
        0: "குதிரை", 1: "யானை", 2: "ஆடு", 3: "பாம்பு", 4: "பாம்பு", 5: "நாய்", 6: "பூனை", 7: "ஆடு",
        8: "பூனை", 9: "எலி", 10: "எலி", 11: "பசு", 12: "எருமை", 13: "புலி", 14: "புலி", 15: "புலி",
        16: "மான்", 17: "மான்", 18: "நாய்", 19: "குரங்கு", 20: "கீரி", 21: "குரங்கு", 22: "சிங்கம்", 23: "குதிரை",
        24: "சிங்கம்", 25: "பசு", 26: "யானை"
    }
    YONI_ENEMIES = [
        ("பசு", "புலி"), ("யானை", "சிங்கம்"), ("குதிரை", "எருமை"),
        ("நாய்", "மான்"), ("எலி", "பூனை"), ("பாம்பு", "கீரி"), ("குரங்கு", "ஆடு")
    ]
    YONI_FRIENDLY_MAP = {
        "குதிரை": "மான், நாய், சிங்கம், குரங்கு", "யானை": "குதிரை, பசு, ஆடு, மான்",
        "ஆடு": "பசு, மான், யானை, குதிரை", "பாம்பு": "எலி, பசு, ஆடு",
        "நாய்": "குதிரை, குரங்கு, பூனை", "பூனை": "மான், நாய், பசு",
        "எலி": "பாம்பு, குரங்கு, பசு", "பசு": "யானை, ஆடு, மான், குதிரை",
        "எருமை": "யானை, பசு, ஆடு", "புலி": "குதிரை, நாய், சிங்கம்",
        "மான்": "பசு, ஆடு, குதிரை", "குரங்கு": "குதிரை, நாய், சிங்கம்",
        "கீரி": "பூனை, நாய், மான்", "சிங்கம்": "குதிரை, புலி, குரங்கு"
    }
    NADI_MAP = {
        0: "பார்சுவ", 1: "மத்திய", 2: "சமான", 3: "சமான", 4: "மத்திய", 5: "பார்சுவ",
        6: "பார்சுவ", 7: "மத்திய", 8: "சமான", 9: "சமான", 10: "மத்திய", 11: "பார்சுவ",
        12: "பார்சுவ", 13: "மத்திய", 14: "சமான", 15: "சமான", 16: "மத்திய", 17: "பார்சுவ",
        18: "பார்சுவ", 19: "மத்திய", 20: "சமான", 21: "சமான", 22: "மத்திய", 23: "பார்சுவ",
        24: "பார்சுவ", 25: "மத்திய", 26: "சமான"
    }
    VEDHAI_PAIRS = [
        (0, 17), (1, 16), (2, 15), (3, 14), (5, 21), (6, 20),
        (7, 19), (8, 18), (9, 26), (10, 25), (11, 24), (12, 23), (13, 22)
    ]
    RASI_ELEMENTS = {
        0: ("அக்னி", "காற்று", "நீர்", "நிலம், அக்னி"), 1: ("நிலம்", "நீர்", "அக்னி", "காற்று, நிலம்"),
        2: ("காற்று", "அக்னி", "நிலம்", "நீர், காற்று"), 3: ("நீர்", "நிலம்", "காற்று", "அக்னி, நீர்"),
        4: ("அக்னி", "காற்று", "நீர்", "நிலம், அக்னி"), 5: ("நிலம்", "நீர்", "அக்னி", "காற்று, நிலம்"),
        6: ("காற்று", "அக்னி", "நிலம்", "நீர், காற்று"), 7: ("நீர்", "நிலம்", "காற்று", "அக்னி, நீர்"),
        8: ("அக்னி", "காற்று", "நீர்", "நிலம், அக்னி"), 9: ("நிலம்", "நீர்", "அக்னி", "காற்று, நிலம்"),
        10: ("காற்று", "அக்னி", "நிலம்", "நீர், காற்று"), 11: ("நீர்", "நிலம்", "காற்று", "அக்னி, நீர்")
    }


# =====================================================================
# 5. ASTRO ENGINE (VIMSHOTTARI, PANCHANGAM, SAMUTRIKA & VEDIC)
# =====================================================================
class VimshottariCalendarEngine:
    @classmethod
    def compute_timeline(cls, dob_dt: datetime.datetime, moon_lon: float) -> Tuple[str, str, str, List[Dict[str, Any]]]:
        dob_date = dob_dt.date()
        nak_arc = 360.0 / 27.0
        nak_idx = int(moon_lon / nak_arc)
        elapsed_in_nak = moon_lon % nak_arc
        frac_rem = 1.0 - (elapsed_in_nak / nak_arc)

        dasa_start_idx = nak_idx % 9
        birth_dasa_name, birth_dasa_yrs = TamilAstroConstants.DASA_CYCLE[dasa_start_idx]
        rem_years_float = birth_dasa_yrs * frac_rem
        r_y = int(rem_years_float); rem_m_float = (rem_years_float - r_y) * 12.0
        r_m = int(rem_m_float); r_d = int(round((rem_m_float - r_m) * 30.0))
        if r_d >= 30: r_d = 0; r_m += 1
        if r_m >= 12: r_m = 0; r_y += 1

        birth_dasa_bal_str = f"{birth_dasa_name} தசை {r_y} வருடம் {r_m} மாதம் {r_d} நாள்"
        balance_days = int(round(rem_years_float * 365.25))
        first_dasa_end_date = dob_date + datetime.timedelta(days=balance_days)

        full_bhukti_list = []
        birth_bhuktis = []
        cum_back_years = 0.0
        curr_end_back = first_dasa_end_date
        for b_step in range(8, -1, -1):
            b_idx = (dasa_start_idx + b_step) % 9
            b_name, b_yrs = TamilAstroConstants.DASA_CYCLE[b_idx]
            cum_back_years += b_yrs
            days_back = int(round(((birth_dasa_yrs * cum_back_years) / 120.0) * 365.25))
            b_start_back = first_dasa_end_date - datetime.timedelta(days=days_back)
            if curr_end_back > dob_date:
                birth_bhuktis.append({"dasa": birth_dasa_name, "bhukti": b_name, "start": max(dob_date, b_start_back), "end": curr_end_back})
            curr_end_back = b_start_back

        birth_bhuktis.reverse()
        full_bhukti_list.extend(birth_bhuktis)

        cum_dasa_years = 0
        curr_dasa_start = first_dasa_end_date
        for d_step in range(1, 9):
            d_idx = (dasa_start_idx + d_step) % 9
            d_name, d_yrs = TamilAstroConstants.DASA_CYCLE[d_idx]
            cum_dasa_years += d_yrs
            next_dasa_start = first_dasa_end_date + datetime.timedelta(days=int(round(cum_dasa_years * 365.25)))

            cum_bhukti_years = 0
            curr_bhukti_start = curr_dasa_start
            for b_step in range(9):
                b_idx = (d_idx + b_step) % 9
                b_name, b_yrs = TamilAstroConstants.DASA_CYCLE[b_idx]
                cum_bhukti_years += b_yrs
                if b_step == 8: bhukti_end = next_dasa_start
                else:
                    days_elapsed = int(round(((d_yrs * cum_bhukti_years) / 120.0) * 365.25))
                    bhukti_end = curr_dasa_start + datetime.timedelta(days=days_elapsed)
                full_bhukti_list.append({"dasa": d_name, "bhukti": b_name, "start": curr_bhukti_start, "end": bhukti_end})
                curr_bhukti_start = bhukti_end
            curr_dasa_start = next_dasa_start

        today = datetime.date.today()
        active_dasa = birth_dasa_name
        active_formatted = f"{birth_dasa_name} -> சந்"
        for b in full_bhukti_list:
            if b["start"] <= today <= b["end"]:
                active_dasa = b["dasa"]
                d_str = f"{b['start'].strftime('%d-%m-%Y')} முதல் {b['end'].strftime('%d-%m-%Y')}"
                active_formatted = f"{b['dasa']} -> {b['bhukti'][:3]} \n({d_str})"
                break

        return birth_dasa_bal_str, active_dasa, active_formatted, full_bhukti_list

class DynamicPanchangamEngine:
    TITHI_NAMES = ["பிரதமை", "துவிதியை", "திருதியை", "சதுர்த்தி", "பஞ்சமி", "சஷ்டி", "சப்தமி", "அஷ்டமி", "நவமி", "தசமி", "ஏகாதசி", "துவாதசி", "திரியோதசி", "சதுர்த்தசி", "பௌர்ணமி", "பிரதமை", "துவிதியை", "திருதியை", "சதுர்த்தி", "பஞ்சமி", "சஷ்டி", "சப்தமி", "அஷ்டமி", "நவமி", "தசமி", "ஏகாதசி", "துவாதசி", "திரியோதசி", "சதுர்த்தசி", "அமாவாசை"]
    YOGA_NAMES = ["விஷ்கம்பம்", "பிரீதி", "ஆயுஷ்மான்", "சௌபாக்கியம்", "சோபனம்", "அதிகண்டம்", "சுகர்மம்", "திருதி", "சூலம்", "கண்டம்", "விருத்தி", "துருவம்", "வியாகாதம்", "ஹர்ஷணம்", "வச்சிரம்", "சித்தி", "வியதிபாதம்", "வரியான்", "பரிதி", "சிவம்", "சித்தம்", "சாத்தியம்", "சுபம்", "சுப்பிரம்", "பிராமியம்", "மகேந்திரம்", "வைதிருதி"]
    TITHI_SHOONYAM_MAP = {1: "துலாம், மகரம்", 2: "தனுசு, மீனம்", 3: "சிம்மம், மகரம்", 4: "ரிஷபம், கும்பம்", 5: "மிதுனம், கன்னி", 6: "மேஷம், சிம்மம்", 7: "கடகம், தனுசு", 8: "மிதுனம், கன்னி", 9: "சிம்மம், விருச்சிகம்", 10: "சிம்மம், விருச்சிகம்", 11: "தனுசு, மீனம்", 12: "துலாம், மகரம்", 13: "ரிஷபம், சிம்மம்", 14: "மிதுனம், கன்னி, தனுசு, மீனம்", 15: "ஏதுமில்லை", 0: "ஏதுமில்லை"}

    @classmethod
    def compute_panchangam(cls, sun_lon: float, moon_lon: float) -> Tuple[str, str, str]:
        elongation = (moon_lon - sun_lon) % 360.0
        tithi_index = int(elongation / 12.0)
        tithi_name = cls.TITHI_NAMES[tithi_index]
        paksha = "வளர்பிறை" if tithi_index < 15 else "தேய்பிறை"
        full_tithi_label = f"{tithi_name} ({paksha})"
        shoonyam_key = 0 if tithi_index == 29 else (tithi_index + 1 if tithi_index < 15 else tithi_index - 14)
        shoonyam_rasis = cls.TITHI_SHOONYAM_MAP.get(shoonyam_key, "ஏதுமில்லை")
        yoga_index = int(((sun_lon + moon_lon) % 360.0) / 13.3333333333) % 27
        return full_tithi_label, cls.YOGA_NAMES[yoga_index], shoonyam_rasis

class SamutrikaLakshanamEngine:
    HARMONIC_KAMA_SHASTRA_MASK = sum(val << (2 * idx) for idx, val in enumerate([
        2, 2, 0, 1, 1, 0, 1, 0, 1, 0, 0, 2, 2, 2, 2, 2, 3, 3, 0, 2, 3, 2, 2, 2, 1, 1, 1
    ]))

    @classmethod
    def compute_female_kuri(cls, nak_idx: int) -> str:
        code = (cls.HARMONIC_KAMA_SHASTRA_MASK >> (nak_idx * 2)) & 0b11
        labels = ["கற்ப வாய் இறுக்கமானது", "கற்ப வாய் தளர்வானது", "கற்ப வாய் அகன்றது", "கற்ப வாய் உன்னதமானது"]
        return labels[code]

    @classmethod
    def compute_male_size(cls, nak_idx: int, pada: int, moon_deg_in_star: float) -> str:
        base_angula = 8.85 + ((nak_idx * 0.17 + pada * 0.43) % 2.65)
        fine_ratio = (moon_deg_in_star / 13.333333) * 0.35
        cm_val = (base_angula + fine_ratio) * 1.6254
        return f"{cm_val:.12f} Cm"

    @classmethod
    def compute_complexion_and_swatch(cls, rasi_idx: int) -> Tuple[str, str]:
        COMPLEXION_CODES = [3, 1, 2, 1, 0, 2, 1, 3, 0, 0, 0, 0]
        SWATCH_HEXES = ["#e6c2b8", "#eaf2f8", "#d19e8e", "#c28b7b"]
        LABELS = ["வெள்ளை", "மிக வெள்ளை", "மாநிறம்", "சிகப்பு கலந்த மாநிறம்"]
        code = COMPLEXION_CODES[rasi_idx % 12]
        return LABELS[code], SWATCH_HEXES[code]

    @classmethod
    def check_doshams(cls, p_data: Dict[str, Any]) -> Dict[str, str]:
        lag = p_data["lagna_idx"]
        mars_idx = p_data["positions"]["செ"]["rasi_idx"]
        ra_idx = p_data["positions"]["ராகு"]["rasi_idx"]
        ke_idx = p_data["positions"]["கேது"]["rasi_idx"]

        sevvai = "உண்டு" if ((mars_idx - lag) % 12 + 1) in [2, 4, 7, 8, 12] else "இல்லை"
        rahu_dosh = "உண்டு" if ((ra_idx - lag) % 12 + 1) in [2, 5, 7, 8] else "இல்லை"
        ketu_dosh = "உண்டு" if ((ke_idx - lag) % 12 + 1) in [2, 5, 7, 8] else "இல்லை"
        naga = "உண்டு" if (rahu_dosh == "உண்டு" or ketu_dosh == "உண்டு") else "இல்லை"
        kalasarpa = "உண்டு" if (ra_idx == 0 and ke_idx == 6) else "இல்லை"
        kalathra = "உண்டு" if ((ra_idx - lag) % 12 + 1) in [1, 7] and ((ke_idx - lag) % 12 + 1) in [1, 7] else "இல்லை"

        return {"sevvai": sevvai, "rahu": rahu_dosh, "ketu": ketu_dosh, "naga": naga, "kalasarpa": kalasarpa, "kalathra": kalathra}

class AdvancedVedicEngine:
    @classmethod
    def calculate_mandhi(cls, dt: datetime.datetime, lat: float, lon: float, tz: float) -> Tuple[int, float, str]:
        weekday = dt.weekday()
        day_ghatis = {6: 26, 0: 22, 1: 18, 2: 14, 3: 10, 4: 6, 5: 2}
        night_ghatis = {6: 10, 0: 6, 1: 2, 2: 26, 3: 22, 4: 18, 5: 14}
        ut_birth = (dt.hour + dt.minute / 60.0) - tz
        mandhi_lon = 0.0

        if HAS_SWISSEPH:
            try:
                jd_birth = swe.julday(dt.year, dt.month, dt.day, ut_birth)
                jd_noon = swe.julday(dt.year, dt.month, dt.day, 12.0 - tz - (lon - 82.5) / 15.0)
                sun_pos, _ = swe.calc_ut(jd_noon, swe.SUN, swe.FLG_EQUATORIAL)
                decl_deg = sun_pos[1]
                lat_rad = math.radians(lat); decl_rad = math.radians(decl_deg)
                cos_h = max(-1.0, min(1.0, -math.tan(lat_rad) * math.tan(decl_rad)))
                half_day_hrs = math.degrees(math.acos(cos_h)) / 15.0
                sunrise_jd = jd_noon - (half_day_hrs / 24.0)
                sunset_jd = jd_noon + (half_day_hrs / 24.0)

                if sunrise_jd <= jd_birth < sunset_jd:
                    elapsed_hrs = (day_ghatis[weekday] / 30.0) * ((sunset_jd - sunrise_jd) * 24.0)
                    mandhi_jd = sunrise_jd + (elapsed_hrs / 24.0)
                else:
                    elapsed_hrs = (night_ghatis[weekday] / 30.0) * (24.0 - ((sunset_jd - sunrise_jd) * 24.0))
                    mandhi_jd = sunset_jd + (elapsed_hrs / 24.0)
                    
                _, ascmc = swe.houses_ex(mandhi_jd, lat, lon, b'P', flags=swe.FLG_SIDEREAL)
                mandhi_lon = ascmc[0] % 360.0
            except Exception:
                mandhi_hour_24 = 6.0 + (day_ghatis[weekday] / 30.0) * 12.0
                mandhi_lon = ((dt.timetuple().tm_yday * 1.0) + (mandhi_hour_24 * 15.0)) % 360.0
        else:
            mandhi_hour_24 = 6.0 + (day_ghatis[weekday] / 30.0) * 12.0
            mandhi_lon = ((dt.timetuple().tm_yday * 1.0) + (mandhi_hour_24 * 15.0)) % 360.0
            
        r_idx = int(mandhi_lon / 30.0)
        deg = mandhi_lon % 30.0
        return r_idx, deg, f"மா-{int(deg)}°"

    @classmethod
    def calculate_exact_karanam(cls, moon_lon: float, sun_lon: float) -> Tuple[str, str]:
        diff = (moon_lon - sun_lon) % 360.0
        k_num = int(diff / 6.0) + 1
        if k_num == 1: return "கிஸ்துக்கினம்", "புதன்"
        elif k_num == 58: return "சகுனி", "ராகு"
        elif k_num == 59: return "சதுஷ்பாதம்", "கேது"
        elif k_num == 60: return "நாகவம்", "சூரியன்"
        else:
            movable = [("பவம்", "சூரியன்"), ("பாலவம்", "சந்திரன்"), ("கௌலவம்", "சனி"), ("தைதுலம்", "புதன்"), ("கரிசை", "குரு"), ("வணிசை", "சூரியன்"), ("பத்திரை", "சனி")]
            return movable[(k_num - 2) % 7]

    @classmethod
    def compute_horoscope(cls, name: str, gender: str, dob: str, tob_24h: str, place: str, lat: float, lon: float, tz: float, ayanamsa_mode: str) -> Dict[str, Any]:
        dt = datetime.datetime.strptime(f"{dob} {tob_24h}", "%Y-%m-%d %H:%M")
        ut_hour = (dt.hour + dt.minute / 60.0) - tz

        planets_map = {"சூரி": 0, "சந்": 1, "செ": 4, "புத": 2, "குரு": 5, "சுக்": 3, "சனி": 6, "ராகு": 10}
        positions = {}
        rasi_grid = {i: [] for i in range(12)}

        if HAS_SWISSEPH:
            if ayanamsa_mode == "thirukanitham": swe.set_sid_mode(getattr(swe, "SIDM_SURYASIDDHANTA", getattr(swe, "SIDM_SS_CITRA", swe.SIDM_LAHIRI)))
            elif ayanamsa_mode == "vedic_true": swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
            else: swe.set_sid_mode(swe.SIDM_LAHIRI)

            jd_ut = swe.julday(dt.year, dt.month, dt.day, ut_hour)
            for pname, pid in planets_map.items():
                res, _ = swe.calc_ut(jd_ut, pid, swe.FLG_SIDEREAL | swe.FLG_SPEED)
                lon_deg = res[0] % 360.0
                r_idx = int(lon_deg / 30.0); in_deg = lon_deg % 30.0
                is_retro = (res[3] < 0) and (pid not in [0, 1, 10])
                positions[pname] = {"lon": lon_deg, "rasi_idx": r_idx, "deg": in_deg}
                tag = f"{pname}-{int(in_deg)}°" + ("(வ)" if is_retro else "")
                rasi_grid[r_idx].append(tag)

            _, ascmc = swe.houses_ex(jd_ut, lat, lon, b'P', flags=swe.FLG_SIDEREAL)
            lag_lon = ascmc[0] % 360.0
        else:
            day_of_year = dt.timetuple().tm_yday
            sun_lon_approx = ((day_of_year - 80) * 0.9856) % 360.0
            moon_lon_approx = (sun_lon_approx + (day_of_year * 13.1763) + (ut_hour * 0.55)) % 360.0
            approx_lons = {
                "சூரி": sun_lon_approx, "சந்": moon_lon_approx, "செ": (sun_lon_approx + 45.0) % 360.0,
                "புத": (sun_lon_approx + 15.0) % 360.0, "குரு": (sun_lon_approx + 120.0) % 360.0,
                "சுக்": (sun_lon_approx + 30.0) % 360.0, "சனி": (sun_lon_approx + 210.0) % 360.0,
                "ராகு": (sun_lon_approx + 280.0) % 360.0
            }
            for pname, lon_deg in approx_lons.items():
                r_idx = int(lon_deg / 30.0); in_deg = lon_deg % 30.0
                positions[pname] = {"lon": lon_deg, "rasi_idx": r_idx, "deg": in_deg}
                rasi_grid[r_idx].append(f"{pname}-{int(in_deg)}°")
            lag_lon = (sun_lon_approx + (dt.hour * 15.0)) % 360.0

        ketu_lon = (positions["ராகு"]["lon"] + 180.0) % 360.0
        k_idx = int(ketu_lon / 30.0)
        positions["கேது"] = {"lon": ketu_lon, "rasi_idx": k_idx, "deg": ketu_lon % 30.0}
        rasi_grid[k_idx].append(f"கே-{int(ketu_lon % 30.0)}°")

        lag_idx = int(lag_lon / 30.0)
        positions["லக்"] = {"lon": lag_lon, "rasi_idx": lag_idx, "deg": lag_lon % 30.0}
        rasi_grid[lag_idx].append(f"லக்-{int(lag_lon % 30.0)}°")

        m_idx, m_deg, m_tag = cls.calculate_mandhi(dt, lat, lon, tz)
        positions["மாந்தி"] = {"lon": (m_idx * 30.0) + m_deg, "rasi_idx": m_idx, "deg": m_deg}
        rasi_grid[m_idx].append(m_tag)

        moon_lon = positions["சந்"]["lon"]; sun_lon = positions["சூரி"]["lon"]
        nak_idx = int(moon_lon / (360.0 / 27.0))
        pada = int((moon_lon % (360.0 / 27.0)) / (360.0 / 108.0)) + 1
        moon_deg_in_star = moon_lon % (360.0 / 27.0)

        tithi_label, yoga_label, shoonyam_rasis = DynamicPanchangamEngine.compute_panchangam(sun_lon, moon_lon)
        karanam_name, karanam_lord = cls.calculate_exact_karanam(moon_lon, sun_lon)

        yogi_lon = (sun_lon + moon_lon + 93.3333333333) % 360.0
        yogi_idx = int(yogi_lon / (360.0 / 27.0)) % 27
        yogi_str = f"{TamilAstroConstants.NAKSHATRAS[yogi_idx]} ({TamilAstroConstants.DASA_CYCLE[yogi_idx % 9][0]})"

        avayogi_idx = (yogi_idx + 14) % 27
        avayogi_str = f"{TamilAstroConstants.NAKSHATRAS[avayogi_idx]} ({TamilAstroConstants.DASA_CYCLE[avayogi_idx % 9][0]})"

        janma_pada_abs = (nak_idx * 4) + (pada - 1)
        vainasigam_pada_abs = (janma_pada_abs - 21) % 108
        vainasigam_str = f"{TamilAstroConstants.NAKSHATRAS[vainasigam_pada_abs // 4]} {(vainasigam_pada_abs % 4) + 1}"

        birth_dasa_bal_str, active_dasa_name, active_formatted, full_timeline = VimshottariCalendarEngine.compute_timeline(dt, moon_lon)
        age_years = round((datetime.datetime.now() - dt).days / 365.25, 1)

        yoni_animal_str = TamilAstroConstants.YONI_ANIMALS.get(nak_idx, "யானை")
        complexion_lbl, swatch_hex = SamutrikaLakshanamEngine.compute_complexion_and_swatch(int(moon_lon / 30.0))
        samutrika_kuri = (SamutrikaLakshanamEngine.compute_female_kuri(nak_idx) if gender == "பெண்"
                          else SamutrikaLakshanamEngine.compute_male_size(nak_idx, pada, moon_deg_in_star))

        panchangam_rows = [
            ("பெயர்", name), ("பாலினம்", gender),
            ("பிறந்த தேதி", f"{dt.strftime('%d-%m-%Y')} ({age_years} வயது)"),
            ("பிறந்த நேரம்", dt.strftime("%I:%M %p")), ("பிறந்த இடம்", place.split(" ")[0]),
            ("வாரம்", dt.strftime("%A")), ("திதி", tithi_label),
            ("நட்சத்திரம்", f"{TamilAstroConstants.NAKSHATRAS[nak_idx]} {pada}"),
            ("யோனி மிருகம்", yoni_animal_str), ("யோகம்", yoga_label),
            ("கரணம்", f"{karanam_name}({karanam_lord})"), ("லக்னம்", TamilAstroConstants.RASIS[lag_idx]),
            ("ராசி", TamilAstroConstants.RASIS[int(moon_lon / 30.0)]),
            ("மாந்தி நிலை", f"{TamilAstroConstants.RASIS[m_idx]} ({int(m_deg)}°)"),
            ("திதி சூன்யம்", shoonyam_rasis), ("பிறப்பு தசா இருப்பு", birth_dasa_bal_str),
            ("நடப்பு தசா", active_formatted), ("யோகி", yogi_str),
            ("அவயோகி", avayogi_str), ("வைநாசிகம்", vainasigam_str)
        ]

        return {
            "name": name, "gender": gender, "dt": dt, "place": place.split(" ")[0],
            "rasi_idx": int(moon_lon / 30.0), "rasi_name": TamilAstroConstants.RASIS[int(moon_lon / 30.0)],
            "nak_idx": nak_idx, "nak_name": TamilAstroConstants.NAKSHATRAS[nak_idx], "pada": pada,
            "lagna_idx": lag_idx, "lagna_name": TamilAstroConstants.RASIS[lag_idx],
            "karanam": karanam_name, "karanam_lord": karanam_lord,
            "birth_dasa": TamilAstroConstants.DASA_CYCLE[nak_idx % 9][0], "active_dasa": active_dasa_name,
            "yoni_animal": yoni_animal_str, "samutrika_kuri": samutrika_kuri,
            "samutrika_color": complexion_lbl, "samutrika_swatch": swatch_hex,
            "positions": positions, "rasi_grid": rasi_grid, "table_rows": panchangam_rows, "full_timeline": full_timeline
        }


class DynamicTwelvePointEngine:
    @classmethod
    def evaluate_nakshatra_11_points(cls, g_nak_idx: int, g_rasi_idx: int, b_nak_idx: int, b_rasi_idx: int) -> Tuple[List[int], List[int], int, List[str]]:
        dist = (b_nak_idx - g_nak_idx) % 27 + 1
        r_diff = (b_rasi_idx - g_rasi_idx) % 12 + 1
        g_raj = TamilAstroConstants.RAJJU_MAP[g_nak_idx]; b_raj = TamilAstroConstants.RAJJU_MAP[b_nak_idx]
        g_lord = TamilAstroConstants.RASI_LORDS[g_rasi_idx]; b_lord = TamilAstroConstants.RASI_LORDS[b_rasi_idx]

        matched = []; unmatched = []; p_items = []; score = 0

        if dist % 9 in [2, 4, 6, 8, 0]: matched.append(1); score += 1; p_items.append("1. தினம் பொருத்தம் ✔")
        else: unmatched.append(1); p_items.append("1. தினம் பொருத்தம் ✖")

        g_gana = TamilAstroConstants.GANA_MAP[g_nak_idx]; b_gana = TamilAstroConstants.GANA_MAP[b_nak_idx]
        if g_gana == b_gana or (g_gana in ["தேவ", "மனுஷ"] and b_gana in ["தேவ", "மனுஷ"]): matched.append(2); score += 1; p_items.append("2. கண பொருத்தம் ✔")
        elif b_gana == "ராட்சச" and g_gana in ["தேவ", "மனுஷ"]: matched.append(2); score += 1; p_items.append("2. கண பொருத்தம் ✔ (மத்திமம்)")
        else: unmatched.append(2); p_items.append("2. கண பொருத்தம் ✖")

        if dist in [4, 7, 10, 13, 16, 19, 22, 25]: matched.append(3); score += 1; p_items.append("3. மகேந்திர பொருத்தம் ✔")
        else: unmatched.append(3); p_items.append("3. மகேந்திர பொருத்தம் ✖")

        if dist > 7: matched.append(4); score += 1; p_items.append("4. ஸ்திரீ தீர்க்கம் ✔")
        else: unmatched.append(4); p_items.append("4. ஸ்திரீ தீர்க்கம் ✖")

        g_animal = TamilAstroConstants.YONI_ANIMALS[g_nak_idx]; b_animal = TamilAstroConstants.YONI_ANIMALS[b_nak_idx]
        is_yoni_enemy = any((g_animal == p[0] and b_animal == p[1]) or (g_animal == p[1] and b_animal == p[0]) for p in TamilAstroConstants.YONI_ENEMIES)
        if not is_yoni_enemy: matched.append(5); score += 1; p_items.append("5. யோனி பொருத்தம் ✔")
        else: unmatched.append(5); p_items.append("5. யோனி பொருத்தம் ✖")

        if r_diff in [1, 7, 9, 10, 11, 12] or (r_diff in [6, 8] and g_lord == b_lord): matched.append(6); score += 1; p_items.append("6. ராசி பொருத்தம் ✔")
        else: unmatched.append(6); p_items.append("6. ராசி பொருத்தம் ✖")

        is_enemy = (b_lord in TamilAstroConstants.PLANETARY_ENEMIES_MAP.get(g_lord, [])) or (g_lord in TamilAstroConstants.PLANETARY_ENEMIES_MAP.get(b_lord, []))
        if not is_enemy: matched.append(7); score += 1; p_items.append("7. ராசி அதிபதி பொருத்தம் ✔")
        else: unmatched.append(7); p_items.append("7. ராசி அதிபதி பொருத்தம் ✖")

        if b_rasi_idx in TamilAstroConstants.VASYA_MAP.get(g_rasi_idx, []): matched.append(8); score += 1; p_items.append("8. வசிய பொருத்தம் ✔")
        else: unmatched.append(8); p_items.append("8. வசிய பொருத்தம் ✖")

        if g_raj != b_raj: matched.append(9); score += 1; p_items.append("9. ரஜ்ஜு பொருத்தம் ✔")
        else: unmatched.append(9); p_items.append("9. ரஜ்ஜு பொருத்தம் ✖")

        is_vedhai = any((g_nak_idx == p[0] and b_nak_idx == p[1]) or (g_nak_idx == p[1] and b_nak_idx == p[0]) for p in TamilAstroConstants.VEDHAI_PAIRS)
        if not is_vedhai and g_raj != b_raj: matched.append(10); score += 1; p_items.append("10. வேதை பொருத்தம் ✔")
        else: unmatched.append(10); p_items.append("10. வேதை பொருத்தம் ✖")

        if TamilAstroConstants.NADI_MAP[g_nak_idx] != TamilAstroConstants.NADI_MAP[b_nak_idx]: matched.append(11); score += 1; p_items.append("11. நாடி பொருத்தம் ✔")
        else: unmatched.append(11); p_items.append("11. நாடி பொருத்தம் ✖")

        return matched, unmatched, score, p_items

    @classmethod
    def evaluate_match(cls, girl: Dict[str, Any], boy: Dict[str, Any], mode: str = "current") -> Dict[str, Any]:
        matrix = []; earned = 100.0
        g_lag = girl["lagna_idx"]; b_lag = boy["lagna_idx"]
        g_to_b = (b_lag - g_lag) % 12 + 1; b_to_g = (g_lag - b_lag) % 12 + 1

        matched_rules, _, nak_score, p_items = cls.evaluate_nakshatra_11_points(girl["nak_idx"], girl["rasi_idx"], boy["nak_idx"], boy["rasi_idx"])
        matrix.append(("1. நட்சத்திர பொருத்தம்", "  " + "\n  ".join(p_items), f"✔({nak_score}/11)"))

        r2_icon = "✔" if g_to_b not in [2, 6, 8, 12] else "✖"
        if r2_icon == "✖": earned -= 10.0
        matrix.append(("2. லக்கினம்", f"பெண் லக்னத்திலிருந்து ஆண் லக்னம் ({g_to_b}) மற்றும் ஆணிலிருந்து பெண் ({b_to_g}). 2, 6, 8, 12 தவிர்ப்பது நலம்.", r2_icon))

        matrix.append(("3. ராசி/சந்திரன்", f"பெண்-{'ஆண்' if girl['rasi_idx']%2==0 else 'பெண்'} ராசி / ஆண்-{'ஆண்' if boy['rasi_idx']%2==0 else 'பெண்'} ராசி.", "✔"))

        gk_lord = girl["karanam_lord"]; bk_lord = boy["karanam_lord"]
        if (gk_lord == "சனி" and bk_lord == "சூரியன்") or (bk_lord == "சனி" and gk_lord == "சூரியன்"): k_stat = f"{gk_lord}/{bk_lord} பகை"; k_icon = "✖"; earned -= 10.0
        else: k_stat = f"{gk_lord}/{bk_lord} சமம்/நட்பு"; k_icon = "✔"
        matrix.append(("4. கரணம்", k_stat, k_icon))

        matrix.append(("5. ஆண்/பெண்", "லக்கினாதிபதி மற்றும் சுக்கிரன்/செவ்வாய் நிலை பொருத்தம்.", "✔"))
        matrix.append(("6. செ/சனி பார்வை", "7-ஆம் இடத்து கிரகங்களின் பார்வை ஆய்வு.", "✔"))

        g_dark = TamilAstroConstants.LAGNA_DARK_HOUSES_MAP.get(g_lag, "இல்லை")
        b_dark = TamilAstroConstants.LAGNA_DARK_HOUSES_MAP.get(b_lag, "இல்லை")
        r7_icon = "✖" if (g_dark != "இல்லை" or b_dark != "இல்லை") else "✔"
        if r7_icon == "✖": earned -= 10.0
        matrix.append(("7. இருண்ட வீடுகள்", f"பெண்: {g_dark} | ஆண்: {b_dark}", r7_icon))

        matrix.append(("8. பாதிக்கப்பட்ட வீடுகள்", "2, 5, 7, 8 வீடுகளின் தோஷ ஆய்வு சமநிலை.", "✔"))

        g_raj = TamilAstroConstants.RAJJU_MAP[girl["nak_idx"]]; b_raj = TamilAstroConstants.RAJJU_MAP[boy["nak_idx"]]
        if g_raj == b_raj: r9_stat = f"ஒரே ரஜ்ஜு ({g_raj}) - தவிர்க்கவும்."; r9_icon = "✖"; earned -= 30.0
        else: r9_stat = f"வேறு ரஜ்ஜு (பெண்-{g_raj} | ஆண்-{b_raj}) - உத்தமம்."; r9_icon = "✔"
        matrix.append(("9. ரஜ்ஜு பொருத்தம்", r9_stat, r9_icon))

        matrix.append(("10. சூரி/சந் நிலை", "சூரிய மற்றும் சந்திரன் நிலை உத்தமம்.", "✔"))

        if girl["active_dasa"] == boy["active_dasa"]: d_stat = f"{girl['active_dasa']} - ஒரே தசா (தசா சந்தி தோஷம்)"; d_icon = "✖"; earned -= 25.0
        else: d_stat = f"{girl['active_dasa']} / {boy['active_dasa']} - வெவ்வேறானவை (தோஷமில்லை)"; d_icon = "✔"
        matrix.append(("11. தசா பொருத்தம்", d_stat, d_icon))

        matrix.append(("12. தோஷங்கள்", "களத்திர தோஷ சமநிலை ஆய்வு.", "✔"))

        malefics = ["சூரி", "சனி", "ராகு", "கேது", "செ", "மாந்தி"]
        g_7th_mals = [p for p in malefics if ((girl["positions"][p]["rasi_idx"] - g_lag) % 12 + 1) == 7]
        b_7th_mals = [p for p in malefics if ((boy["positions"][p]["rasi_idx"] - b_lag) % 12 + 1) == 7]

        if g_7th_mals or b_7th_mals:
            g_msg = f"பெண்ணின் 7-ல் ({', '.join(g_7th_mals)})" if g_7th_mals else "பெண்ணின் 7-ஆம் இடம் தூய்மை"
            b_msg = f"ஆணின் 7-ல் ({', '.join(b_7th_mals)})" if b_7th_mals else "ஆணின் 7-ஆம் இடம் தூய்மை"
            seventh_house_note = f"எச்சரிக்கை: {g_msg} | {b_msg}. கவனமாக ஆராயவும்."
            seventh_house_color = "#8B0000"
        else:
            seventh_house_note = "7-ஆம் இடம் தூய்மை: இருவர் ஜாதகத்திலும் 7-ஆம் இடத்தில் தோஷ கிரகங்கள் இல்லை."
            seventh_house_color = "#0a4b33"

        final_pct = max(10, min(100, int(earned)))
        if final_pct <= 40: badge = f"*{final_pct}%*\n✖ தவிர்க்க"; color = "#ffcccc"
        elif final_pct <= 60: badge = f"*{final_pct}%*\n-- சராசரி"; color = "#fff2cc"
        else: badge = f"*{final_pct}%*\n✔ உத்தமம்"; color = "#d9ead3"

        return {
            "girl": girl, "boy": boy, "final_pct": final_pct,
            "recommendation": badge, "rec_color": color, "matrix": matrix,
            "diag_msg": f"தோஷ ஆய்வு: இருவர் ஜாதகத்திலும் தோஷ சமநிலை சரியாக உள்ளது ({final_pct}%)",
            "seventh_note": seventh_house_note, "seventh_color": seventh_house_color
        }


# =====================================================================
# 7. SUB-TABS (KUDUMPA JOTHIDAM REFERENCE & PREDICTION ENGINE)
# =====================================================================
class KudumpaJothidamBookReferenceTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#f2f4f4", **kwargs)
        self._build_ui()

    def _build_ui(self):
        hdr_frame = tk.Frame(self, bg="#001f3f", pady=10); hdr_frame.pack(fill="x")
        tk.Label(hdr_frame, text="குடும்ப ஜோதிடம் — சாஸ்திர விதிகள் (LIFCO Book Canonical Reference)", font=("Helvetica", 14, "bold"), fg="white", bg="#001f3f").pack()
        book_nb = ttk.Notebook(self); book_nb.pack(fill="both", expand=True, padx=12, pady=10)

        tab_bhava = tk.Frame(book_nb, bg="white"); book_nb.add(tab_bhava, text=" 1. பாவ பலன்கள் (12 வீடுகள்) ")
        self._build_bhava_table(tab_bhava)

        tab_balar = tk.Frame(book_nb, bg="white"); book_nb.add(tab_balar, text=" 2. பாலாரிஷ்டம் & தோஷ விதிகள் ")
        self._build_balarishtam_table(tab_balar)

        tab_graha = tk.Frame(book_nb, bg="white"); book_nb.add(tab_graha, text=" 3. நவக்கிரக காரகத்துவம் ")
        self._build_graha_table(tab_graha)

        tab_star = tk.Frame(book_nb, bg="white"); book_nb.add(tab_star, text=" 4. நட்சத்திர பாத பலன்கள் ")
        self._build_star_table(tab_star)

    def _build_bhava_table(self, container):
        columns = ("House", "Name", "ClassicalSignifications", "LordshipRule")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=20)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#C8B7A6", foreground="#2C1A14", relief="raised")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=26, background="#FDF8E7", fieldbackground="#FDF8E7", foreground="#2C1A14")
        
        tree.heading("House", text="பாவம்"); tree.heading("Name", text="பெயர்")
        tree.heading("ClassicalSignifications", text="சாஸ்திர பலன்கள்"); tree.heading("LordshipRule", text="அதிபதி விதி")
        for col, w in zip(columns, [100, 160, 480, 400]): tree.column(col, width=w, anchor=tk.W if col in ["ClassicalSignifications", "LordshipRule"] else tk.CENTER)
        scroll = ttk.Scrollbar(container, orient="vertical", command=tree.yview); tree.configure(yscroll=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        bhava_data = [
            ("1-ஆம் இடம்", "லக்னம் (உடல்)", "உயிர், ஜீவன், தேகம், தோற்றம், ஆயுள் பலம், புகழ்", "லக்னாதிபதி ஆட்சியாகவோ உச்சமாகவோ இருந்தால் பூரண ஆயுள் மற்றும் பிரதாபம்"),
            ("2-ஆம் இடம்", "வாக்கு / தனம்", "குடும்பம், தனம், கண் பார்வை, வாக்கு வன்மை", "2-ஆம் அதிபதி பலமுற்றால் வாக்கு சாதுர்யம், செல்வம் மற்றும் குடும்ப விருத்தி"),
            ("3-ஆம் இடம்", "சகோதரம் / தைரியம்", "பேச்சு வல்லமை, தைரியம், இளைய சகோதரம், அணிகலம்", "3-ஆம் அதிபதி பலமுற்றால் சகோதர ஆதரவு, ஆள் அடிமை மற்றும் போகம்"),
            ("4-ஆம் இடம்", "மாத்ரு / சுகம்", "வீடு, வாகனம், நிலம், மாதா, வித்தை, வியாபாரம்", "4-ஆம் அதிபதி பலமுற்றால் மாளிகை போன்ற வீடு, மாடு கன்று பால் பாக்கியம்"),
            ("5-ஆம் இடம்", "புத்திரம் / புண்ணியம்", "சந்ததி, புகழ், அம்மாள், பிரபுத்வம், மேல் படிப்பு", "5-ஆம் அதிபதி பலமுற்றால் புத்திர விருத்தி, யோகாப்யாசம் மற்றும் சாஸ்திர ஞானம்"),
            ("6-ஆம் இடம்", "ரோகம் / சத்ரு", "சத்ரு, ரோகம், வழக்கு, கடன், திருட்டு பயம்", "6-ஆம் அதிபதி சுப பலமுற்றால் சத்ரு ஜயம் மற்றும் கடன் நிவர்த்தி"),
            ("7-ஆம் இடம்", "களத்திரம் / மனைவி", "மனைவி, மாரக ஸ்தானம், கூட்டாளிகள், காமம்", "7-ஆம் அதிபதி பலமுற்றால் நல்ல மனைவி மற்றும் கூட்டு வியாபார லாபம்"),
            ("8-ஆம் இடம்", "ஆயுள் / அஷ்டமம்", "ஆயுள், மரண வழி, அவமானம், வறுமை, கண்டம்", "8-ஆம் அதிபதி பலமுற்றால் தீர்க்க ஆயுள்; பாப பலமுற்றால் கண்டம் மற்றும் சிறை"),
            ("9-ஆம் இடம்", "பாக்கியம் / பித்ரு", "கடவுள் பக்தி, குரு உபதேசம், தர்மம், பிதா, பிரயாணம்", "9-ஆம் அதிபதி பலமுற்றால் பித்ரு ஆசீர்வாதம், தர்ம சிந்தனை மற்றும் புகழ்"),
            ("10-ஆம் இடம்", "ஜீவனம் / தொழில்", "ராஜ்யாதிபத்யம், தொழில், கர்மம், ஞானம், அந்தஸ்து", "10-ஆம் அதிபதி பலமுற்றால் அரசாங்க கீர்த்தி, உயர்பதவி மற்றும் செல்வ செழிப்பு"),
            ("11-ஆம் இடம்", "லாபம் / மூத்த சகோ", "மூத்த சகோதரம், லாபம், ஆடை ஆபரண சேர்க்கை", "11-ஆம் அதிபதி பலமுற்றால் சகல விதங்களிலும் லாபம் மற்றும் சகோதர ஆதரவு"),
            ("12-ஆம் இடம்", "விரயம் / மோட்சம்", "செலவு, சயன சுகம், மோட்சம், அயல்நாடு வாசம்", "12-ஆம் அதிபதி சுப பலமுற்றால் நல்ல செலவுகள் மற்றும் சயன சுகம்")
        ]
        for row in bhava_data: tree.insert("", tk.END, values=row)

    def _build_balarishtam_table(self, container):
        columns = ("RuleNo", "DoshamType", "PlanetaryAfflictionRule", "ClassicalRemedyOutcome")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=20)
        tree.heading("RuleNo", text="விதி"); tree.heading("DoshamType", text="தோஷ வகை")
        tree.heading("PlanetaryAfflictionRule", text="கிரஹ தோஷ அமைப்பு"); tree.heading("ClassicalRemedyOutcome", text="சாஸ்திர பரிகாரம் / பலன்")
        for col, w in zip(columns, [80, 180, 500, 380]): tree.column(col, width=w, anchor=tk.W if col in ["PlanetaryAfflictionRule", "ClassicalRemedyOutcome"] else tk.CENTER)
        scroll = ttk.Scrollbar(container, orient="vertical", command=tree.yview); tree.configure(yscroll=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        balar_data = [
            ("விதி 1", "சிசு பாலாரிஷ்டம்", "லக்னத்திலிருந்து 6, 8-ல் சந்திரன் பாபக்கிரஹ வீட்டிலிருந்து பாப பார்வை பெறுதல்", "சிசுவுக்கு பாலாரிஷ்ட தோஷம்; குரு பார்வை இருந்தால் தோஷ நிவர்த்தி"),
            ("விதி 2", "சிசு பாலாரிஷ்டம்", "5-ல் சனி, ராகு அல்லது கேது தனித்து அமர்தல்", "சிசுவிற்கு அரிஷ்டம்; சாந்தி பரிகாரங்களால் நிவர்த்தி"),
            ("விதி 3", "தாயார் அரிஷ்டம்", "லக்னத்தில் சந்திரன், சுக்ரன் இருந்து 7-ல் சனி ஒரே பாதத்தில் அமர்தல்", "தாயாருக்கும் குழந்தைக்கும் அரிஷ்டம்"),
            ("விதி 4", "தகப்பனார் அரிஷ்டம்", "5-ல் சூரியன், சந்திரன் மற்றும் செவ்வாயுடன் கூடி அமர்தல்", "தகப்பனாருக்கும் சிசுவுக்கும் அரிஷ்டம்"),
            ("விதி 5", "அம்மான் அரிஷ்டம்", "லக்னத்துக்கு 5-ல் சனியோடு சந்திரன் அல்லது சூரியனோடு செவ்வாய் அமர்தல்", "தாய் மாமனுக்கு அரிஷ்டம்; சுபக்கிரஹ பார்வை இருந்தால் தோஷ நிவர்த்தி"),
            ("விதி 6", "கெண்ட தோஷம்", "லக்னாதிபதி பலஹீனமாய் 2-ல் இருக்க 8-ல் கிருஷ்ணபக்ஷ சந்திரன் அமர்தல்", "சிசுவுக்கு 8 நாள் வரையில் கெண்டம்"),
            ("விதி 7", "செவ்வாய் தோஷம்", "லக்னத்திற்கு 2, 4, 7, 8, 12-ல் செவ்வாய் அமர்தல்", "களத்திர தோஷம்; பரிகாரம் மற்றும் தோஷ சாம்யத்தால் திருமணம் செய்யலாம்"),
            ("விதி 8", "ராகு-கேது தோஷம்", "லக்னத்திற்கு 1, 7-ல் ராகு மற்றும் கேது அமர்தல்", "களத்திர தோஷம்; குரு பார்வை மற்றும் சுப சேர்க்கையால் தோஷ நிவர்த்தி")
        ]
        for row in balar_data: tree.insert("", tk.END, values=row)

    def _build_graha_table(self, container):
        columns = ("Graha", "Karakatvam", "Exaltation", "Debilitation", "FriendlySigns")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=20)
        tree.heading("Graha", text="கிரஹம்"); tree.heading("Karakatvam", text="காரகத்துவம்")
        tree.heading("Exaltation", text="உச்சம்"); tree.heading("Debilitation", text="நீசம்"); tree.heading("FriendlySigns", text="நட்பு வீடுகள்")
        for col, w in zip(columns, [120, 360, 160, 160, 340]): tree.column(col, width=w, anchor=tk.W if col in ["Karakatvam", "FriendlySigns"] else tk.CENTER)
        scroll = ttk.Scrollbar(container, orient="vertical", command=tree.yview); tree.configure(yscroll=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        graha_data = [
            ("சூரியன்", "பித்ரு காரகன்: பிதா, ஆத்மா, சிரசு, வலது நேத்திரம், தைரியம், ராஜ சேவை", "மேஷம்", "துலாம்", "விருச்சிகம், தனுசு, கடகம், மீனம்"),
            ("சந்திரன்", "மாத்ரு காரகன்: மாதா, மனது, பராசக்தி, சுகபோஜனம், இடது கண், கீர்த்தி", "ரிஷபம்", "விருச்சிகம்", "மிதுனம், சிம்மம், கன்னி"),
            ("செவ்வாய்", "ப்ராத்ரு காரகன்: சகோதரம், பூமி, சுப்பிரமணியர், தைரியம், அதிகாரம்", "மகரம்", "கடகம்", "சிம்மம், தனுசு, மீனம்"),
            ("புதன்", "வித்யா காரகன்: அம்மான், கல்வி, விஷ்ணு, சாதுர்யம், கணிதம், சிற்பம்", "கன்னி", "மீனம்", "ரிஷபம், சிம்மம், துலாம்"),
            ("குரு", "புத்ர காரகன்: புத்திரர், பிரம்மா, ஞானம், தனம், ஆசாரியத்வம், சாந்தம்", "கடகம்", "மகரம்", "மேஷம், சிம்மம், கன்னி, விருச்சிகம்"),
            ("சுக்ரன்", "களத்ர காரகன்: களத்திரம், கிருகம், வாகனம், அழகு, பரிமள வாசனை", "மீனம்", "கன்னி", "மிதுனம், தனுசு, மகரம், கும்பம்"),
            ("சனி", "ஆயுள் காரகன்: தீர்க்காயுசு, சாஸ்தா, ஜீவனம், விவசாயம், இரும்பு, உழைப்பு", "துலாம்", "மேஷம்", "ரிஷபம், மிதுனம்"),
            ("ராகு", "பிதாமஹ காரகன்: ஞானம், பிதுர் பாட்டன் வம்சம், வெளிநாடு, பிரதாபம்", "கன்னி", "மீனம்", "மிதுனம், கன்னி, துலாம், தனுசு"),
            ("கேது", "மாதாமஹ காரகன்: ஞானம், மாதுர் பாட்டன் வம்சம், தவம், மோட்சம்", "மீனம்", "கன்னி", "மகரம், மீனம்")
        ]
        for row in graha_data: tree.insert("", tk.END, values=row)

    def _build_star_table(self, container):
        columns = ("StarName", "Pada1", "Pada2", "Pada3", "Pada4")
        tree = ttk.Treeview(container, columns=columns, show="headings", height=20)
        tree.heading("StarName", text="நட்சத்திரம்"); tree.heading("Pada1", text="1-ஆம் பாதம்"); tree.heading("Pada2", text="2-ஆம் பாதம்")
        tree.heading("Pada3", text="3-ஆம் பாதம்"); tree.heading("Pada4", text="4-ஆம் பாதம்")
        for col, w in zip(columns, [160, 240, 240, 240, 240]): tree.column(col, width=w, anchor=tk.W)
        scroll = ttk.Scrollbar(container, orient="vertical", command=tree.yview); tree.configure(yscroll=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        star_data = [
            ("அஸ்வினி", "தெய்வீக அருள், தனவான்", "சாஸ்திர ஆர்வம், அன்பானவர்", "வேத விஞ்ஞான பிரியம்", "விசால புத்தி கூர்மை, நீதி"),
            ("பரணி", "பருத்த தேகம், நற்குணம்", "தான தருமம், எதிரி ஜயம்", "அதிர்ஷ்டம், சந்தோஷம்", "காரிய சாத்தியம், சமர்த்தர்"),
            ("கார்த்திகை", "பூமி காணி சொத்து, ஆசாரம்", "கலை ஆர்வம், திறமை", "தைரியம், மெதுவான குணம்", "சண்டை பிரியம், உழைப்பு"),
            ("ரோஹிணி", "கம்பீர தோற்றம், தனவான்", "ஆசார அனுஷ்டானம், சத்தியம்", "கணித மேதை, கலை பிரியம்", "நீதி நேர்மை, செல்வாக்கு"),
            ("மிருகசீரிடம்", "விசால புத்தி, அழகு", "உண்மை பேசுதல், சத்தியவான்", "உதார குணம், சாது", "சத்திய நெறி, தரும சிந்தனை"),
            ("திருவாதிரை", "சுத்த ஹிருதயம், திறமை", "கண்டிப்பான பேச்சு, தைரியம்", "உழைப்பு, கணித ஆர்வம்", "சுபகாரியவாதி, சாமர்த்தியம்"),
            ("புனர்பூசம்", "கல்வி ஊக்கம், பித்த தேகம்", "பேசும் திறமை, டாம்பீகம்", "நீண்ட ஆயுள், புரிந்துகொள்ளல்", "அழகான அங்கலக்ஷணம், ஈகை"),
            ("பூசம்", "தெய்வ பக்தி, தார்மீக சிந்தனை", "புத்திசாலி, செல்வந்தர்", "சதா சிரித்துப் பேசுதல், புகழ்", "காரிய சாத்தியம், தைரியம்"),
            ("ஆயில்யம்", "செல்வந்தர், சாதுர்யம்", "சிவந்த மேனி, ஆசாரம்", "தைரியம், மெதுவான குணம்", "பண சம்பாத்திய பிரியம்"),
            ("மகம்", "சாஸ்திர ஆராய்ச்சி, தருமம்", "கௌரவம், பரிசுத்த குணம்", "சாது, பலவான், அமைதி", "மதுரமான பேச்சு, சீலம்"),
            ("பூரம்", "ஆசார சீலர், புத்தி சாதுர்யம்", "விவசாய ஈடுபாடு, மேன்மை", "கீர்த்தி, உண்மை, நேர்மை", "பெரியோர் பக்தி, உழைப்பு"),
            ("உத்திரம்", "இனிமையான சொல், நற்குணம்", "தைரியசாலி, உழைப்பு", "தெய்வீக வழிபாடு, நாணயம்", "நன்றி மறவாமை, தைரியம்"),
            ("ஹஸ்தம்", "படித்தவர், நற்காரிய பிரியம்", "கலை பிரியம், திட சரீரம்", "வியாபார குணம், உழைப்பு", "உயர்ந்த தோற்றம், சந்தோஷம்"),
            ("சித்திரை", "காரியவாதி, சாதுர்யம்", "கல்வி ஊக்கம், உழைப்பு", "பராக்ரமம், பரந்த நோக்கம்", "திறமைசாலி, வெற்றி"),
            ("சுவாதி", "தெய்வீக வழிபாடு, நற்குணம்", "திட தேகம், புத்தி விசாலம்", "தைரியம், உழைப்பு", "குணமறிந்து பழகுதல்"),
            ("விசாகம்", "கல்வி ஊக்கம், சாஸ்திர ஆர்வம்", "திறமைசாலி, சாஸ்திர ஞானம்", "திரேக பலம், புரிந்துகொள்ளல்", "செல்வந்தர், வாக்கு சாமர்த்தியம்"),
            ("அனுஷம்", "ஆசார சீலர், மேன்மை அந்தஸ்து", "அரசாங்க கௌரவம், சங்கீதம்", "திறமை, தர்ம சிந்தனை", "புகழ், நற்குணம்"),
            ("கேட்டை", "கலை தேர்ச்சி, தர்ம குணம்", "சங்கீத பிரியம், சாதுர்யம்", "உழைப்பு, தைரியம்", "காரிய சாத்தியம், உழைப்பு"),
            ("மூலம்", "சுறுசுறுப்பு, செல்வந்தர்", "கல்வி ஊக்கம், சாதுர்யம்", "அழகான அங்கலக்ஷணம்", "திரேக பலம், சத்ரு ஜயம்"),
            ("பூராடம்", "புத்தி சாதுர்யம், புகழ்", "உழைப்பு, காரிய சாத்தியம்", "செல்வந்தர், தைரியம்", "திட தேகம், தைரியசாலி"),
            ("உத்திராடம்", "கல்வி பிரியம், சாமர்த்தியம்", "சாஸ்திர ஞானம், பலசாலி", "தைரியம், உழைப்பு", "சுறுசுறுப்பு, தனவான்"),
            ("திருவோணம்", "திட தேகம், தர்ம சிந்தனை", "தனவான், பெரியோர் பக்தி", "பொதுக்காரிய பற்றுதல்", "செல்வாக்கு, அறிவாளி"),
            ("அவிட்டம்", "சுக சௌகர்யம், செல்வாக்கு", "நிதான புத்தி, தைரியம்", "உயர்ந்த கம்பீர தோற்றம்", "செல்வம், தைரியம்"),
            ("சதயம்", "வசீகர தோற்றம், பொறுமை", "நற்குணம், காரிய சாத்தியம்", "பிரபல நோக்கம், உழைப்பு", "தீர யோசித்தல், திறமை"),
            ("பூரட்டாதி", "திட சரீரம், பக்தி", "விசுவாசம், பக்தி", "படித்த அறிஞர், நாகரீகம்", "தொழில் கீர்த்தி, நாணயம்"),
            ("உத்திரட்டாதி", "அழகான வாக்கு, செல்வாக்கு", "திறமைசாலி, நற்குணம்", "தெய்வீக வழிபாடு, உழைப்பு", "கல்வி சிறந்த கவிஞர்"),
            ("ரேவதி", "அழகான தோற்றம், சகஜ குணம்", "தைரியம், சுயநலம்", "நற்குணம், உழைப்பு", "நீதி நேர்மை, சத்ரு ஜயம்")
        ]
        for row in star_data: tree.insert("", tk.END, values=row)


class KudumpaJothidamPredictionTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#EAE0C8", **kwargs)
        self._build_ui()

    def _build_ui(self):
        hdr_frame = tk.Frame(self, bg="#3E2723", pady=10, bd=3, relief="raised"); hdr_frame.pack(fill="x")
        tk.Label(hdr_frame, text="குடும்ப ஜோதிடம் — முழுமையான ஜாதகப் பலன்கள் & திருமண சாம்ய ஆய்வு", font=("Helvetica", 14, "bold"), fg="#F1E3A0", bg="#3E2723").pack()

        self.syn_nb = ttk.Notebook(self)
        self.syn_nb.pack(fill="both", expand=True, padx=12, pady=10)

        self.tab_bride_bhava = tk.Frame(self.syn_nb, bg="#FDF8E7")
        self.syn_nb.add(self.tab_bride_bhava, text=" 1.3.1 பெண்ணின் முழுமையான பலன்கள் ")
        self._build_person_bhava_layout(self.tab_bride_bhava, "bride")

        self.tab_groom_bhava = tk.Frame(self.syn_nb, bg="#FDF8E7")
        self.syn_nb.add(self.tab_groom_bhava, text=" 1.3.2 ஆணின் முழுமையான பலன்கள் ")
        self._build_person_bhava_layout(self.tab_groom_bhava, "groom")

        self.tab_synergy = tk.Frame(self.syn_nb, bg="#FDF8E7")
        self.syn_nb.add(self.tab_synergy, text=" 1.3.3 திருமண சாம்ய ஆய்வு (Joint Synergy) ")
        self._build_synergy_layout(self.tab_synergy)

    def _build_person_bhava_layout(self, container, person_type):
        paned = ttk.PanedWindow(container, orient="vertical")
        paned.pack(fill="both", expand=True, padx=6, pady=6)
        
        top_frame = tk.Frame(paned, bg="white"); paned.add(top_frame, weight=2)
        columns = ("BhavaNum", "BhavaTitle", "LordRasi", "ClassicalPrediction")
        tree = ttk.Treeview(top_frame, columns=columns, show="headings", height=10)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#C8B7A6", foreground="#2C1A14", relief="raised")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=26, background="#FDF8E7", fieldbackground="#FDF8E7", foreground="#2C1A14")
        
        tree.heading("BhavaNum", text="பாவம்"); tree.heading("BhavaTitle", text="பாவ பெயர்")
        tree.heading("LordRasi", text="அதிபதி & ராசி"); tree.heading("ClassicalPrediction", text="சாஸ்திர பலன்")
        for col, w in zip(columns, [100, 160, 160, 600]): tree.column(col, width=w, anchor=tk.W if col == "ClassicalPrediction" else tk.CENTER)
        scroll = ttk.Scrollbar(top_frame, orient="vertical", command=tree.yview); tree.configure(yscroll=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        
        if person_type == "bride": self.bride_tree = tree
        else: self.groom_tree = tree

        bot_frame = tk.Frame(paned, bg="#FDF8E7", bd=3, relief="sunken"); paned.add(bot_frame, weight=3)
        text_widget = tk.Text(bot_frame, font=("Helvetica", 12, "bold"), bg="#FEFBEA", fg="#2C1A14", wrap="word", padx=10, pady=10)
        t_scroll = ttk.Scrollbar(bot_frame, orient="vertical", command=text_widget.yview); text_widget.configure(yscroll=t_scroll.set)
        text_widget.pack(side="left", fill="both", expand=True); t_scroll.pack(side="right", fill="y")
        text_widget.config(state="disabled")
        
        if person_type == "bride": self.bride_text = text_widget
        else: self.groom_text = text_widget

    def _build_synergy_layout(self, container):
        paned = ttk.PanedWindow(container, orient="vertical")
        paned.pack(fill="both", expand=True, padx=6, pady=6)
        
        top_frame = tk.Frame(paned, bg="white"); paned.add(top_frame, weight=2)
        columns = ("SynergyCategory", "FeatureTitle", "BrideState", "GroomState", "JointOutcome")
        tree = ttk.Treeview(top_frame, columns=columns, show="headings", height=10)
        tree.heading("SynergyCategory", text="ஆய்வு பிரிவு"); tree.heading("FeatureTitle", text="அம்ச தலைப்பு")
        tree.heading("BrideState", text="பெண் நிலை"); tree.heading("GroomState", text="ஆண் நிலை")
        tree.heading("JointOutcome", text="இணைந்த பலன் & தோஷ சாம்யம்")
        for col, w in zip(columns, [160, 200, 180, 180, 500]): tree.column(col, width=w, anchor=tk.W if col == "JointOutcome" else tk.CENTER)
        scroll = ttk.Scrollbar(top_frame, orient="vertical", command=tree.yview); tree.configure(yscroll=scroll.set)
        tree.pack(side="left", fill="both", expand=True); scroll.pack(side="right", fill="y")
        self.synergy_tree = tree

        bot_frame = tk.Frame(paned, bg="#FDF8E7", bd=3, relief="sunken"); paned.add(bot_frame, weight=3)
        text_widget = tk.Text(bot_frame, font=("Helvetica", 12, "bold"), bg="#EAE0C8", fg="#2C1A14", wrap="word", padx=10, pady=10)
        t_scroll = ttk.Scrollbar(bot_frame, orient="vertical", command=text_widget.yview); text_widget.configure(yscroll=t_scroll.set)
        text_widget.pack(side="left", fill="both", expand=True); t_scroll.pack(side="right", fill="y")
        text_widget.config(state="disabled")
        self.synergy_text = text_widget

    def update_predictions(self, g_data: Dict[str, Any], b_data: Dict[str, Any], match_res: Dict[str, Any]):
        self._populate_person_tree(self.bride_tree, self.bride_text, g_data, "பெண்")
        self._populate_person_tree(self.groom_tree, self.groom_text, b_data, "ஆண்")
        self._populate_synergy_tree(g_data, b_data, match_res)

    def _get_planet_house_prediction(self, planet_short: str, house: int) -> str:
        preds = {
            "சூரி": {
                1: "உடல் உஷ்ணம், தலைமைப் பண்பு, நேத்திர பாதிப்பு ஏற்படலாம்.",
                2: "பேச்சில் கண்டிப்பு, குடும்பத்தில் முன்கோபம், அரசு வழியில் தன வரவு.",
                3: "அபரிமிதமான தைரியம், இளைய சகோதரருக்கு சிரமம்.",
                4: "தாய் மற்றும் வாகன சுகத்தில் சிறு தடைகள், பரம்பரை சொத்து கிட்டும்.",
                5: "அறிவு கூர்மை, அரசாங்க லாபம், புத்திர தோஷம் (சற்று).",
                6: "சத்ரு ஜெயம், நோய் நிவர்த்தி, அதிகாரப் பதவி மற்றும் லாபம்.",
                7: "களத்திர தோஷம், மனைவியுடன்/கணவனுடன் கருத்து வேறுபாடு.",
                8: "ஆயுள் கண்டம், அலைச்சல், உஷ்ண வியாதி, தந்தைக்கு சிரமம்.",
                9: "பித்ரு பாக்கியம், தர்ம சிந்தனை, தெய்வ பக்தி.",
                10: "ஜீவன விருத்தி, அரசு உத்தியோகம், சமூக அந்தஸ்து (திக்பலம்).",
                11: "எல்லா வகையிலும் லாபம், மூத்த சகோதரருக்கு நலம்.",
                12: "வெளியூர் வாசம், விரயம், தூக்கக் குறைவு."
            },
            "சந்": {
                1: "முக வசீகரம், கற்பனைத் திறன், சளித் தொல்லைகள் வரலாம்.",
                2: "இனிமையான வாக்கு, தன லாபம், குடும்ப சுகம்.",
                3: "இளைய சகோதரி லாபம், தைரியம், அடிக்கடி அலைச்சல்.",
                4: "தாயாருக்கு நலம் (திக்பலம்), மாளிகை, வாகன சுகம்.",
                5: "பெண் குழந்தை அதிகம், புத்திசாலி, தெய்வ பக்தி.",
                6: "நீர் சம்பந்தமான வியாதி, கடன், சஞ்சலம் (மறைவு).",
                7: "அழகான களத்திரம், பிரயாணங்களால் வியாபார லாபம்.",
                8: "பாலாரிஷ்ட தோஷம், கண்டம், மன உளைச்சல் (மறைவு).",
                9: "தர்ம சிந்தனை, பாக்கிய விருத்தி, வெளிநாட்டுப் பயணம்.",
                10: "தொழில் சீரமைப்பு, வியாபார லாபம், புகழ்.",
                11: "மூத்த சகோதரி நலம், பல வழிகளில் லாபம்.",
                12: "தூக்கமின்மை, கண் பார்வை குறைபாடு, சுப விரயம் (மறைவு)."
            },
            "செ": {
                1: "முன்கோபம், ரத்த காயம், அதிக தைரியம்.",
                2: "கலகப் பேச்சு, குடும்பத்தில் சிறு சச்சரவு, தனம்.",
                3: "இளைய சகோதரர்களுக்கு தோஷம், அளவற்ற வீரம்.",
                4: "வீடு வாகனங்களில் தடங்கல், தாயாருக்கு தோஷம்.",
                5: "புத்திர தோஷம், கோபம், எந்திரத் தொழில்.",
                6: "சத்ரு ஜெயம், கடன் தீரும், அதிகாரம்.",
                7: "செவ்வாய் தோஷம், களத்திர பாதிப்பு, முன்கோபம்.",
                8: "செவ்வாய் தோஷம், ஆயுள் கண்டம், விபத்து.",
                9: "பித்ரு விரோதம், துணிச்சலான செயல்கள்.",
                10: "அதிகாரம், போலீஸ்/ராணுவப் பதவி, நிலபுலன் விருத்தி (திக்பலம்).",
                11: "பூமி லாபம், மூத்த சகோதரருக்கு பாதிப்பு.",
                12: "செவ்வாய் தோஷம், தூக்கமின்மை, வீண் செலவு."
            },
            "புத": {
                1: "புத்திக் கூர்மை, கணித/ஜோதிட ஞானம் (திக்பலம்).",
                2: "நகைச்சுவை பேச்சு, கல்வித் திறன், தன லாபம்.",
                3: "மாமன் ஆதரவு, தைரியம், எழுத்துத் திறன்.",
                4: "வித்யா பாக்கியம், தாய்வழி லாபம், நல்ல வாகனம்.",
                5: "மாமன் வழியில் நலம், நல்ல அறிவு, புத்திர பாக்கியம்.",
                6: "நரம்பு தளர்ச்சி, தாய் மாமனுக்கு தோஷம் (மறைவு).",
                7: "அறிவான களத்திரம், வியாபார விருத்தி.",
                8: "கல்வியில் தடை, மாமன் தோஷம் (மறைவு).",
                9: "சாஸ்திர ஞானம், சிறந்த பாக்கியம்.",
                10: "வியாபார லாபம், கணக்கு/ஐடி துறை வேலை.",
                11: "பல வழிகளில் வியாபார லாபம், நலம்.",
                12: "கல்வியில் சிறு தடை, சுப செலவுகள் (மறைவு)."
            },
            "குரு": {
                1: "தெய்வ கடாட்சம், ஆயுள் விருத்தி (திக்பலம்).",
                2: "சிறந்த குடும்பம், பண வரவு, இனிமையான பேச்சு.",
                3: "தைரியக் குறைவு, சகோதர நலம்.",
                4: "சிறந்த வீடு, வாகனம், தாய் சுகம்.",
                5: "சாஸ்திர ஞானம், புத்திர தோஷம் (காரகோ பாவ நாஸ்தி).",
                6: "கடன், எதிரி, பித்தம் (மறைவு).",
                7: "நல்ல களத்திரம், திருமண சுகம், நற்பெயர்.",
                8: "மறைவு ஸ்தானம், எதிர்பாராத கஷ்டங்கள்.",
                9: "தெய்வ பக்தி, சிறப்பான பித்ரு பாக்கியம்.",
                10: "தொழிலில் நேர்மை, ஆசிரியர்/வங்கி வேலை.",
                11: "எல்லா லாபங்களும் தடையின்றி கிடைக்கும்.",
                12: "சுப விரயம், கோவில் திருப்பணிகள்."
            },
            "சுக்": {
                1: "வசீகரம், கலை ஆர்வம், செல்வம்.",
                2: "நேத்திர சுகம், தன லாபம், குடும்ப சுகம்.",
                3: "தைரியம், சகோதரி லாபம்.",
                4: "மாளிகை, ஆடம்பர வாகனம், சுகம் (திக்பலம்).",
                5: "பெண் குழந்தைகள், கலைகளில் தேர்ச்சி.",
                6: "களத்திர தோஷம், மர்ம நோய் (மறைவு).",
                7: "களத்திர தோஷம் (காரகோ பாவ நாஸ்தி), அதிக ஆசை.",
                8: "எதிர்பாராத தன லாபம், களத்திர தோஷம்.",
                9: "பாக்கிய விருத்தி, தர்மம், செல்வம்.",
                10: "கலை, ஆபரணத் தொழில், வியாபாரம்.",
                11: "வாகன லாபம், பெண்களால் சிறப்பான லாபம்.",
                12: "போக சுகம், சயன சுகம், அதிக செலவு."
            },
            "சனி": {
                1: "பிடிவாதம், சோம்பல், வாத நோய்.",
                2: "பேச்சில் கடுமை, குடும்பத்தில் சிறு சிரமம்.",
                3: "அதிக தைரியம், நீண்ட ஆயுள்.",
                4: "தாய், வாகன சுகக் குறைவு, தடைகள்.",
                5: "புத்திர தோஷம், மந்த புத்தி.",
                6: "சத்ரு ஜெயம், கடன் அடைபடும், ரோக நிவர்த்தி.",
                7: "களத்திர தோஷம் (திக்பலம்), காலதாமத திருமணம்.",
                8: "நீண்ட ஆயுள், வீண் அலைச்சல்.",
                9: "பித்ரு தோஷம், தெய்வ பக்தி குறைவு.",
                10: "கடின உழைப்பு, அடிமைத் தொழில் அல்லது தொழிற்சாலை.",
                11: "எல்லா வழிகளிலும் லாபம், நீண்ட ஆயுள்.",
                12: "வீண் விரயம், அலைச்சல், காலில் அடிபடுதல்."
            },
            "ராகு": {
                1: "நாக தோஷம், சர்ப்ப சாந்தி அவசியம்.",
                2: "நாக தோஷம், வாக்கு வன்மை.",
                3: "மிகச் சிறந்த தைரியம், சத்ரு ஜெயம்.",
                4: "நாக தோஷம், அலைச்சல்.",
                5: "புத்திர தோஷம், சர்ப்ப சாந்தி அவசியம்.",
                6: "சத்ரு ஜெயம், திடீர் பண வரவு.",
                7: "களத்திர தோஷம், சர்ப்ப சாந்தி அவசியம்.",
                8: "நாக தோஷம், கண்டம்.",
                9: "பித்ரு தோஷம், வெளிநாடு.",
                10: "தொழிலில் அலைச்சல்/வெளிநாடு.",
                11: "மிகச் சிறந்த லாபம், சத்ரு ஜெயம்.",
                12: "களத்திர தோஷம், விரயம்."
            },
            "கேது": {
                1: "களத்திர தோஷம், பற்றின்மை.",
                2: "களத்திர தோஷம், வீண் வாக்குவாதம்.",
                3: "சத்ரு ஜெயம், தைரியம்.",
                4: "ஞான காரகன், பற்றின்மை.",
                5: "புத்திர தோஷம், சர்ப்ப சாந்தி அவசியம்.",
                6: "சத்ரு ஜெயம், ஆன்மீக சிந்தனை.",
                7: "களத்திர தோஷம், சர்ப்ப சாந்தி அவசியம்.",
                8: "களத்திர தோஷம், ஞான காரகன்.",
                9: "மோட்சம், தெய்வ பக்தி.",
                10: "மோட்சம், தொழிலில் ஞானம்.",
                11: "சத்ரு ஜெயம், ஆன்மீக லாபம்.",
                12: "மோட்சம், வெளிநாடு."
            }
        }
        return preds.get(planet_short, {}).get(house, "பரிகாரங்களால் நன்மை உண்டாகும்.")

    def _generate_individual_prediction(self, p_data, person_title):
        lines = []
        lines.append(f"★ {person_title} ஜாதகத்தில் உள்ள அனைத்து கிரகங்களின் முழுமையான பலன்கள் ★\n")
        
        lag_idx = p_data["lagna_idx"]
        planet_full_names = {
            "சூரி": "சூரியன்", "சந்": "சந்திரன்", "செ": "செவ்வாய்",
            "புத": "புதன்", "குரு": "குரு", "சுக்": "சுக்கிரன்",
            "சனி": "சனி", "ராகு": "ராகு", "கேது": "கேது"
        }
        
        for p_short, p_full in planet_full_names.items():
            if p_short in p_data["positions"]:
                p_rasi = p_data["positions"][p_short]["rasi_idx"]
                house = (p_rasi - lag_idx) % 12 + 1
                pred_text = self._get_planet_house_prediction(p_short, house)
                lines.append(f"• {p_full} {house}-ஆம் இடத்தில் ({TamilAstroConstants.RASIS[p_rasi]}) அமர்ந்துள்ளார்:")
                lines.append(f"  பலாபலன்: {pred_text}\n")
                
        lines.append("★ கிரக பலங்கள் (உச்சம் / நீசம்) ★")
        exalted = []; debilitated = []
        exalt_map = {"சூரி": 0, "சந்": 1, "செ": 9, "புத": 5, "குரு": 3, "சுக்": 11, "சனி": 6}
        deb_map = {"சூரி": 6, "சந்": 7, "செ": 3, "புத": 11, "குரு": 9, "சுக்": 5, "சனி": 0}
        
        for p in ["சூரி", "சந்", "செ", "புத", "குரு", "சுக்", "சனி"]:
            if p_data["positions"][p]["rasi_idx"] == exalt_map.get(p, -1): exalted.append(p)
            if p_data["positions"][p]["rasi_idx"] == deb_map.get(p, -1): debilitated.append(p)
            
        if exalted:
            lines.append(f"   ஜாதகத்தில் ({', '.join(exalted)}) உச்சம் பெற்றுள்ளதால், அந்த கிரகங்களின் காரகத்துவ பலன்கள் (அதிகாரம், செல்வம்) வாழ்வில் முழுமையாகக் கிடைக்கும்.")
        if debilitated:
            lines.append(f"   ஜாதகத்தில் ({', '.join(debilitated)}) நீசம் பெற்றுள்ளதால், அந்த கிரகங்களின் பலன்களில் சற்றே தடங்கல்கள் ஏற்படலாம். உரிய பரிகாரங்கள் நன்மையளிக்கும்.")
        if not exalted and not debilitated:
            lines.append("   ஜாதகத்தில் கிரகங்கள் அனைத்தும் சம பலத்துடன் (ஆட்சி, நட்பு) இயல்பான நிலையில் அமைந்துள்ளன.")
            
        return "\n".join(lines)

    def _populate_person_tree(self, tree: ttk.Treeview, text_box: tk.Text, p_data: Dict[str, Any], gender: str):
        for item in tree.get_children(): tree.delete(item)
        lag_idx = p_data["lagna_idx"]

        bhava_titles = [
            "1-லக்னம் (உடல்)", "2-தனம்/வாக்கு", "3-தைரியம்/சகோ", "4-சுகம்/மாத்ரு",
            "5-புத்திரம்/புண்ணியம்", "6-ரோகம்/சத்ரு", "7-களத்திரம்/திருமணம்", "8-ஆயுள்/அஷ்டமம்",
            "9-பாக்கியம்/பித்ரு", "10-ஜீவனம்/தொழில்", "11-லாபம்/மூத்த சகோ", "12-விரயம்/மோட்சம்"
        ]

        for house_step in range(12):
            house_num = house_step + 1
            rasi_idx = (lag_idx + house_step) % 12
            rasi_name = TamilAstroConstants.RASIS[rasi_idx]
            lord_name = TamilAstroConstants.RASI_LORDS[rasi_idx]

            sitting_planets = [p for p, d in p_data["positions"].items() if d["rasi_idx"] == rasi_idx and p not in ["லக்", "மாந்தி"]]
            sit_str = f" | அமர்ந்தவை: {','.join(sitting_planets)}" if sitting_planets else ""

            if house_num == 1: pred = f"லக்னாதிபதி ({lord_name}) சுப பலமுற்றால் தீர்க்க ஆயுள், தேக சுகம் ஏற்படும்.{sit_str}"
            elif house_num == 2: pred = f"2-ஆம் அதிபதி ({lord_name}) பலமுற்றால் வாக்கு சாதுர்யம், செல்வம் விருத்தி.{sit_str}"
            elif house_num == 4: pred = f"4-ஆம் அதிபதி ({lord_name}) பலமுற்றால் வீடு, வாகனம், பால் பாக்கியம்.{sit_str}"
            elif house_num == 5: pred = f"5-ஆம் அதிபதி ({lord_name}) பலமுற்றால் புத்திர விருத்தி, சாஸ்திர ஞானம்.{sit_str}"
            elif house_num == 7: pred = f"7-ஆம் அதிபதி ({lord_name}) பலமுற்றால் நல்ல களத்திரம், வியாபார லாபம்.{sit_str}"
            elif house_num == 10: pred = f"10-ஆம் அதிபதி ({lord_name}) பலமுற்றால் அரசாங்க கீர்த்தி, உயர்பதவி.{sit_str}"
            elif house_num in [6, 8, 12]: pred = f"மறைவு ஸ்தானம் ({house_num}): சுப பலமுற்றால் விபரீத ராஜயோகம்.{sit_str}"
            else: pred = f"{house_num}-ஆம் அதிபதி ({lord_name}) சுப பலமுற்றால் லாப விருத்தி மற்றும் சமூக மதிப்பு.{sit_str}"

            tree.insert("", tk.END, values=(f"{house_num}-ஆம் பாவம்", bhava_titles[house_step], f"{lord_name} ({rasi_name})", pred))

        malefics = ["சூரி", "செ", "சனி", "ராகு", "கேது"]
        fifth_idx = (lag_idx + 4) % 12
        fifth_mals = [p for p in malefics if p_data["positions"][p]["rasi_idx"] == fifth_idx]
        if fifth_mals: balar_pred = f"லக்னத்துக்கு 5-ல் ({','.join(fifth_mals)}) அமர்ந்துள்ளதால் தாய் மாமனுக்கு அரிஷ்டம் ஏற்படும்."
        else: balar_pred = "லக்னத்துக்கு 5-ஆம் இடம் தூய்மையாக உள்ளதால் தாய் மாமனுக்கு அரிஷ்டம் இல்லை."
        tree.insert("", tk.END, values=("பாலாரிஷ்டம்", "அம்மான் அரிஷ்டம்", "5-ஆம் பாவம்", balar_pred))

        text_box.config(state="normal")
        text_box.delete("1.0", tk.END)
        text_box.insert(tk.END, self._generate_individual_prediction(p_data, p_data["name"] + f" ({gender})"))
        text_box.config(state="disabled")

    def _populate_synergy_tree(self, g_data: Dict[str, Any], b_data: Dict[str, Any], match_res: Dict[str, Any]):
        for item in self.synergy_tree.get_children(): self.synergy_tree.delete(item)

        g_dosh = SamutrikaLakshanamEngine.check_doshams(g_data)
        b_dosh = SamutrikaLakshanamEngine.check_doshams(b_data)

        s_outcome = "இருவருக்கும் செவ்வாய் தோஷம் உள்ளதால் தோஷ சாம்யம் ஏற்பட்டு தோஷம் நிவர்த்தியாகும்." if (g_dosh["sevvai"] == "உண்டு" and b_dosh["sevvai"] == "உண்டு") else (
                    "இருவருக்கும் செவ்வாய் தோஷம் இல்லாததால் தோஷமின்மை உத்தமம்." if (g_dosh["sevvai"] == "இல்லை" and b_dosh["sevvai"] == "இல்லை") else
                    "ஒருவருக்கு மட்டும் செவ்வாய் தோஷம் உள்ளதால் தோஷ சாம்யம் இல்லை; கவனமாகப் பொருத்தம் பார்க்கவும்.")
        self.synergy_tree.insert("", tk.END, values=("தோஷ சாம்யம்", "செவ்வாய் தோஷ சமநிலை", f"செவ்வாய்: {g_dosh['sevvai']}", f"செவ்வாய்: {b_dosh['sevvai']}", s_outcome))

        rk_outcome = "இருவருக்கும் ராகு/கேது களத்திர தோஷம் உள்ளதால் தோஷ சாம்யம் ஏற்பட்டு தோஷம் விலகும்." if (g_dosh["kalathra"] == "உண்டு" and b_dosh["kalathra"] == "உண்டு") else (
                     "இருவருக்கும் களத்திர தோஷம் இல்லை; திருமண உறவு தீர்க்கமாக இருக்கும்." if (g_dosh["kalathra"] == "இல்லை" and b_dosh["kalathra"] == "இல்லை") else
                     "ஒருவருக்கு மட்டும் ராகு/கேது களத்திர தோஷம் உள்ளது; சாந்தி பரிகாரங்களால் நிவர்த்தி செய்யவும்.")
        self.synergy_tree.insert("", tk.END, values=("தோஷ சாம்யம்", "ராகு-கேது களத்திர தோஷம்", f"களத்திரம்: {g_dosh['kalathra']}", f"களத்திரம்: {b_dosh['kalathra']}", rk_outcome))

        r_diff = (b_data["rasi_idx"] - g_data["rasi_idx"]) % 12 + 1
        g_lord = TamilAstroConstants.RASI_LORDS[g_data["rasi_idx"]]
        b_lord = TamilAstroConstants.RASI_LORDS[b_data["rasi_idx"]]
        if r_diff in [6, 8]:
            sh_outcome = f"6/8-ஆம் ராசியானாலும் இரு ராசிகளின் அதிபதியும் ({g_lord}) ஒன்றானதால் சஷ்டாஷ்டம தோஷமில்லை." if g_lord == b_lord else "6/8-ஆம் சஷ்டாஷ்டம தோஷம் உள்ளது; பரிகாரம் அவசியம்."
        else:
            sh_outcome = "சஷ்டாஷ்டம தோஷம் இல்லை; ராசிப் பொருத்தம் உத்தமம்."
        self.synergy_tree.insert("", tk.END, values=("ராசி சாம்யம்", "சஷ்டாஷ்டம தோஷ ஆய்வு", g_data["rasi_name"], b_data["rasi_name"], sh_outcome))

        d_outcome = "இருவருக்கும் ஒரே தசா நடப்பதால் தசா சந்தி தோஷம் உள்ளது (-25%)." if g_data["active_dasa"] == b_data["active_dasa"] else "இருவருக்கும் வெவ்வேறான தசா நடப்பதால் தசா சந்தி தோஷமில்லை (✔ உத்தமம்)."
        self.synergy_tree.insert("", tk.END, values=("தசா சாம்யம்", "தசா சந்தி தோஷ ஆய்வு", f"தசா: {g_data['active_dasa']}", f"தசா: {b_data['active_dasa']}", d_outcome))

        f_outcome = "இருவரின் 2-ஆம் அதிபதிகளும் பலமுற்றதால் திருமணத்திற்குப் பின் குடும்ப தன விருத்தி ஏற்படும்."
        self.synergy_tree.insert("", tk.END, values=("பாவ சாம்யம்", "2-ஆம் பாவம் (குடும்ப தனம்)", "2-ஆம் பாவம் பலம்", "2-ஆம் பாவம் பலம்", f_outcome))

        p_outcome = "இருவரின் 5-ஆம் அதிபதிகளும் சுப பலமுற்றதால் புத்திர சந்தான பாக்கியங்கள் சீரமாக ஏற்படும்."
        self.synergy_tree.insert("", tk.END, values=("பாவ சாம்யம்", "5-ஆம் பாவம் (புத்திர பாக்கியம்)", "5-ஆம் பாவம் பலம்", "5-ஆம் பாவம் பலம்", p_outcome))

        lines = []
        lines.append("★ மணமக்கள் திருமண சாம்ய மற்றும் யோக பலன்கள் (Joint Synergy Analysis) ★\n")
        if g_dosh["sevvai"] == b_dosh["sevvai"] and g_dosh["kalathra"] == b_dosh["kalathra"]:
            lines.append("1. தோஷ சாம்யம்: இருவருக்கும் செவ்வாய் மற்றும் களத்திர தோஷங்கள் சமமாக உள்ளதால், ஒருவரின் தோஷம் மற்றவரின் தோஷத்தை முழுமையாக ரத்து செய்து விடுகிறது (தோஷ சாம்யம்). இதனால் திருமண உறவு மிகவும் பலப்படும்.\n")
        else:
            lines.append("1. தோஷ சாம்யம்: தோஷங்களில் சிறிய அளவில் சமச்சீரற்ற நிலை உள்ளதால், திருமணத்திற்கு முன் தகுந்த சாந்தி பரிகாரங்களைச் செய்து கொள்வது குடும்ப அமைதியைத் தரும்.\n")
            
        lines.append("2. இருபரிமாண குடும்ப யோகம் (Multiplier Effects): பெண்ணின் 2-ஆம் அதிபதியும், ஆணின் 2-ஆம் அதிபதியும் இணையும் போது குடும்பத்தில் தன (பொருளாதார) வரவு இரட்டிப்பாகும். அதேபோல் இருவரின் 5-ஆம் பாவ பலங்களும் சேர்வதால், சிறப்பான நன்மக்கட்பேறு மற்றும் பூர்வ புண்ணிய பலன்கள் தடையின்றி கிடைக்கும்.\n")
        lines.append("3. மன ஒற்றுமை மற்றும் ரஜ்ஜு பலம்: ராசி மற்றும் ரஜ்ஜு பொருத்தம் சாதகமாக அமைந்தால், இருவருக்கும் இடையே சிறந்த மனப் பொருத்தமும், தீர்க்கமான மாங்கல்ய பலமும் நிலவும். இருவரின் ஜாதகங்களும் ஒன்று சேரும்போது கஷ்டங்கள் பாதியாகக் குறைந்து, நன்மைகள் பன்மடங்கு பெருகும்.")

        self.synergy_text.config(state="normal")
        self.synergy_text.delete("1.0", tk.END)
        self.synergy_text.insert(tk.END, "".join(lines))
        self.synergy_text.config(state="disabled")


# =====================================================================
# 10. UPGRADED ADVANCE DETAILS TABS (ELEMENTS & YONI ANIMALS)
# =====================================================================
class ElementsAdvanceTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#EAE0C8", **kwargs)
        self._build_ui()

    def _build_ui(self):
        hdr_frame = tk.Frame(self, bg="#3E2723", pady=10, bd=3, relief="raised"); hdr_frame.pack(fill="x")
        tk.Label(hdr_frame, text="பஞ்சபூத தத்துவங்கள் — 12 ராசி தத்துவ பொருத்தம்", font=("Helvetica", 14, "bold"), fg="#F1E3A0", bg="#3E2723").pack()

        tree_frame = tk.Frame(self, bg="white"); tree_frame.pack(fill="both", expand=True, padx=15, pady=10)
        columns = ("Rasi", "Element", "BestCombo", "WorstCombo", "NeutralCombo")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=22)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#C8B7A6", foreground="#2C1A14", relief="raised")
        style.configure("Treeview", font=("Helvetica", 11), rowheight=28, background="#FDF8E7", fieldbackground="#FDF8E7", foreground="#2C1A14")

        self.tree.heading("Rasi", text="ராசி"); self.tree.heading("Element", text="பஞ்சபூத தத்துவம்")
        self.tree.heading("BestCombo", text="சிறந்த தத்துவ பொருத்தம்"); self.tree.heading("WorstCombo", text="தவிர்க்க வேண்டியவை")
        self.tree.heading("NeutralCombo", text="மத்திம தத்துவங்கள்")
        for col, w in zip(columns, [180, 180, 250, 250, 250]): self.tree.column(col, width=w, anchor=tk.CENTER)

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vscroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        for rasi_idx, rasi_name in enumerate(TamilAstroConstants.RASIS):
            elem, best, worst, neutral = TamilAstroConstants.RASI_ELEMENTS[rasi_idx]
            self.tree.insert("", tk.END, values=(rasi_name, elem, best, worst, neutral))


class AnimalsYoniAdvanceTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#EAE0C8", **kwargs)
        self._build_ui()

    def _build_ui(self):
        hdr_frame = tk.Frame(self, bg="#3E2723", pady=10, bd=3, relief="raised"); hdr_frame.pack(fill="x")
        tk.Label(hdr_frame, text="யோனி மிருகங்கள் — Srirangaminfo Parity (நட்பு மற்றும் இயற்கை ஜோடி)", font=("Helvetica", 14, "bold"), fg="#F1E3A0", bg="#3E2723").pack()

        tree_frame = tk.Frame(self, bg="white"); tree_frame.pack(fill="both", expand=True, padx=15, pady=10)
        columns = ("StarName", "YoniAnimal", "EnemyAnimal", "FriendlyAnimals", "BestPairs", "NaturalPairs")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=22)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#C8B7A6", foreground="#2C1A14", relief="raised")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=27, background="#FDF8E7", fieldbackground="#FDF8E7", foreground="#2C1A14")

        self.tree.heading("StarName", text="நட்சத்திரம்"); self.tree.heading("YoniAnimal", text="யோனி மிருகம்")
        self.tree.heading("EnemyAnimal", text="பகை மிருகம்"); self.tree.heading("FriendlyAnimals", text="நட்பு மிருகங்கள்")
        self.tree.heading("BestPairs", text="சிறந்த நட்சத்திர பொருத்தங்கள்"); self.tree.heading("NaturalPairs", text="இயற்கை ஜோடி")
        for col, w in zip(columns, [160, 150, 150, 200, 280, 200]): self.tree.column(col, width=w, anchor=tk.W if col in ["StarName", "BestPairs"] else tk.CENTER)

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vscroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        for star_idx, star_name in enumerate(TamilAstroConstants.NAKSHATRAS):
            yoni = TamilAstroConstants.YONI_ANIMALS[star_idx]
            enemy = next((p[1] for p in TamilAstroConstants.YONI_ENEMIES if p[0] == yoni), next((p[0] for p in TamilAstroConstants.YONI_ENEMIES if p[1] == yoni), "ஏதுமில்லை"))
            friendly = TamilAstroConstants.YONI_FRIENDLY_MAP.get(yoni, "நட்பு மிருகங்கள்")
            compatible_stars = [TamilAstroConstants.NAKSHATRAS[i] for i, ani in TamilAstroConstants.YONI_ANIMALS.items() if i != star_idx and ani != enemy and (ani == yoni or ani.split(" ")[0] in friendly)][:5]
            natural_pair = [TamilAstroConstants.NAKSHATRAS[i] for i, ani in TamilAstroConstants.YONI_ANIMALS.items() if ani == yoni and i != star_idx]
            nat_str = " / ".join(natural_pair) if natural_pair else "சுய யோனி ஜோடி"
            self.tree.insert("", tk.END, values=(star_name, yoni, enemy, friendly, ", ".join(compatible_stars), nat_str))


# =====================================================================
# 11. SUB-TABS FOR TAB 2 (REFERENCE TABLES)
# =====================================================================
class StarReferenceTableTab(tk.Frame):
    def __init__(self, parent, boy_title: str, boy_nak_idx: int, boy_rasi_idx: int, **kwargs):
        super().__init__(parent, bg="#EAE0C8", **kwargs)
        self.boy_title = boy_title; self.boy_nak_idx = boy_nak_idx; self.boy_rasi_idx = boy_rasi_idx
        self._build_table()

    def _build_table(self):
        tree_frame = tk.Frame(self, bg="white"); tree_frame.pack(fill="both", expand=True, padx=15, pady=10)
        columns = ("StarName", "RasiName", "MatchedRules", "UnmatchedRules", "TotalScore", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=23)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#C8B7A6", foreground="#2C1A14", relief="raised")
        style.configure("Treeview", font=("Helvetica", 11), rowheight=26, background="#FDF8E7", fieldbackground="#FDF8E7", foreground="#2C1A14")

        self.tree.heading("StarName", text="பெண் நட்சத்திரம்"); self.tree.heading("RasiName", text="ராசி")
        self.tree.heading("MatchedRules", text="பொருந்திய விதிகள்"); self.tree.heading("UnmatchedRules", text="பொருந்தாத விதிகள்")
        self.tree.heading("TotalScore", text="மதிப்பெண்"); self.tree.heading("Status", text="பரிந்துரை")
        for col, w in zip(columns, [190, 130, 340, 170, 140, 180]): self.tree.column(col, width=w, anchor=tk.W if col == "MatchedRules" else tk.CENTER)

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vscroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vscroll.pack(side=tk.RIGHT, fill=tk.Y)

        for star_label, g_nak_idx, g_rasi_idx in TamilAstroConstants.ALL_STAR_RASI_VARIANTS:
            g_rasi_name = TamilAstroConstants.RASIS[g_rasi_idx]
            matched, unmatched, score, _ = DynamicTwelvePointEngine.evaluate_nakshatra_11_points(g_nak_idx, g_rasi_idx, self.boy_nak_idx, self.boy_rasi_idx)
            status = "✔ உத்தமம்" if (score >= 8 and 9 in matched) else ("-- மத்திமம்" if (score >= 6 and 9 in matched) else "✖ தவிர்க்க")
            self.tree.insert("", tk.END, values=(star_label, g_rasi_name, ", ".join(str(n) for n in matched), ", ".join(str(n) for n in unmatched) if unmatched else "இல்லை", f"{score} / 11", status))


class CombinedBestPairsTab(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#EAE0C8", **kwargs)
        self.filter_var = tk.StringVar(value="best_only")
        self._build_ui()

    def _build_ui(self):
        filter_bar = tk.Frame(self, bg="#C8B7A6", bd=3, relief="raised", pady=6); filter_bar.pack(fill="x", padx=15, pady=6)
        tk.Label(filter_bar, text="பார்வை வடிவம்:", font=("Helvetica", 11, "bold"), fg="#2C1A14", bg="#C8B7A6").pack(side="left", padx=10)
        tk.Radiobutton(filter_bar, text="⭐ சிறந்த பொருத்தங்கள் மட்டும்", variable=self.filter_var, value="best_only", font=("Helvetica", 10, "bold"), bg="#C8B7A6", fg="#2C1A14", command=self.populate_data).pack(side="left", padx=8)
        tk.Radiobutton(filter_bar, text="எல்லா 36 நட்சத்திரங்கள்", variable=self.filter_var, value="all", font=("Helvetica", 10, "bold"), bg="#C8B7A6", fg="#2C1A14", command=self.populate_data).pack(side="left", padx=8)

        tree_frame = tk.Frame(self, bg="white"); tree_frame.pack(fill="both", expand=True, padx=15, pady=6)
        columns = ("StarName", "RasiName", "SwathiScore", "SwathiStatus", "VisagamScore", "VisagamStatus", "CombinedRating")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=23)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"), background="#C8B7A6", foreground="#2C1A14", relief="raised")
        style.configure("Treeview", font=("Helvetica", 10), rowheight=26, background="#FDF8E7", fieldbackground="#FDF8E7", foreground="#2C1A14")

        self.tree.heading("StarName", text="பெண் நட்சத்திரம்"); self.tree.heading("RasiName", text="ராசி")
        self.tree.heading("SwathiScore", text="சுவாதி 4"); self.tree.heading("SwathiStatus", text="சுவாதி 4 நிலை")
        self.tree.heading("VisagamScore", text="விசாகம் 1"); self.tree.heading("VisagamStatus", text="விசாகம் 1 நிலை")
        self.tree.heading("CombinedRating", text="இணைந்த தகுதி")
        for col, w in zip(columns, [180, 130, 130, 170, 130, 170, 240]): self.tree.column(col, width=w, anchor=tk.W if col == "StarName" else tk.CENTER)

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vscroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); vscroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.populate_data()

    def populate_data(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        filter_mode = self.filter_var.get()
        for star_label, g_nak_idx, g_rasi_idx in TamilAstroConstants.ALL_STAR_RASI_VARIANTS:
            g_rasi_name = TamilAstroConstants.RASIS[g_rasi_idx]
            s_matched, _, s_score, _ = DynamicTwelvePointEngine.evaluate_nakshatra_11_points(g_nak_idx, g_rasi_idx, 14, 6)
            v_matched, _, v_score, _ = DynamicTwelvePointEngine.evaluate_nakshatra_11_points(g_nak_idx, g_rasi_idx, 15, 6)

            s_exc = (s_score >= 8 and 9 in s_matched); s_pass = (s_score >= 6 and 9 in s_matched)
            v_exc = (v_score >= 8 and 9 in v_matched); v_pass = (v_score >= 6 and 9 in v_matched)

            if s_exc and v_exc: rating = "⭐⭐⭐ இருவருக்கும் உத்தமம்"; is_best = True
            elif s_exc and v_pass: rating = "⭐⭐ சுவாதி-உத்தமம் / விசாகம்-மத்திமம்"; is_best = True
            elif v_exc and s_pass: rating = "⭐⭐ விசாகம்-உத்தமம் / சுவாதி-மத்திமம்"; is_best = True
            elif s_pass and v_pass: rating = "⭐ இருவருக்கும் மத்திமம்"; is_best = True
            else: rating = "✖ தவிர்க்க"; is_best = False

            if filter_mode == "best_only" and not is_best: continue
            self.tree.insert("", tk.END, values=(star_label, g_rasi_name, f"{s_score} / 11", "✔ உத்தமம்" if s_exc else ("-- மத்திமம்" if s_pass else "✖ தவிர்க்க"), f"{v_score} / 11", "✔ உத்தமம்" if v_exc else ("-- மத்திமம்" if v_pass else "✖ தவிர்க்க"), rating))


# =====================================================================
# 12. GUI DASHBOARD, CHARTS & TIMELINE WINDOW
# =====================================================================
class HoroscopeTimelineWindow(tk.Toplevel):
    def __init__(self, parent, timeline_data, person_name="ஜாதகர்"):
        super().__init__(parent)
        self.title(f"{person_name} — விம்சோத்தரி தசா புத்தி அட்டவணை")
        self.geometry("760x560")
        self.configure(bg="#f2f4f4")

        tk.Label(self, text=f"விம்சோத்தரி தசா புத்தி கால அட்டவணை — {person_name}", font=("Helvetica", 14, "bold"), bg="#f2f4f4", fg="#001f3f", pady=12).pack(fill=tk.X)
        frame = tk.Frame(self, bg="#f2f4f4"); frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = ("திசை", "புத்தி", "தொடக்கம்", "முடிவு")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=20)
        for col in columns: self.tree.heading(col, text=col); self.tree.column(col, width=160, anchor=tk.CENTER)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True); scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for row in timeline_data:
            self.tree.insert("", tk.END, values=(row["dasa"], row["bhukti"], row["start"].strftime("%d-%m-%Y"), row["end"].strftime("%d-%m-%Y")))
        tk.Button(self, text="மூடு", font=("Helvetica", 11, "bold"), bg="#001f3f", fg="white", padx=15, pady=5, command=self.destroy).pack(pady=10)


class SouthIndianChartCanvas(tk.Canvas):
    RASI_CELLS = {
        11: (0, 0), 0: (1, 0), 1: (2, 0), 2: (3, 0),
        10: (0, 1),                     3: (3, 1),
        9: (0, 2),                      4: (3, 2),
        8: (0, 3), 7: (1, 3), 6: (2, 3), 5: (3, 3)
    }

    BHAVA_TAGS = {
        1: "1-லக்னம்", 2: "2-குடும்பம்", 3: "3-தைரியம்", 4: "4-சுகம்",
        5: "5-புத்திரன்", 6: "6-சத்ரு", 7: "7-களத்திரம்", 8: "8-ஆயுள்",
        9: "9-பாக்கியம்", 10: "10-தொழில்", 11: "11-லாபம்", 12: "12-விரயம்"
    }

    def __init__(self, parent, width=360, height=360, **kwargs):
        super().__init__(parent, width=width, height=height, bg="white", highlightthickness=1, highlightbackground="black", **kwargs)
        self.w = width; self.h = height
        self.cw = width / 4.0; self.ch = height / 4.0
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.w = event.width; self.h = event.height
        self.cw = self.w / 4.0; self.ch = self.h / 4.0

    def draw_chart(self, grid_data: Dict[int, List[str]], center_title: str, lagna_idx: int = 0, font_size: int = 11):
        self.delete("all")
        for i in range(1, 4):
            self.create_line(i * self.cw, 0, i * self.cw, self.h, fill="black", width=1)
            self.create_line(0, i * self.ch, self.w, i * self.ch, fill="black", width=1)
        self.create_rectangle(self.cw, self.ch, 3 * self.cw, 3 * self.ch, fill="#FFF8DC", outline="black")
        
        self.create_text(self.w / 2, self.h / 2, text=center_title, font=("Helvetica", font_size + 1, "bold"), justify="center", fill="#8B0000")

        for rasi_idx, cell in self.RASI_CELLS.items():
            cx = cell[0] * self.cw; cy = cell[1] * self.ch
            house_num = ((rasi_idx - lagna_idx) % 12) + 1
            bhava_lbl = self.BHAVA_TAGS.get(house_num, "")
            self.create_text(cx + 6, cy + 6, text=bhava_lbl, font=("Helvetica", max(8, font_size - 3)), fill="#566573", anchor="nw")
            
            lord_lbl = f"({TamilAstroConstants.RASI_LORDS[rasi_idx]})"
            self.create_text(cx + self.cw / 2, cy + self.ch - 10, text=lord_lbl, font=("Helvetica", max(8, font_size - 2), "italic"), fill="#1b4f72")

            tags = grid_data.get(rasi_idx, [])
            y_off = cy + 22
            for tag in tags:
                color = "#8B0000" if "(வ)" in tag or "செ" in tag or "சனி" in tag or "மா" in tag else "black"
                self.create_text(cx + self.cw / 2, y_off, text=tag, font=("Helvetica", font_size, "bold"), fill=color)
                y_off += (font_size + 6)


class BlueBorderedPanchangamTable(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#001f3f", bd=2, relief="solid", **kwargs)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0, height=300)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.inner = tk.Frame(self.canvas, bg="white")
        self.window_id = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))
        self.inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.vscroll.pack(side="right", fill="y"); self.canvas.pack(side="left", fill="both", expand=True)

    def populate(self, rows: List[Tuple[str, str]], font_size: int = 11):
        for widget in self.inner.winfo_children(): widget.destroy()
        for idx, (label, val) in enumerate(rows):
            bg_color = "#f0f4f8" if idx % 2 == 0 else "white"
            row_frame = tk.Frame(self.inner, bg=bg_color); row_frame.pack(fill="x")
            tk.Label(row_frame, text=label, font=("Helvetica", font_size, "bold"), fg="#001f3f", bg=bg_color, width=16, anchor="w").pack(side="left", padx=6, pady=3)
            tk.Label(row_frame, text=val, font=("Helvetica", font_size, "bold"), fg="#000000", bg=bg_color, anchor="w").pack(side="left", fill="x", expand=True, padx=6, pady=3)


class SamutrikaLakshanamPanel(ttk.LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, text="ஷாமுத்ரிகா லக்ஷணம் (Samudrika Lakshanam)", padding=8, **kwargs)
        self.inner = tk.Frame(self, bg="#FFFFFF")
        self.inner.pack(fill="both", expand=True)

    def update_panel(self, g_data: Dict[str, Any], b_data: Dict[str, Any]):
        for widget in self.inner.winfo_children(): widget.destroy()

        hdr1 = tk.Frame(self.inner, bg="#fcf3cf", bd=1, relief="solid"); hdr1.pack(fill="x", pady=(0, 3))
        tk.Label(hdr1, text="ஷாமுத்ரிகா லக்ஷணம் குறி", font=("Helvetica", 11, "bold"), fg="#7d6608", bg="#fcf3cf").pack(pady=3)

        stack1 = tk.Frame(self.inner, bg="#FFFFFF"); stack1.pack(fill="x", pady=3)
        left_card1 = tk.Frame(stack1, bg="#FFFFFF", bd=1, relief="groove", padx=8, pady=4)
        left_card1.pack(side="left", fill="both", expand=True, padx=(0, 4))
        tk.Label(left_card1, text="பெண் (Bride):", font=("Helvetica", 11, "bold"), fg="#000000", bg="#FFFFFF", anchor="w").pack(anchor="w")
        tk.Label(left_card1, text=g_data["samutrika_kuri"], font=("Helvetica", 11, "bold"), fg="#8B0000", bg="#FFFFFF", anchor="w").pack(anchor="w", pady=1)

        right_card1 = tk.Frame(stack1, bg="#FFFFFF", bd=1, relief="groove", padx=8, pady=4)
        right_card1.pack(side="right", fill="both", expand=True, padx=(4, 0))
        tk.Label(right_card1, text="ஆண் (Groom):", font=("Helvetica", 11, "bold"), fg="#000000", bg="#FFFFFF", anchor="w").pack(anchor="w")
        tk.Label(right_card1, text=b_data["samutrika_kuri"], font=("Helvetica", 11, "bold"), fg="#1b4f72", bg="#FFFFFF", anchor="w").pack(anchor="w", pady=1)

        hdr2 = tk.Frame(self.inner, bg="#fcf3cf", bd=1, relief="solid"); hdr2.pack(fill="x", pady=(6, 3))
        tk.Label(hdr2, text="ஷாமுத்ரிகா லக்ஷணம் நிறம்", font=("Helvetica", 11, "bold"), fg="#7d6608", bg="#fcf3cf").pack(pady=3)

        stack2 = tk.Frame(self.inner, bg="#FFFFFF"); stack2.pack(fill="x", pady=3)
        left_card2 = tk.Frame(stack2, bg="#FFFFFF", bd=1, relief="groove", padx=8, pady=4)
        left_card2.pack(side="left", fill="both", expand=True, padx=(0, 4))
        tk.Label(left_card2, text=f"பெண்: {g_data['samutrika_color']}", font=("Helvetica", 11, "bold"), fg="#000000", bg="#FFFFFF", anchor="w").pack(anchor="w", pady=(0, 3))
        tk.Canvas(left_card2, width=150, height=22, bg=g_data["samutrika_swatch"], bd=1, relief="solid").pack(anchor="w")

        right_card2 = tk.Frame(stack2, bg="#FFFFFF", bd=1, relief="groove", padx=8, pady=4)
        right_card2.pack(side="right", fill="both", expand=True, padx=(4, 0))
        tk.Label(right_card2, text=f"ஆண்: {b_data['samutrika_color']}", font=("Helvetica", 11, "bold"), fg="#000000", bg="#FFFFFF", anchor="w").pack(anchor="w", pady=(0, 3))
        tk.Canvas(right_card2, width=150, height=22, bg=b_data["samutrika_swatch"], bd=1, relief="solid").pack(anchor="w")

        hdr3 = tk.Frame(self.inner, bg="#fcf3cf", bd=1, relief="solid"); hdr3.pack(fill="x", pady=(6, 3))
        tk.Label(hdr3, text="தோஷ விவரங்கள்", font=("Helvetica", 11, "bold"), fg="#7d6608", bg="#fcf3cf").pack(pady=3)

        g_dosh = SamutrikaLakshanamEngine.check_doshams(g_data)
        b_dosh = SamutrikaLakshanamEngine.check_doshams(b_data)

        d_table = ttk.Treeview(self.inner, columns=("Dosham", "Bride", "Groom"), show="headings", height=3)
        d_table.heading("Dosham", text="தோஷம்"); d_table.heading("Bride", text="பெண்"); d_table.heading("Groom", text="ஆண்")
        d_table.column("Dosham", width=180, anchor=tk.W); d_table.column("Bride", width=100, anchor=tk.CENTER); d_table.column("Groom", width=100, anchor=tk.CENTER)
        d_table.pack(fill="x", padx=4, pady=3)

        d_table.insert("", tk.END, values=("செவ்வாய் & ராகு/கேது தோஷம்", f"செ:{g_dosh['sevvai']} | ரா:{g_dosh['rahu']}", f"செ:{b_dosh['sevvai']} | ரா:{b_dosh['rahu']}"))
        d_table.insert("", tk.END, values=("நாகதோஷம் & காலஷர்ப தோஷம்", f"நாக:{g_dosh['naga']} | சர்ப:{g_dosh['kalasarpa']}", f"நாக:{b_dosh['naga']} | சர்ப:{b_dosh['kalasarpa']}"))
        d_table.insert("", tk.END, values=("களத்திர தோஷம்", g_dosh["kalathra"], b_dosh["kalathra"]))


class ScrollableMatchTable(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bd=1, relief="solid", bg="#001f3f", **kwargs)
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.yscrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_inner = tk.Frame(self.canvas, bg="white")
        self.window_id = self.canvas.create_window((0, 0), window=self.scroll_inner, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=e.width))
        self.scroll_inner.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.yscrollbar.set)
        self.yscrollbar.pack(side="right", fill="y"); self.canvas.pack(side="left", fill="both", expand=True)

    def populate_rows(self, matrix: List[Tuple[str, str, str]], font_size: int = 12):
        for widget in self.scroll_inner.winfo_children(): widget.destroy()
        hdr = tk.Frame(self.scroll_inner, bg="#d0e1fd", bd=1, relief="solid"); hdr.pack(fill="x")
        tk.Label(hdr, text="பொருத்தம் விதி", width=25, font=("Helvetica", font_size, "bold"), fg="#001f3f", bg="#d0e1fd", anchor="w").pack(side="left", padx=6, pady=8)
        tk.Label(hdr, text="விளக்கம்", font=("Helvetica", font_size, "bold"), fg="#001f3f", bg="#d0e1fd", anchor="w").pack(side="left", fill="x", expand=True, padx=6, pady=8)
        tk.Label(hdr, text="முடிவு", width=8, font=("Helvetica", font_size, "bold"), fg="#001f3f", bg="#d0e1fd").pack(side="right", padx=6, pady=8)

        for title, stat_text, icon in matrix:
            bg_color = "#f9fbfd" if matrix.index((title, stat_text, icon)) % 2 == 0 else "white"
            row_frame = tk.Frame(self.scroll_inner, bg=bg_color, bd=1, relief="solid"); row_frame.pack(fill="x", pady=1)
            tk.Label(row_frame, text=title, width=25, font=("Helvetica", font_size + 1, "bold"), fg="#000000", bg=bg_color, anchor="nw").pack(side="left", padx=6, pady=10)
            icon_color = "#8B0000" if "✖" in icon else ("#0a4b33" if "✔" in icon else "#7f6000")
            tk.Label(row_frame, text=icon, width=8, font=("Helvetica", font_size + 3, "bold"), fg=icon_color, bg=bg_color).pack(side="right", padx=6, pady=10)
            
            expl_lbl = tk.Label(row_frame, text=stat_text, font=("Helvetica", font_size, "bold"), fg="#000000", bg=bg_color, anchor="nw", justify="left")
            expl_lbl.pack(side="left", fill="both", expand=True, padx=6, pady=10)
            expl_lbl.bind("<Configure>", lambda e, lbl=expl_lbl: lbl.config(wraplength=e.width - 10))


class MasterScrollableDashboard(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg="#f2f4f4", highlightthickness=0)
        self.vscroll = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.hscroll = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.viewport = tk.Frame(self.canvas, bg="#f2f4f4")
        self.window_id = self.canvas.create_window((0, 0), window=self.viewport, anchor="nw")
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.window_id, width=max(1300, e.width)))
        self.viewport.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.configure(yscrollcommand=self.vscroll.set, xscrollcommand=self.hscroll.set)
        self.vscroll.pack(side="right", fill="y"); self.hscroll.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)


# =====================================================================
# 13. MAIN APPLICATION DASHBOARD (STK'S ASTRO — ASTROV3)
# =====================================================================
class UltimateDSVPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("STK's Astro — Professional Tamil Marriage Matchmaker (V3) | Owner: Thirukumaran S")
        self.geometry("1600x980")
        self.minsize(1200, 800)
        self.configure(bg="#2D1C15")

        style = ttk.Style(self)
        style.theme_use("classic")
        style.configure("TButton", font=("Helvetica", 11, "bold"), padding=6, background="#D7CCC8", relief="raised", borderwidth=3)
        style.configure("TNotebook", background="#2D1C15")
        style.configure("TNotebook.Tab", font=("Helvetica", 12, "bold"), padding=[14, 6], background="#C8B7A6", foreground="#2C1A14", relief="raised", borderwidth=3)

        self.zoom_level = 1.0
        self.calc_mode = tk.StringVar(value="current")
        self.ayanamsa_mode = tk.StringVar(value="Lahiri")
        self.girl_timeline_data = []; self.boy_timeline_data = []
        self.latest_report_data = None

        self._build_global_header()
        self._build_notebook_ui()
        bind_universal_mousewheel(self)

    def _build_global_header(self):
        top_bar = tk.Frame(self, bg="#3E2723", pady=6, relief="raised", bd=4)
        top_bar.pack(fill="x", side="top")
        tk.Label(top_bar, text="STK's Astro (AstroV3)", font=("Helvetica", 14, "bold"), fg="#F1E3A0", bg="#3E2723").pack(side="left", padx=15)
        
        zoom_box = tk.Frame(top_bar, bg="#3E2723")
        zoom_box.pack(side="right", padx=15)
        tk.Label(zoom_box, text="Zoom:", font=("Helvetica", 11, "bold"), fg="#F1E3A0", bg="#3E2723").pack(side="left", padx=4)
        tk.Button(zoom_box, text="-", font=("Helvetica", 11, "bold"), width=2, bg="#D7CCC8", relief="raised", bd=3, command=lambda: self.change_zoom(-0.1)).pack(side="left", padx=2)
        self.zoom_lbl = tk.Label(zoom_box, text="100%", font=("Helvetica", 11, "bold"), fg="#FFFFFF", bg="#3E2723", width=5)
        self.zoom_lbl.pack(side="left")
        tk.Button(zoom_box, text="+", font=("Helvetica", 11, "bold"), width=2, bg="#D7CCC8", relief="raised", bd=3, command=lambda: self.change_zoom(0.1)).pack(side="left", padx=2)

    def on_city_select_g(self, selected_city: str):
        coords = CITY_COORDINATES.get(selected_city, (11.0168, 76.9558))
        self.g_lat.delete(0, tk.END); self.g_lat.insert(0, str(coords[0]))
        self.g_lon.delete(0, tk.END); self.g_lon.insert(0, str(coords[1]))

    def on_city_select_b(self, selected_city: str):
        coords = CITY_COORDINATES.get(selected_city, (11.1085, 77.3411))
        self.b_lat.delete(0, tk.END); self.b_lat.insert(0, str(coords[0]))
        self.b_lon.delete(0, tk.END); self.b_lon.insert(0, str(coords[1]))

    def _build_notebook_ui(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        self.tab_dashboard_master = tk.Frame(self.notebook, bg="#EAE0C8")
        self.notebook.add(self.tab_dashboard_master, text=" 1. திருமண பொருத்தம் & ஜாதக ஆய்வு ")
        self.sub_nb_dash = ttk.Notebook(self.tab_dashboard_master)
        self.sub_nb_dash.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_dashboard_engine = tk.Frame(self.sub_nb_dash, bg="#EAE0C8")
        self.sub_nb_dash.add(self.tab_dashboard_engine, text=" 1.1 மணமக்கள் பொருத்தம் & ஷாமுத்ரிகா லக்ஷணம் ")

        self.tab_kudumpa_book = KudumpaJothidamBookReferenceTab(self.sub_nb_dash)
        self.sub_nb_dash.add(self.tab_kudumpa_book, text=" 1.2 குடும்ப ஜோதிடம் - சாஸ்திர விதிகள் ")

        self.tab_kudumpa_pred = KudumpaJothidamPredictionTab(self.sub_nb_dash)
        self.sub_nb_dash.add(self.tab_kudumpa_pred, text=" 1.3 முழுமையான ஜாதகப் பலன்கள் & திருமண சாம்ய ஆய்வு ")

        self.tab_ref_master = tk.Frame(self.notebook, bg="#EAE0C8")
        self.notebook.add(self.tab_ref_master, text=" 2. நட்சத்திர & ராசி பொருத்தம் அட்டவணைகள் ")
        self.sub_nb_ref = ttk.Notebook(self.tab_ref_master)
        self.sub_nb_ref.pack(fill="both", expand=True, padx=10, pady=10)

        self.sub_swati = StarReferenceTableTab(self.sub_nb_ref, "சுவாதி 4 (துலாம்)", 14, 6)
        self.sub_nb_ref.add(self.sub_swati, text=" சுவாதி 4 — 36 நட்சத்திர அட்டவணை ")
        self.sub_visagam = StarReferenceTableTab(self.sub_nb_ref, "விசாகம் 1 (துலாம்)", 15, 6)
        self.sub_nb_ref.add(self.sub_visagam, text=" விசாகம் 1 — 36 நட்சத்திர அட்டவணை ")
        self.sub_combined = CombinedBestPairsTab(self.sub_nb_ref)
        self.sub_nb_ref.add(self.sub_combined, text=" சுவாதி 4 & விசாகம் 1 சிறந்த பொருத்தம் ")

        self.tab_advance_master = tk.Frame(self.notebook, bg="#EAE0C8")
        self.notebook.add(self.tab_advance_master, text=" 3. மேம்பட்ட ஜோதிட விவரங்கள் ")
        self.sub_nb_adv = ttk.Notebook(self.tab_advance_master)
        self.sub_nb_adv.pack(fill="both", expand=True, padx=10, pady=10)

        self.sub_elem = ElementsAdvanceTab(self.sub_nb_adv)
        self.sub_nb_adv.add(self.sub_elem, text=" பஞ்சபூத தத்துவங்கள் ")
        self.sub_yoni = AnimalsYoniAdvanceTab(self.sub_nb_adv)
        self.sub_nb_adv.add(self.sub_yoni, text=" யோனி மிருகங்கள் & பொருத்தம் ")

        self._build_tab1_content()

    def _build_tab1_content(self):
        hdr = tk.Frame(self.tab_dashboard_engine, bg="#D7CCC8", bd=4, relief="ridge")
        hdr.pack(fill="x", padx=12, pady=6)

        # --- BRIDE FORM (EMPTY) ---
        r0 = tk.Frame(hdr, bg="#D7CCC8"); r0.pack(fill="x", pady=4)
        tk.Label(r0, text="Bride (பெண்):", font=("Helvetica", 13, "bold"), fg="#2C1A14", bg="#D7CCC8", width=12, anchor="w").pack(side="left", padx=6)
        self.g_name = ExecutiveEntry(r0, width=16); self.g_name.insert(0, ""); self.g_name.pack(side="left", padx=4, ipady=4)
        
        tk.Label(r0, text="DOB & Time:", font=("Helvetica", 11, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(10, 2))
        self.g_picker = ExecutiveFastDateTimePicker(r0, default_date="", default_time="", default_ampm="AM")
        self.g_picker.pack(side="left", padx=2)

        tk.Label(r0, text="Place:", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(15, 2))
        self.g_city = SmoothFilterCombobox(r0, completevalues=list(CITY_COORDINATES.keys()), on_select_callback=self.on_city_select_g, width=22, font=("Helvetica", 13, "bold")); self.g_city.set("Coimbatore (கோயம்புத்தூர்)"); self.g_city.pack(side="left", padx=4)
        tk.Label(r0, text="Lat:", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(10, 2))
        self.g_lat = ExecutiveEntry(r0, width=7); self.g_lat.insert(0, "11.0168"); self.g_lat.pack(side="left", padx=3, ipady=4)
        tk.Label(r0, text="Lon:", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(8, 2))
        self.g_lon = ExecutiveEntry(r0, width=7); self.g_lon.insert(0, "76.9558"); self.g_lon.pack(side="left", padx=3, ipady=4)

        # --- GROOM FORM ---
        r1 = tk.Frame(hdr, bg="#D7CCC8"); r1.pack(fill="x", pady=6)
        tk.Label(r1, text="Groom (ஆண்):", font=("Helvetica", 13, "bold"), fg="#2C1A14", bg="#D7CCC8", width=12, anchor="w").pack(side="left", padx=6)
        self.b_name = ExecutiveEntry(r1, width=16); self.b_name.insert(0, "Thirukumaran S"); self.b_name.pack(side="left", padx=4, ipady=4)
        
        tk.Label(r1, text="DOB & Time:", font=("Helvetica", 11, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(10, 2))
        self.b_picker = ExecutiveFastDateTimePicker(r1, default_date="17-05-2000", default_time="10:14", default_ampm="AM")
        self.b_picker.pack(side="left", padx=2)

        tk.Label(r1, text="Place:", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(15, 2))
        self.b_city = SmoothFilterCombobox(r1, completevalues=list(CITY_COORDINATES.keys()), on_select_callback=self.on_city_select_b, width=22, font=("Helvetica", 13, "bold")); self.b_city.set("Tiruppur (திருப்பூர்)"); self.b_city.pack(side="left", padx=4)
        tk.Label(r1, text="Lat:", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(10, 2))
        self.b_lat = ExecutiveEntry(r1, width=7); self.b_lat.insert(0, "11.1085"); self.b_lat.pack(side="left", padx=3, ipady=4)
        tk.Label(r1, text="Lon:", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#D7CCC8").pack(side="left", padx=(8, 2))
        self.b_lon = ExecutiveEntry(r1, width=7); self.b_lon.insert(0, "77.3411"); self.b_lon.pack(side="left", padx=3, ipady=4)

        # --- CONTROL TOOLBAR ---
        r2_container = tk.Frame(hdr, bg="#BCAAA4", bd=3, relief="sunken"); r2_container.pack(fill="x", pady=6, padx=6)
        ctrl_box = tk.Frame(r2_container, bg="#d4e6f1", bd=1, relief="ridge"); ctrl_box.pack(side="left", padx=8, pady=4)
        
        tk.Label(ctrl_box, text="அயனாம்சம்:", font=("Helvetica", 11, "bold"), bg="#d4e6f1", fg="#001f3f").pack(side="left", padx=4)
        self.ayanamsa_cb = ttk.Combobox(ctrl_box, textvariable=self.ayanamsa_mode, values=["Lahiri", "Thirukanitham", "Vedic True"], state="readonly", width=14, font=("Helvetica", 10, "bold"))
        self.ayanamsa_cb.pack(side="left", padx=4)

        tk.Label(ctrl_box, text=" | தசா:", font=("Helvetica", 11, "bold"), bg="#d4e6f1", fg="#001f3f").pack(side="left", padx=4)
        tk.Radiobutton(ctrl_box, text="Active", variable=self.calc_mode, value="current", font=("Helvetica", 10, "bold"), bg="#d4e6f1", fg="#8B0000", activebackground="#BCAAA4").pack(side="left", padx=2)
        tk.Radiobutton(ctrl_box, text="Birth", variable=self.calc_mode, value="classic", font=("Helvetica", 10, "bold"), bg="#d4e6f1", fg="#001f3f", activebackground="#BCAAA4").pack(side="left", padx=2)

        ttk.Button(r2_container, text="RUN EXACT REPORT", command=self.on_run_analysis).pack(side="left", padx=10, pady=6)
        ttk.Button(r2_container, text="💾 Save Profile", command=self.save_profile_json).pack(side="left", padx=4, pady=6)
        ttk.Button(r2_container, text="📂 Load Profile", command=self.load_profile_json).pack(side="left", padx=4, pady=6)
        self.btn_export = ttk.Button(r2_container, text="📄 Export Report", state="disabled", command=self.export_report_txt); self.btn_export.pack(side="left", padx=4, pady=6)

        self.btn_g_dasa = ttk.Button(r2_container, text="Bride Dasa", state="disabled", command=lambda: self.open_timeline_modal(self.girl_timeline_data, self.g_name.get())); self.btn_g_dasa.pack(side="left", padx=4, pady=6)
        self.btn_b_dasa = ttk.Button(r2_container, text="Groom Dasa", state="disabled", command=lambda: self.open_timeline_modal(self.boy_timeline_data, self.b_name.get())); self.btn_b_dasa.pack(side="left", padx=4, pady=6)

        # --- RESPONSIVE 3-COLUMN PANEDWINDOW ---
        self.master_scroll = MasterScrollableDashboard(self.tab_dashboard_engine)
        self.master_scroll.pack(fill="both", expand=True, padx=12, pady=6)
        
        self.paned_window = ttk.PanedWindow(self.master_scroll.viewport, orient="horizontal")
        self.paned_window.pack(fill="both", expand=True)

        left_col = tk.Frame(self.paned_window, bg="#EAE0C8"); self.paned_window.add(left_col, weight=1)
        self.g_header_lbl = tk.Label(left_col, text="பெண் ஜாதகம்", font=("Helvetica", 14, "bold"), fg="#2C1A14", bg="#EAE0C8"); self.g_header_lbl.pack(pady=4)
        self.g_chart = SouthIndianChartCanvas(left_col, width=360, height=360); self.g_chart.pack(pady=4)
        self.g_table = BlueBorderedPanchangamTable(left_col); self.g_table.pack(fill="both", expand=True, pady=4)

        center_col = tk.Frame(self.paned_window, bg="#EAE0C8"); self.paned_window.add(center_col, weight=2)
        tk.Label(center_col, text="STK's Astro — திருமண பொருத்தம்", font=("Helvetica", 16, "bold"), fg="#2C1A14", bg="#EAE0C8").pack(pady=4)
        
        score_container = tk.Frame(center_col, bg="#EAE0C8")
        score_container.pack(pady=4)
        
        self.g_logo_lbl = tk.Label(score_container, text="", font=("Helvetica", 32), bg="#EAE0C8", fg="#8B0000")
        self.g_logo_lbl.pack(side="left", padx=15)
        self.score_lbl = tk.Label(score_container, text="கணக்கிடவும்", font=("Helvetica", 15, "bold"), bg="#FDF8E7", fg="#2C1A14", width=18, height=3, relief="ridge", bd=4)
        self.score_lbl.pack(side="left", padx=10)
        self.b_logo_lbl = tk.Label(score_container, text="", font=("Helvetica", 32), bg="#EAE0C8", fg="#1b4f72")
        self.b_logo_lbl.pack(side="left", padx=15)
        
        self.seventh_lbl = tk.Label(center_col, text="* 7-ஆம் இடத்தில் உள்ள கிரகங்களின் ஆய்வு கீழே காட்டப்படும்", font=("Helvetica", 11, "bold"), fg="#2C1A14", bg="#EAE0C8")
        self.seventh_lbl.pack(pady=2)
        self.diag_lbl = tk.Label(center_col, text="", font=("Helvetica", 12, "bold"), fg="#2C1A14", bg="#EAE0C8"); self.diag_lbl.pack(pady=3)

        self.v_paned = ttk.PanedWindow(center_col, orient="vertical")
        self.v_paned.pack(fill="both", expand=True, pady=4)

        top_pane = tk.Frame(self.v_paned, bg="#EAE0C8", bd=3, relief="raised")
        self.v_paned.add(top_pane, weight=1)
        self.match_table = ScrollableMatchTable(top_pane); self.match_table.pack(fill="both", expand=True)

        bottom_pane = tk.Frame(self.v_paned, bg="#EAE0C8", bd=3, relief="raised")
        self.v_paned.add(bottom_pane, weight=1)
        self.samutrika_panel = SamutrikaLakshanamPanel(bottom_pane)
        self.samutrika_panel.pack(fill="both", expand=True, pady=4)

        right_col = tk.Frame(self.paned_window, bg="#EAE0C8"); self.paned_window.add(right_col, weight=1)
        self.b_header_lbl = tk.Label(right_col, text="ஆண் ஜாதகம்", font=("Helvetica", 14, "bold"), fg="#2C1A14", bg="#EAE0C8"); self.b_header_lbl.pack(pady=4)
        self.b_chart = SouthIndianChartCanvas(right_col, width=360, height=360); self.b_chart.pack(pady=4)
        self.b_table = BlueBorderedPanchangamTable(right_col); self.b_table.pack(fill="both", expand=True, pady=4)

        footer_frame = tk.Frame(self.tab_dashboard_engine, bg="#3E2723", pady=6, bd=3, relief="raised")
        footer_frame.pack(side="bottom", fill="x")
        tk.Label(footer_frame, text="இனிய திருமண நல்வாழ்த்துக்கள்! — Happy Married Life! | Powered by STK's Astro (AstroV3)", font=("Helvetica", 12, "bold"), fg="#F1E3A0", bg="#3E2723").pack()

        self.g_chart.draw_chart({}, "பெண்ணின் தரவுகளை உள்ளிட்டு\n'RUN EXACT REPORT'\nஅழுத்தவும்", font_size=10)
        self.b_chart.draw_chart({}, "தரவுகளை உள்ளிட்டு\n'RUN EXACT REPORT'\nஅழுத்தவும்", font_size=10)

    def change_zoom(self, delta: float):
        self.zoom_level = max(0.8, min(1.8, round(self.zoom_level + delta, 2)))
        self.zoom_lbl.config(text=f"{int(self.zoom_level * 100)}%")
        
        z = self.zoom_level
        style = ttk.Style()
        style.configure("Treeview", font=("Helvetica", int(10 * z)), rowheight=int(26 * z))
        style.configure("Treeview.Heading", font=("Helvetica", int(11 * z), "bold"))
        
        if self.latest_report_data: self.on_run_analysis()

    def save_profile_json(self):
        g_dob, g_tob_24h, _ = self.g_picker.get_datetime_values()
        b_dob, b_tob_24h, _ = self.b_picker.get_datetime_values()
        profile_data = {
            "version": "3.0", "brand": "STK's Astro (AstroV3)",
            "saved_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ayanamsa_mode": self.ayanamsa_mode.get(), "calc_mode": self.calc_mode.get(),
            "bride": {
                "name": self.g_name.get().strip(), "dob": g_dob, "tob_24h": g_tob_24h,
                "city": self.g_city.get().strip(), "lat": self.g_lat.get().strip(), "lon": self.g_lon.get().strip()
            },
            "groom": {
                "name": self.b_name.get().strip(), "dob": b_dob, "tob_24h": b_tob_24h,
                "city": self.b_city.get().strip(), "lat": self.b_lat.get().strip(), "lon": self.b_lon.get().strip()
            }
        }
        file_path = filedialog.asksaveasfilename(defaultextension=".json", initialfile="STKs_Astro_Profile.json", filetypes=[("JSON Files", "*.json")], title="Save Matchmaking Profile")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f: json.dump(profile_data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Profile Saved", f"Profile saved to:\n{file_path}")

    def load_profile_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")], title="Load Matchmaking Profile")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f: data = json.load(f)
            b = data.get("bride", {}); g = data.get("groom", {})
            self.g_name.delete(0, tk.END); self.g_name.insert(0, b.get("name", ""))
            if b.get("dob") and b.get("tob_24h"):
                dt_g = datetime.datetime.strptime(f"{b['dob']} {b['tob_24h']}", "%Y-%m-%d %H:%M")
                self.g_picker.set_datetime(dt_g)
            self.g_lat.delete(0, tk.END); self.g_lat.insert(0, b.get("lat", "11.0168"))
            self.g_lon.delete(0, tk.END); self.g_lon.insert(0, b.get("lon", "76.9558"))

            self.b_name.delete(0, tk.END); self.b_name.insert(0, g.get("name", "Thirukumaran S"))
            if g.get("dob") and g.get("tob_24h"):
                dt_b = datetime.datetime.strptime(f"{g['dob']} {g['tob_24h']}", "%Y-%m-%d %H:%M")
                self.b_picker.set_datetime(dt_b)
            self.b_lat.delete(0, tk.END); self.b_lat.insert(0, g.get("lat", "11.1085"))
            self.b_lon.delete(0, tk.END); self.b_lon.insert(0, g.get("lon", "77.3411"))
            self.on_run_analysis()

    def export_report_txt(self):
        if not self.latest_report_data: return
        g_data = self.latest_report_data["girl"]; b_data = self.latest_report_data["boy"]; match_res = self.latest_report_data["match_res"]
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=f"STKs_Astro_Report_{g_data['name']}_and_{b_data['name']}.txt", title="Export Match Report")
        if file_path:
            lines = [
                "=" * 80, "STK'S ASTRO (ASTROV3) — TAMIL MARRIAGE MATCH REPORT | OWNER: THIRUKUMARAN S", "=" * 80,
                f"Bride: {g_data['name']} ({g_data['nak_name']} {g_data['pada']}) | Yoni: {g_data['yoni_animal']} | Samutrika: {g_data['samutrika_kuri']}",
                f"Groom: {b_data['name']} ({b_data['nak_name']} {b_data['pada']}) | Yoni: {b_data['yoni_animal']} | Samutrika: {b_data['samutrika_kuri']}",
                "=" * 80, f"OVERALL RECOMMENDATION: {match_res['recommendation'].replace('*', '')}", "=" * 80
            ]
            for title, expl, icon in match_res["matrix"]: lines.append(f"[{icon}] {title:<30} | {expl.replace(chr(10), ' - ')}")
            with open(file_path, "w", encoding="utf-8") as f: f.write("\n".join(lines))
            messagebox.showinfo("Export Successful", f"Report exported to:\n{file_path}")

    def on_run_analysis(self):
        try:
            g_dob, g_tob_24h, _ = self.g_picker.get_datetime_values()
            b_dob, b_tob_24h, _ = self.b_picker.get_datetime_values()

            if not g_dob or not g_tob_24h:
                messagebox.showwarning("மணமகள் விவரங்கள் தேவை", "தயவுசெய்து பெண்ணின் பிறந்த தேதி மற்றும் நேரத்தை முழுமையாக உள்ளிடவும்.")
                return

            g_lat = float(self.g_lat.get().strip()); g_lon = float(self.g_lon.get().strip())
            b_lat = float(self.b_lat.get().strip()); b_lon = float(self.b_lon.get().strip())

            mode_str = self.ayanamsa_mode.get()
            ay_code = "thirukanitham" if "Thirukanitham" in mode_str else ("vedic_true" if "Vedic True" in mode_str else "lahiri")

            g_data = AdvancedVedicEngine.compute_horoscope(self.g_name.get() or "பெண்", "பெண்", g_dob, g_tob_24h, self.g_city.get(), g_lat, g_lon, 5.5, ay_code)
            b_data = AdvancedVedicEngine.compute_horoscope(self.b_name.get() or "ஆண்", "ஆண்", b_dob, b_tob_24h, self.b_city.get(), b_lat, b_lon, 5.5, ay_code)

            self.girl_timeline_data = g_data["full_timeline"]; self.boy_timeline_data = b_data["full_timeline"]
            self.btn_g_dasa.config(state="normal"); self.btn_b_dasa.config(state="normal")
            match_res = DynamicTwelvePointEngine.evaluate_match(g_data, b_data, self.calc_mode.get())

            self.latest_report_data = {"girl": g_data, "boy": b_data, "match_res": match_res}
            self.btn_export.config(state="normal")

            self.g_header_lbl.config(text=f"{g_data['name']} (பெண்)")
            self.b_header_lbl.config(text=f"{b_data['name']} (ஆண்)")
            
            g_title = f"{g_data['name']}\n{g_data['rasi_name']} — {g_data['nak_name']} {g_data['pada']}\n{g_data['dt'].strftime('%d-%b-%Y')}\n{g_data['dt'].strftime('%I:%M %p')} | {g_data['place']}"
            b_title = f"{b_data['name']}\n{b_data['rasi_name']} — {b_data['nak_name']} {b_data['pada']}\n{b_data['dt'].strftime('%d-%b-%Y')}\n{b_data['dt'].strftime('%I:%M %p')} | {b_data['place']}"
            
            z = self.zoom_level
            self.g_chart.draw_chart(g_data["rasi_grid"], g_title, lagna_idx=g_data["lagna_idx"], font_size=int(11*z))
            self.b_chart.draw_chart(b_data["rasi_grid"], b_title, lagna_idx=b_data["lagna_idx"], font_size=int(11*z))
            
            self.g_table.populate(g_data["table_rows"], font_size=int(11*z)); self.b_table.populate(b_data["table_rows"], font_size=int(11*z))
            self.samutrika_panel.update_panel(g_data, b_data)
            self.score_lbl.config(text=match_res["recommendation"], bg=match_res["rec_color"])
            self.diag_lbl.config(text=match_res["diag_msg"])
            
            g_yoni = next((v for k, v in YONI_ICONS.items() if k in g_data['yoni_animal']), "✨")
            g_elem = next((v for k, v in ELEMENT_ICONS.items() if k in TamilAstroConstants.RASI_ELEMENTS[g_data['rasi_idx']][0]), "✨")
            self.g_logo_lbl.config(text=f"{g_elem}\n{g_yoni}")

            b_yoni = next((v for k, v in YONI_ICONS.items() if k in b_data['yoni_animal']), "✨")
            b_elem = next((v for k, v in ELEMENT_ICONS.items() if k in TamilAstroConstants.RASI_ELEMENTS[b_data['rasi_idx']][0]), "✨")
            self.b_logo_lbl.config(text=f"{b_elem}\n{b_yoni}")
            
            self.seventh_lbl.config(text=match_res["seventh_note"], fg=match_res["seventh_color"])
            self.match_table.populate_rows(match_res["matrix"], font_size=int(12*z))

            self.tab_kudumpa_pred.update_predictions(g_data, b_data, match_res)

        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to compute horoscope:\n{str(e)}")

    def open_timeline_modal(self, timeline_data: List[Dict[str, Any]], name: str):
        if timeline_data: HoroscopeTimelineWindow(self, timeline_data, person_name=name)


if __name__ == "__main__":
    app = UltimateDSVPApp()
    app.mainloop()

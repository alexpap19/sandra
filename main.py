import threading
import time
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import platform
from kivymd.app import MDApp
from plyer import notification, vibrator

if platform == "win":
    import winsound

# ΠΡΟΣΑΡΜΟΣΜΕΝΟ ΠΡΟΓΡΑΜΜΑ ΜΕ ΤΙΣ ΝΕΕΣ ΩΡΕΣ ΣΑΣ
DIET_PLAN = {
    "Monday": {
        "06:40": "🥣 Γιαούρτι 2% + 2 κ.σ. βρώμη + 1 κ.γ. μέλι + 5 αμύγδαλα",
        "07:10": "🏃 45' περπάτημα",
        "13:30": "🍏 1 μήλο",
        "14:30": "🍗 150γρ. Ψητό κοτόπουλο + Σαλάτα εποχής",
        "17:15": "🥛 1 ποτήρι ξινόγαλο",
        "20:00": "🍳 Ομελέτα (2 αυγά) + Σαλάτα αγγούρι-ντομάτα",
    },
    "Tuesday": {
        "06:40": "🍞 1 φέτα ψωμί ολικής + 1 αυγό βραστό",
        "07:10": "🏃 40' περπάτημα",
        "13:30": "🥝 1 ακτινίδιο",
        "14:30": "🍲 1.5 φλιτζάνι Φακές + Σαλάτα λάχανο-καρότο",
        "17:15": "🥜 5-6 ανάλατα αμύγδαλα",
        "20:00": "🐟 Πράσινη σαλάτα με 1 τόνο σε νερό + 1 κρητικό παξιμαδάκι",
    },
    "Wednesday": {
        "06:40": "🥣 Γιαούρτι 2% + 1 κ.σ. καρύδια + 1 κ.γ. μέλι",
        "07:10": "🏃 30' περπάτημα",
        "13:30": "🍓 1 αποξηραμένο σύκο",
        "14:30": "🍲 1.5 φλιτζάνι Φασολάκια λαδερά + 50γρ. ανθότυρο",
        "17:15": "🥣 1 γιαούρτι 2%",
        "20:00": "🍢 2 καλαμάκια κοτόπουλο ψητά + Σαλάτα εποχής (1 κ.σ. λάδι)",
    },
    "Thursday": {
        "06:40": "🍞 1 φέτα ψωμί ολικής + 1 κ.σ. ταχίνι (χωρίς ζάχαρη)",
        "07:10": "🏃 45' περπάτημα",
        "13:30": "🍌 1/2 μπανάνα",
        "14:30": "🧆 150γρ. Ψητό μπιφτέκι + Βραστά χόρτα + 1/2 φλ. καστανό ρύζι",
        "17:15": "🧀 1 μικρό κομμάτι κίτρινο τυρί",
        "20:00": "🍅 Ντάκος: 1 παξιμάδι + ντομάτα τριμμένη + 1 κ.σ. λάδι + 60γρ. ανθότυρο",
    },
    "Friday": {
        "06:40": "🥣 Γιαούρτι 2% + 2 κ.σ. βρώμη + 1/2 μπανάνα",
        "07:10": "🏃 40' περπάτημα",
        "13:30": "🍏 1 μήλο",
        "14:30": "🍲 1.5 φλιτζάνι Ρεβίθια + Σαλάτα εποχής + 5-6 ελιές",
        "17:15": "🥛 1 ποτήρι κεφίρ",
        "20:00": "🍳 Ομελέτα (2 αυγά) με μανιτάρια & πιπεριές + Σαλάτα μαρούλι",
    },
    "Saturday": {
        "06:40": "🍞 1 αυγό βραστό + 1 φέτα ψωμί ολικής + 1/4 αβοκάντο",
        "07:10": "🏃 30' περπάτημα",
        "13:30": "🥝 1 ακτινίδιο",
        "14:30": "🐟 150γρ. Ψητό ψάρι + Βραστό κολοκυθάκι & 1 μικρή πατάτα",
        "17:15": "🥜 5 καρύδια",
        "20:00": "🥪 1 τοστ ολικής με 1 φέτα γαλοπούλα & 1 φέτα τυρί χαμηλών λιπαρών + αγγούρι",
    },
    "Sunday": {
        "06:40": "🍞 2 μικρά παξιμαδάκια ολικής + 1 κομμάτι ανθότυρο",
        "07:10": "🏃 40' περπάτημα",
        "13:30": "🍊 1 φρούτο εποχής",
        "14:30": "🥩 150γρ. Ψητό άπαχο μοσχάρι + Μεγάλη σαλάτα εποχής + 1/2 φλ. πλιγούρι",
        "17:15": "🥣 1 γιαούρτι 2%",
        "20:00": "🥣 1 μπολ σούπα λαχανικών με 60γρ. βραστό κοτόπουλο",
    },
}

DAYS_GR = {
    "Monday": "Δευτέρα",
    "Tuesday": "Τρίτη",
    "Wednesday": "Τετάρτη",
    "Thursday": "Πέμπτη",
    "Friday": "Παρασκευή",
    "Saturday": "Σάββατο",
    "Sunday": "Κυριακή",
}

KV = """
MDScreenManager:
    id: screen_manager

    MDScreen:
        name: "locked_screen"
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "15dp"

            MDCard:
                orientation: "vertical"
                padding: "15dp"
                size_hint: (1, None)
                height: "120dp"
                md_bg_color: 0.1, 0.5, 0.2, 1
                radius: [15]

                MDLabel:
                    id: current_day_label
                    text: "Ημέρα"
                    font_style: "H5"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    halign: "center"

                MDLabel:
                    id: current_time_label
                    text: "00:00"
                    font_style: "H6"
                    theme_text_color: "Custom"
                    text_color: 0.9, 0.9, 0.9, 1
                    halign: "center"

            MDCard:
                orientation: "vertical"
                padding: "20dp"
                size_hint: (1, 1)
                md_bg_color: 1, 1, 1, 1
                radius: [15]
                elevation: 2

                MDLabel:
                    text: "📋 Τρέχουσα Δραστηριότητα / Γεύμα:"
                    font_style: "Subtitle1"
                    bold: True
                    theme_text_color: "Secondary"
                    size_hint_y: None
                    height: "30dp"

                MDLabel:
                    id: current_task_label
                    text: "Δεν υπάρχει προγραμματισμένο γεύμα αυτή την ώρα."
                    font_style: "H6"
                    theme_text_color: "Primary"
                    halign: "center"
                    valign: "middle"

            MDLabel:
                text: "🔒 Το χρονόμετρο ξεκλειδώνει αυτόματα στις 07:10 π.μ."
                font_style: "Caption"
                theme_text_color: "Secondary"
                halign: "center"
                size_hint_y: None
                height: "20dp"

    MDScreen:
        name: "timer_screen"
        md_bg_color: 0.95, 0.95, 0.95, 1

        MDBoxLayout:
            orientation: 'vertical'
            padding: "20dp"
            spacing: "20dp"

            MDLabel:
                text: "🏃 Ώρα για Περπάτημα!"
                halign: "center"
                font_style: "H4"
                theme_text_color: "Primary"
                size_hint_y: None
                height: "60dp"

            Widget:

            MDLabel:
                id: timer_label
                text: "40:00"
                halign: "center"
                font_style: "H2"
                theme_text_color: "Error" if app.timer_running else "Primary"
                size_hint_y: None
                height: "100dp"

            Widget:

            MDRaisedButton:
                id: start_btn
                text: "ΕΝΑΡΞΗ ΠΕΡΙΠΑΤΟΥ"
                pos_hint: {"center_x": .5}
                size_hint: (0.7, None)
                height: "50dp"
                md_bg_color: 0.1, 0.6, 0.3, 1
                on_release: app.toggle_timer()
"""


class WalkApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_running = False
        self.seconds_left = 40 * 60
        self.timer_event = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        Clock.schedule_interval(self.update_app_state, 1)
        return Builder.load_string(KV)

    def update_app_state(self, dt):
        now = datetime.now()
        day_name = now.strftime("%A")
        time_str = now.strftime("%H:%M:%S")

        greek_day = DAYS_GR.get(day_name, day_name)
        self.root.ids.current_day_label.text = f"📆 {greek_day}"
        self.root.ids.current_time_label.text = f"🕒 {time_str}"

        current_hour_minute = now.strftime("%H:%M")
        today_plan = DIET_PLAN.get(day_name, {})

        current_task = "📭 Δεν υπάρχει κάτι προγραμματισμένο αυτή την ώρα."
        sorted_hours = sorted(today_plan.keys())

        for i in range(len(sorted_hours)):
            start_time = sorted_hours[i]
            if current_hour_minute >= start_time:
                if i + 1 < len(sorted_hours):
                    end_time = sorted_hours[i + 1]
                    if current_hour_minute < end_time:
                        current_task = today_plan[start_time]
                        break
                else:
                    current_task = today_plan[start_time]

        self.root.ids.current_task_label.text = current_task

        # ΝΕΑ ΩΡΑ: Ξεκλειδώνει αυτόματα στις 07:10 π.μ.
        if now.hour == 7 and now.minute == 10:
            if self.root.current == "locked_screen":
                self.root.current = "timer_screen"
                self.trigger_alarm_alert()
        else:
            if not self.timer_running and self.root.current == "timer_screen":
                self.root.current = "locked_screen"

    def toggle_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.root.ids.start_btn.text = "ΑΚΥΡΩΣΗ"
            self.root.ids.start_btn.md_bg_color = (0.8, 0.2, 0.2, 1)
            self.timer_event = Clock.schedule_interval(self.update_timer, 1)
        else:
            self.stop_and_reset_timer()

    def update_timer(self, dt):
        if self.seconds_left > 0:
            self.seconds_left -= 1
            mins, secs = divmod(self.seconds_left, 60)
            self.root.ids.timer_label.text = f"{mins:02d}:{secs:02d}"
        else:
            self.stop_and_reset_timer()
            self.trigger_alarm_alert()
            self.root.current = "locked_screen"

    def stop_and_reset_timer(self):
        self.timer_running = False
        if self.timer_event:
            Clock.unschedule(self.timer_event)
        self.seconds_left = 40 * 60
        self.root.ids.timer_label.text = "40:00"
        self.root.ids.start_btn.text = "ΕΝΑΡΞΗ ΠΕΡΙΠΑΤΟΥ"
        self.root.ids.start_btn.md_bg_color = (0.1, 0.6, 0.3, 1)

    def trigger_alarm_alert(self):
        if platform == "win":
            try:
                for _ in range(3):
                    winsound.Beep(2000, 300)
                    time.sleep(0.1)
            except Exception as e:
                print(e)
        elif platform == "android":
            try:
                vibrator.vibrate(2)
                notification.notify(
                    title="Ντριν Ντριν!",
                    message="Ώρα για περπάτημα!",
                    app_name="WalkApp",
                )
            except Exception as e:
                print(e)


if __name__ == "__main__":
    WalkApp().run()

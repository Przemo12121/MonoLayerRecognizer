from tkinter import *
import tkinter.messagebox   
from custom_ui.constants import BUTTONS_BG, BUTTONS_BG_PRESSED, DISPLAY_LABELS_BG, MAIN_WINDOW_BG, PROCESS_RUNNING_MARK

class ProcessConfig:
    def __init__(self, start: tuple[int, int], end: tuple[int, int], step: int, exposure_time_ms: int):
        self.start = start
        self.end = end
        self.step = step
        self.exposure_time_ms = exposure_time_ms

class AutoControls:
    def __init__(self, frame: Frame, win: Tk, motor_position_provider, on_start, on_stop):
        self.__frame = frame
        self.__win = win
        self.__motor_position_provider = motor_position_provider
        self.__on_start = on_start
        self.__on_stop = on_stop
        
    def build(self, config: ProcessConfig):
        label_width = 18
        buttons_width = 7
        buttons_height = 3

        x_start_variable = StringVar(value=str(config.start[0]))
        x_end_variable = StringVar(value=str(config.end[0]))
        y_start_variable = StringVar(value=str(config.start[1]))
        y_end_variable = StringVar(value=str(config.end[1]))
        step_variable = StringVar(value=str(config.step))
        exposure_variable = StringVar(value=str(config.exposure_time_ms))

        Label(self.__frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=8, columnspan=6, pady=1)
        
        set_start_btn = Button(self.__frame, text="Set\nstart\npostion", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        set_start_btn.grid(column=0, row=9, columnspan=3)
        
        set_end_btn = Button(self.__frame, text="Set\nend\npostion", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        set_end_btn.grid(column=4, row=9, columnspan=3)

        Label(self.__frame, text="Autonomic process controls", background=MAIN_WINDOW_BG).grid(column=0, row=16, columnspan=8, pady=2)

        Label(self.__frame, text="Start position", background=MAIN_WINDOW_BG).grid(column=0, row=17, columnspan=8, pady=2)
        Label(self.__frame, text="X", background=MAIN_WINDOW_BG).grid(column=0, row=18)
        x_start_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=x_start_variable)
        x_start_entry.grid(column=1, row=18, columnspan=10)
        Label(self.__frame, text="Y", background=MAIN_WINDOW_BG).grid(column=0, row=19)
        y_start_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=y_start_variable)
        y_start_entry.grid(column=1, row=19, columnspan=10)

        Label(self.__frame, text="End position", background=MAIN_WINDOW_BG).grid(column=0, row=20, columnspan=8, pady=2)
        Label(self.__frame, text="X", background=MAIN_WINDOW_BG).grid(column=0, row=21)
        x_end_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=x_end_variable)
        x_end_entry.grid(column=1, row=21, columnspan=10)
        Label(self.__frame, text="Y", background=MAIN_WINDOW_BG).grid(column=0, row=22)
        y_end_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=y_end_variable)
        y_end_entry.grid(column=1, row=22, columnspan=10)

        Label(self.__frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=23, columnspan=6, pady=1)
        Label(self.__frame, text="Step", background=MAIN_WINDOW_BG).grid(column=0, row=24)
        step_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=step_variable)
        step_entry.grid(column=1, row=24, columnspan=10)
        Label(self.__frame, text="Exposure [ms]", background=MAIN_WINDOW_BG).grid(column=0, row=25, columnspan=2)
        exposure_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=int(label_width/2), justify="right", textvariable=exposure_variable)
        exposure_entry.grid(column=2, row=25, columnspan=7)

        def on_set_start_clicked():
            (x, y, _) = self.__motor_position_provider()
            x_start_variable.set(str(x))
            y_start_variable.set(str(y))

        def on_set_end_clicked():
            (x, y, _) = self.__motor_position_provider()
            x_end_variable.set(str(x))
            y_end_variable.set(str(y))

        set_start_btn.config(command=on_set_start_clicked)
        set_end_btn.config(command=on_set_end_clicked)

        Label(self.__frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=26, columnspan=6, pady=4)
        buttons_height = 1
        buttons_width = 4
        start_btn = Button(self.__frame, text="Start", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        start_btn.grid(column=1, row=27, columnspan=1)
        stop_btn = Button(self.__frame, text="Stop", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        stop_btn.grid(column=4, row=27, columnspan=1)
        stop_btn.config(state="disabled")
        
        Label(self.__frame, text="Status: ", background=MAIN_WINDOW_BG).grid(column=0, row=30, columnspan=2, pady=20)
        status_label = Label(self.__frame, text="Not running", background=MAIN_WINDOW_BG)
        status_label.grid(column=2, row=30, columnspan=2, pady=20)

        def start_btn_command():
            err = []
            if not x_start_variable.get().isdigit():
                err.append("X coordinate of start position")
            if not y_start_variable.get().isdigit():
                err.append("Y coordinate of start position")
            if not x_end_variable.get().isdigit():
                err.append("X coordinate of start position")
            if not y_end_variable.get().isdigit():
                err.append("Y coordinate of end position")
            if not step_variable.get().isdigit():
                err.append("Camera step")
            if not exposure_variable.get().isdigit():
                err.append("Camera exposure time")

            if len(err) > 0:
                self.__show_errors(err)
                return

            start_btn.config(state="disabled")
            stop_btn.config(state="normal")
            set_start_btn.config(state="disabled")
            set_end_btn.config(state="disabled")
            x_start_entry.config(state="disabled")
            x_end_entry.config(state="disabled")
            y_start_entry.config(state="disabled")
            y_end_entry.config(state="disabled")
            step_entry.config(state="disabled")
            exposure_entry.config(state="disabled")

            status_label.config(text="Running", foreground=PROCESS_RUNNING_MARK)

            self.__on_start()

        def stop_btn_command():
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
            set_start_btn.config(state="normal")
            set_end_btn.config(state="normal")
            x_start_entry.config(state="normal")
            x_end_entry.config(state="normal")
            y_start_entry.config(state="normal")
            y_end_entry.config(state="normal")
            step_entry.config(state="normal")
            exposure_entry.config(state="normal")

            self.__on_stop()
            status_label.config(text="Not running", foreground="black")

        start_btn.config(command=start_btn_command)
        stop_btn.config(command=stop_btn_command)

    def __show_errors(self, fields: list[str]):
        errList = [f"- {field}." for field in fields]
        errList = '\n'.join(errList)
        tkinter.messagebox.showerror("Invalid input data", f"Below fields have invalid input data:\n\n{errList}\n\nThey must be natural number.")

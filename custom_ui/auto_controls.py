from tkinter import *
import tkinter.messagebox   
from tkinter import filedialog
from custom_ui.constants import BUTTONS_BG, BUTTONS_BG_PRESSED, DISPLAY_LABELS_BG, MAIN_WINDOW_BG, PROCESS_RUNNING_MARK

class ProcessConfig:
    def __init__(self, start: tuple[int, int], end: tuple[int, int], steps: tuple[int, int, int], exposure_time_ms: int, treshold: float, output_dir_path: str):
        self.start = start
        self.end = end
        self.steps = steps
        self.exposure_time_ms = exposure_time_ms
        self.treshold = treshold
        self.output_dir_path = output_dir_path

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
        x_step_variable = StringVar(value=str(config.steps[0]))
        y_step_variable = StringVar(value=str(config.steps[1]))
        z_step_variable = StringVar(value=str(config.steps[2]))
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
        Label(self.__frame, text="Step x", background=MAIN_WINDOW_BG).grid(column=0, row=24)
        x_step_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=x_step_variable)
        x_step_entry.grid(column=1, row=24, columnspan=10)
        Label(self.__frame, text="Step y", background=MAIN_WINDOW_BG).grid(column=0, row=25)
        y_step_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=y_step_variable)
        y_step_entry.grid(column=1, row=25, columnspan=10)
        Label(self.__frame, text="Step z", background=MAIN_WINDOW_BG).grid(column=0, row=26)
        z_step_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=z_step_variable)
        z_step_entry.grid(column=1, row=26, columnspan=10)
        Label(self.__frame, text="Exposure [ms]", background=MAIN_WINDOW_BG).grid(column=0, row=27, columnspan=2)
        exposure_entry = Entry(self.__frame, background=DISPLAY_LABELS_BG, width=int(label_width/2), justify="right", textvariable=exposure_variable)
        exposure_entry.grid(column=2, row=27, columnspan=7)

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

        dir_label = Label(self.__frame, text="", background=MAIN_WINDOW_BG)

        def select_directory():
            output_directory = filedialog.askdirectory()
            dir_label.config(text=output_directory)

        Label(self.__frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=29, columnspan=6, pady=4)
        output_dir_btn = Button(self.__frame, text="Select output directory", command=select_directory, background=MAIN_WINDOW_BG, width=buttons_width * 3, height=buttons_height)
        output_dir_btn.grid(column=0, row=30, columnspan=8, pady=2)
        dir_label.grid(column=0, row=31, columnspan=6, pady=1)

        Label(self.__frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=32, columnspan=6, pady=4)
        buttons_height = 1
        buttons_width = 4
        start_btn = Button(self.__frame, text="Start", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        start_btn.grid(column=1, row=33, columnspan=1)
        stop_btn = Button(self.__frame, text="Stop", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        stop_btn.grid(column=4, row=33, columnspan=1)
        stop_btn.config(state="disabled")
        
        Label(self.__frame, text="Status: ", background=MAIN_WINDOW_BG).grid(column=0, row=35, columnspan=2, pady=20)
        status_label = Label(self.__frame, text="Not running", background=MAIN_WINDOW_BG)
        status_label.grid(column=2, row=35, columnspan=2, pady=20)

        def start_btn_command():
            err = []
            if not AutoControls.__is_int(x_start_variable.get()):
                err.append("X coordinate of start position")
            if not AutoControls.__is_int(y_start_variable.get()):
                err.append("Y coordinate of start position")
            if not AutoControls.__is_int(x_end_variable.get()):
                err.append("X coordinate of start position")
            if not AutoControls.__is_int(y_end_variable.get()):
                err.append("Y coordinate of end position")
            if not x_step_variable.get().isdigit():
                err.append("Camera step (x coordinate)")
            if not y_step_variable.get().isdigit():
                err.append("Camera step (y coordinate)")
            if not z_step_variable.get().isdigit():
                err.append("Camera step (z coordinate)")
            if not exposure_variable.get().isdigit():
                err.append("Camera exposure time")
            if not dir_label.cget("text"):
                err.append("Output directory not selected")

            if len(err) > 0:
                AutoControls.__show_errors(err)
                return

            start_btn.config(state="disabled")
            stop_btn.config(state="normal")
            set_start_btn.config(state="disabled")
            set_end_btn.config(state="disabled")
            x_start_entry.config(state="disabled")
            x_end_entry.config(state="disabled")
            y_start_entry.config(state="disabled")
            y_end_entry.config(state="disabled")
            x_step_entry.config(state="disabled")
            y_step_entry.config(state="disabled")
            z_step_entry.config(state="disabled")
            exposure_entry.config(state="disabled")
            output_dir_btn.config(state="disabled")

            status_label.config(text="Running", foreground=PROCESS_RUNNING_MARK)
            
            config.start = (int(x_start_variable.get()), int(y_start_variable.get()))
            config.end = (int(x_end_variable.get()), int(y_end_variable.get()))
            config.exposure_time_ms = int(exposure_variable.get())
            config.steps = (int(x_step_variable.get()), int(y_step_variable.get()), int(z_step_variable.get()))
            config.output_dir_path = dir_label.cget("text")

            self.__on_start(config)

        def stop_btn_command():
            start_btn.config(state="normal")
            stop_btn.config(state="disabled")
            set_start_btn.config(state="normal")
            set_end_btn.config(state="normal")
            x_start_entry.config(state="normal")
            x_end_entry.config(state="normal")
            y_start_entry.config(state="normal")
            y_end_entry.config(state="normal")
            x_step_entry.config(state="normal")
            y_step_entry.config(state="normal")
            z_step_entry.config(state="normal")
            exposure_entry.config(state="normal")
            output_dir_btn.config(state="normal")

            self.__on_stop()
            status_label.config(text="Not running", foreground="black")

        start_btn.config(command=start_btn_command)
        stop_btn.config(command=stop_btn_command)

    @staticmethod
    def __show_errors(fields: list[str]):
        errList = [f"- {field}." for field in fields]
        errList = '\n'.join(errList)
        tkinter.messagebox.showerror("Invalid input data", f"Below fields have invalid input data:\n\n{errList}\n\nThey must be integer number.")

    @staticmethod
    def __is_int(s: str) -> bool:
        if s[0] == "-":
            return s[1:].isdigit()
        else:
            return s.isdigit()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Graphical user interface for pypwdgen
"""

import tkinter as tk
from tkinter import messagebox
from pypwdgen.core import Password
from pypwdgen.config import PARAMETERS


class ClipboardException(Exception):
    pass


class MainWindow(tk.Frame):
    """Main window"""

    def __init__(self, master: tk.Tk):
        """Main window creation.

        :param master: tkinter root
        """
        self._master = master
        tk.Frame.__init__(self, self._master)
        self._configure_gui()

        self._password_length = tk.IntVar()
        self._password_length.set(PARAMETERS["length"]["DEFAULT"])
        self._password_number = tk.IntVar()
        self._password_number.set(PARAMETERS["number"]["DEFAULT"])
        self._password_complexity = tk.IntVar()
        self._password_complexity.set(PARAMETERS["complexity"]["DEFAULT"])

        # Create window content
        self._create_parameters_group()
        self._create_actions_group()
        self._create_result_group()

    def _configure_gui(self) -> None:
        """Configure main settings of the main window."""
        self._master.geometry('460x500')
        self._master.minsize(460, 500)
        self._master.title("pypwdgen-gui")
        self.pack(fill=tk.BOTH, expand=True)

    def _create_parameters_group(self) -> None:
        """Create the group 'Parameters' in the main window."""
        self._group_parameters = tk.LabelFrame(self, text="Parameters")
        self._group_parameters.pack(fill=tk.X, side=tk.TOP, padx=5, pady=5)

        self._create_parameters_sliders(self._group_parameters)

    def _create_parameters_sliders(self, master: tk.LabelFrame) -> None:
        """Create the 'Number' and 'length' sliders from 'Parameters' group.

        Moving the sliders updates the associated variable.

        :param tk.LabelFrame master: parent element
        """
        self._slider_number = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_=PARAMETERS["number"]["MIN"],
            to=PARAMETERS["number"]["MAX"],
            label="Number of passwords",
            variable=self._password_number,
        )
        self._slider_number.pack(expand=True, fill=tk.X)

        self._slider_length = tk.Scale(
            master,
            orient=tk.HORIZONTAL,
            from_=PARAMETERS["length"]["MIN"],
            to=PARAMETERS["length"]["MAX"],
            label="Length of passwords",
            variable=self._password_length,
        )
        self._slider_length.pack(expand=True, fill=tk.X)

    def _create_actions_group(self) -> None:
        """Create the group 'Actions' in the main window."""
        self._group_actions = tk.LabelFrame(self, text="Actions", height=50)
        self._group_actions.pack(side=tk.TOP, fill="x", padx=5, pady=5, )

        self._create_actions_buttons(self._group_actions)

    def _create_actions_buttons(self, master: tk.LabelFrame) -> None:
        """Creates the buttons from 'Actions' group.

        :param tk.LabelFrame master: parent element
        """
        self._button_generate = tk.Button(master, text="Generate", command=self._generate_passwords)
        self._button_generate.pack(side=tk.LEFT)

        self._button_copy = tk.Button(master, text="Copy", command=self._copy_passwords, state=tk.DISABLED)
        self._button_copy.pack(side=tk.LEFT)

        self._button_reset = tk.Button(master, text="Reset", command=self._reset)
        self._button_reset.pack(side=tk.LEFT)

    def _create_result_group(self) -> None:
        """Create the group 'Result' in the main window."""
        self._group_result = tk.LabelFrame(self, text="Result")
        self._group_result.pack(fill=tk.BOTH, side=tk.BOTTOM, padx=5, pady=5, expand=True)

        self._create_result_text_area(self._group_result)

    def _create_result_text_area(self, master: tk.LabelFrame) -> None:
        """Creates the text area and scrollbar which will contain the generated passwords.

        :param tk.LabelFrame master: parent element
        """
        self._scrollbar_y = tk.Scrollbar(master, orient=tk.VERTICAL)
        self._scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        self._result_text_area = tk.Text(
            master,
            wrap=tk.NONE,
            state=tk.DISABLED,
            bg="#D9D9D9",
            padx=10,
            pady=10,
            yscrollcommand=self._scrollbar_y.set,
        )
        self._result_text_area.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self._scrollbar_y['command'] = self._result_text_area.yview

    def _generate_passwords(self) -> None:
        """Generates passwords from sliders values"""
        number = self._password_number.get()
        length = self._password_length.get()
        complexity = self._password_complexity.get()

        password_list = [str(Password(length, complexity)) for i in range(number)]

        self._result_text_area.configure(state=tk.NORMAL)
        self._result_text_area.delete("1.0", tk.END)
        self._result_text_area.insert(tk.END, '\n'.join(password for password in password_list))
        self._result_text_area.configure(state=tk.DISABLED)

        # Activate the copy button
        self._button_copy.configure(state=tk.NORMAL)

    def _copy_passwords(self) -> None:
        """Copy generated passwords to the system clipboard"""
        passwords = self._result_text_area.get("1.0", tk.END)
        if passwords == "\n":
            messagebox.showwarning(title="No passwords", message="No password generated, nothing is copied.")
        else:
            try:
                self.clipboard_clear()
                self.clipboard_append(passwords)
                messagebox.showinfo(title="Copied", message="The passwords are copied to the clipboard!")
            except Exception as e:
                messagebox.showerror(title=type(e), message=str(e))

    def _reset(self) -> None:
        """Resets parameters and result to defaults"""
        self._password_number.set(PARAMETERS["number"]["DEFAULT"])
        self._password_length.set(PARAMETERS["length"]["DEFAULT"])
        self._password_complexity.set(PARAMETERS["complexity"]["DEFAULT"])

        self._result_text_area.configure(state=tk.NORMAL)
        self._result_text_area.delete("1.0", tk.END)
        self._result_text_area.configure(state=tk.DISABLED)

        self._button_copy.configure(state=tk.DISABLED)


def main() -> None:
    """Main function"""
    root = tk.Tk()
    main_window = MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    import sys

    sys.exit(main())

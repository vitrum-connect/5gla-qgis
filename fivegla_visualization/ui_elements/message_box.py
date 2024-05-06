from qgis.PyQt.QtWidgets import QMessageBox


class MessageBox:
    """ MessageBox class to show error and info messages
    """

    def __init__(self):
        self.msg_box = QMessageBox()

    def show_conditional_box(self, condition, info_message, error_message):
        """ Shows a message box based on the condition
        """
        if condition:
            self.show_info_box(info_message)
        else:
            self.show_error_box(error_message)

    def show_error_box(self, error_message):
        """ Shows an error message box

        :param error_message:
        :return:  None
        """
        self.msg_box.setWindowTitle("Error")
        self.msg_box.setIcon(QMessageBox.Critical)
        self.msg_box.setText(error_message)
        ok_button = self.msg_box.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        self.msg_box.exec_()

    def show_info_box(self, info_message):
        """ Shows an information message box
        :param info_message:
        :return: None
        """
        self.msg_box.setWindowTitle("Information")
        self.msg_box.setIcon(QMessageBox.Information)
        self.msg_box.setText(info_message)
        ok_button = self.msg_box.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        self.msg_box.exec_()

from qgis.PyQt.QtWidgets import QMessageBox


class MessageBox:
    """ MessageBox class to show custom message boxes

    """

    @staticmethod
    def show_conditional_box(condition, info_message, error_message):
        """ Shows a message box based on the condition
        """
        if condition:
            MessageBox.show_info_box(info_message)
        else:
            MessageBox.show_error_box(error_message)

    @staticmethod
    def show_error_box(error_message):
        """ Shows an error message box

        :param error_message:
        :return:  None
        """
        msg_box = QMessageBox()

        msg_box.setWindowTitle("Error")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(error_message)
        ok_button = msg_box.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        msg_box.exec_()

    @staticmethod
    def show_info_box(info_message):
        """ Shows an information message box
        :param info_message:
        :return: None
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Information")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(info_message)
        ok_button = msg_box.addButton(QMessageBox.Ok)
        ok_button.setDefault(True)
        msg_box.exec_()

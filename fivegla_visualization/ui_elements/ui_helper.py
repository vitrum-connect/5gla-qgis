class UiHelper:
    def __init__(self):
        pass

    @staticmethod
    def combo_box_filler(items, combo_box):
        """Fills the combo box with the given items

        :param items: The items to fill the combo box with
        :param combo_box: The combo box to fill

        :return: None
        """

        combo_box.clear()
        for item in items:
            combo_box.addItem(item)

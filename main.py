from sys import platform

if platform == "linux":
    import linux_controller as controller
else:
    raise NotImplementedError("Your operating system is not supported")


class TournamentManager:
    MAIN_WINDOW_NAME = 'VEX Tournament Manager'
    FIELD_CONTROL_NAME = 'Field Control'

    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 1920

    FIELD_CONTROL_SIZE = 485

    QUEUE_MINIMIZE_X = 25
    QUEUE_X = 60
    QUEUE_SCROLL_X = 165

    QUEUE_START_Y = 90

    QUEUE_SPACING = 16

    QUEUE_ELEMENTS_PER_WINDOW = 45

    DEFAULT_SCROLL_POSITION = -2

    SAVE_SCORE_X = 479
    SAVE_SCORE_Y = 782

    QUEUE_BUTTON_OFFSET = 10

    START_X = 1674
    START_Y = 126

    def __init__(self):
        self.main_window = controller.get_window_by_name(self.MAIN_WINDOW_NAME)
        self.control_window = controller.get_window_by_name(self.FIELD_CONTROL_NAME)

        self.reset_windows()
        self.queue_scroll_top()

        self.current_match = 0  # TODO figure this out from the database, we can't assume this
        self.current_scroll = self.DEFAULT_SCROLL_POSITION

    def is_bottom_match(self, match):
        bottom_match = self.current_scroll + self.QUEUE_ELEMENTS_PER_WINDOW - 1
        return match == bottom_match

    def get_match_height(self, match):
        top_match = self.current_scroll + 1
        bottom_match = self.current_scroll + self.QUEUE_ELEMENTS_PER_WINDOW - 1

        if match > bottom_match:
            self.queue_scroll_down()
            return self.get_match_height(match)
        elif match < top_match:
            self.queue_scroll_up()
            return self.get_match_height(match)
        else:
            offset = (match - top_match + 1) * self.QUEUE_SPACING
            position = offset + self.QUEUE_START_Y
            return position

    def reset_windows(self):
        controller.move_window(self.main_window, 0, 0)
        controller.resize_window(self.main_window, self.SCREEN_WIDTH - self.FIELD_CONTROL_SIZE, self.SCREEN_HEIGHT)

        controller.move_window(self.control_window, self.SCREEN_WIDTH - self.FIELD_CONTROL_SIZE, 0)

    def toggle_qual_minimized(self):
        self.queue_scroll_top()
        controller.click_at(self.QUEUE_MINIMIZE_X, self.QUEUE_START_Y + self.QUEUE_SPACING * 2)
        self.queue_scroll_top()

    def queue_scroll_up(self):
        controller.click_at(self.QUEUE_SCROLL_X, self.QUEUE_START_Y)

        if self.current_scroll > self.DEFAULT_SCROLL_POSITION:
            self.current_scroll -= 1

    def queue_scroll_down(self):
        controller.click_at(self.QUEUE_SCROLL_X, self.QUEUE_START_Y + self.QUEUE_SPACING * (self.QUEUE_ELEMENTS_PER_WINDOW - 1))
        self.current_scroll += 1

    def queue_scroll_top(self):
        controller.click_at(self.QUEUE_SCROLL_X, self.QUEUE_START_Y + self.QUEUE_SPACING)
        self.current_scroll = self.DEFAULT_SCROLL_POSITION

    def select_match(self, match):
        match_height = self.get_match_height(match)
        controller.click_at(self.QUEUE_X, match_height)
        if self.is_bottom_match(match):
            self.current_scroll += 1

    def save_scores(self, match):
        self.select_match(match)
        controller.click_at(self.SAVE_SCORE_X, self.SAVE_SCORE_Y)

    def queue_match(self, match):
        match_height = self.get_match_height(match)
        controller.click_at(self.QUEUE_X, match_height, right=True)
        controller.click_at(self.QUEUE_X + self.QUEUE_BUTTON_OFFSET, match_height + self.QUEUE_BUTTON_OFFSET)

    def start_match(self):
        controller.click_at(self.START_X, self.START_Y)


manager = TournamentManager()
manager.queue_match(10)
manager.start_match()


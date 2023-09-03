from RoboView.Robot.component.view.ComponentView import ComponentView


class ActorControlView(ComponentView):
    def __init__(self, root, actor, settings_key, width, height):
        super().__init__(root, actor.get_name(), settings_key, width, height)
        self._actor = actor

    def build_context_menue(self):
        super().build_context_menue()
        self._context_menue.add_command(label="get settings", command=self.on_get_settings)
        self._context_menue.add_command(label="load defaults", command=self.on_load_defaults)
        self._context_menue.add_command(label="save defaults", command=self.on_save_defaults)
        self._context_menue.add_separator()

    def on_get_settings(self):
        self._actor.remote_get_settings()

    def on_load_defaults(self):
        self._actor.remote_load_defaults()

    def on_save_defaults(self):
        self._actor.remote_save_defaults()

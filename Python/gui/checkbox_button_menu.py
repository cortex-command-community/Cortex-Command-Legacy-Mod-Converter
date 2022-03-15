import PySimpleGUI as sg


from Python import shared_globals as cfg


def handle_button_press(window, buttonmenu_name, selected_button_name, user_settings_button_mappings):
	buttonmenu = get_button_menu(window, buttonmenu_name)
	menu_definition = get_menu_definition(buttonmenu)

	selected_button_index = get_user_settings_button_index(user_settings_button_mappings, selected_button_name)

	buttons = get_button_menu_buttons(menu_definition)
	toggle_button(user_settings_button_mappings, selected_button_name, buttons, selected_button_index)

	buttonmenu.update(menu_definition)


def get_button_menu(window, buttonmenu_name):
	return window[buttonmenu_name]


def get_menu_definition(buttonmenu):
	return buttonmenu.MenuDefinition


def get_button_menu_buttons(menu_definition):
	return menu_definition[1]


def toggle_button(user_settings_button_mappings, selected_button_name, buttons, selected_button_index):
	toggle_button_user_entry_setting(user_settings_button_mappings, selected_button_name)
	toggle_button_visually(buttons, selected_button_index)


def toggle_button_visually(buttons, selected_button_index):
	current_button_string = buttons[selected_button_index]

	if current_button_string[0] == cfg.CHECKMARK:
		buttons[selected_button_index] = cfg.NO_CHECKMARK + current_button_string[1:]
	else:
		buttons[selected_button_index] = cfg.CHECKMARK + current_button_string[1:]


def toggle_button_user_entry_setting(user_settings_button_mappings, selected_button_name):
	user_settings_button_key = get_user_settings_button_value(user_settings_button_mappings, selected_button_name)

	current_user_settings_button_state = sg.user_settings_get_entry(user_settings_button_key)
	sg.user_settings_set_entry(user_settings_button_key, not current_user_settings_button_state)


def get_user_settings_button_index(user_settings_button_mappings, selected_button_name):
	""" We can't do a simple lookup due to the checkmark that may be in selected_button_name, so we need to use the in operator """
	for i, button_name in enumerate(user_settings_button_mappings.keys()):
		if button_name in selected_button_name:
			return i


def get_user_settings_button_value(user_settings_button_mappings, selected_button_name):
	""" We can't do a simple lookup due to the checkmark that may be in selected_button_name, so we need to use the in operator """
	for k, v in user_settings_button_mappings.items():
		if k in selected_button_name:
			return v

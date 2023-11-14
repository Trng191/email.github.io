import PySimpleGUI as sg
import email_interface

sg.theme('LightPurple')

layout = [
    [sg.Column([[sg.Text("Enter full name:"), sg.Input(key='-NAME-', do_not_clear=True, size=(40, 1), default_text='Your name here')],
                [sg.Text("Enter recipient's address:"), sg.Input(
                    key='-EMAIL_ADDRESS-', do_not_clear=True, size=(40, 1), default_text='mangmaytinhremotecontrol@gmail.com')],
                [sg.Text("Enter subject:"), sg.Input(
                    key='-SUBJECT-', do_not_clear=True, size=(40, 1))],
                [sg.Multiline("", do_not_clear=True, key='-MESSAGE-', size=(60, 10))]],
               element_justification='right')],
    [sg.Button('Send Email'), sg.Exit()]
]

window = sg.Window('Mail Box', layout)


def validate(values):
    is_valid = True
    values_invalid = []

    if len(values['-NAME-']) == 0:
        values_invalid.append('Name')
        is_valid = False

    if len(values['-EMAIL_ADDRESS-']) == 0:
        values_invalid.append('Passport Number')
        is_valid = False

    if '@' not in values['-EMAIL_ADDRESS-']:
        values_invalid.append('Email Address')
        is_valid = False

    if len(values['-SUBJECT-']) == 0:
        values_invalid.append('SUBJECT')
        is_valid = False

    if len(values['-MESSAGE-']) == 0:
        values_invalid.append('MESSAGE')
        is_valid = False

    result = [is_valid, values_invalid]
    return result


def generate_error_message(values_invalid):
    error_message = ''
    for value_invalid in values_invalid:
        error_message += ('\nInvalid' + ':' + value_invalid)

    return error_message


while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Send Email':
        validation_result = validate(values)
        if validation_result[0]:
            email_interface.send_email("test.sender.pp@gmail.com", values['-EMAIL_ADDRESS-'],
                                       values['-SUBJECT-'], values['-MESSAGE-'])
            sg.popup('EMAIL SENT!')
        else:
            error_message = generate_error_message(validation_result[1])
            sg.popup(error_message)
window.close()

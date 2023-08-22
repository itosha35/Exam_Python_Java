
import os
import json
import datetime


def del_notes(notes: list) -> dict:
    show_on_screen(notes)
    print('Какую заметку желаете удалить?')
    found = find_notes(notes)
    if found:
        show_on_screen(found)
        value = input('Подтвердите операцию удаления: Да/Нет\n>>>')
        if value.lower() == 'да':
            notes.remove(found[0])
            print('Удаление завершено.')
            return {}
        elif value.lower() == 'нет':
            print('Команда удаления отменена.')
            return {}
        else:
            print('Введена неверная команда.')
            return {}
    else:
        print('Ничего не нашли ;(')
        return {}


def save_change_notes(notes: list) -> dict:
    found = find_notes(notes)
    if found:
        show_on_screen(found)
        print("Что желаете изменить: название[1], содержание[2]?")
        value = input('Введите параметр для изменения:\n>>>').lower()
        if value == '1':
            found[0]['heading'] = input(
                'Введите название заметки:\n>>> ').upper()
        elif value == '2':
            found[0]['body'] = input('Введите текст заметки:\n>>> ').upper()
        found[0]['data'] = f"внесены изменения: {datetime.date.today()}"
    else:
        print('Ничего не нашли ;(')
        return {}


def find_notes(notes: list) -> dict:
    heading = input('Введите название заметки:\n>>> ').upper()
    found = list(filter(lambda el: heading in el['heading'], notes))
    if found:
        show_on_screen(found, dict())
        return found
    else:
        print('Ничего не нашли ;(')
        return {}


def file_path(file_name='all_notes'):
    return os.path.join(os.path.dirname(__file__), f'{file_name}.txt')


def load_from_file():
    path = file_path()
    if os.stat(path).st_size:

        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        return data
    else:
        return []


def save_to_file(contact: list) -> None:
    path = file_path()

    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(contact, file, ensure_ascii=False)


def show_on_screen(contacts: list, filter: dict) -> None:
    decode_keys = dict(
        heading='Название заметки:',
        body='Текст заметки:',
        data='Дата создания заметки',
    )
    pretty_text = str()
    for num, elem in enumerate(contacts, 1):
        if (len(filter) != 0):
            if date_interval(filter["start_date"], filter["end_date"], elem["data"]):
                pretty_text += f'Заметка №{num}:\n'
                pretty_text += '\n'.join(
                    f'{decode_keys[k]} {v}' for k, v in elem.items())
                pretty_text += '\n**********\n'
        else:
            pretty_text += f'Заметка №{num}:\n'
            pretty_text += '\n'.join(
                f'{decode_keys[k]} {v}' for k, v in elem.items())
            pretty_text += '\n**********\n'
    if (len(pretty_text) != 0):
        print(pretty_text)
    else:
        print("Нет элементов для отображения")


def new_notes(notes: list) -> None:
    notes.append(
        dict(
            heading=input('Введите название заметки:\n>>> ').upper(),
            body=input('Введите текст заметки:\n>>> ').upper(),
            data=str(datetime.date.today()),
        )
    )


def menu():
    commands = [
        'Показать все заметки',
        'Найти заметку',
        'Создать заметку',
        'Изменить заметку',
        'Удалить заметку',
        'Выйти'
    ]
    print('Выберите действие:')
    print('\n'.join(f'{n}. {v}' for n, v in enumerate(commands, 1)))
    choice = input('>>> ')

    try:
        choice = int(choice)
        if choice < 0 or len(commands) < choice:
            raise Exception('Такой команды нет')
        choice -= 1
    except ValueError as ex:
        print('Введите команду заново...')
        menu()
    except Exception as ex:
        print(ex)
        menu()
    else:
        return choice


def date_interval(t1, t2, d) -> bool:
    tt1 = datetime.datetime.strptime(t1, "%Y-%m-%d")
    tt2 = datetime.datetime.strptime(t2, "%Y-%m-%d")
    tdate = datetime.datetime.strptime(d, "%Y-%m-%d")
    if (tt1 <= tdate <= tt2):
        return True
    else:
        return False


def main() -> None:
    data = load_from_file()
    command = menu()
    if command == 0:
        if (input("Выбрать интервал дат? (Y_1 / N_0): ") in ['Y', 'y', '1']):
            ff = dict()
            ff["start_date"] = input(
                "Укажите начало интревала ГОД-МЕСЯЦ-ДЕНЬ: ")
            ff["end_date"] = input("Укажите конец интервала ГОД-МЕСЯЦ-ДЕНЬ: ")
            show_on_screen(data, ff)
        else:
            show_on_screen(data, dict())
        save_to_file(data)
        main()
    elif command == 1:
        find_notes(data)
        save_to_file(data)
        main()
    elif command == 2:
        new_notes(data)
        save_to_file(data)
        main()
    elif command == 3:
        save_change_notes(data)
        save_to_file(data)
        main()
    elif command == 4:
        del_notes(data)
        save_to_file(data)
        main()
    elif command == 5:
        save_to_file(data)
        print('Конец программы!')


if __name__ == '__main__':
    main()

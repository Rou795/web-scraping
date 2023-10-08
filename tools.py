import datetime

def logger(path):

# пришлось убрать поле с аргументами, так как в функции парсинга передаётся текст страницы после парсинга

    def __logger(old_function):
        def new_function(*args, **kwargs):
            start = datetime.datetime.now()

            result = old_function(*args, **kwargs)

            row = (f'Time start: {start}\n'
                   f'Function name: {old_function.__name__}\n'
                   f'Result: {result}\n\n')
            with open(path, 'a') as f:
                f.write(row)

            return result

        return new_function

    return __logger
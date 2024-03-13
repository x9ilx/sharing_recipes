import csv
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Загружает данные из приложенных CSV-файлов (../data/)'

    def print_divider(self):
        """Печатает разделитель в вывод."""
        self.stdout.write(
            self.style.SUCCESS(
                '---------------------------------------------------------'
            )
        )

    def get_data_file_path(self, data_file_name):
        path = settings.BASE_DIR / data_file_name
        result = Path.absolute(path)
        if result:
            self.stdout.write(
                self.style.SUCCESS(f'Файл с данными "{path}" найден')
            )
            return result
        self.stdout.write(
            self.style.ERROR(f'Файл с данными "{path}" не найден')
        )
        return None

    def check_installed_apps(self, app_name):
        if apps.is_installed(app_name):
            self.stdout.write(
                self.style.SUCCESS(f'Приложение "{app_name}" найдено')
            )
            return True

        self.stdout.write(
            self.style.ERROR(f'Приложение "{app_name}" не найдено')
        )
        return False

    def check_table_exist(self, table_name):
        if table_name in connection.introspection.table_names():
            self.stdout.write(
                self.style.SUCCESS(f'Запись в таблицу "{table_name}":')
            )
            return True
        self.stdout.write(
            self.style.ERROR(
                (
                    f'Таблица "{table_name}" не найдена '
                    f'(необходимо выполнить миграции)'
                )
            )
        )
        return False

    def load_tags(self, data_file_path, model):
        with open(data_file_path, newline='', encoding='UTF-8') as csvfile:
            csv_reader = csv.DictReader(f=csvfile)

            index = 0
            index_all = 0
            for row in csv_reader:
                try:
                    index = index + 1
                    index_all = index_all + 1
                    model.objects.update_or_create(**row)

                except Exception as ex:
                    index = index - 1
                    self.stdout.write(
                        self.style.ERROR(f'Запись "{row}" не добавлена: {ex}')
                    )
            self.stdout.write(
                self.style.SUCCESS(
                    (f'\nДобавлено {index} записей ' f'из {index_all}\n\n')
                )
            )

    def load_ingredients(self, data_file_path, model):
        model_units = apps.get_model('recipe', 'MeasurimentUnit')

        with open(data_file_path, newline='', encoding='UTF-8') as csvfile:
            csv_reader = csv.DictReader(
                f=csvfile, fieldnames=['name', 'measuriment_unit']
            )

            index = 0
            index_all = 0
            with transaction.atomic():
                for row in csv_reader:
                    try:
                        index = index + 1
                        index_all = index_all + 1
                        (
                            unit,
                            add_result,
                        ) = model_units.objects.update_or_create(
                            name=row['measuriment_unit']
                        )
                        model.objects.update_or_create(
                            name=row['name'], measurement_unit=unit
                        )

                    except Exception as ex:
                        index = index - 1
                        self.stdout.write(
                            self.style.ERROR(
                                f'Запись "{row}" не добавлена: {ex}'
                            )
                        )
            self.stdout.write(
                self.style.SUCCESS(
                    (f'\nДобавлено {index} записей ' f'из {index_all}\n\n')
                )
            )

    def load_data(self, app_name, model_name, data_file_name, load_func):
        model = apps.get_model(app_name, model_name)
        table_name = model.objects.model._meta.db_table

        if self.check_table_exist(table_name):
            data_file_path = self.get_data_file_path(data_file_name)

            if data_file_path:
                load_func(data_file_path, model)
                return

            self.stdout.write('\n')
            self.stdout.write(
                self.style.ERROR(
                    (
                        f'Ошибка при загрузке данных в таблицу "{table_name}" '
                        f'из файла "../{data_file_name}"'
                    )
                )
            )
            self.stdout.write('\n\n')

    def handle(self, *args, **kwargs):

        self.print_divider()

        if self.check_installed_apps('recipe'):
            self.load_data('recipe', 'Tag', './data/tags.csv', self.load_tags)
            self.load_data(
                'recipe',
                'Ingredient',
                'data/ingredients.csv',
                self.load_ingredients,
            )

        self.print_divider()

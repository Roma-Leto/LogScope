"""
cli.py
Модуль интерфейса пользователя
"""

import argparse

from logscope.analyze import analyze_main
from logscope.generator import generate_log


def main():
    print("[DEBUG CLI] Получена команда:")
    parser = argparse.ArgumentParser(
        prog="logscope",
        description="Утилита для анализа системных логов",
        epilog="",
        formatter_class=argparse.RawTextHelpFormatter,  # Перенос строк
        allow_abbrev=False,  # Запретить сокращения.
    )

    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Допустимые команды"
    )

    parser_generator = subparsers.add_parser("generate", help="Запуск генератора")
    parser_analyze = subparsers.add_parser("analyze", help="Запуск анализатора")

    parser_generator.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        help="Задаёт имя сгенерированного файла (не обязательно).",
    )

    parser_generator.add_argument(
        "-l",
        "--lines",
        type=int,
        required=False,
        default=1000,
        help="Задаёт количество строк в файле. По умолчанию - 1000.",
    )

    parser_analyze.add_argument(
        "-f",
        "--file",
        type=str,
        help="Путь к лог-файлу для анализа",
    )

    args = parser.parse_args()

    if args.command == "generate":
        generate_log(file_name=args.file, lines=args.lines)
    elif args.command == "analyze":
        analyze_main(file_name=args.file)


if __name__ == "__main__":
    main()

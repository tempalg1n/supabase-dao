import argparse

from supabase import Client, create_client

from utils.config import Config, load_config
from utils.dao import TableDAO
from utils.dto import Table



def _parse_args() -> argparse.Namespace:
    """
    args:

    tablename: name of table in Supabase
    fetch: if you want to retrieve data from specified table, set the flag to true
    make_csv: if you want to generate csv for received data, provide path here
    insert: pass this flag the path to the table you want to load
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--table_name', '-t', metavar='NAME', required=True)
    arg_parser.add_argument('--fetch', '-f', metavar='BOOL', default=False)
    arg_parser.add_argument('--make_csv', '-csv', metavar='PATH')
    arg_parser.add_argument('--insert', '-i', metavar='PATH')
    return arg_parser.parse_args()


def main():
    config: Config = load_config()
    supabase: Client = create_client(config.supabase.url, config.supabase.key)
    table_dao: TableDAO = TableDAO(supabase)
    args: argparse.Namespace = _parse_args()

    if args.insert:
        try:
            table_dto = Table.from_path(args.insert)
            table_dao.save(args.table_name, table_dto)

            return f"Data was successfully entered into the table '{args.table_name}'"

        except Exception:
            raise NameError("File or path is not valid. Can't transfer data.")

    if args.fetch:
        result = table_dao.get_all(
            table_name=args.table_name,
            path_for_csv=args.make_csv if args.make_csv else None
        )
        if not result:
            print(
                "WARNING: check the RLS for your table so that key access is available for you."
            )
        return result

    if not args.fetch and not args.insert:
        raise ValueError(
            "You should specify what you want to do by setting one of the fetch or/and insert flags to some value."
        )


if __name__ == '__main__':
    print(main())

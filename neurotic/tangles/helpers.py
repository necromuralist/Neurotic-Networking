# python standard library
from functools import partial

# from pypi
from tabulate import tabulate

org_table = partial(tabulate, headers="keys", tablefmt="orgtbl",
                    showindex=False)

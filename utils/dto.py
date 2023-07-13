from __future__ import annotations

import os
from dataclasses import dataclass

import pandas as pd
import csv
from pandas import DataFrame


@dataclass
class Table:
    path: str | None = None
    csv: DataFrame | None = None
    rows: list[dict[str, str]] | None = None

    @classmethod
    def from_path(cls, path: str) -> Table:
        csv: DataFrame | None = pd.read_csv(path)
        return cls(
            path=path,
            csv=csv,
            rows=csv.to_dict('records')
        )

    def to_csv(self, path: str) -> None:
        keys = self.rows[0].keys()
        try:
            with open(path, 'w', newline='') as output_file:
                dict_writer = csv.DictWriter(output_file, keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.rows)
            self.path = path
            self.csv = pd.read_csv(path)
        except Exception:
            raise ValueError(f'Invalid csv path "{path}"')


@dataclass
class Image:
    path: str | None = None
    title: str | None = None
    is_preview: bool | None = None

    @classmethod
    def from_path(cls, path: str):
        if os.path.basename(path).endswith('jpg'):
            return cls(
                path=path,
                title=os.path.basename(path),
                is_preview=True if os.path.basename(path).split(".")[0].lower().endswith("preview") else False
            )

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import pandas as pd


def parse_xls_content(data: bytes, date: str) -> list[tuple]:
    xls_data = pd.read_excel(BytesIO(data), usecols="B:F,O")

    start_idx = xls_data[
        xls_data.iloc[:, 0] == "Единица измерения: Метрическая тонна"
    ].index[0]

    end_idx = xls_data.iloc[start_idx + 3 :, 0][
        (xls_data.iloc[start_idx + 3 :, 0] == "Итого:")
        | (xls_data.iloc[start_idx + 3 :, 0].isna())
    ].index[0]

    df_filtered = xls_data.iloc[start_idx + 3 : end_idx].reset_index(drop=True)

    col_contract_count = df_filtered.columns[-1]
    df_filtered[col_contract_count] = pd.to_numeric(
        df_filtered[col_contract_count].replace("-", 0), errors="coerce"
    )

    df_filtered = df_filtered[df_filtered[col_contract_count] > 0]

    parsed_data = []

    for row in df_filtered.itertuples(index=False):
        try:
            parsed_data.append(
                (
                    row[0],  # Товар
                    row[1],  # Наименование
                    row[0][:4],  # Продукт
                    row[0][4:7],  # Тип поставки
                    row[2] if row[2] != "-" else None,  # Базис поставки
                    row[0][-1],  # Тип поставки
                    int(row[3]) if row[3] != "-" else 0,  # Объём
                    int(row[4]) if row[4] != "-" else 0,  # Итоговая сумма
                    (int(row[5]) if row[5] != "-" else 0),  # Количество сделок
                    date,  # Дата
                )
            )
        except Exception as e:
            logging.error(f"Ошибка при парсинге строки: {e}")

    return parsed_data


async def parse_xls_data(xls_content: bytes, date: str) -> list[tuple]:
    with ThreadPoolExecutor() as executor:
        parsed_data = await asyncio.get_running_loop().run_in_executor(
            executor, parse_xls_content, xls_content, date
        )
    return parsed_data

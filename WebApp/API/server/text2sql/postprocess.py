def default_postprocessing(sql: str) -> str:
    sql = sql.split('|')[-1]
    return sql
aggregates = [
  'SUM',
  'AVG',
  'COUNT',
  'MIN',
  'MAX'
]

def fix_aggregate_syntax(sql):
  is_exist_aggregate = False
  aggregate_function = None
  for aggregate in aggregates:
    if aggregate in sql:
      is_exist_aggregate = True
      aggregate_function = aggregate

  if not is_exist_aggregate:
    return sql

  aggregate_expression_start_pos = sql.find(aggregate_function)
  aggregate_expression_end_pos = sql.find('FROM') - 1

  aggregate_expression = sql[aggregate_expression_start_pos:aggregate_expression_end_pos]
  aggregate_arg = aggregate_expression[len(aggregate_function) + 1:]

  sql = sql.replace(aggregate_expression, f'{aggregate_function}({aggregate_arg})')

  return sql
  

fix_aggregate_syntax(sample)

def default_postprocessing(sql: str) -> str:
    sql = sql.split('|')[-1]

    # Fix syntax error of aggregate function
    sql = fix_aggregate_syntax(sql)

    return sql

export const datatype_mapping = {
  number: 'INT',
  string: 'TEXT',
}

export function generate_table_statement(
  obj: Record<string, any>,
  dataset: Record<string, any>[],
) {
  const schema_string = Object.entries(obj)
    .filter(([key]) => !!key)
    .reduce((res, [key, value]) => {
      try {
        value = JSON.parse(value)
      } catch (e) {}

      return [
        ...res,
        `${key.toLocaleLowerCase().replace(' ', '_')} ${
          // @ts-ignore
          datatype_mapping[typeof value] || 'BLOB'
        }`,
      ]
    }, [] as string[])
    .join(', ')

  const data_string = dataset
    .map((obj) =>
      Object.entries(obj)
        .filter(([key]) => !!key)
        .map(([_, value]) => {
          try {
            value = JSON.parse(value)
          } catch (e) {}

          if (typeof value == 'string') return `'${value}'`
          return value
        })
        .join(', '),
    )
    .reduce(
      (res, record) =>
        `${res}INSERT INTO tech_challenge VALUES (${record}); \ `,
      '',
    )

  return `DROP TABLE IF EXISTS tech_challenge; \
          CREATE TABLE tech_challenge (${schema_string}); \
          ${data_string}
  `
}

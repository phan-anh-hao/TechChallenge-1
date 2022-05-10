from preprocess import default_preprocessing, sample

schema, question, sql = sample['schema'], sample['question'], sample['sql']
schema, question, sql = default_preprocessing(schema, question, sql)

print(schema)
print(question)
print(sql)

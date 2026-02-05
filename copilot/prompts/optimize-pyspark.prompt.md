# Optimize PySpark Code

Analyze the selected PySpark code and suggest optimizations for better performance and scalability.

## Focus Areas

1. **Avoid Shuffles**: Minimize expensive shuffle operations
2. **Partitioning**: Optimal partitioning before joins and aggregations
3. **Caching Strategy**: Cache DataFrames only when reused multiple times
4. **Broadcast Joins**: Use broadcast for small-large table joins
5. **Column Pruning**: Select only needed columns early
6. **Predicate Pushdown**: Filter data as early as possible
7. **Avoid Collect**: Don't use `.collect()` on large DataFrames

## Optimization Patterns

### Partition Before Join
```python
# Before
result = large_df.join(other_df, "key")

# After - repartition on join key first
result = (large_df.repartition("key")
          .join(other_df.repartition("key"), "key"))
```

### Broadcast Small Tables
```python
# Before
result = large_df.join(small_df, "key")

# After - broadcast the small table
from pyspark.sql.functions import broadcast
result = large_df.join(broadcast(small_df), "key")
```

### Filter Early
```python
# Before
df = spark.read.parquet("data/")
df = df.select("col1", "col2", "col3", "col4", "col5")
df = df.filter(col("col1") > 100)

# After - filter and select early
df = (spark.read.parquet("data/")
      .filter(col("col1") > 100)
      .select("col1", "col2", "col3"))
```

### Cache Wisely
```python
# Before - caching DataFrame used only once
df = df.filter(...).cache()
result = df.count()  # Only used once - no benefit

# After - cache only when reused
df = df.filter(...)
result1 = df.count()
result2 = df.groupBy("col").count()  # Recomputes the filter

# Better - cache when reusing
df = df.filter(...).cache()
result1 = df.count()
result2 = df.groupBy("col").count()  # Uses cached result
df.unpersist()  # Clean up when done
```

Please analyze the selected code and suggest specific optimizations.

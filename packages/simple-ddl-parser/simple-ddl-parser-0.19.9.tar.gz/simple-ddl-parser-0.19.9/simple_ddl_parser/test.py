from simple_ddl_parser import DDLParser


ddl = """
CREATE EXTERNAL TABLE test (
test STRING NULL COMMENT 'xxxx',
)
PARTITIONED BY (snapshot STRING, cluster STRING)
"""
parse_result = DDLParser(ddl).run(output_mode="hql", group_by_type=True)
import pprint
pprint.pprint(parse_result)

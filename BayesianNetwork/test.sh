#!/bin/bash
for i in {1..10}
do
echo "loop $i" && \
python3 misc/query_creator.py 100000 ./queries/test_query.json && \
python b_net_A3_xx.py ./structures/structure.json ./values/values.json queries/test_query.json && \
python b_net_A3_xx_other.py ./structures/structure.json ./values/values.json queries/test_query.json && \
python3 output/checker.py ./output/output.json ./output/answer.json
done
#!/bin/bash

for ((i = 1; i <= 10; i++)); do
    NR=$RANDOM
    echo "nr: $NR" > in/unit_test1/values.yaml
    cat vals_template.yaml >> in/unit_test1/values.yaml
    rm -rf  output/*; python3 prelucrare_intrebare.py < python_values 
    echo $NR | python3 run_unit_tests.py
    DIFF=$(diff expected_rez out_rez) 
    if [ "$DIFF" != "" ] 
        then
            echo "Unit test number $i wrong. stopping"
    fi
done

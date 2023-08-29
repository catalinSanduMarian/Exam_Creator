#!/bin/bash

DIR_NAME=test_run
QUEST=question
VALUE_FILE=values.yaml
QTEXT=question_text.tex

rm -rf $DIR_NAME
mkdir $DIR_NAME
cd $DIR_NAME

mkdir $QUEST
touch $QUEST/$VALUE_FILE
touch $QUEST/$QTEXT

for i in {1..100}
do
    cp -r $QUEST $QUEST$i
    echo "\documentclass{exam}" > $QUEST$i/$QTEXT
    echo "\begin{document}" >> $QUEST$i/$QTEXT
    echo "\paragraph{" >> $QUEST$i/$QTEXT
    echo "this is question$i \\\\" >> $QUEST$i/$QTEXT
    cat ../values_file > $QUEST$i/$VALUE_FILE
    cat ../input_file >> $QUEST$i/$QTEXT
    echo "}" >> $QUEST$i/$QTEXT
    echo "\end{document}" >> $QUEST$i/$QTEXT
    
done
rm -rf $QUEST
cp ../quest_types .
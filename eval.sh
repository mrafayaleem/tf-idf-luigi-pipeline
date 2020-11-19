echo "a b c % c d e" > documents.txt &&
echo "*** Executing..." &&
./run.sh documents.txt &&
echo "*** Evaluating..." &&
wc -l similarity.csv &&
echo "Done! We haven't evaluated the correctness of your submission, but the archive structure looks good!"
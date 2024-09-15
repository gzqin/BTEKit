# 1 =======
# Get scatter.dat containing scattering channels

time python BTE-scatter.py >|scatter.dat &

#time BTE-scatter3.py >|scatter3.dat &
#time BTE-scatter5.py >|scatter5.dat &

# 2 =======
# Get informatin for each phonon branch along the specific PATH
# 2.1 -----
# Gamma-K for honeycomb BZ
sort -g -k 4 scatter.dat -o scatter.dat
#vi scatter.dat 
head -n 343 scatter.dat >|scatter.dat2

# 2.2 -----
# Get the data along Gamma-M for honeycomb BZ
#FILENAME=scatter.dat
DATAFILE=scatter.dat
FILENAME=G-M.dat
ATOM_NUMBER=8
BRANCH_NUMBER=$(($ATOM_NUMBER * 3))
head -n $(($BRANCH_NUMBER + 1)) $DATAFILE >|$FILENAME
cat $DATAFILE | cut -d ' ' -f 3 | sort -g | uniq | tail -n +3 |\
while read DATA
do
    grep "$DATA" $DATAFILE | sort -g -k 4 | head -$BRANCH_NUMBER >>$FILENAME
done

for i in $(seq 1 1 $BRANCH_NUMBER)
do
    head -n 1 $FILENAME >|$i.dat
    cat $FILENAME | grep "^$i " | sort -g -k 3 >>$i.dat
done
sed -i -e 's/X/FA/g' 1.dat
sed -i -e 's/X/TA/g' 2.dat
sed -i -e 's/X/LA/g' 3.dat
sed -i -e 's/X/FO/g' 4.dat
sed -i -e 's/X/TO/g' 5.dat
sed -i -e 's/X/LO/g' 6.dat

# 2.3 -----
# Split the branch for NU.dat
DATAFILE=NU.dat
ATOM_NUMBER=2
BRANCH_NUMBER=$(($ATOM_NUMBER * 3))

for i in $(seq 1 1 $BRANCH_NUMBER)
do
    head -n 1 $DATAFILE >|$i.dat
    cat $DATAFILE | grep "^$i " | sort -g -k 3 >>$i.dat
done
sed -i -e 's/X/FA/g' 1.dat
sed -i -e 's/X/TA/g' 2.dat
sed -i -e 's/X/LA/g' 3.dat
sed -i -e 's/X/FO/g' 4.dat
sed -i -e 's/X/TO/g' 5.dat
sed -i -e 's/X/LO/g' 6.dat


# ===========================================================

head -n 1 scatter.dat >|1.dat
head -n 1 scatter.dat >|2.dat
head -n 1 scatter.dat >|3.dat

cat scatter.dat2 | grep "^1 " | sort -g -k 3 >>1.dat
cat scatter.dat2 | grep "^2 " | sort -g -k 3 >>2.dat
cat scatter.dat2 | grep "^3 " | sort -g -k 3 >>3.dat

sed -i -e 's/X/ZA/g' 1.dat
sed -i -e 's/X/TA/g' 2.dat
sed -i -e 's/X/LA/g' 3.dat

cat POSCAR | \
(
read LINE
read LINE
read LINE
echo "lattvec(:,1)= $LINE"
read LINE
echo "lattvec(:,2)= $LINE"
read LINE
echo "lattvec(:,3)= $LINE"
read LINE
read LINE
read LINE
COUNT=0
while read LINE
do
    COUNT=$(($COUNT + 1))
    echo "positions(:,$COUNT)= $LINE"
done
)

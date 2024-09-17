# BTEkit
# Post-data processing for ShengBTE
材料热输运性质的计算涉及包括VASP、Phonopy、Thirdorder以及ShengBTE等多个相关软件和程序的调用，且求解步骤涉及多个中间变量，过程复杂，各个软件之间的开发文档彼此独立，因此新用户很难快速掌握这些计算流程。尽管目前有vaspkit软件可用于处理VASP计算相关的文件生成与后处理，但其目前尚未包含加速热输运性质计算的功能，且无法应用于集群的并发作业提交场景。
因此，经由秦光照老师、韦依等人共同努力，开发了一款新的BTEKit热输运性质模拟与分析计算平台BTEKit。总体程序采用python和shell语言编写，主要用于Linux系统下热输运性质计算过程中的数据预-后处理，并帮助使用者简明、快速地掌握集群中并发作业的批量提交方法，建立不同计算软件之间的使用桥梁。BTEKit的主要功能如下：

（1）有限位移差分法计算声子谱任务批量生成与提交

（2）三阶力常数计算的计算任务批量生成、提交与阶段半径测试

（3）波恩有效电荷微扰计算

（4）BTE计算热输运性质	

（5）弹性常数计算（能量-应变法）	

与这一程序相关的软件包及其主要功能范围说明如下：

（1）VASP: VASP (Vienna Ab-initio Simulation Package) 是一种广泛应用的第一性原理计算软件，用于模拟凝聚态物质中的电子结构和原子动力学。它基于密度泛函理论 (DFT)，能够计算材料的电子态、能量、力等物理量；

（2）Phonopy 是一个开源的声子计算工具，主要用于计算晶体的声子谱、自由能、比热容和热导等热力学性质。它可以与 VASP 等 DFT 软件结合使用，生成力常数，并计算声子的相关性质。

（3）Thirdorder: Thirdorder 是一个用于计算三阶力常数的软件，用于描述声子与声子之间的非谐性相互作用。它生成的数据可供 ShengBTE 使用，进行晶体的热导率计算。

（4）ShengBTE: ShengBTE (Sheng's Boltzmann Transport Equation solver) 是一款解决玻尔兹曼输运方程的软件，专门用于计算材料中的晶格热导率，能够预测在不同温度下材料的热传导特性。

BTEKit支持Linux系统，对应集群可以是PBS或Slurm集群，需要在安装了python3.X的环境下运行（thirdorder软件包现已更新版本v1.1.3，支持在python3.X环境下运行）。
正式发布后安装方法与其他的python软件包类似，可以通过在Linux界面中键入以下命令行以完成安装。
```
pip install BTEKit
```
也可下载github文件进行本地安装：
```
unzip BTEKit-main.zip
cd BTEKit-main
pip install .
```
BTEKit支持在任意文件夹下调用，且无需修改bash环境变量，调用方式如下：
```
(base) [user@server ~/BTEKit]$ btekit 
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose:
```
安装完成后，在用户的任意文件夹下打开命令行界面，输入btekit均可调用BTEKit程序，用户可以按照英文提示键入数字以选择想要执行的功能。

# 程序功能说明：
## 声子谱计算（有限位移差分法）
在进行声子谱计算之前，首先需要调用VASP完成结构优化。在通过VASP计算获得弛豫后的CONTCAR文件后，新建文件夹用于计算声子谱，这里为便于演示，将新建文件夹命名为2nd，并准备声子谱计算所需的输入文件：
（1）输入文件准备：需要准备的文件包括：INCAR，KPOINTS，POSCAR，POTCAR，vasp提交脚本。将此前结构优化所得的CONTCAR文件复制到新建的2nd文件夹中，重命名为POSCAR；利用vaspkit工具或手动编写声子谱计算所需的INCAR和KPOINTS文件内容。
```
mkdir 2nd
cp CONTCAR POSCAR
```
（2）利用BTEKit在计算文件夹中生成相关命令，选择功能1：phonopy calculation即可在选择在对应文件夹中生成哪些文件，如下：
(base) [user@server ~/calc-standard-qsub/2nd]$ btekit
```
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 1

Select a Phonopy-related task:
0: phonopy-command
1: Loop-phonopy.sh
2: band-example.conf
3: mesh-example.conf
4：GruneisenPlot.sh
```
首先生成command文件到计算文件夹：
```
Enter the number for the task you want to execute: 0
phonopy-command has been generated in 	/public/home/user/calc-standard-qsub/2nd
```
（3）查看复制的command文件
```
cat phonopy-command
```
包含内容如下，详细注释了计算过程中需要执行的命令，用户可以根据如下命令完成声子谱计算任务的批量提交与计算结果的读取：
```
phonopy -d --dim="x y z"
./Loop-phonopy.sh $(pwd)/vasp.slurm   
 # need to prepare the vasp.pbs in advance
phonopy -f run-*/vasprun.xml; phonopy --factor=521.471 --full-fc --writefc -p -s band.conf; phonopy-bandplot --gnuplot >|band.dat
phonopy -p -s mesh.conf
```
（4）批量生成计算任务。首先在计算文件夹2nd中生成Loop-phonopy.sh文件：
```
(base) [user@server ~/calc-standard-qsub/phonopy]$BTEKit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 1

Select a Phonopy-related task:
0: phonopy-command
1: Loop-phonopy.sh
2: band-example.conf
3: mesh-example.conf
4：GruneisenPlot.sh
Enter the number for the task you want to execute: 1
Loop-phonopy.sh has been generated in /public/home/user/calc-standard-qsub/2nd
Execution permission has been granted to Loop-phonopy.sh
```
接下来执行command中的以下命令，完成扩胞和任务批量自动提交：
```
phonopy -d --dim="x y z"  # 对POSCAR文件原胞进行扩胞，一般应包含接近100个原子，超胞的晶格尺寸应达到10Å
./Loop-phonopy.sh $(pwd)/vasp.slurm # 这里需要根据集群类型选择合适的提交脚本，以代替vasp.slurm，执行这句命令可以批量提交计算任务
```

（5）结果后处理：
计算任务结束后，执行command中的命令：
```
phonopy -f run-*/vasprun.xml; phonopy --factor=521.471 --full-fc --writefc -p -s band.conf; phonopy-bandplot --gnuplot >|band.dat
phonopy -p -s mesh.conf
```
完成二阶力常数文件FORCE_CONSTANTS的生成；
通过选择功能1中的命令2和3分别生成band-example.conf和mesh-example.conf文件，用于生成band.dat文件和图片，注意需要对上述两个文件的参数进行手动设置。具体来说，通过执行命令：
``` 
phonopy --factor=521.471 --full-fc --writefc -p -s band.conf
```
得到band.dat文件，后通过执行
```
phonopy-bandplot --gnuplot >|band.dat phonopy -p -s mesh.conf
```
得到最终的声子谱图像。
如果通phonopy--gruneisen命令得到计算结果：gruneisen.yaml，还可进一步用功能：
```
4：GruneisenPlot.sh
```
来获取gruneisen.dat文件，用于origin中画图作业。
## 三阶力常数计算
在进行声子谱计算的同时可以计算三阶力常数，利用BTEKit提交任务的步骤如下：
（1）输入文件准备。与计算二阶力常数相似，新建文件夹用于计算三阶力常数，这里为便于演示，将新建文件夹命名为3rd，并编写INCAR，KPOINTS，POSCAR，POTCAR，vasp提交脚本文件。
（2）利用BTEKit在计算文件夹中生成相关命令，选择功能2：3rd_order calculation即可在选择在对应文件夹中生成哪些文件，如下：
```
(base) [user@server ~/calc-standard-qsub/phonopy]$BTEKit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 2

Select a 3rd-order-related task:
0: 3rd-command
1: Loop-3rd.sh
2: checkpend.sh
3: BTE-copy3rd.sh
4: traceIFC-distance.sh
Enter the number for the task you want to execute:
```
其中功能0可以用于生成包含三阶力常数计算命令的command文件：
```
Enter the number for the task you want to execute: 0
3rd-command has been generated in 	/public/home/user/calc-standard-qsub/3rd
```
（3）查看复制的command文件
```
cat 3rd-command
```
包含内容如下，详细注释了计算过程中需要执行的命令，用户可以根据如下命令完成三阶力常数计算任务的批量提交与计算结果的读取：
```
nohup ./Loop-3rd.sh $(pwd)/vasp.slurm &    # need to prepare the vasp.slurm in advance
find run-* -name vasprun.xml | thirdorder_vasp.py reap a b c -d 

== LOG ==
```
（4）批量生成计算任务。首先在计算文件夹3rd中生成Loop-3rd.sh文件：
```
(base) [user@server ~/C/calc-standard-qsub/phonopy]$BTEKit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 2

Select a 3rd-order-related task:
0: 3rd-command
1: Loop-3rd.sh
2: checkpend.sh
3: BTE-copy3rd.sh
4: traceIFC-distance.sh
Enter the number for the task you want to execute: 1
Loop-3rd.sh has been generated in /public/home/user/calc-standard-qsub/3rd
```
接下来执行3rd-command中的以下命令，完成扩胞和任务批量自动提交：
```
thirdorder_vasp.py sow a b c -d  # a b c表示xyz轴方向扩胞的倍数，d 为截止半径[nm/-integer]考虑范围内多少个临近原子的受力来计算力常数矩阵，d需要测试，测试到底考虑多少个临近原子受力，取得越大，则需要计算的力常数矩阵就越多，计算时间长，但精度会提高。一般情况d取<=-10 或 >=0.6
nohup ./Loop-3nd.sh $(pwd)/vasp.slurm &  # 这里需要根据集群类型选择合适的提交脚本，以代替vasp.slurm，执行这句命令可以批量提交计算任务
由于三阶计算的任务量大，所以BTEKit中包含了检查计算任务是否全部完成的脚本，即输入数字2对应的checkpend.sh，用于监测队列中的任务是否正常运行，防止集群网络异常引起的任务失效。
Select a 3rd-order-related task:
0: 3rd-command
1: Loop-3rd.sh
2: checkpend.sh
3: BTE-copy3rd.sh
4: traceIFC-distance.sh
```
（5）结果后处理：
计算任务结束后，执行command中的命令：
```
find run-* -name vasprun.xml | thirdorder_vasp.py reap a b c -d完成三阶力常数文件FORCE_CONSTANTS的生成；
```
为了节省计算资源，秦老师编写了脚本BTE-copy3rd.sh，通过选择
```
3: BTE-copy3rd.sh
```
并执行这一脚本：
```
bash BTE-copy3rd.sh
```
可以通过对比POSCAR文件的第一行信息，提取出考虑截止半径d取较小值的vasprun.xml文件，再计算出截止半径d处于这一特定值下的三阶力常数矩阵。
注意：
I.手动创建新的文件夹用于存放截止半径d为特定数值时的三阶力常数矩阵计算结果，并复制POSCAR文件到新建文件夹。
II.使用thirdorder命令生成对应的3RD.POSCAR.*计算文件
```
thirdorder_vasp.py sow a b c -d
```
III.利用btekit在这一文件夹下生成BTE-copy3rd.sh文件并执行，注意脚本BTE-copy3rd.sh需要手动修改其中的：
```
DIR="../3rd"  # original dir
```
这里的DIR需要指定存放初次计算结果的文件夹，默认值为../3rd。
得到的计算结果文件夹形式为：run-$i，执行结果示例如下：
```
../3nd/run-001/ --> run-001/
../3nd/run-001/ --> run-002/
../3nd/run-003/ --> run-003/
../3nd/run-004/ --> run-004/
../3nd/run-001/ --> run-005/
……
```
为了获取原子间距离及对应的力常数（Interatomic Force Constants, IFC）矩阵，可以利用功能4：
```
4: traceIFC-distance.sh
```
并执行这一脚本：
```
bash traceIFC-distance.sh
```
其主要功能是根据 SPOSCAR 文件中的原子坐标计算原子间的几何距离，并根据 FORCE_CONSTANTS 文件中的力常数矩阵提取和计算力常数的迹（trace），最终输出每对原子间的几何距离和相应的力常数迹，用于分析材料中的力常数矩阵随原子间距离的变化。
## 波恩有效电荷微扰计算
波恩有效电荷及介电常数计算需要准备的文件包括：
```
BTE-EpsilonBorn.sh  INCAR  KPOINTS  POSCAR POTCAR  vasp任务提交脚本
```
其中INCAR、KPOINTS、POTCAR文件可以通过vaspkit并手动修改参数生成，这里不再赘述。提交vasp计算任务并等待计算结束，接下来可以通过调用btekit命令获取BTE-EpsilonBorn.sh，从OUTCAR文件中读取结果：
```
(base) [user@server ~/C/calc-standard-qsub/phonopy]$BTEKit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 5

Select an Epsilon-Born-related task:
1: BTE-EpsilonBorn.sh
Enter the number for the task you want to execute: 1
BTE-EpsilonBorn.sh has been generated in /public/home/user/calc-standard-qsub/epsilon-born
```
通过执行命令：
```
bash BTE-EpsilonBorn.sh
```
可以得到用于编辑BTE计算所用CONTROL文件的计算结果信息，例如对于石墨烯，生成结果如下：
```
epsilon(:,1)=5.588515 0.000000 -0.000000
epsilon(:,2)=0.000000 5.588515 0.000000
epsilon(:,3)=-0.000000 -0.000000 1.115895
born(:,1,1)=0.02406 0.00000 0.00000
born(:,2,1)=-0.02255 0.01546 0.00000
born(:,3,1)=0.00000 -0.00000 0.00010
born(:,1,2)=0.00680 0.00000 0.00000
born(:,2,2)=0.02255 0.01546 0.00000
born(:,3,2)=-0.00000 0.00000 0.00010
```
3.4 BTE计算热输运性质
（1）相关脚本调用：
调用方法如下，输入数字3并且选择所需的脚本文件，即可自动生成对应文件。
```
FORCE_CONSTANTS_2ND  FORCE_CONSTANTS_3RD  CONTROL文件  bte任务提交脚本
```
可选的功能如下：
```
(base) [user@server ~/benchmark/shengbte]$ btekit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 3

Select a BTE-related task:
1: BTE2quantity.sh
2: BTE.boundaryRescale.sh
3: BTE-poscar.sh
4: BTE-RestructBTE.sh
5: BTE-scatter-process.sh
6: BTE-scatter.py
7: BTE-scatter2.py
8: BTE-scatter3.py
9: BTE-scatter4.py
10: BTE-scatter5.py
11: BTE-scatterNU.py
12: BTE-scatterNU-new.py
13: BTE-T-inc.sh
14: BTE-T-inc-collect.sh
15: BTE-testQgrid.sh
16: GruneisenPlot.sh
Enter the number for the BTE task you want to execute:
```
（2）输入文件准备：
```
FORCE_CONSTANTS_2ND  FORCE_CONSTANTS_3RD  CONTROL文件  bte任务提交脚本
```
其中FORCE_CONSTANTS_2ND代表二阶力常数计算结果，FORCE_CONSTANTS_3RD代表三阶力常数计算结果；CONTROL文件部分内容需要手动编写，结构信息可以通过脚本BTE-poscar.sh提取。首先将结构优化后的CONTCAR文件复制到BTE文件夹中，重命名为POSCAR，然后选择
功能3：
```
3: BTE-poscar.sh
```
来读取编写CONTROL文件所需的结构信息。以石墨烯为例，得到的数值如下：
```
lattvec(:,1)= 2.1366667377693123    1.2336051319783392    0.0000000000000000
lattvec(:,2)= -2.1366667377693123    1.2336051319783392    0.0000000000000000
lattvec(:,3)= 0.0000000000000000    0.0000000000000000   20.0000000000000000
positions(:,1)= 0.3333333322770884  0.6666666677257175  0.2660467765596696
positions(:,2)= 0.6666666677251498  0.3333333322758101  0.2660467765596902
positions(:,3)= 
positions(:,4)= 0.00000000E+00  0.00000000E+00  0.00000000E+00
positions(:,5)= 0.00000000E+00  0.00000000E+00  0.00000000E+00
```
而波恩有效电荷数值计算结果则主要通过3.3部分中提到的BTE-EpsilonBorn.sh提取。对于CONTROL文件中ngrid;scalebroad等其他变量的取值，理论上都需要做收敛性测试，具体方法见后续；
（3）结果后处理：提交计算任务，待程序完成运算后可以得到计算结果文件形如BTE.*，相关计算结果文件的详细说明可以参考ShengBTE官网https://bitbucket.org/sousaw/shengbte/src/master/README.md。
通过调用不同的后处理文件可以进一步读取结果，其中：
```
1: BTE2quantity.sh
```
1的主要功能是自动输出包括声子群速度（velocity）, 弛豫时间（relaxation time）, Grüneisen 参数（gruneisen）, 散射相空间（P3）, 热导率（kappa）在内的计算结果，输出如下：
```
(base) [user@server ~/benchmark/shengbte]$ btekit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 3

Select a BTE-related task:
1: BTE2quantity.sh
2: BTE-boundaryRescale.sh
3: BTE-poscar.sh
4: BTE-RestructBTE.sh
5: BTE-scatterNU.py
6: BTE-scatterNU-new.py
7: BTE-scatter-process.sh
8: BTE-T-inc.sh
9: BTE-T-inc-collect.sh
10: BTE-testQgrid.sh
11: GruneisenPlot.sh
Enter the number for the BTE task you want to execute: 1
BTE2quantity.sh has been generated in /public/home/user/benchmark/shengbte
Execution permission has been granted to BTE2quantity.sh
BTE-velocity.py has been generated in /public/home/user/benchmark/shengbte
BTE-relaxationTime.py has been generated in /public/home/user/benchmark/shengbte
BTE-P3.py has been generated in /public/home/user/benchmark/shengbte
BTE-kappa.py has been generated in /public/home/user/benchmark/shengbte
velocity
relaxation time
gruneisen
P3
kappa
```
提取的结果文件包括：
```
velocity.dat
relaxationTime.dat
gruneisen.dat
P3.dat
kappa.dat
```
对于其他输出计算结果的程序功能的简要说明如下：
```
2: BTE.boundaryRescale.sh
```
可以用于获取热导率随系统尺寸的变化曲线，并输出不同尺寸对应的 xx, yy, zz 方向上的热导率值。
```
4: BTE-RestructBTE.sh
```
这段脚本的作用是准备和提交多个目录中的第三阶力常数（3rd-order force constants）计算和ShengBTE任务，具体说明如下：
对于输入文件，需要准备的目录和文件包括：
```
3nd-XXX/：多个第三阶力常数的计算目录
3nd/：基础的第三阶力常数文件夹
shengbte/：ShengBTE计算目录
BTE.bsub：用于提交任务的PBS脚本
```
对于输出文件，包括：
```
FORCE_CONSTANTS_3RD：每个3rd-XXX/目录中会生成第三阶力常数文件
各种ShengBTE输出文件，比如vasprun.xml、热导率相关数据文件等
```
存在两个参数需要特殊设置：
I. $SC="a b c"：三阶力常数计算的网格参数设置。
II. NUMBER=10：表示会创建并提交10个任务，每个任务都对应一个不同的3rd-XXX/目录，可以设置其他取值。
任务说明：
该脚本自动化了$NUMBER个目录下第三阶力常数的生成，并自动链接第三阶力常数文件到ShengBTE目录，最后提交ShengBTE计算任务。
```
5: BTE-scatterNU.py
6: BTE-scatterNU-new.py
```
用于计算：
```
7: BTE-scatter-process.sh
```
可以用于获取散射通道数据（scatter channels），并对数据进行处理、排序和提取，生成针对特定路径的声子分支信息。以下是对其输入文件、输出文件、特殊设置和作用的说明：（缺乏输入文件BTE.scatter报错）
输入文件：
```
NU.dat：包含与声子模式和通道相关的数据。
BTE.scatter：散射率计算结果
```
输出文件：
```
scatter.dat：包含散射率和声子模式信息。
scatter.dat2：从 scatter.dat 文件提取并保存前 343 行的数据。
G-M.dat：包含从 scatter.dat 中沿Gamma-M方向提取的散射数据。
{1..6}.dat：每个声子模式的单独数据文件。
```
从NU.dat 中得到的多个 1.dat 到 6.dat 文件：分别存储NU模式的分支数据。
有一个参数需要特殊设置，即ATOM_NUMBER，代表了系统中原子的数量。需要特殊设置是由于声子分支数量 BRANCH_NUMBER是ATOM_NUMBER的三倍，因此脚本需要根据原子数量计算声子分支数，并提取相关数据。
```
8: BTE-T-inc.sh
```
I.准备输入文件：
```
CONTROL	FORCE_CONSTANTS_2ND	  FORCE_CONSTANTS_3RD
```
II.选择3: BTE relative results read中的功能8，可以自动执行脚BTE-T-inc.sh，计算温度区间在（50,800）之内，间隔区间为25的所有热导率结果。
III.自动批量生成计算任务文件夹，并提交ShengBTE计算任务。
```
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-50
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-75
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-100
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-125
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-150
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-175
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-200
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-225
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-250
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-275
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-300
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-325
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-350
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-375
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-400
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-425
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-450
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-475
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-500
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-525
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-550
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-575
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-600
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-625
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-650
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-675
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-700
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-725
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-750
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-775
/public/home/user/graphene_2023/graphene-PBE-benchmark/shengbte/T-inc/T-800
```
IV.输出结果：每个文件夹下包含的内容如下：
```
BTE.out: ShengBTE 计算的标准输出文件，包含计算过程的详细信息。
BTE.err: ShengBTE 计算的错误输出文件，用于调试和分析错误。
BTE.kappa_tensor: 包含热导率张量（Iterative 和 RTA 方法）的文件。
BTE.kappa: 包含各个声子分支的热导贡献的数据文件。
```
V.使用功能：
```
9: BTE-T-inc-collect.sh
```
来收集计算文件夹T-inc下的所有计算结果，并生成文ThermalConductivity-T.txt，包含不同温度下的热导率以及各个声子分支（如 ZA、TA、LA 等）的贡献，按照温度从 TEMP_INC 范围内的值进行记录。
功能：
```
11: "BTE-gruneisen.py
```
主要用于处理ShengBTE计算结果文件BTE.omega和BTE.gruneisen，输出文本结果的每一行都包含了两个值：频率值（Hz），以及对应的Grüneisen参数，用于进一步画图分析Grüneisen参数随着频率的变化情况。
（4）关于收敛测试：
提供了功能
```
10: BTE-testQgrid.sh
```
来辅助测试 Q 空间格子取点的收敛性，用于材料热导率计算中的格子点密度优化。执行这一脚本可以通过更改 CONTROL中的ngrid 的值，生成不同密度的 q 点格子，并使用 ShengBTE 进行不同热导率计算，最后收集热导率张量的数据。
脚本可以手动设置GRID参数来设置CONTROL中的ngrid 的值。默认值为GRID='1 1 20'，定义了 q 空间的格子点数范围，q 点密度范围从 1 到 20，表示二维或者三维 q 空间的网格。
最后，通过收集计算结果：从各个 grid-$grid 目录中提取 BTE.kappa_tensor 文件的数据，收集对应热导率张量并输出到 Qgrids.dat 文件中，用于后续分析格子点数对计算结果的影响。
## 弹性常数计算（能量-应变法）
如果采用能量-应变法计算弹性常数，则需要脚本辅助生成不同应变范围内的计算文件夹。采用功能4-1可以方便的生成计算任务，如下：
```
(base) [weiyi22@server ~/graphene_2023/graphene-PBE-benchmark/elastic]$ btekit
Select a category:
1: phonopy calculation
2: 3rd_order calculation
3: BTE relative results read
4: elastic_constants calculation submit
5: epsilon-born results read
Enter the number for the category you want to choose: 4

Select an Elastic-related task:
1: cal_ela.sh
Enter the number for the task you want to execute: 1
cal_ela.sh has been generated in /public/home/user/graphene_2023/graphene-PBE-benchmark/elastic
Execution permission has been granted to cal_ela.sh
```
执行完毕后会自动生成脚本cal_ela.sh。
调用vaspkit-201可以生成不同应变范围内，不同应变方向对应的计算文件夹。接下来利用我们的脚本cal_ela.sh即可提交所有文件夹下的计算任务。

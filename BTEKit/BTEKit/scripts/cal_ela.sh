# 弹性性质计算
#!/bin/bash
root_path=`pwd`
for cij in `ls -F | grep /$`
do
  cd ${root_path}/$cij
  for s in strain_*
  do
    cd ${root_path}/$cij/$s
echo `pwd`
    cp ../../vasp.slurm .
#  ./vasp.slurm
# 上面两行vasp.job 替换为 超算运算的脚本文件名
sbatch vasp.slurm
# Add here your vasp_submit_job_script     把这一行替换为提交运算的命令
  done
done
cd ${root_path}

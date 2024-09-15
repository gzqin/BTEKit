#!/bin/bash

echo velocity
python BTE-velocity.py >|velocity.dat
echo relaxation time
python BTE-relaxationTime.py >|relaxationTime.dat
echo gruneisen
python BTE-gruneisen.py >|gruneisen.dat
echo P3
python BTE-P3.py >|P3.dat
echo kappa
python BTE-kappa.py >|kappa.dat

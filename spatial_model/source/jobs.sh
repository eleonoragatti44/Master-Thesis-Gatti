# echo -e "31 deg\n"
# python3 main.py run --name_datetime=_31deg --angular_thresh=0.54105206812 --num_replicates=1000
# echo -e "32 deg\n"
# python3 main.py run --name_datetime=_32deg --angular_thresh=0.55850536064 --num_replicates=1000
# echo -e "33 deg\n"
# python3 main.py run --name_datetime=_33deg --angular_thresh=0.57595865316 --num_replicates=1000
# echo -e "34 deg\n"
# python3 main.py run --name_datetime=_34deg --angular_thresh=0.59341194568 --num_replicates=1000
echo -e "1b\n"
python3 main.py run --name_datetime=_b1 --angular_thresh=0.6981317008 --beta=1 --num_replicates=100
echo -e "2b\n"
python3 main.py run --name_datetime=_b2 --angular_thresh=0.6981317008 --beta=2 --num_replicates=100
echo -e "4b\n"
python3 main.py run --name_datetime=_b4 --angular_thresh=0.6981317008 --beta=4 --num_replicates=100
echo -e "6b\n"
python3 main.py run --name_datetime=_b6 --angular_thresh=0.6981317008 --beta=6 --num_replicates=100
echo -e "8b\n"
python3 main.py run --name_datetime=_b8 --angular_thresh=0.6981317008 --beta=8 --num_replicates=100
echo -e "10b\n"
python3 main.py run --name_datetime=_b10 --angular_thresh=0.6981317008 --beta=10 --num_replicates=100
echo -e "20b\n"
python3 main.py run --name_datetime=_b20 --angular_thresh=0.6981317008 --beta=20 --num_replicates=100
echo -e "40b\n"
python3 main.py run --name_datetime=_b40 --angular_thresh=0.6981317008 --beta=40 --num_replicates=100
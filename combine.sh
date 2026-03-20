#!/bin/bash

prefix='wuv_'
output_prefix='wuvimg_'
start_num=0
num_images=7500
image_count=0

while [[ $start_num -lt num_images ]]
do
	echo $start_num
	./ffmpeg -i "$prefix$start_num.png" -i "$prefix$((++start_num)).png" -i "$prefix$((++start_num)).png" -i "$prefix$((++start_num)).png" -filter_complex "[0:v][1:v]blend=all_expr='if(lt(A,0.9*B),A,B)'[blend1]; [blend1][2:v]blend=all_expr='if(lt(A,0.9*B),A,B)'[blend2]; [blend2][3:v]blend=all_expr='if(lt(A,0.9*B),A,B)'" "$output_prefix$image_count.png"

	((start_num++))
	((image_count++))

done	

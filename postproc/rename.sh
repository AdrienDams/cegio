for year in {1980..1995}; do
 echo $year
 for month in {1..9}; do
  echo $month
  mv arctic446x450_002.clm2.h0.${year}-0${month}.nc arctic446x450_003.clm2.h0.${year}-0${month}.nc
 done
 for month in {10..12}; do
  echo $month
  mv arctic446x450_002.clm2.h0.${year}-${month}.nc arctic446x450_003.clm2.h0.${year}-${month}.nc
 done
done

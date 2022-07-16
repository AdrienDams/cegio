#!/bin/bash

## ~~~~~~~~~~~~~~~~~~~~~~~~~ start user input ~~~~~~~~~~~~~~~~~~~~~~~~~
# HINT:
#   * You can change the values right of the "=" as you wish.
#   * The "%j" in the log file names means that the job id will be inserted

#SBATCH --job-name=test_slk_job   # Specify job name
#SBATCH --output=test_job.o%j    # name for standard output log file
#SBATCH --error=test_job.e%j     # name for standard error output log file
#SBATCH --partition=shared     # Specify partition name
#SBATCH --ntasks=1             # Specify max. number of tasks to be invoked
#SBATCH --time=48:00:00        # Set a limit on the total run time
#SBATCH --account=aa0049       # Charge resources on this project account
## ~~~~~~~~~~~~~~~~~~~~~~~~~ end user input ~~~~~~~~~~~~~~~~~~~~~~~~~

casenum=arctic446x450_003
source_folder=/work/aa0049/a271098/archive/${casenum}/lnd/hist/monthly
target_namespace=/arch/aa0049/$USER/CTSM/${casenum}/lnd/hist/monthly

echo "doing 'slk archive -R ${source_folder} ${target_namespace}'"
slk archive -R ${source_folder}/* ${target_namespace}

# '$?' captures the exit code of the previous command
if [ $? -ne 0 ]; then
 echo "an error occurred in slk archive call"
else
 echo "archival successful"
fi

# slk list ${target_namespace} | cat

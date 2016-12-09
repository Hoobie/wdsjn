:: For Windows only

SET RESULTS_PATH=///c/Users/hoobie/Source/Repos/wdsjn/results/:/usr/src/app/results/

ECHO Rebuild Docker image
CALL docker build -t wdsjn .

ECHO Run container
CALL docker run -v %RESULTS_PATH% -it --rm wdsjn

:: For Windows only

ECHO Rebuild Docker image
CALL docker build -t wdsjn .

ECHO Run container
CALL docker run -v ///c/Users/hoobie/Source/Repos/wdsjn/results/:/usr/src/app/results/ -it --rm wdsjn

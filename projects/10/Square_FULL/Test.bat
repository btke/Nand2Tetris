@echo off 
cd "C:\Users\justm\OneDrive\CS\Nand2Tetris\nand2tetris\tools"
echo on 
call TextComparer ../projects/10/Square_FULL/Main.xml ../projects/10/Square_FULL/MainCmp.xml 
call TextComparer ../projects/10/Square_FULL/SquareGame.xml ../projects/10/Square_FULL/SquareGameCmp.xml 
call TextComparer ../projects/10/Square_FULL/Square.xml ../projects/10/Square_FULL/SquareCmp.xml 
echo on 
pause
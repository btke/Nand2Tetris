@echo off 
cd "C:\Users\justm\OneDrive\CS\Nand2Tetris\nand2tetris\tools"
echo on 
call TextComparer ../projects/10/Square_TK/MainT.xml ../projects/10/Square_TK/MainCmp.xml 
call TextComparer ../projects/10/Square_TK/SquareGameT.xml ../projects/10/Square_TK/SquareGameCmp.xml 
call TextComparer ../projects/10/Square_TK/SquareT.xml ../projects/10/Square_TK/SquareCmp.xml 
echo on 
pause
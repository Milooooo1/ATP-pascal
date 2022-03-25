PROGRAM example;

function aMinB(a, b): integer;
var
    c : integer;
begin
    c = a - b
    result = c
end;

function aPlusB(a, b): integer;
begin
    result = a + b
end;

function odd(n): integer;
var
    nMinEen : integer;
begin
    if (n <= 0) then
        result = 0
    else 
        nMinEen = n - 1
        result = even(nMinEen)
    end;
end;

function even(n): integer;
var
    nMinEen : integer;
begin
    if(n <= 0) then
        result = 1
    else
        nMinEen = n - 1
        result = odd(nMinEen)
    end;
end;


VAR
    a : integer;
    b : integer;
    c : integer;
BEGIN
    b = 2
    a = ((4 - b) + (b - 1)) + (4 * 4)
    printInt()
    c = aMinB(a, 4)
    printInt()
    odd(9)
    printInt()
    if (c >= 0) THEN
        if( c <= 10) THEN
            c = 1
        else
            c = 2
        end;
    else
        c = 3
    end;
    printInt()
END.
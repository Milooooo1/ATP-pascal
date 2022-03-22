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
    {a = (4 + (2 + 2)) * (3 - 1)
    b = 6
    c = 2 + b}
    {b = 10
    c = (2 + 2)
    c = ((a + b) * (60 / (2 + 8)))
    c = aMinB(6, 5)
    WHILE (a < b) DO
    BEGIN
        a = a + 1
    END;

    IF (a < 0) THEN
        a = (10 + a) / 2
        a + 2
    ELSE
        IF (b > 2) THEN
            c = (2 / 2) > 6
        ELSE
            c = 2
        END;
        a = 100
    END;
    a = 9
    b = odd(a)}

END.
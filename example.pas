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
end; {end of myfunction}

VAR
    a : integer;
    b : integer;
    c : integer;
BEGIN
    a = 1
    b = 10
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

END.
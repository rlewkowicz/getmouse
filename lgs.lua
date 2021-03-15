mouse = 0
active = 0
x = 0
y = 0
xdir = 0
ydir = 0
counterx = 0
countery = 0

function getfiles()
    mouse = dofile[[R:\mouse.lua]]
    active = dofile[[R:\active.lua]]
    x, y, xdir, ydir = dofile[[R:\xy.lua]]
    while x == nil or y == nil or mouse == nil or xdir == nil or ydir==nil do
        x, y, xdir, ydir = dofile[[R:\xy.lua]]
        mouse = dofile[[R:\mouse.lua]]
    end
    while active == nil do
        active = dofile[[R:\active.lua]]
    end
end

function OnEvent(event, arg)
    start = 1
    initx = 1
    inity = 1
    while 1==1 do
        pcall(getfiles)
        Sleep(1)
        if active == 1 then
            if mouse > 2 then
                PressMouseButton( 1 )
                if counterx > 0 then 
                    if initx == 1 then
                        initx = 0
                        -- MoveMouseRelative( xdir, 0 )
                    end
                    counterx = counterx-1
                else
                    MoveMouseRelative( xdir, 0 )
                    counterx = x
                end

                if countery > 0 then 
                    if inity == 1 then
                        inity = 0
                        -- MoveMouseRelative( 0, ydir )
                    end
                    countery = countery-1
                   -- OutputLogMessage(countery .. "\n")
                else
                    MoveMouseRelative( 0, ydir )
                    countery = y
                end

            else
                ReleaseMouseButton( 1 )
                counterx = x
                countery = y
                inity = 1
                initx = 1
            end
        end
    end    
end

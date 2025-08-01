local filestr = {}

function filestr.fileExists(path)
    if not fs.exists(path) then        
        local fname = fs.getName(path)
        path = shell.dir().."/"..fname
        
        if not fs.exists(path) then        
            print("File not found!")
            return nil
        end
    end
    
    return path
end

function filestr.fileToString(path)
    local file = fs.open(path, "r")
    
    if not file then error("File not found") end 
    
    local content = ""    
    
    local line = file.readLine()
    while line ~= nil do
        content = content..line.."\n"
        line = file.readLine()
    end
    
    return content
end

return filestr

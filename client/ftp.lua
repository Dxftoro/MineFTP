local args = {...}

local filestr = require("filestr")

if not args[1] then
    error("No such args!")
end

-- CLIENT-AVAIBLE ROUTES
local fileSendUrl = "http://26.70.26.159:5000/ftp"

-- ARGUMENTS
local method = args[1]
local path = args[2]

-- REQUEST METHODS AND UTILITIES
if method == "post" then
    local configPath = filestr.fileExists("userconfig.json")
    local user = "unknown"
    
    if configPath ~= nil then
        local configString = filestr.fileToString(configPath)
        local config = textutils.unserialiseJSON(configString)
        user = config["user"]
    end
    
    path = filestr.fileExists(path)
    print("Uploading "..path.."...")

    local file = fs.open(path, "r")
    if not file then error("File not found!") end

    local filename = fs.getName(path)
    local content = filestr.fileToString(path)

    local urlSafeContent = textutils.urlEncode(content)
    local postData = "user="..user..
                     "&filename="..filename..
                     "&content="..urlSafeContent

    local response = http.post(fileSendUrl, postData)
    print(response.readAll())
    
elseif method == "get" then
    print("Trying to get \""..path.."\" from the server...")
    local getRequest = fileSendUrl.."?path="..path
    
    local response = http.get(getRequest)
    local content = response.readAll()
    
    local file = fs.open(shell.dir().."/"..path, "w")
    file.write(content)
    file.close()
    
    print("File \""..path.."\" saved!")

-- LIST ALL FILES LOADED ON SERVER
elseif method == "ls" then
    print("List of files:")
    print("===============================")
    local getRequest = fileSendUrl.."?path=ls"
    local response = http.get(getRequest)
    
    print(response.readAll())
end 

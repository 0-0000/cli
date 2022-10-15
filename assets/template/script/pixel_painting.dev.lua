---Create a block Pixel Painting.



---Print standard log
---@param level string Log type.
---@param content string Log content
local function log(level, content)
  if level == "fatal" then
    level = "#R[dm][fatal]"
    -- Show error message.
    Game:msgBox("#RDev-Mini-cli Error:\n\t" .. content .. "#n")
  elseif level == "error" then
    level = "#R[dm][error]"
  elseif level == "warning" then
    level = "#Y[dm][warning]"
  elseif level == "info"  then
    level = "#B[dm][info]"
  else -- Debug message.
    print("[dm][debug]" .. content)
    return
  end
  content = level .. content .. "#n"
  print(content)
  Chat:sendSystemMsg(content) -- Show message in the chat box.
end


-- Check script scope.
if _dm_type ~= nil then
  log("fatal", "Do not merge multiple scripts!")
  error("Do not merge multiple scripts!")
end

-- Define vars.
local _dm_type = "PixelPainting"
local _dm_position = {
  x = [[$POSITION_X]],
  y = [[$POSITION_Y]],
  z = [[$POSITION_Z]]
}
local _dm_size = { width = [[$SIZE_WIDTH]], height = [[$SIZE_HEIGHT]] }
local _dm_painting = [[$PAITING]]
local _dm_block_id = [[$BLOCK_ID]]

---Place a block.
---@param id number Block ID.
---@param color number RGB.
---@param position table Given x, y, z.
---@return boolean result Create successfully.
local function place_block(id, color, position)
  ---@todo(KaiKai) Check whether here is a block, and return false if there is.
  return (Block:placeBlock(id, position.x, position.y, position.z, 5, color)
          == ErrorCode.OK)
end


local function make()
  local height = _dm_size.height
  for x, tab in pairs(_dm_painting) do
    for y, id in pairs(tab) do
      place_block(_dm_block_id, id, {
        x = _dm_position.x + x - 1,
        y = _dm_position.y + y - 1,
        z = _dm_position.z
      })
    end
  end
end


---Entry.
local function main()
  log("info", "Start creating Pixel Painting.")
  make()
  log("info", "Pixel Painting created successfully.")
end



ScriptSupportEvent:registerEvent("Game.Start", main)
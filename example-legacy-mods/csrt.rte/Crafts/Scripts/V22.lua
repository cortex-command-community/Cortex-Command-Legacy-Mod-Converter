
dofile("CSRT.rte/Constants.lua")
require("Crafts/Scripts/NativeV22")
--dofile("CSRT.rte/Crafts/Scripts/NativeV22.lua")

function Create(self)
	self.AI = NativeDropShipAI:Create(self)
end

function UpdateAI(self)
	self.AI:Update(self)
end

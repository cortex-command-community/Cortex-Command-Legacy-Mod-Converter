-- originally created by clunatic, modified by chiko
dofile("Base.rte/Constants.lua")
dofile("ScrapperFaction.rte/Actors/Basic/MeleeAI/OldNativeHumanAI.lua")		--Change this to point to the right location

function Create(self)
	self.AI = MeleeNativeHumanAI:Create(self)
end

function UpdateAI(self)
	self.AI:Update(self)
end

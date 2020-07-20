-- who in the sam hell thought it was a good idea to give those special ed kids access to guns?
-- originally created by clunatic, modified by chiko
dofile("Base.rte/Constants.lua")
dofile("ScrapperFaction.rte/Actors/Basic/MeleeAI/OldNativeHumanAI.lua")		--Change this to point to the right location

function Create(self)
	self.AI = MeleeNativeHumanAI:Create(self)
end

function Update(self)
	if self:IsPlayerControlled() == true then
		self.IgnoresTeamHits = false
	else
		self.IgnoresTeamHits = true
	end
end

function UpdateAI(self)
	self.AI:Update(self)
end

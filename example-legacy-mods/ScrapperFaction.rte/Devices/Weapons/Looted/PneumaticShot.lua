function Create(self)
	local Effect
	local Offset = self.Vel*(20*TimerMan.DeltaTimeSecs)	-- the effect will be created the next frame so move it one frame backwards towards the barrel
	
	-- bullets
	for i = 1, 4 do
		Effect = CreateMOPixel("Particle Looted Pneumatic Gun", "ScrapperFaction.rte")
		if Effect then
			Effect.Vel = self.Vel
			Effect.Pos = self.Pos
			Effect.Team = self.Team
			Effect.IgnoresTeamHits = true
			MovableMan:AddParticle(Effect)
		end
	end
	
	-- smoke forward
	for i = 1, 4 do
		Effect = CreateMOSParticle("Small Smoke Ball 1", "Base.rte")	-- ("Side Thruster Blast Ball 1", "Base.rte")
		if Effect then
			Effect.Vel = self:RotateOffset(Vector(RangeRand(6,9),RangeRand(-3,3)))
			Effect.Pos = self.Pos - Offset
			MovableMan:AddParticle(Effect)
		end
	end
	
end

function Update(self)
	local Effect
	local Offset = self.Vel*(20*TimerMan.DeltaTimeSecs)	-- the effect will be created the next frame so move it one frame backwards towards the barrel
	
end

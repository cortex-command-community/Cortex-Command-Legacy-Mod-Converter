
function Update(self)

-- note i moved everything to update. function Create happens once when the thing appears into existence
-- Update is on every single frame, thats how you make stuff actually happen

	if self.HFlipped then
	-- if we are facing to the left
		self.negNum = -1;
		-- this number is used to multiply stuff below so its actually to the left or right properly
		-- if we skipped this stuff would always go to the right
	else
		self.negNum = 1;
	end

	local Effect
	-- declare Effect as a local variable so it isnt literally game-wide
	-- we could also do self.Effect everywhere below and avoid this step but who cares
	local NailEffect

	if self.FiredFrame then
		-- bullets
		for i = 1, 1 do
		
			Effect = CreateMOPixel("Particle Looted Nailgun", "ScrapperFaction.rte")
			if Effect then
				Effect.Pos = self.MuzzlePos;
				-- obvious
				Effect.Vel = (self.Vel) + (Vector(0, RangeRand(-5,5)) + Vector(100*self.negNum,0)):RadRotate(self.RotAngle) -- note the parantheses, important
				-- first the nail has the same velocity as the gun, relativity and all that
				-- then we give it some randomization up and down
				-- after that we give it a big boost in the direction it should actually go (i.e. away from the gun), so the 100, previously 230 and 150 but edited to fix the nail sticking physics, is basically FireVel
				-- randomization and big boost are both rotated according to the gun's angle
				Effect.Team = self.Team -- self.Team is the gun's team. should be correct unless it's like on the ground and somehow fired
				Effect.IgnoresTeamHits = true
				-- no need for ignoresteamhits, friendly fire global script handles that i think --actually without ignoresteamhits it damages allies and even your actor
				MovableMan:AddParticle(Effect)
			end
				
			NailEffect = CreateMOSRotating("Shot Looted Nailgun", "ScrapperFaction.rte")
			if NailEffect then
				NailEffect.Pos = self.MuzzlePos;
				NailEffect.Vel = Effect.Vel -- exact same stuff as the actual bullet above
				NailEffect.Team = self.Team
				MovableMan:AddParticle(NailEffect)								
			end
			
		end
	
		-- smoke
		for i = 1, 2 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.MuzzlePos;
				-- obvious
				Effect.Vel = (self.Vel + Vector(RangeRand(-20,20), RangeRand(-20,20)) + Vector(100*self.negNum,0):RadRotate(self.RotAngle)) / 30
				-- same stuff as the nail except the randomization isnt tied to the gun's rot angle and is also heavier
				-- finally we divide everything by 30 because the values are very big by default.
				-- messing with that last number will make the smoke faster or slower
				Effect.Team = self.Team
				MovableMan:AddParticle(Effect)
			end
		end
	end	
end

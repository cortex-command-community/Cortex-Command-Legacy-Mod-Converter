function Create(self)
	self.goldPerCoin = 1;
	
	self.updateTimer = Timer();
	self.updateDelay = 300;	-- Time window to pickup after dropped
end
function Update(self)
	self.RotAngle = 0;
	local parent = self:GetParent();
	if self.FiredFrame or (self.updateTimer:IsPastSimMS(self.updateDelay) and not parent) then
		self.updateDelay = 17;	-- New update delay
		self.updateTimer:Reset();
		for actor in MovableMan.Actors do
			if actor.ClassName ~= "ACRocket" and actor.ClassName ~= "ACDropShip" and actor.ClassName ~= "ADoor" then
				local dist = SceneMan:ShortestDistance(actor.Pos, self.Pos, SceneMan.SceneWrapsX);
				if dist.Magnitude < (self.Radius + actor.Radius) then
					local particleCount = 3;
					for i = 1, particleCount do
						local part = CreateMOSParticle("Mario.rte/Sparkle");
						part.Pos = self.Pos + Vector(self.Radius * (i / particleCount), 0):RadRotate(6.28 * math.random());
						part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
						MovableMan:AddParticle(part);
					end
					ActivityMan:GetActivity():SetTeamFunds(ActivityMan:GetActivity():GetTeamFunds(actor.Team) + self:GetGoldValue(0, 1, 1), actor.Team);
					AudioMan:PlaySound("Base.rte/GUIs/Sounds/Poing".. math.random(6) ..".wav", SceneMan:TargetDistanceScalar(actor.Pos), false, false, -1);
					self.ToDelete = true;
				end
			end
		end
	elseif parent then
		self.updateTimer:Reset();
		self.updateDelay = 300;
	end
end
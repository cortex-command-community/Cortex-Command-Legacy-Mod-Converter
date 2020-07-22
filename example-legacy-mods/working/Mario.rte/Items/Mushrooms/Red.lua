function Create(self)
	self.moveSpeed = 5;
	self.updateTimer = Timer();
	self.updateDelay = 300;	-- Time window to pickup after dropped
end
function Update(self)
	self.Vel.X = self.moveSpeed * (self.Vel.X / math.abs(self.Vel.X));
	self.AngularVel = self.AngularVel / 2;
	self.RotAngle = 0;
	local parent = self:GetParent();
	elseif self.FiredFrame or (self.updateTimer:IsPastSimMS(self.updateDelay) and not parent) then
		self.updateDelay = 17;	-- New update delay
		self.updateTimer:Reset();
		local terrCheck = SceneMan:GetTerrMatter(self.Pos.X, self.Pos.Y + 8);
		if terrCheck ~= 0 then
			self.Vel.Y = self.Vel.Y / 2 - 1;	-- Lift from ground
		end
		for actor in MovableMan.Actors do
			if actor.ClassName ~= "ACRocket" and actor.ClassName ~= "ACDropShip" and actor.ClassName ~= "ADoor" then
				local dist = SceneMan:ShortestDistance(actor.Pos, self.Pos, SceneMan.SceneWrapsX);
				if dist.Magnitude < (self.Radius + actor.Radius) then
					actor:SetNumberValue("1UPs", actor:GetNumberValue("1UPs") + 1);
					AudioMan:PlaySound("Mario.rte/Sounds/smw/smw_power-up.wav ", SceneMan:TargetDistanceScalar(actor.Pos), false, false, -1);
					local particleCount = 3;
					for i = 1, particleCount do
						local part = CreateMOSParticle("Mario.rte/Sparkle");
						part.Pos = self.Pos + Vector(self.Radius * (i / particleCount), 0):RadRotate(6.28 * math.random());
						part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
						MovableMan:AddParticle(part);
					end
					local part = CreateMOSParticle("Mario.rte/1UP Effect");
					part.Pos = self.AboveHUDPos + Vector(0, 5);
					MovableMan:AddParticle(part);
					actor:FlashWhite(50);
					if not actor:NumberValueExists("Red Mushroom") then
						actor:SetNumberValue("Red Mushroom", 1);
						actor.MaxHealth = actor.MaxHealth * 2;
						actor.GibImpulseLimit = actor.GibImpulseLimit * 1.5;
						actor.ImpulseDamageThreshold = actor.ImpulseDamageThreshold * 1.5;
					end
					actor.Health = math.min(actor.Health * 1.5 + 50, actor.MaxHealth);
					actor:RemoveAnyRandomWounds(99);
					self.ToDelete = true;
					break;
				end
			end
		end
	elseif parent then
		self.updateTimer:Reset();
		self.updateDelay = 300;
	end
end
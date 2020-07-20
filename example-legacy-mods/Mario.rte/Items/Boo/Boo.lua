function Create(self)
	self.moveSpeed = 1;
	self.attackStrength = 30;
	self.searchRange = FrameMan.ResX * 0.4;
	self.updateTimer = Timer();
	
	self.phase = 0;
end
function Update(self)
	self.Vel = self.Vel * 0.9;
	if self.updateTimer:IsPastSimMS(100) then
		self.updateTimer:Reset();
		local dist = Vector(0, 0);
		local actor = MovableMan:GetClosestEnemyActor(self.Team, self.Pos, self.searchRange, dist);
		if actor and actor.Status < 2 then
			if math.abs(dist.AbsRadAngle - actor:GetAimAngle(false)) > 1.5 then
				self.target = actor;
				self.phase = 1;
			else	-- The actor is looking towards the Boo
				self.phase = 2;
			end
		else
			self.phase = 0;
			local part = CreateMOPixel("Mario.rte/Boo Glow ".. self.phase);	-- Fade out
			part.Pos = self.Pos;
			MovableMan:AddParticle(part);
		end
	end
	if self.target and IsActor(self.target) then
		local dist = SceneMan:ShortestDistance(self.Pos, self.target.Pos, SceneMan.SceneWrapsX);
		if dist.Magnitude < self.searchRange then
			local attackRange = self.Radius + self.target.Radius;
			if dist.Magnitude < attackRange then
				self.target.Status = 1;
				local size = math.sqrt(self.target.Mass * 0.3 + 1);
				self.target.Vel = self.target.Vel + dist:SetMagnitude(self.attackStrength / size);
				self.Vel = Vector(-dist.X, -dist.Y):SetMagnitude(attackRange * (1 / size));
			else
				self.Vel = self.Vel + dist:SetMagnitude(self.moveSpeed);
			end
		else
			self.target = nil;
		end
	else
		self.target = nil;
	end
	if self.phase ~= 0 then
		local gfx = CreateMOPixel("Mario.rte/Boo Glow ".. self.phase);
		gfx.Pos = self.Pos;
		MovableMan:AddParticle(gfx);
	end
end
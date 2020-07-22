function Create(self)
	self.checkDelay = 600;
	self.range = 100;
	self.checkTimer = Timer();
	self.spitTimer = Timer();	-- for manual attacks
	
	self.lastWoundCount = 0;
end
function Update(self)
	local parent = self:GetParent();
	if parent and IsActor(parent) and ToActor(parent).Status == 0 and ToActor(parent).Health > 0 then
		parent = ToActor(parent);
		local spit = false;
		local healthFactor = 1 + parent.Health * 0.1;
		local aimTrace = Vector(self.range, 0):RadRotate(parent:GetAimAngle(true));
		if parent:GetController():IsState(Controller.WEAPON_FIRE) or (self.WoundCount > self.lastWoundCount and self.WoundCount <= self.GibWoundLimit) then
			spit = true;
		elseif self.checkTimer:IsPastSimMS(self.checkDelay) then
			parent.Frame = 0;
			self.Frame = math.random(self.FrameCount - 1) - 1;
			self.checkDelay = 6000 / healthFactor;
			self.range = 10 * healthFactor;
			-- find an enemy and spit at them
			local moRay = SceneMan:CastMORay(self.Pos, aimTrace, self.ID, self.Team, 0, false, math.sqrt(self.range) / 2);
			if moRay ~= 255 then
				local mo = MovableMan:GetMOFromID(MovableMan:GetMOFromID(moRay).RootID);
				if mo and IsActor(mo) then
					spit = true;
				end
			end
			self.checkTimer:Reset();
		end
		if spit and self.spitTimer:IsPastSimMS(self.checkDelay) then
			self.spitTimer:Reset();
			self.Frame = 2;	parent.Frame = 1;	-- mouth wide open, stomach drawn in
			local partCount = 10 + healthFactor;
			local partSpread = math.sqrt(partCount) * 0.1;	-- in rad
			for i = 1, partCount do
				local part = CreateMOPixel("4Z.rte/Spitter Goo ".. math.random(2));
				part.Sharpness = math.random(part.Sharpness, part.Sharpness * 2);
				if i < (partCount * 0.3) then	-- a third of the particles are MOSs with script
					part = CreateMOSParticle("4Z.rte/Spitter Goo");
					part.Lifetime = part.Lifetime * RangeRand(0.5, 1.0);
				end
				part.Pos = self.Pos;
				part.Team = self.Team;	part.IgnoresTeamHits = true;
				part.Vel = self.Vel + Vector(aimTrace.X, aimTrace.Y):RadRotate(RangeRand(-partSpread, partSpread) / 2) * RangeRand(0.1, 0.2);
				MovableMan:AddParticle(part);
			end
			local sounds = {"flesh_squishy_impact_hard2.wav", "flesh_squishy_impact_hard4.wav"};
			AudioMan:PlaySound("4Z.rte/Actors/Zombies/Sounds/".. sounds[math.random(#sounds)], SceneMan:TargetDistanceScalar(self.Pos) + (1 / healthFactor), false, true, -1);
		end
		self.lastWoundCount = self.WoundCount;
	end
end
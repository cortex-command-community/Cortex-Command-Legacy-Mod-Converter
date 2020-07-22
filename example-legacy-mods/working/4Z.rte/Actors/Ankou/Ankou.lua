function Create(self)
	self.flyStrength = 40;
	self.parts = {self, self.Head, self.FGArm, self.FGLeg, self.BGArm, self.BGLeg};
	self.idleOffset = {0, 0, 0, 0};	-- 1 = FGLength, 2 = FGAngle, 3 = BGLength, 4 = BGAngle
	self.updTimerSlow = Timer();	-- updates move paths and legless damage
	
	self.hurtTimer = Timer();
	
	self.lastWoundCount = 0;
end
function Update(self)
	if not self.dead then
		self.ctrl = self:GetController();
		self.Health = self.MaxHealth;
		local negNum = self.HFlipped and -1 or 1;
		--[[ glow
		if math.random(self.MaxHealth) <= self.Health then
			local glow = CreateMOPixel("Glow Red Huge");
			glow.Pos = Vector(self.Pos.X, self.Pos.Y);
			MovableMan:AddParticle(glow);
		end
		for i = 1, #self.parts do
			local part = self.parts[i];
			if part and IsMOSRotating(part) then
				local suffix = "".. part.Frame;
				local negNum = 1;
				if part.HFlipped then
					negNum = -1;
					suffix = "HFlipped ".. part.Frame;
				end
				local glow = CreateMOPixel(part.PresetName .." Glow ".. suffix);
				glow.Pos = part.Pos + Vector((ToMOSprite(part):GetSpriteWidth() / 2 + part.SpriteOffset.X) * negNum, ToMOSprite(part):GetSpriteHeight() / 2 + part.SpriteOffset.Y):RadRotate(part.RotAngle);
				glow.EffectRotAngle = part.RotAngle;
				MovableMan:AddParticle(glow);
			end
		end]]--
		-- destroy items
		if self.EquippedItem and self.ctrl:IsState(Controller.WEAPON_FIRE) then
			if IsHDFirearm(self.EquippedItem) and ToHDFirearm(self.EquippedItem):NeedsReloading() then
				ToMOSRotating(self.EquippedItem):GibThis();
			end
		end
		-- break apart
		if self.TotalWoundCount > self.lastWoundCount then
			for i = 1, #self.parts do
				local part = self.parts[i];
				if part and IsAttachable(part) and part.WoundCount > 0 then
					part.JointStrength = part.JointStrength - 1 * (1 + part.WoundCount + self.WoundCount);
				end
			end
		end
		self.JetTimeLeft = 1;	-- infinite flight
		if self.updTimerSlow:IsPastSimMS(1000) then
			self.updTimerSlow:Reset();
			self:UpdateMovePath();
			--if self.AIMode ~= Actor.AIMODE_BRAINHUNT then
			--	self.AIMode = Actor.AIMODE_BRAINHUNT;
			--end
			if self.Jetpack then
				for em in self.Jetpack.Emissions do
					em.ParticlesPerMinute = self.Mass * self.flyStrength;
					em.BurstSize = self.Mass * (self.flyStrength / 1000);
				end
			end
			local partsTotal = 0;
			for i = 1, #self.parts do
				local part = self.parts[i];
				if part and IsMOSRotating(part) and part.RootID == self.ID then
					partsTotal = partsTotal + 1;
				end
			end
			if partsTotal < 2 then
				self.dead = true;
			end
		end
		self.ctrl:SetState(Controller.AIM_SHARP, false);
		local flail = 1 / (1 + self.Health * 0.1);
		-- flail arms
		for i = 1, #self.idleOffset do
			self.idleOffset[i] = self.idleOffset[i] + math.random() * flail;
		end
		-- pick the MO that spews damage
		local attackMO = self;
		if self.Head then
			attackMO = self.Head;
		end
		if self.BGArm then
			attackMO = self.BGArm;
			if not self.FGArm and self.BGArm.GetsHitByMOs == false then
				self.BGArm.GetsHitByMOs = true;
			else
				self.BGArm.GetsHitByMOs = false;
			end
			ToArm(self.BGArm).IdleOffset = Vector(11 + math.sin(self.idleOffset[3]) + flail, 1):RadRotate(self:GetAimAngle(false) + math.sin(self.idleOffset[4]) * flail);
		end
		if self.FGArm then
			attackMO = self.FGArm;
			ToArm(self.FGArm).IdleOffset = Vector(11 + math.sin(self.idleOffset[1]) + flail, 2):RadRotate(self:GetAimAngle(false) + math.sin(self.idleOffset[2]) * flail);
		end
		if self.Status < 1 and self.hurtTimer:IsPastSimMS(600 - self.Health * 3) then

			local dmg = CreateMOPixel("Particle Claw ".. math.random(2), "4Z.rte");			-- bite
			dmg.Pos = attackMO.Pos;
			dmg.Vel = self.Vel + Vector(50, 0):RadRotate(self:GetAimAngle(true));
			dmg.Team = self.Team;
			dmg.IgnoresTeamHits = true;
			MovableMan:AddParticle(dmg);
		
			self.hurtTimer:Reset();
		end
		if self.FGLeg or self.BGLeg then
			self.ctrl:SetState(Controller.BODY_CROUCH, false);
		else
			if math.random() < 0.1 then
				self.ctrl:SetState(Controller.BODY_CROUCH, false);
			else
				self.ctrl:SetState(Controller.BODY_CROUCH, true);
			end
		end
		if self.ctrl:IsState(Controller.BODY_JUMP) then	-- these mother fuckers fly
			local turn = self.RotAngle + (math.pi / 2 - self:GetAimAngle(false)) * negNum;
			self.AngularVel = self.AngularVel * 0.5 - turn;
			if self.Vel.Magnitude + math.abs(self.AngularVel) > 10 then
				self.Vel = Vector(self.Vel.X, self.Vel.Y) / (1 + self.Vel.Magnitude * 0.01);
			end
			self.ctrl:SetState(Controller.BODY_CROUCH, false);
		elseif math.abs(self.AngularVel) < 20 and self.Status < 1 then	-- don't spin to death okay
			-- "hunch" n stagger a bit
			self.AngularVel = self.AngularVel - (0.2 * math.random() - (self:GetAimAngle(false)) * 0.1) * negNum;
		end
	end
	self.lastWoundCount = self.TotalWoundCount;
end
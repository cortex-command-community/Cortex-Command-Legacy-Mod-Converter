function Create(self)
	self.parts = {self, self.Head, self.FGArm, self.BGArm, self.FGLeg, self.BGLeg};
	self.idleOffset = {0, 0, 0, 0};	-- 1 = FGLength, 2 = FGAngle, 3 = BGLength, 4 = BGAngle
	self.updTimerSlow = Timer();	-- updates move paths and legless damage
end
function Update(self)
	local partsTotal = 0;
	for i = 1, #self.parts do
		local part = self.parts[i];
		if part and IsMOSRotating(part) and part.RootID == self.ID then
			if part.Scale ~= 0 then
				if part.WoundCount < (part.GibWoundLimit / 3) then
					partsTotal = partsTotal + 1;
				else
					part.Scale = 0;
					part:RemoveWounds(part.WoundCount + 1);
					-- fake gibbing
					local gib = CreateMOSRotating(part:GetModuleAndPresetName() .." Gib");
					gib.Pos = part.Pos;
					gib.Vel = part.Vel;
					gib.AngularVel = part.AngularVel;
					MovableMan:AddParticle(gib);
					gib:GibThis();
				end
			end
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
	end
	if partsTotal == 0 then
		for i = 1, #self.parts do
			local part = self.parts[i];
			local suffix = "".. part.Frame;
			local negNum = 1;
			if part.HFlipped then
				negNum = -1;
				suffix = "HFlipped ".. part.Frame;
			end
			if part and IsMOSRotating(part) and part.RootID == self.ID then
				local glow = CreateMOPixel(part.PresetName .." Glow ".. suffix);
				glow.Pos = part.Pos + Vector((ToMOSprite(part):GetSpriteWidth() / 2 + part.SpriteOffset.X) * negNum, ToMOSprite(part):GetSpriteHeight() / 2 + part.SpriteOffset.Y):RadRotate(part.RotAngle);
				glow.EffectRotAngle = part.RotAngle;
				glow.Vel = Vector(part.Vel.X, part.Vel.Y);
				glow.Lifetime = 2000;
				MovableMan:AddParticle(glow);
			end
		end
		self.ToDelete = true;
	else
		self.ctrl = self:GetController();
		self.Health = self.MaxHealth;
		
		if self.EquippedItem and self.ctrl:IsState(Controller.WEAPON_FIRE) then
			local rand = math.random();
			if rand < 0.1 then
				ToMOSRotating(self.EquippedItem):GibThis();
			end
		end
			
		if self.updTimerSlow:IsPastSimMS(1000) then
			self.updTimerSlow:Reset();
			self:UpdateMovePath();
			if self.AIMode ~= Actor.AIMODE_BRAINHUNT then
				self.AIMode = Actor.AIMODE_BRAINHUNT;
			end
			if not (self.FGLeg and self.BGLeg) then
				self.Health = self.Health - 1;
			end
		end
		self.ctrl:SetState(Controller.AIM_SHARP, false);
		local flail = 1 / (1 + self.Health * 0.1);
		-- flail arms
		for i = 1, #self.idleOffset do
			self.idleOffset[i] = self.idleOffset[i] + math.random() * flail;
		end
		if self.FGArm then
			ToArm(self.FGArm).IdleOffset = Vector(11 + math.sin(self.idleOffset[1]) + flail, 2):RadRotate(self:GetAimAngle(false) + math.sin(self.idleOffset[2]) * flail);
		end
		if self.BGArm then
			if (not self.FGArm or self.FGArm.Scale == 0) and self.BGArm.GetsHitByMOs == false then
				self.BGArm.GetsHitByMOs = true;
			else
				self.BGArm.GetsHitByMOs = false;
			end
			ToArm(self.BGArm).IdleOffset = Vector(11 + math.sin(self.idleOffset[3]) + flail, 1):RadRotate(self:GetAimAngle(false) + math.sin(self.idleOffset[4]) * flail);
		end
		if self.FGLeg or self.BGLeg then
			self.ctrl:SetState(Controller.BODY_CROUCH, false);
		else
			self.ctrl:SetState(Controller.BODY_CROUCH, true);
		end
	end
end
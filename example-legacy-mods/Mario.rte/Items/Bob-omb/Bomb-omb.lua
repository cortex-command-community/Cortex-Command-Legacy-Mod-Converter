function Create(self)
	self.dir = 0;
	self.recoveryTimer = Timer();
end
function Update(self)
	if self:IsActivated() then
		local part = CreateMOSParticle("Mario Smoke 1");
		part.Pos = self.Pos;
		MovableMan:AddParticle(part);
		if self.Vel.Magnitude < 5 then
			if self.recoveryTimer:IsPastSimMS(500) then
				self.RotAngle = 0;
				self.AngularVel = -self.dir;
			end
		else
			self.recoveryTimer:Reset();
			if self.Vel.X ~= 0 then
				self.dir = self.Vel.X / math.abs(self.Vel.X);
			end
		end
	end
end
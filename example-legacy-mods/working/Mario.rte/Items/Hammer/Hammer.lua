function Create(self)
	self.origMass = self.Mass;
	self.lastVel = self.Vel.Magnitude;
end
function Update(self)
	if self.ID == self.RootID then
		local negNum = 1;
		if self.HFlipped then
			negNum = -1;
		end
		self.AngularVel = -negNum - self.Vel.Magnitude * negNum;
		self.Mass = self.origMass * 10 + self.Vel.Magnitude;
		if self.lastVel > 5 then
			self.DamageOnCollision = 1;
			local part = CreateMOPixel("Mario.rte/MO Damager");
			part.Vel = self.Vel;
			part.Pos = self.Pos;
			part.Mass = self.Mass;
			part.Sharpness = self.Material.StructuralIntegrity;
			part.Team = self.Team;
			part.IgnoresTeamHits = true;
			MovableMan:AddParticle(part);
		else
			self.DamageOnCollision = 0;
		end
	elseif self.Mass > self.origMass then
		self.Mass = self.origMass;
		self:Deactivate();
	end
	self.lastVel = self.Vel.Magnitude;
end
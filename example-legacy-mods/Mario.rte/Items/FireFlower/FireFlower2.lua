function Create(self)
	self.fireVel = 10;
	self.wasFired = false;
end

function Update(self)
	if parent.EquippedItem and IsHDFirearm(parent.EquippedItem) then
		local weapon = ToHDFirearm(parent.EquippedItem);
		if self.wasFired == true then
			self.wasFired = false;
			local negNum = 1;
			if weapon.HFlipped then
				negNum = -1;
			end
			local checkPos = weapon.MuzzlePos + Vector(self.fireVel / 2, 0):RadRotate(weapon.RotAngle);
			for part in MovableMan.Particles do
				if part.HitsMOs then
					local dist = SceneMan:ShortestDistance(weapon.MuzzlePos, part.Pos, SceneMan.SceneWrapsX);
					if dist < self.fireVel then
						local fireball = CreateMOSParticle("Flame Hurt 1");
						fireball.Pos = part.Pos;
						fireball.Vel = part.Vel;
						fireball.Lifetime = part.Lifetime;
						fireball.GlobalAccScalar = part.GlobalAccScalar;
						fireball.AirResistance = part.AirResistance;
					end
				end
			end
		end
		if weapon.FiredFrame then
			self.wasFired = true;
		else
			self.fireVel = weapon.Radius;
			if weapon.Magazine and weapon.Magazine.NextRound then
				self.fireVel = self.fireVel + weapon.Magazine.NextRound.FireVel;
			end
		end
	end
end
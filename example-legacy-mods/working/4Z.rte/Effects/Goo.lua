function Create(self)
	self.strength = 0.1;
	self.effectTime = self.Lifetime;	-- duration in which effect can still take place, in MS
end
function Update(self)
	if self.Vel.Magnitude > 5 and self.Age < self.effectTime and self.Age > (600 / self.Vel.Magnitude) and math.random(self.effectTime) > self.Age then
		local checkPos = self.Pos + Vector(self.Vel.X, self.Vel.Y) * 0.3;
		local moCheck = SceneMan:GetMOIDPixel(checkPos.X, checkPos.Y);
		if moCheck ~= 255 then
			local mo = ToMOSRotating(MovableMan:GetMOFromID(moCheck));
			local rootMO = MovableMan:GetMOFromID(mo.RootID);
			if mo and IsActor(rootMO) then
				local actor = ToActor(rootMO);
				local parts = {actor};
				local walking = false;
				if IsAHuman(actor) then
					actor = ToAHuman(actor);
					parts = {actor, actor.Head, actor.FGArm, actor.BGArm, actor.FGLeg, actor.BGLeg};
				elseif IsACrab(actor) then
					actor = ToACrab(actor);
					parts = {actor, actor.Turret, actor.RFGLeg, actor.RBGLeg, actor.LFGLeg, actor.LBGLeg};
				end
				local strength = 1 + self.strength;
				if actor:HasObjectInGroup("Infected") then	-- heal and buff zombies
					actor.Health = math.min(actor.Health + math.floor(strength), actor.MaxHealth);
					if actor.Jetpack then
						local speed = actor:GetLimbPathSpeed(1);
						local speedFactor = 2 + speed * 2;
						actor:SetLimbPathSpeed(1, speed + math.floor(strength * 20 / speedFactor) / 20);
						for em in actor.Jetpack.Emissions do
							em.BurstSize = em.BurstSize + math.floor(strength * 10 / speedFactor);
						end
					end
					actor.GibImpulseLimit = actor.GibImpulseLimit + (strength * 10);
					actor.ImpulseDamageThreshold = actor.ImpulseDamageThreshold + (strength * 10);
					mo.GibWoundLimit = mo.GibWoundLimit + strength;
					if actor.Scale > 0 and actor.Scale < 1.25 then	-- do you even lift bro?
						actor.Scale = actor.Scale + self.strength / (1 + actor.Scale);
					end
					for i = 1, #parts do
						if parts[i] then
							parts[i].DamageMultiplier = parts[i].DamageMultiplier / strength;
							if IsAttachable(parts[i]) then
								ToAttachable(parts[i]).JointStrength = ToAttachable(parts[i]).JointStrength + (strength * 10);
							end
						end
					end
				else	-- hurt and weaken the player
					if math.random(actor.Mass + actor.Material.StructuralIntegrity) < (strength * 100) then
						actor.Health = actor.Health - self.strength;
						if walking then
							local speed = actor:GetLimbPathSpeed(1);
							actor:SetLimbPathSpeed(1, speed / (1 + speed * self.strength * 0.1));
						end
						actor.ImpulseDamageThreshold = math.max(actor.ImpulseDamageThreshold - (strength * 10), 1);
						if actor.Status == 0 then
							actor.Status = 1;
						end
					end
					mo.DamageMultiplier = mo.DamageMultiplier + self.strength;
				end
				for i = 1, 2 do
					local part = CreateMOSParticle("Spitter Smoke");
					part.Pos = self.Pos;
					part.Lifetime = part.Lifetime * RangeRand(1.0, 1.5);
					part.Vel = Vector(-self.Vel.X, -self.Vel.Y):RadRotate(RangeRand(-0.2, 0.2)) * RangeRand(0.0, 0.2);
					MovableMan:AddParticle(part);
					self.ToDelete = true;
				end
			end
		end
	end
	self.Sharpness = self.Sharpness * 0.99;
end
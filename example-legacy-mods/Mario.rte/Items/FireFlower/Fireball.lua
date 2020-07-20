function Create(self)
	self.speed = 20;
	self.GlobalAccScalar = 1 + self.speed / 3;	-- GlobalAccScalar basically determines bounce height
	self.dir = 0;
	if self.Vel.X ~= 0 then
		self.dir = self.Vel.X / math.abs(self.Vel.X);
	end
	self.Lifetime = FrameMan.ResX * 30 / self.speed;
	self.fire = CreateMOSParticle("Flame "..math.random(2).." Hurt");
end
function Update(self)
	local dir = self.Vel.X / math.abs(self.Vel.X);
	if dir ~= self.dir then
		self.ToDelete = true;
	else
		local part = CreateMOSParticle("Fire Flower Smoke");
		part.Pos = self.Pos;
		--part.Vel = self.Vel * 0.1;
		part.Lifetime = math.random(150, 200);
		MovableMan:AddParticle(part);
		self.Vel.X = dir * self.speed;
		if math.abs(self.Vel.Y) > self.speed then
			self.Vel.Y = self.Vel.Y / math.abs(self.Vel.Y) * self.speed;
		end
		local checkPos = self.Pos + Vector(0, self.Vel.Y * 0.3);
		local terrCheck = SceneMan:GetTerrMatter(checkPos.X, checkPos.Y);
		if terrCheck ~= 0 then
			self.Vel.Y = -self.Vel.Y / math.abs(self.Vel.Y) * self.speed;
		end
		if self.Vel.Magnitude > self.speed then
			self.Vel = self.Vel * 0.9;
		end
	end
end
function Destroy(self)
	if self.fire then
		self.fire.Pos = Vector(self.Pos.X, self.Pos.Y) - Vector(self.Vel.X, self.Vel.Y) * 0.3;
		self.fire.Vel = Vector(self.Vel.X, self.Vel.Y);
		self.fire.Lifetime = self.fire.Lifetime * 0.5;
		MovableMan:AddParticle(self.fire);
	end
end
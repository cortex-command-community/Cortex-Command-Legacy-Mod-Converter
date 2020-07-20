function Create(self)
	self.width = ToMOSprite(self):GetSpriteWidth();
	self.height = ToMOSprite(self):GetSpriteHeight();
	self.offset = Vector(self.SpriteOffset.X, self.SpriteOffset.Y);
end
function Update(self)
	local suffix = "".. self.Frame;
	local negNum = 1;
	if self.HFlipped then
		negNum = -1;
		suffix = "HFlipped ".. self.Frame;
	end
	local glow = CreateMOPixel(self.PresetName .." Glow ".. suffix);
	glow.Pos = self.Pos + Vector((self.width / 2 + self.offset.X) * negNum, self.height / 2 + self.offset.Y):RadRotate(self.RotAngle);
	glow.EffectRotAngle = self.RotAngle;
	MovableMan:AddParticle(glow);
end
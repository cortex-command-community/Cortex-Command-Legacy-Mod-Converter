function Taunt(self)
	local sfx = CreateAEmitter("Taunt Zod")
	sfx.Pos = self.Pos
	MovableMan:AddParticle(sfx)
end